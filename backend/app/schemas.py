from pydantic import BaseModel
from typing import List


class ProductIn(BaseModel):
    name: str
    cost: float
    sale_price: float
    shipping_days: int
    competition_level: float


class ProductBatch(BaseModel):
    products: List[ProductIn]
