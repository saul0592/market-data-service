from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class MovingAverage(Base):
    __tablename__ = "symbol_averages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, index=True)
    average = Column(Float)
    timestamp = Column(DateTime)