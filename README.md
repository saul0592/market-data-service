##Market Data Service

This project is a microservice to consume andproduce event of price using Kafka, API REST with FastAPI.

I'm a currently student of Computer Science at BMCC eager to grow my potential as a software enginer thourgh internships and real-world experience.

##Technologies

- Python 3.8+
- FastAPI
- Kafka (Confluent)
- PostgreSQL
- SQLAlchemy Async
- Docker y Docker Compose

##Requirements

- Docker y Docker Compose
- Python 3.8+
- Kafka (Confluent Kafka) and PostgreSQL

## Instalation

1. Clone the repository 

git clone https://github.com/saul0592/market-data-service.git
cd market-data-service

2. Create your own enviroment:

python -m venv venv
source venv/bin/activate

3. Install the dependences
pip install -r requirements.txt

5. Run the servers database, Kafka and Zookeeper

6. Beging the API:

uvicorn app.main:app --reload

7. Run Kafka Consume:

python run_consumer.py

---To Build the Docker Compose--

docker-compose up --build

---EndPoint--

GET /prices/latest?symbol=XXX&provider=YYY--> it will obtain the last price of a symbol and provider

---Project structure---

app/
 ├── services/           # Logic 
 ├── models/             # Model SQLAlchemy
 ├── core/               # settings and utilities
 ├── schemas/            # Schemas Pydantic
 └── main.py             # Start FastAPI
run_consumer.py          # Consumer Script Kafka
docker-compose.yml       # settings containers
requirements.txt         # Python dependences

---Considerations--

Data base has to be run before to initiate the services
Kafka should be available and running

---Conctact--


Saul Mendoza
saul.mendoza50@stu.bmcc.cuny.edu
9176693622
https://github.com/saul0592 
https://www.linkedin.com/in/saul-mendoza-722754214/ 