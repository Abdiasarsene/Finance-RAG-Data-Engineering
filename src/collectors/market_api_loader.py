# src/collectors/market_api_loader.py  
import os 
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

RAW_DATA_DIR = Path("./data/market")
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantag.co/query"

def fetch_stock_price(symbol: str = "AAPL") -> dict:
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol, 
        "apikey": API_KEY
    }
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    return r.json()

def api_to_json(symbol: str) ->dict:
    data = fetch_stock_price(symbol)
    return {
        "source": "api",
        "symbol": symbol,
        "data_collected": datetime.now(timezone).isoformat(),
        "metadata": {
            "provider": "AlphaVantage",
            "status_code": 200
        }
    }

def ingest_market_data(symbols=["AAPL", "MSFT"], output_dir= RAW_DATA_DIR):
    os.makedirs(output_dir, exist_ok=True)
    for symbol in symbols:
        doc_json = api_to_json(symbol)
        out_path = output_dir / f"{symbol}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(doc_json, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    ingest_market_data()