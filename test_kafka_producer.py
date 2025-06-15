from kafka_producer import produce_price_event

test_message = {
    "symbol": "AAPL",
    "price": 196.45,
    "timestamp": "2025-06-13T00:00:00Z",
    "source": "alpha_vantage",
    "raw_response_id": "123e4567-e89b-12d3-a456-426614174000"
}

produce_price_event(test_message)
print("Mensaje enviado a Kafka")

