from fastapi import APIRouter, Query
from datetime import datetime

router = APIRouter()

@router.get("/prices/latest")
async def get_latest_price(symbol: str, provider: str = Query("yfinance")):
    return {
        "symbol" : symbol.upper(),
        "price" : 150.25,
        "timestamp" : datetime.utcnow().isoformat() + "Z",
        "provider" : provider
    }