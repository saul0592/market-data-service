# app/services/price_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.price import Price, RawMarketData 
import uuid
from datetime import datetime

async def get_latest_price(symbol: str, provider: str, session: AsyncSession):
    stmt = (
        select(Price)
        .where(Price.symbol == symbol.upper(), Price.provider == provider)
        .order_by(Price.timestamp.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


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
        "source": raw_data.provider,
        "raw_response_id": str(raw_data.id),
    }
    produce_price_event(price_event)

    return raw_data



async def save_price(data: dict, db: AsyncSession):
    price = Price(
        symbol=data["symbol"].upper(),
        price=data["price"],
        timestamp=datetime.fromisoformat(data["timestamp"].replace("Z", "")),
        provider=data["provider"]
    )
    db.add(price)
    await db.commit()
    await db.refresh(price)
    return price