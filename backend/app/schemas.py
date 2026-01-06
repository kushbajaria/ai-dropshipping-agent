# app/schemas.py

from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    supplier: str
    cost: float
    sale_price: float
    niche: str
