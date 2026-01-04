from confluent_kafka import Producer
import json

# Configuración del producer
producer_config = {
    "bootstrap.servers": "kafka:9092"  # nombre del servicio Kafka en docker-compose
}

producer = Producer(producer_config)

def send_message(topic: str, message: dict):
    """Envía un mensaje JSON a Kafka"""
    producer.produce(topic, json.dumps(message).encode('utf-8'))
    producer.flush()  # fuerza el envío inmediato
    print(f"Mensaje enviado a {topic}: {message}")

# Ejemplo de uso
if __name__ == "__main__":
    send_message("test-topic", {"symbol": "AAPL", "price": 172.5})
