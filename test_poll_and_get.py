import asyncio
import httpx

API_URL = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient() as client:
        # Paso 1: Hacer POST a /prices/poll con todos los campos requeridos
        poll_payload = {
            "symbols": ["AAPL"],
            "interval": "1min",
            "provider": "alpha_vantage"
        }
        poll_resp = await client.post(f"{API_URL}/prices/poll", json=poll_payload)
        print("Poll status:", poll_resp.status_code)
        print("Poll raw response:", poll_resp.text)

        # Paso 2: Hacer GET a /prices/latest
        get_resp = await client.get(f"{API_URL}/prices/latest", params={
            "symbol": "AAPL",
            "provider": "alpha_vantage"
        })
        print("Get latest price status:", get_resp.status_code)
        print("Price data:", get_resp.text)

asyncio.run(main())


