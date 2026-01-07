from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from app.schema import ProductBatch
from app.ingestion import ingest_products
from app.auth import verify_api_key
from app.database import get_db
from app.schemas import ProductCreate, ProductRead
from app.models import Product
from app.scoring_v2 import analyze_product_complete

router = APIRouter(prefix="/products", tags=["Products"])


class ProductAnalysisRequest(BaseModel):
    """Request model for instant product analysis"""
    selling_price: float = Field(..., gt=0, description="Product selling price")
    product_cost: float = Field(..., gt=0, description="Cost from supplier")
    shipping_from_supplier: float = Field(default=0.0, ge=0, description="Shipping cost from supplier")
    shipping_to_customer: float = Field(default=0.0, ge=0, description="Shipping cost to customer")
    shipping_days: int = Field(default=14, ge=1, le=90, description="Estimated shipping days")
    seller_count: Optional[int] = Field(default=None, ge=0, description="Number of sellers")
    review_count: int = Field(default=0, ge=0, description="Total product reviews")
    platform: str = Field(default="shopify", description="Platform: shopify, amazon, etsy, tiktok")
    ad_cost_percent: float = Field(default=20.0, ge=0, le=100, description="Ad cost as % of selling price")


@router.post("/analyze")
def analyze_product(
    request: ProductAnalysisRequest,
    api_key=Depends(verify_api_key)
):
    """
    🎯 INSTANT PRODUCT ANALYSIS
    
    Get comprehensive profit analysis and success probability in seconds.
    This is the core feature that makes your platform worth $29/mo.
    
    Returns:
    - True net profit after ALL costs (platform fees, payment fees, ads, returns)
    - Success probability score (0-100%)
    - Clear BUY/SKIP recommendation
    - Key factors and warnings
    """
    try:
        analysis = analyze_product_complete(
            selling_price=request.selling_price,
            product_cost=request.product_cost,
            shipping_from_supplier=request.shipping_from_supplier,
            shipping_to_customer=request.shipping_to_customer,
            shipping_days=request.shipping_days,
            seller_count=request.seller_count,
            review_count=request.review_count,
            platform=request.platform.lower(),
            ad_cost_percent=request.ad_cost_percent,
        )
        
        return {
            "success": True,
            "analysis": analysis,
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analyze-products")
def analyze_products(
    batch: ProductBatch,
    api_key=Depends(verify_api_key)
):
    results = ingest_products([p.dict() for p in batch.products])
    return {
        "owner": api_key["key"],
        "count": len(results),
        "results": results
    }


@router.get("/health", dependencies=[Depends(verify_api_key)])
def health_check():
    return {"status": "ok"}


@router.post(
    "/",
    response_model=list[ProductRead],
    dependencies=[Depends(verify_api_key)]
)
def create_products(
    products: list[ProductCreate],
    db: Session = Depends(get_db)
):
    db_products = []

    for product in products:
        db_product = Product(**product.dict())
        db.add(db_product)
        db_products.append(db_product)

    db.commit()

    for p in db_products:
        db.refresh(p)

    return db_products
