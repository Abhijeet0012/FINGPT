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
    get_user_info_from_token,
    run_all_agents,
    stream_openai_response,
    generate_recommendations,
    log_query,
    get_offers_from_db
)
from routes.auth import router as auth_router, SECRET_KEY, ALGORITHM

from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from database import SessionLocal
from models.models import Offer, QueryLog, User, UserProfile
from prompts.recommendations_prompt import RECOMMENDATIONS_PROMPT
from agents.classification_agent import ClassificationAgent

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

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

classification_agent = ClassificationAgent()

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    logger.info("WebSocket connection initiated at /ws/stream")
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        logger.info(f"Received data from client: {data}")
        data_json = json.loads(data)
        query = data_json.get("query")
        token = data_json.get("token")  # Expect JWT token in the initial message
        if not query:
            logger.warning("No query provided in WebSocket request.")
            await websocket.send_text(json.dumps({"error": "No query provided"}))
            await websocket.close()
            return
        if not token:
            logger.warning("No token provided in WebSocket request.")
            await websocket.send_text(json.dumps({"error": "No token provided"}))
            await websocket.close()
            return
        # Validate JWT and get user/profile
        try:
            user, user_profile_dict, db = get_user_info_from_token(token)
            logger.info(f"User authenticated: {user.email if hasattr(user, 'email') else str(user)}")
        except Exception as e:
            logger.error(f"JWT validation or user fetch failed: {str(e)}")
            await websocket.send_text(json.dumps({"error": str(e)}))
            await websocket.close()
            return
        # Generate a trace_id
        trace_id = str(uuid.uuid4())
        import time
        start_time = time.time()
        logger.info(f"Processing query with trace_id={trace_id}: {query}")
        # --- Classification step ---
        categories = classification_agent.process_query(query)
        logger.info(f"Classification categories for query '{query}': {categories}")
        sql_data = sql_explanation = pdf_response = api_response = None
        if "DB_QUERY" in categories or "BOTH" in categories:
            sql_result = run_sql_agent_sync(query)
            sql_data = sql_result.get("result", "No SQL data available")
            sql_explanation = sql_result.get("explanation", "")
            logger.info(f"SQL Agent result: {sql_data}, explanation: {sql_explanation}")
        if "PDF_EXTRACTION" in categories or "BOTH" in categories:
            pdf_result = run_pdf_agent_sync(query)
            pdf_response = pdf_result.get("response", "No PDF data available")
            logger.info(f"PDF Agent result: {pdf_response}")
        if "EXTERNAL_API" in categories:
            api_response = get_offers_from_db(db)
            logger.info(f"Offers DB result: {api_response}")
        # --- End classification step ---
        analysis_prompt = FINAL_RESPONSE_PROMPT.format(
            user_profile=json.dumps(user_profile_dict, indent=2),
            chat_history="",  # No chat history
            query=query,
            sql_data=sql_data,
            sql_explanation=sql_explanation,
            pdf_response=pdf_response,
            api_response=api_response
        )
        logger.info(f"Analysis prompt prepared for OpenAI streaming. Trace ID: {trace_id}")
        queue = asyncio.Queue()
        stop_token = object()
        answer_chunks = []
        loop = asyncio.get_running_loop()
        thread = threading.Thread(target=stream_openai_response, args=(analysis_prompt, queue, stop_token, answer_chunks, loop))
        thread.start()
        while True:
            chunk = await queue.get()
            if chunk is stop_token:
                break
            await websocket.send_text(chunk)
        answer_full = ''.join(answer_chunks)
        logger.info(f"Streaming complete for trace_id={trace_id}. Answer length: {len(answer_full)}")
        # Generate recommendations using LLM
        recommendations = generate_recommendations(query, answer_full)
        logger.info(f"Recommendations generated for trace_id={trace_id}: {recommendations}")
        await websocket.send_text(json.dumps({"recommendations": recommendations}))
        await websocket.close()
        # After streaming, log the query
        end_time = time.time()
        processing_time = round(end_time - start_time, 3)
        log_query(trace_id, user, query, answer_full, processing_time, db)
        logger.info(f"Query logged for trace_id={trace_id}. Processing time: {processing_time}s")
        db.close()
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected by client.")
        pass
    except Exception as e:
        logger.error(f"Exception in websocket_stream: {str(e)}")
        await websocket.send_text(json.dumps({"error": str(e)}))
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)