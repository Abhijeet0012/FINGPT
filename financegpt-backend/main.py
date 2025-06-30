from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
import asyncio
from typing import List, Optional
import json
import threading
import os
from jose import JWTError, jwt
import uuid
import re

from prompts.report_prompt import FINAL_RESPONSE_PROMPT
from routes.query import (
    router as query_router,
    openai_client,
    run_sql_agent_sync,
    run_pdf_agent_sync,
    run_offers_agent_sync,
)
from routes.auth import router as auth_router, SECRET_KEY, ALGORITHM

from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from database import SessionLocal
from models.models import Offer, QueryLog, User, UserProfile
from prompts.recommendations_prompt import RECOMMENDATIONS_PROMPT

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="FinanceGPT Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query_router)
app.include_router(auth_router)

# Pydantic schema for Offer
class OfferSchema(BaseModel):
    id: int
    product_name: str
    promo_interest_rate: Optional[str] = None
    signup_bonus: Optional[str] = None
    valid_till: date

    class Config:
        from_attributes = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/offers", response_model=List[OfferSchema])
async def get_offers(db: Session = Depends(get_db)):
    """
    Get all offers from the database.
    """
    try:
        offers = db.query(Offer).all()
        return offers
    except Exception as e:
        logger.error(f"Error fetching offers: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error fetching offers"
        )

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    chat_history = []  # Track chat history for this session
    try:
        data = await websocket.receive_text()
        data_json = json.loads(data)
        query = data_json.get("query")
        token = data_json.get("token")  # Expect JWT token in the initial message
        if not query:
            await websocket.send_text(json.dumps({"error": "No query provided"}))
            await websocket.close()
            return
        if not token:
            await websocket.send_text(json.dumps({"error": "No token provided"}))
            await websocket.close()
            return
        # Validate JWT and get user
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("sub")
            if user_email is None:
                raise Exception("Invalid token: no subject")
        except JWTError as e:
            await websocket.send_text(json.dumps({"error": f"Invalid token: {str(e)}"}))
            await websocket.close()
            return
        # Fetch user and profile
        db: Session = SessionLocal()
        user = db.query(User).filter(User.email == user_email).first()
        if not user or not user.profile:
            await websocket.send_text(json.dumps({"error": "User not found or profile missing"}))
            await websocket.close()
            db.close()
            return
        user_profile_dict = {
            "name": user.profile.name,
            "age": user.profile.age,
            "income": str(user.profile.income),
            "employment_type": user.profile.employment_type,
            "risk_appetite": user.profile.risk_appetite,
            "financial_goals": user.profile.financial_goals,
            "credit_score": user.profile.credit_score,
            "kyc_verified": user.profile.kyc_verified
        }
        # Generate a trace_id
        trace_id = str(uuid.uuid4())
        # Add the first user message to chat history
        chat_history.append({"role": "user", "content": query})
        # Run agents concurrently
        loop = asyncio.get_running_loop()
        sql_future = loop.run_in_executor(None, run_sql_agent_sync, query)
        pdf_future = loop.run_in_executor(None, run_pdf_agent_sync, query)
        offers_future = loop.run_in_executor(None, run_offers_agent_sync)
        import time
        start_time = time.time()
        sql_result, pdf_result, offers_result = await asyncio.gather(sql_future, pdf_future, offers_future)
        sql_data = sql_result.get("result", "No SQL data available")
        sql_explanation = sql_result.get("explanation", "No SQL explanation available")
        pdf_response = pdf_result.get("response", "No PDF data available")
        api_response = offers_result.get("result", "No promotion data available")
        # Format chat history as a readable string
        formatted_chat_history = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history
        ])
        analysis_prompt = FINAL_RESPONSE_PROMPT.format(
            user_profile=json.dumps(user_profile_dict, indent=2),
            chat_history=formatted_chat_history,
            query=query,
            sql_data=sql_data,
            sql_explanation=sql_explanation,
            pdf_response=pdf_response,
            api_response=api_response
        )
        queue = asyncio.Queue()
        stop_token = object()
        loop = asyncio.get_running_loop()
        answer_chunks = []
        def stream_chunks_to_queue(loop):
            try:
                response_stream = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": analysis_prompt}],
                    temperature=0.1,
                    max_tokens=2000,
                    stream=True
                )
                for chunk in response_stream:
                    if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        answer_chunks.append(content)
                        asyncio.run_coroutine_threadsafe(queue.put(content), loop)
            finally:
                asyncio.run_coroutine_threadsafe(queue.put(stop_token), loop)
        thread = threading.Thread(target=stream_chunks_to_queue, args=(loop,))
        thread.start()
        while True:
            chunk = await queue.get()
            if chunk is stop_token:
                break
            await websocket.send_text(chunk)
        answer_full = ''.join(answer_chunks)
        # Add assistant response to chat history
        chat_history.append({"role": "assistant", "content": answer_full})
        # Generate recommendations using LLM
        rec_prompt = RECOMMENDATIONS_PROMPT.format(user_query=query, assistant_answer=answer_full)
        try:
            rec_response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": rec_prompt}],
                temperature=0.2,
                max_tokens=256
            )
            rec_text = rec_response.choices[0].message.content.strip()
            logger.error(f"Raw LLM recommendations output: {rec_text}")
            # Parse the JSON array from the LLM output
            try:
                recommendations = json.loads(rec_text)
            except Exception:
                # Try to extract the first JSON array from the output
                match = re.search(r'\[.*?\]', rec_text, re.DOTALL)
                if match:
                    try:
                        recommendations = json.loads(match.group(0))
                    except Exception:
                        recommendations = []
                else:
                    recommendations = []
            if not isinstance(recommendations, list):
                recommendations = []
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            recommendations = []
        await websocket.send_text(json.dumps({"recommendations": recommendations}))
        await websocket.close()
        # After streaming, log the query
        end_time = time.time()
        processing_time = round(end_time - start_time, 3)
        # For confidence_score, set a placeholder (e.g., 1.0) unless you have a real value
        confidence_score = 1.0
        query_log = QueryLog(
            trace_id=trace_id,
            user_id=user.id,
            user_name=user.profile.name,
            query=query,
            answer=answer_full,
            confidence_score=confidence_score,
            processing_time=processing_time
        )
        db.add(query_log)
        db.commit()
        db.close()
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(json.dumps({"error": str(e)}))
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)