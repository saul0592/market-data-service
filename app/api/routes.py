from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.price import PriceResponse, PollRequest, PollResponse
from app.services.price_service import get_latest_price, save_raw_market_data, save_price
from app.services.market_data_provider import fetch_alpha_vantage_price
from app.core.database import get_db

router = APIRouter()

@router.get("/prices/latest")
async def get_latest_price_route(
    symbol: str,
    provider: str,
    db: AsyncSession = Depends(get_db)
):
    price = await get_latest_price(symbol, provider, db)
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return price

@router.post("/prices/poll", response_model=PollResponse, status_code=202)
async def poll_prices(data: PollRequest, db: AsyncSession = Depends(get_db)):
    print("▶️ poll_prices llamado")
    print(f" Request recibida: {data}")

    try:
        for symbol in data.symbols:
            print(f" Searching price: {symbol}")
            fetched_data = await fetch_alpha_vantage_price(symbol)
            print(f"Data: {fetched_data}")

            await save_raw_market_data(fetched_data, db)
            print("Data saved")

            await save_price(fetched_data, db)
            print(" Price saved")
    except Exception as e:
        print(f" Error in poll_prices: {e}")
        raise HTTPException(status_code=500, detail="Fail polling")

    return PollResponse(
        job_id="poll_123",
        status="accepted",
        config=data
    )
