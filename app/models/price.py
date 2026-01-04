import uuid
from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.core.database import Base 
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()



class Price(Base):
    __tablename__ = "prices"
    symbol = Column(String, primary_key=True)
    provider = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    price = Column(Float)




class RawMarketData(Base):
    __tablename__ = "raw_market_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    timestamp= Column(DateTime, default=datetime.utcnow, index=True)
    provider = Column(String, nullable=False)
    raw_response= Column(String)


class ProcessedPricePoint(Base):
    __tablename__ = "processed_price_points"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    timestamp= Column(DateTime, default=datetime.utcnow, index=True)
    provider = Column(String, nullable=False)

class MovingAvarage(Base):
    __tablename__= "moving_averages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True, nullable=False)
    average = Column(Float, nullable=False)
    timestamp= Column(DateTime, default=datetime.utcnow, index=True)

class PollingJobConfig(Base):
    __tablename__ = "polling_job_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbols = Column(String, nullable=False)
    interval= Column(Integer, nullable=False)
    provider = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)

class PriceMessage(BaseModel):
    symbol: str
    price: float