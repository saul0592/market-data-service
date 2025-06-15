import httpx
import os
import logging

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

if not ALPHA_VANTAGE_API_KEY:
    raise RuntimeError("ALPHA_VANTAGE_API_KEY is not set in environment variables.")

async def fetch_alpha_vantage_price(symbol: str):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            price = float(data["Global Quote"]["05. price"])
            timestamp = data["Global Quote"]["07. latest trading day"] + "T00:00:00Z"
        except (KeyError, ValueError) as e:
            logging.error(f"Error parsing Alpha Vantage data for {symbol}: {e}")
            raise Exception("Error obtaining Alpha Vantage data")
        except httpx.HTTPError as e:
            logging.error(f"HTTP error fetching Alpha Vantage data for {symbol}: {e}")
            raise
    return {
        "symbol": symbol,
        "price": price,
        "timestamp": timestamp,
        "provider": "alpha_vantage",
        "raw_response": resp.text
    }
