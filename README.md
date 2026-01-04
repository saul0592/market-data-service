# Market Data Service (Microservice)

> High-performance microservice designed to ingest, process, and stream real-time financial market data using **Apache Kafka** and **FastAPI**.

## Overview
This project simulates a production-grade backend architecture for financial systems. It acts as a scalable microservice that consumes market prices via Kafka events, persists data asynchronously, and exposes real-time information through a REST API.

**Key Features:**
* **Event-Driven Architecture:** Uses **Apache Kafka** (Confluent) for high-throughput data streaming.
* **Async Processing:** Implemented with **SQLAlchemy Async** for non-blocking database operations.
* **Containerized:** Fully dockerized environment for consistent deployment.
* **RESTful API:** Built with **FastAPI** for high performance and auto-documentation.

## Tech Stack
* **Language:** Python 3.11
* **Framework:** FastAPI
* **Streaming:** Apache Kafka (Confluent) & Zookeeper
* **Database:** PostgreSQL (Async)
* **ORM:** SQLAlchemy (Async)
* **DevOps:** Docker & Docker Compose

## Quick Start (Docker)
The easiest way to run the service is using Docker Compose. This will set up the API, Database, Zookeeper, and Kafka automatically.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/saul0592/market-data-service.git](https://github.com/saul0592/market-data-service.git)
    cd market-data-service
    ```

2.  **Build and Run:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the API:**
    * **Swagger UI (Docs):** Visit `http://localhost:8000/docs` to test endpoints.
    * **Base URL:** `http://localhost:8000`

## Manual Installation (Local Dev)
If you prefer running it without Docker containers:

1.  **Environment Setup:**
    ```bash
    python -m venv venv
    # Windows:
    source venv/Scripts/activate
    # Mac/Linux:
    source venv/bin/activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Services:**
    * Ensure PostgreSQL and Kafka are running locally.
    * **Start API:**
        ```bash
        uvicorn app.main:app --reload
        ```
    * **Start Consumer:**
        ```bash
        python run_consumer.py
        ```

## API Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`  | `/prices/latest` | Get the latest price for a specific symbol. |
| `GET`  | `/mock/prices/latest` | Get a mock latest price (for testing). |
| `POST` | `/send-price` | Send a price to Kafka for asynchronous processing. |
| `POST` | `/prices/poll` | Poll multiple symbols from Alpha Vantage and store them. |


**Example Request (Send Price to Kafka):**
```bash
curl -X POST "http://localhost:8000/send-price" \
-H "Content-Type: application/json" \
-d '{"symbol": "AAPL", "price": 172.5}'
 ```


## Project Structure
```text
app/
├── core/       # Configuración y utilidades (database, settings)
├── models/     # SQLAlchemy models
├── schemas/    # Pydantic schemas
├── services/   # Lógica de negocio (fetching, saving, etc.)
├── api/        # Rutas de FastAPI
└── main.py     # Entry point FastAPI
run_consumer.py # Kafka consumer script
docker-compose.yml
requirements.txt
README.md
diagram.md

Saul Mendoza
saul.mendoza50@stu.bmcc.cuny.edu
9176693622
https://github.com/saul0592 
https://www.linkedin.com/in/saul-mendoza-722754214/ 
