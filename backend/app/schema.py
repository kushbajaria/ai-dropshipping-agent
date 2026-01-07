# app/schema.py

from pydantic import BaseModel, Field
from typing import List, Optional

class ProductIn(BaseModel):
    """Input schema for product analysis"""
    name: str
    cost: float = Field(..., description="Product cost from supplier")
    sale_price: float = Field(..., description="Selling price to customer")
    shipping_days: int = Field(default=14, description="Estimated shipping days")
    competition_level: float = Field(default=0.5, description="Competition level 0-1 (legacy)")
    
    # New fields for enhanced profit calculation
    supplier: Optional[str] = Field(default="Unknown", description="Supplier name")
    niche: Optional[str] = Field(default="General", description="Product niche/category")
    platform: Optional[str] = Field(default="shopify", description="Platform: shopify, amazon, etsy, tiktok")
    shipping_from_supplier: Optional[float] = Field(default=0.0, description="Shipping cost from supplier")
    shipping_to_customer: Optional[float] = Field(default=0.0, description="Shipping cost to customer")
    seller_count: Optional[int] = Field(default=None, description="Number of sellers")
    review_count: Optional[int] = Field(default=0, description="Total product reviews")
    ad_cost_percent: Optional[float] = Field(default=20.0, description="Ad cost as % of selling price")

class ProductBatch(BaseModel):
    products: List[ProductIn]
