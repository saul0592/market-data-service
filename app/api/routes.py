import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.price import PriceResponse
from app.core.database import get_db
from app.models.price import Price
from app.services.market_data_provider import fetch_alpha_vantage_price
from app.services.price_service import save_raw_market_data, save_price
from app.schemas.price import PollResponse, PollRequest

router = APIRouter()

@router.get("/prices/latest", response_model=PriceResponse)
async def get_latest_price(symbol: str, provider: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Price)
        .where(Price.symbol == symbol.upper())
        .where(Price.provider == provider)
        .order_by(Price.timestamp.desc())
        .limit(1)
    )

    try:
        result = await db.execute(stmt)
        price_obj = result.scalar_one_or_none()
    except Exception as e:
        logging.error(f"Database query error for {symbol} {provider}: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")

    if price_obj:
        return {
            "symbol": price_obj.symbol,
            "price": price_obj.price,
            "timestamp": price_obj.timestamp.isoformat() + "Z",
            "provider": price_obj.provider,
        }

    if provider == "alpha_vantage":
        try:
            fetched_data = await fetch_alpha_vantage_price(symbol)
        except Exception as e:
            logging.error(f"Fetching from Alpha Vantage failed: {e}")
            raise HTTPException(status_code=502, detail=f"Fetching from Alpha Vantage failed: {e}")

        try:
            await save_raw_market_data(fetched_data, db)
            await save_price(fetched_data, db)
        except Exception as e:
            logging.error(f"Saving fetched data failed: {e}")
            raise HTTPException(status_code=500, detail="Saving fetched data failed")

        # Reconsultar y devolver el dato guardado
        try:
            result = await db.execute(stmt)
            price_obj = result.scalar_one_or_none()
            if price_obj:
                return {
                    "symbol": price_obj.symbol,
                    "price": price_obj.price,
                    "timestamp": price_obj.timestamp.isoformat() + "Z",
                    "provider": price_obj.provider,
                }
            else:
                logging.error("Price not found after saving data")
                raise HTTPException(status_code=500, detail="Price not found after saving")
        except Exception as e:
            logging.error(f"Database query after saving error: {e}")
            raise HTTPException(status_code=500, detail="Database query after saving failed")

    raise HTTPException(status_code=404, detail="Price not found and provider not supported")


@router.post("/prices/poll", response_model=PollResponse, status_code=202)
async def poll_prices(data: PollRequest, db: AsyncSession = Depends(get_db)):
    print(" poll_prices llamado")
    print(f" Request recibida: {data}")

    try:
        for symbol in data.symbols:
            print(f" searching: {symbol}")
            fetched_data = await fetch_alpha_vantage_price(symbol)
            print(f" Data: {fetched_data}")

            await save_raw_market_data(fetched_data, db)
            print(" data saved")

            await save_price(fetched_data, db)
            print(" data saved")
    except Exception as e:
        print(f" Error en poll_prices: {e}")
        raise HTTPException(status_code=500, detail="Fallo en el polling")

    return PollResponse(
        job_id="poll_123",
        status="accepted",
        config=data
    )