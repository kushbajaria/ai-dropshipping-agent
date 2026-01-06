from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    cost: float
    sale_price: float
    shipping_days: int
    competition_level: float

class ProductRead(ProductCreate):
    id: int
    viability_score: Optional[float]
    risk_score: Optional[float]
    competition_score: Optional[float]
    insight: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
