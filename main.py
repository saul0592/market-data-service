from fastapi import FastAPI 
from app.api import prices
app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "service is running"}

app.include_router(prices.router)
