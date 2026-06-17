import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=BASE_DIR / ".env")

API_KEY=os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Check your env file locaton and formal")

from openai import OpenAI
client = OpenAI(api_key=API_KEY)

def generate_ai_report(ticker: str, metrics: dict):
    prompt = f"""
    You are a proffessional equity research analyst.
    
    Write a structured investment report for the stock below.
    
    TICKER: {ticker}
    
    FINANCIAL METRICS:
    {metrics}
    
    Return the report in this format:
    1. Executive Summary
    2. Bull Case
    3. Bear Case
    4. Key Risks
    5. Investment View (BUY or HOLD or SELL)
    
    Keep it proffessional and thorough.
    Use clear line breaks and bullet points 
    no fluff but valuable content for an investor to read
    """
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    
    return response.output_text