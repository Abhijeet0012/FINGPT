from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import asyncio
from typing import Dict
import logging
import os
from agents.sql_agent import SQLAgent
from agents.pdf_agent import PDFAgent
from prompts.report_prompt import FINAL_RESPONSE_PROMPT
from openai import OpenAI
from concurrent.futures import ProcessPoolExecutor
import json
import httpx
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import User, QueryLog, Offer
from prompts.recommendations_prompt import RECOMMENDATIONS_PROMPT
import threading
import re
import time
from utils import get_user_info_from_token, generate_recommendations, log_query, QueryRequest
from agents.classification_agent import ClassificationAgent
from datetime import date

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize OpenAI client and agents
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sql_agent = SQLAgent(table_name="financial_products")
pdf_agent = PDFAgent()
classification_agent = ClassificationAgent()

# Create a global process pool executor
process_pool = ProcessPoolExecutor(max_workers=3)

# --- Modular helpers for websocket business logic ---

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def run_all_agents(query: str, db: Session):
    loop = asyncio.get_running_loop()
    sql_future = loop.run_in_executor(None, run_sql_agent_sync, query)
    pdf_future = loop.run_in_executor(None, run_pdf_agent_sync, query)
    offers_future = loop.run_in_executor(None, get_offers_from_db, db)
    sql_result, pdf_result, offers_result = await asyncio.gather(sql_future, pdf_future, offers_future)
    sql_data = sql_result.get("result", "No SQL data available")
    sql_explanation = sql_result.get("explanation", "")
    pdf_response = pdf_result.get("response", "No PDF data available")
    api_response = offers_result  # This is now a list of offers
    return sql_data, sql_explanation, pdf_response, api_response

def stream_openai_response(analysis_prompt, queue, stop_token, answer_chunks, loop):
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
    asyncio.run_coroutine_threadsafe(queue.put(stop_token), loop)

def run_sql_agent_sync(query: str) -> Dict:
    try:
        return sql_agent.process_query(query)
    except Exception as e:
        logger.error(f"SQL Agent error: {str(e)}")
        return {"status": "error", "error": str(e)}

def run_pdf_agent_sync(query: str) -> Dict:
    try:
        response = pdf_agent.process_query(query)
        return {"status": "success", "response": response}
    except Exception as e:
        logger.error(f"PDF Agent error: {str(e)}")
        return {"status": "error", "error": str(e)}

def get_offers_from_db(db: Session):
    """
    Get all offers from the database and serialize them as OfferSchema dicts.
    """
    try:
        offers = db.query(Offer).all()
        return [OfferSchema.model_validate(offer).model_dump() for offer in offers]
    except Exception as e:
        logger.error(f"Error fetching offers: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error fetching offers"
        )

# Pydantic schema for Offer
class OfferSchema(BaseModel):
    id: int
    product_name: str
    promo_interest_rate: str | None = None
    signup_bonus: str | None = None
    valid_till: date

    class Config:
        from_attributes = True
