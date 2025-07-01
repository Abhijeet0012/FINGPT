import os
from openai import OpenAI
from prompts.classification_prompt import CLASSIFICATION_PROMPT
from dotenv import load_dotenv

load_dotenv()

class ClassificationAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def process_query(self, user_query: str):
        prompt = CLASSIFICATION_PROMPT.format(query=user_query)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        categories = response.choices[0].message.content.strip()
        # Split and clean the categories
        return [cat.strip() for cat in categories.split(',') if cat.strip()] 