from fastapi import APIRouter, HTTPException
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

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize OpenAI client and agents
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sql_agent = SQLAgent(table_name="financial_products")
pdf_agent = PDFAgent()

# Create a global process pool executor
process_pool = ProcessPoolExecutor(max_workers=3)

class QueryRequest(BaseModel):
    query: str

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

def run_offers_agent_sync() -> Dict:
    """
    Fetches promotional offers from the offers API.
    """
    try:
        response = httpx.get("http://127.0.0.1:8000/offers")
        response.raise_for_status()  # Raise an exception for bad status codes
        offers_list = response.json()
        return {"status": "success", "result": json.dumps(offers_list)}
    except httpx.RequestError as e:
        logger.error(f"Error calling offers API: {e}")
        return {"status": "error", "error": f"Error calling offers API: {e}"}
    except Exception as e:
        logger.error(f"Error processing offers: {e}")
        return {"status": "error", "error": str(e)}

# async def generate_final_response(query: str, sql_result: Dict, pdf_result: Dict, offers_result: Dict) -> Dict:
#     try:
#         sql_data = sql_result.get("result", "No SQL data available")
#         sql_explanation = sql_result.get("explanation", "No SQL explanation available")
#         pdf_response = pdf_result.get("response", "No PDF data available")
#         api_response = offers_result.get("result", "No promotion data available")
#         analysis_prompt = FINAL_RESPONSE_PROMPT.format(
#             query=query,
#             sql_data=sql_data,
#             sql_explanation=sql_explanation,
#             pdf_response=pdf_response,
#             api_response=api_response
#         )
#         response = openai_client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": analysis_prompt}],
#             temperature=0.1,
#             max_tokens=2000
#         )
#         analysis = response.choices[0].message.content
#         final_report = {
#             "status": "success",
#             "analysis": analysis,
#             "metadata": {
#                 "model": "gpt-4o-mini",
#                 "query": query,
#                 "data_sources": ["SQL Database", "PDF Documents", "Promotions API"]
#             }
#         }
#         return final_report
#     except Exception as e:
#         logger.error(f"Error generating detailed report: {str(e)}")
#         return {"status": "error", "error": str(e)}

# @router.post("/query")
# async def process_query(request: QueryRequest):
#     try:
#         loop = asyncio.get_running_loop()
#         sql_future = loop.run_in_executor(process_pool, run_sql_agent_sync, request.query)
#         pdf_future = loop.run_in_executor(process_pool, run_pdf_agent_sync, request.query)
#         offers_future = loop.run_in_executor(process_pool, run_offers_agent_sync)
        
#         sql_result, pdf_result, offers_result = await asyncio.gather(sql_future, pdf_future, offers_future)

#         final_report = await generate_final_response(request.query, sql_result, pdf_result, offers_result)
#         response = {
#             "sql_agent": sql_result,
#             "pdf_agent": pdf_result,
#             "offers_agent": offers_result,
#             "final_report": final_report,
#             "combined_response": {
#                 "status": "success",
#                 "message": "Analysis completed with detailed report"
#             }
#         }
#         if sql_result.get("status") == "error" and pdf_result.get("status") == "error" and offers_result.get("status") == "error":
#             raise HTTPException(
#                 status_code=500,
#                 detail="All agents failed to process the query"
#             )
#         return response
#     except Exception as e:
#         logger.error(f"Error processing query: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error processing query: {str(e)}"
#         ) 