import os
import psycopg2
from openai import OpenAI
from typing import Dict, List
from prompts.sql_agent import SQL_GENERATION_PROMPT

from dotenv import load_dotenv

load_dotenv()


class SQLAgent:
    def __init__(self, table_name: str):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cursor = self.conn.cursor()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def execute_sql(self, sql_query: str) -> List:
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"SQL Error: {str(e)}")

    def generate_sql(self, natural_language_query: str) -> str:
        prompt = SQL_GENERATION_PROMPT.format(query=natural_language_query)
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content

    def process_query(self, natural_language_query: str) -> Dict:
        try:
            # Generate SQL from natural language
            sql_query = self.generate_sql(natural_language_query)

            print(sql_query)
            
            # Execute the SQL query
            result = self.execute_sql(sql_query)
            
            # Generate explanation
            return {
                "status": "success",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
