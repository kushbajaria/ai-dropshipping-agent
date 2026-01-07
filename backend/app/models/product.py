from sqlalchemy import String, Float, Integer, JSON, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    # Basic Info
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    supplier: Mapped[str] = mapped_column(String(255))
    niche: Mapped[str] = mapped_column(String(100))
    platform: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="shopify")

    # Pricing - Basic
    cost: Mapped[float] = mapped_column(Float)  # Product cost from supplier
    sale_price: Mapped[float] = mapped_column(Float)  # Selling price to customer
    
    # Pricing - Detailed Costs (NEW)
    shipping_from_supplier: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)
    shipping_to_customer: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)
    packaging_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=1.0)
    platform_fee: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    payment_fee: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ad_cost_estimate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    return_reserve: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Profit Calculations (NEW - calculated from above)
    gross_profit: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    net_profit: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    gross_margin_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    net_margin_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    margin_rating: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # EXCELLENT, GOOD, etc.
    
    # Market Intelligence
    shipping_days: Mapped[int] = mapped_column(Integer)
    competition_level: Mapped[float] = mapped_column(Float)
    seller_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # NEW
    review_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # NEW
    demand_trend: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # RISING, STABLE, FALLING
    
    # Success Analysis (NEW)
    success_probability: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 0-100
    recommendation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # STRONG_BUY, CONSIDER, SKIP
    confidence_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # HIGH, MEDIUM, LOW
    
    # AI Insights
    ai_analysis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Detailed analysis
    key_factors: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # List of factors
    warnings: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # List of warnings
    
    # Metadata
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
