import json
import asyncio
from datetime import datetime
from confluent_kafka import Consumer
from sqlalchemy import select, desc
from app.core.database import SessionLocal
from app.models.price import Price
from app.models.average import MovingAverage
import uuid
import os

KAFKA_CONFIG = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    'group.id': 'ma-consumer-group',
    'auto.offset.reset': 'earliest'
}

TOPIC = "price-events"

async def handle_message(data: dict):
    async with SessionLocal() as session:
        await calculate_and_store_moving_average(session, data)

async def calculate_and_store_moving_average(session, price_event):
    symbol = price_event["symbol"]
    timestamp = datetime.fromisoformat(price_event['timestamp'].replace("Z", ""))
    price = price_event["price"]

    # Traemos las últimas 5 prices
    result = await session.execute(
        select(Price.price)
        .where(Price.symbol == symbol.upper())
        .order_by(desc(Price.timestamp))
        .limit(5)
    )
    prices = result.scalars().all()

    if len(prices) < 5:
        print(f"Not enough data for {symbol} to calculate moving average")
        return

    average = round(sum(prices) / len(prices), 2)
    print(f"{symbol} MA: {average}")

    ma_record = MovingAverage(
        id=uuid.uuid4(),
        symbol=symbol.upper(),
        average=average,
        timestamp=timestamp
    )

    session.add(ma_record)
    await session.commit()

def start_consumer():
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([TOPIC])

    print(f"[Kafka] Listening on topic: {TOPIC} ...")

    loop = asyncio.get_event_loop()

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                print(f"[Kafka Error] {msg.error()}")
                continue

            try:
                data = json.loads(msg.value().decode('utf-8'))
                print("[Kafka] Received:", data)
                
                loop.run_until_complete(handle_message(data))
            except Exception as e:
                print(f"[Kafka] Error processing message: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    start_consumer()


TOPIC = "price-events"

async def handle_message(data: dict):
    async with SessionLocal() as session:
        await calculate_and_store_moving_average(session, data)

async def calculate_and_store_moving_average(session, price_event):
    symbol = price_event["symbol"]
    timestamp = datetime.fromisoformat(price_event['timestamp'].replace("Z", ""))
    price = price_event["price"]

    # Traemos las últimas 5 prices
    result = await session.execute(
        select(Price.price)
        .where(Price.symbol == symbol.upper())
        .order_by(desc(Price.timestamp))
        .limit(5)
    )
    prices = result.scalars().all()

    if len(prices) < 5:
        print(f"Not enough data for {symbol} to calculate moving average")
        return

    average = round(sum(prices) / len(prices), 2)
    print(f"{symbol} MA: {average}")

    ma_record = MovingAverage(
        id=uuid.uuid4(),
        symbol=symbol.upper(),
        average=average,
        timestamp=timestamp
    )

    session.add(ma_record)
    await session.commit()

def start_consumer():
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([TOPIC])

    print(f"[Kafka] Listening on topic: {TOPIC} ...")

    loop = asyncio.get_event_loop()

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                print(f"[Kafka Error] {msg.error()}")
                continue

            try:
                data = json.loads(msg.value().decode('utf-8'))
                print("[Kafka] Received:", data)
                
                loop.run_until_complete(handle_message(data))
            except Exception as e:
                print(f"[Kafka] Error processing message: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    start_consumer()
