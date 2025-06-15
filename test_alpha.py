import asyncio
import os
import httpx
import logging

async def test_fetch():
    symbol = "AMZN"
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        print("API key missing")
        return

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        print(f"Status code: {resp.status_code}")
        data = resp.json()
        print("Response JSON:", data)

asyncio.run(test_fetch())
