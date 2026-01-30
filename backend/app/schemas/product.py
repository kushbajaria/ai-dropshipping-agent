from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime


class ProductAnalysisCreate(BaseModel):
    """Schema for saving a product analysis to the database"""
    name: str
    supplier: str = "Unknown"
    niche: str = "General"
    platform: str = "shopify"
    
    # Pricing
    cost: float
    sale_price: float
    shipping_from_supplier: float = 0.0
    shipping_to_customer: float = 0.0
    packaging_cost: float = 1.0
    platform_fee: Optional[float] = None
    payment_fee: Optional[float] = None
    ad_cost_estimate: Optional[float] = None
    return_reserve: Optional[float] = None
    
    # Profit calculations
    gross_profit: Optional[float] = None
    net_profit: Optional[float] = None
    gross_margin_percent: Optional[float] = None
    net_margin_percent: Optional[float] = None
    margin_rating: Optional[str] = None
    
    # Market data
    shipping_days: int
    competition_level: float
    seller_count: Optional[int] = None
    review_count: Optional[int] = None
    demand_trend: Optional[str] = None
    
    # Success analysis
    success_probability: Optional[int] = None
    recommendation: Optional[str] = None
    confidence_level: Optional[str] = None
    
    # AI insights
    ai_analysis: Optional[str] = None
    key_factors: Optional[Dict] = None
    warnings: Optional[Dict] = None


class ProductCreate(BaseModel):
    name: str
    cost: float
    sale_price: float
    shipping_days: int
    competition_level: float


class ProductRead(BaseModel):
    """Schema for reading a saved product from the database"""
    id: int
    name: str
    supplier: str
    niche: str
    platform: str
    
    # Pricing
    cost: float
    sale_price: float
    shipping_from_supplier: Optional[float]
    shipping_to_customer: Optional[float]
    packaging_cost: Optional[float]
    platform_fee: Optional[float]
    payment_fee: Optional[float]
    ad_cost_estimate: Optional[float]
    return_reserve: Optional[float]
    
    # Profit calculations
    gross_profit: Optional[float]
    net_profit: Optional[float]
    gross_margin_percent: Optional[float]
    net_margin_percent: Optional[float]
    margin_rating: Optional[str]
    
    # Market data
    shipping_days: int
    competition_level: float
    seller_count: Optional[int]
    review_count: Optional[int]
    demand_trend: Optional[str]
    
    # Success analysis
    success_probability: Optional[int]
    recommendation: Optional[str]
    confidence_level: Optional[str]
    
    # AI insights
    ai_analysis: Optional[str]
    key_factors: Optional[Dict]
    warnings: Optional[Dict]
    
    # Metadata
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
