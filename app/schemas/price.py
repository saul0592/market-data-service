from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PriceResponse(BaseModel):
    symbol : str
    price: float
    timestamp : Optional[str]
    provider : str

class PollRequest(BaseModel):
    symbols: List[str]
    interval : Optional[str]=None
    provider : str

class PollResponse(BaseModel):
    job_id : str
    status : str
    config : PollRequest