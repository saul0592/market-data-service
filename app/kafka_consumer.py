import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session
from app.models.price import Price
from datetime import datetime

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC_NAME = "test-topic"

async def save_price_to_db(symbol: str, price: float):
    async with async_session() as session:  # tu AsyncSession factory
        async with session.begin():
            new_price = Price(
                symbol=symbol.upper(),
                price=price,
                timestamp=datetime.utcnow(),
                provider="manual"  # o “test” si quieres
            )
            session.add(new_price)
        await session.commit()
    logging.info(f"Saved {symbol} at {price} to DB")

async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="market-data-consumer"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode("utf-8"))
            logging.info(f"Received message: {data}")
            await save_price_to_db(data["symbol"], data["price"])
    finally:
        await consumer.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(consume())
