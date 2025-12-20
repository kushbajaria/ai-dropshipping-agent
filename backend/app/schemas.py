from pydantic import BaseModel

class ProductIn(BaseModel):
    title: str
    source: str
    category: str

    cost_price: float
    shipping_cost: float
    shipping_time_days: int

    selling_price: float
    rating: float | None = None
    review_count: int | None = None
