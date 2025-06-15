import os
import httpx
import logging
import asyncio
import os
print("API key en FastAPI:", os.getenv("ALPHA_VANTAGE_API_KEY"))
async def fetch_alpha_vantage_price(symbol: str, retries=3, timeout=10):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise RuntimeError("ALPHA_VANTAGE_API_KEY is not set in environment variables.")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }

    for attempt in range(retries):
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                price = float(data["Global Quote"]["05. price"])
                timestamp = data["Global Quote"]["07. latest trading day"] + "T00:00:00Z"
                return {
                    "symbol": symbol,
                    "price": price,
                    "timestamp": timestamp,
                    "provider": "alpha_vantage",
                    "raw_response": resp.text
                }
            except (KeyError, ValueError) as e:
                logging.error(f"Error parsing Alpha Vantage data for {symbol}: {e}")
                raise Exception("Error obtaining Alpha Vantage data")
            except httpx.RequestError as e:
                logging.warning(f"Request error on attempt {attempt+1} for {symbol}: {e}")
            except httpx.HTTPStatusError as e:
                logging.warning(f"HTTP status error on attempt {attempt+1} for {symbol}: {e}")
        
        await asyncio.sleep(2 ** attempt)
    
    raise Exception(f"Failed to fetch data from Alpha Vantage for symbol {symbol} after {retries} retries.")
