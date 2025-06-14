from fastapi import APIRouter, HTTPException
from app.schemas.price import PriceResponse, PollRequest, PollResponse
from datetime import datetime

router = APIRouter()

@router.get("/prices/latest", response_model=PriceResponse)
async def get_latest_price(symbol: str, provider: str = "alpha_vantage"):
    #Dummy data
    return PriceResponse(
        symbol = symbol,
        price = 150.25,
        timestamp = datetime.utcnow().isoformat() + "Z",
        provider = provider,
    )

@router.post("/prices/poll", response_model= PollResponse, status_code=202)
async def poll_prices(data: PollRequest):
    #Dummy job id and accepted status
    return PollResponse(
        job_id = "poll_123",
        status = "accepted",
        config = request, 
    )