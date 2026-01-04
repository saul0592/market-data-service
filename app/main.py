from fastapi import FastAPI
from app.api.routes import router as api_router
from pydantic import BaseModel


app = FastAPI()
app.include_router(api_router)

class PriceMessage(BaseModel):
    symbol: str
    price: float

@app.get("/")
async def root():
    return {"message": "Market Data Service API"}

@app.post("/send-price")
def send_price(data: PriceMessage):
    message = {"symbol": data.symbol, "price": data.price}
    send_message("test-topic", message)
    return {"status": "enviado", "message": message}