from fastapi import FastAPI
import yfinance as yf
from backend.llm import generate_ai_report



app = FastAPI()

@app.get("/")
def home():
    return {"status": "AI Equity Research API running"}

@app.get("/stock/{ticker}")
def stock(ticker: str):
    stock = yf.Ticker(ticker)
    data = stock.info
    
    return {
        "ticker": ticker,
        "name": data.get("shortName"),
        "sector": data.get("sector"),
        "marketCap": data.get("marketCap"),
        "pe_ratio": data.get("trailingPE"),
        "price": data.get("currentPrice"),
        "currency": data.get("currency"),
    }
    
@app.get("/report/{ticker}")
def report(ticker: str):
    try:
        
       stock = yf.Ticker(ticker)
       data = stock.info
    
       metrics = {
        "pe": data.get("trailingPE"),
        "marketCap": data.get("marketCap"),
        "debt_To_Equity":  data.get("debtToEquity")
    }
     
   
    
       ai_report = generate_ai_report(ticker, metrics)
            
       return  {
        "ticker": ticker,
        "metrics": metrics,
        "ai_report": ai_report
    }

    except Exception as e:
        return {
            "error": str(e)
        }