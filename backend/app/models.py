from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source = Column(String, nullable=False)
    category = Column(String, nullable=False)

    cost_price = Column(Float, nullable=False)
    shipping_cost = Column(Float, nullable=False)
    shipping_time_days = Column(Integer, nullable=False)

    selling_price = Column(Float, nullable=False)
    rating = Column(Float)
    review_count = Column(Integer)

    demand_score = Column(Float)
    competition_score = Column(Float)
    risk_score = Column(Float)
    viability_score = Column(Float)

    ai_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, index=True, nullable=False)
    endpoint = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)