# app/services/price_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.price import Price, RawMarketData 
from app.services.kafka_producer import produce_price_event
from sqlalchemy import select, update
import uuid
from datetime import datetime

async def get_latest_price(symbol: str, provider: str, db: AsyncSession):
    query = (
        select(Price)
        .where(Price.symbol == symbol.upper())
        .where(Price.provider == provider)
        .order_by(Price.timestamp.desc())
        .limit(1)
    )
    result = await db.execute(query)
    price_obj = result.scalar_one_or_none()
    if price_obj is None:
        return None

    # Retorna un dict para la respuesta JSON
    return {
        "symbol": price_obj.symbol,
        "price": price_obj.price,
        "timestamp": price_obj.timestamp.isoformat(),
        "provider": price_obj.provider,
    }


async def save_raw_market_data(data: dict, db: AsyncSession):
    raw_data = RawMarketData(
        id=uuid.uuid4(),
        symbol=data["symbol"],
        price=data["price"],
        timestamp=datetime.fromisoformat(data["timestamp"].replace("Z", "")),
        provider=data["provider"],
        raw_response=data["raw_response"],
    )
    db.add(raw_data)
    await db.commit()
    await db.refresh(raw_data)

    price_event = {
        "symbol": raw_data.symbol,
        "price": raw_data.price,
        "timestamp": raw_data.timestamp.isoformat(),
        "provider": raw_data.provider,
        "raw_response_id": str(raw_data.id),
    }
    produce_price_event(price_event)

    return raw_data




async def save_price(data: dict, db: AsyncSession):
    timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", ""))
    query = select(Price).where(
        Price.symbol == data["symbol"].upper(),
        Price.provider == data["provider"],
        Price.timestamp == timestamp,
    )
    result = await db.execute(query)
    price_obj = result.scalar_one_or_none()

    if price_obj:
        price_obj.price = data["price"]
        db.add(price_obj)
    else:
        price_obj = Price(
            symbol=data["symbol"].upper(),
            price=data["price"],
            timestamp=timestamp,
            provider=data["provider"],
        )
        db.add(price_obj)
    await db.commit()
    await db.refresh(price_obj)
    return price_obj