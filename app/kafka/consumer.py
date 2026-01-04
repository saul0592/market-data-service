from confluent_kafka import Consumer
import json

# Configuración del consumer
consumer_config = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "my-group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)
topic = "test-topic"
consumer.subscribe([topic])

print(f"Escuchando mensajes en {topic}...")

try:
    while True:
        msg = consumer.poll(1.0)  # espera 1 segundo
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        data = json.loads(msg.value().decode('utf-8'))
        print(f"Mensaje recibido: {data}")

except KeyboardInterrupt:
    print("Deteniendo consumer...")

finally:
    consumer.close()
