from confluent_kafka import Producer
import json
import os
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    if err is not None:
        print(f"Error: {err}")
    else:
        print(f"Message send it to {msg.topic()} [{msg.partition()}]")


def produce_price_event(price_data: dict):
    topic = "price-events"
    message= json.dumps(price_data)
    producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
    producer.flush()