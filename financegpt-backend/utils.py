import os
import re
import json
import logging
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import User, QueryLog
from prompts.recommendations_prompt import RECOMMENDATIONS_PROMPT
from openai import OpenAI
from pydantic import BaseModel

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_user_info_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise Exception("Invalid token: no subject")
    except JWTError as e:
        raise Exception(f"Invalid token: {str(e)}")
    db: Session = SessionLocal()
    user = db.query(User).filter(User.email == user_email).first()
    if not user or not user.profile:
        db.close()
        raise Exception("User not found or profile missing")
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
    return user, user_profile_dict, db

def generate_recommendations(user_query, assistant_answer):
    rec_prompt = RECOMMENDATIONS_PROMPT.format(user_query=user_query, assistant_answer=assistant_answer)
    try:
        rec_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": rec_prompt}],
            temperature=0.2,
            max_tokens=256
        )
        rec_text = rec_response.choices[0].message.content.strip()
        logger.error(f"Raw LLM recommendations output: {rec_text}")
        try:
            recommendations = json.loads(rec_text)
        except Exception:
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
    return recommendations

def log_query(trace_id, user, query, answer, processing_time, db):
    confidence_score = 1.0
    query_log = QueryLog(
        trace_id=trace_id,
        user_id=user.id,
        user_name=user.profile.name,
        query=query,
        answer=answer,
        confidence_score=confidence_score,
        processing_time=processing_time
    )
    db.add(query_log)
    db.commit()

class QueryRequest(BaseModel):
    query: str 