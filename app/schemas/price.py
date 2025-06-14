from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PriceResponse(BaseModel):
    symbol : str
    price: float
    timestamp : str
    provider : Optional[str] = None

class PollRequest(BaseModel):
    symbols: List[str]
    interval : int
    provider : Optional[str]= None

class PollResponse(BaseModel):
    job_id : str
    status : str
    config : PollRequest