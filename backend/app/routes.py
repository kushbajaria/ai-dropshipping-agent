from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from pydantic import BaseModel, Field
from typing import Optional, List

from app.schema import ProductBatch
from app.ingestion import ingest_products
from app.auth import verify_api_key
from app.database import get_db
from app.schemas import ProductCreate, ProductRead, ProductAnalysisCreate
from app.models import Product
from app.scoring_v2 import analyze_product_complete
from app.product_fetcher import fetch_product_auto

router = APIRouter(prefix="/products", tags=["Products"])


class ProductAnalysisRequest(BaseModel):
    """Request model for instant product analysis"""
    product_name: str = Field(default="Unknown Product", description="Product name")
    selling_price: float = Field(..., gt=0, description="Product selling price")
    product_cost: float = Field(..., gt=0, description="Cost from supplier")
    shipping_from_supplier: float = Field(default=0.0, ge=0, description="Shipping cost from supplier")
    shipping_to_customer: float = Field(default=0.0, ge=0, description="Shipping cost to customer")
    shipping_days: int = Field(default=14, ge=1, le=90, description="Estimated shipping days")
    seller_count: Optional[int] = Field(default=None, ge=0, description="Number of sellers")
    review_count: int = Field(default=0, ge=0, description="Total product reviews")
    platform: str = Field(default="shopify", description="Platform: shopify, amazon, etsy, tiktok")
    ad_cost_percent: float = Field(default=20.0, ge=0, le=100, description="Ad cost as % of selling price")
    save_to_db: bool = Field(default=False, description="Save this analysis to database")


@router.post("/analyze")
def analyze_product(
    request: ProductAnalysisRequest,
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db)
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
    
    Optionally saves results to database if save_to_db=true
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
        
        saved_product_id = None
        if request.save_to_db:
            # Save analysis to database
            profit_breakdown = analysis["profit_analysis"]
            success_analysis = analysis["success_analysis"]
            
            db_product = Product(
                name=request.product_name,
                supplier="Auto-detected",
                niche="General",
                platform=request.platform.lower(),
                cost=request.product_cost,
                sale_price=request.selling_price,
                shipping_from_supplier=request.shipping_from_supplier,
                shipping_to_customer=request.shipping_to_customer,
                packaging_cost=profit_breakdown.get("packaging_cost", 1.0),
                platform_fee=profit_breakdown.get("platform_fee"),
                payment_fee=profit_breakdown.get("payment_processing_fee"),
                ad_cost_estimate=profit_breakdown.get("ad_cost"),
                return_reserve=profit_breakdown.get("return_reserve"),
                gross_profit=profit_breakdown.get("gross_profit"),
                net_profit=profit_breakdown.get("net_profit"),
                gross_margin_percent=profit_breakdown.get("gross_margin_percent"),
                net_margin_percent=profit_breakdown.get("net_margin_percent"),
                margin_rating=profit_breakdown.get("margin_rating"),
                shipping_days=request.shipping_days,
                competition_level=success_analysis.get("success_probability", 0) / 100.0,
                seller_count=request.seller_count,
                review_count=request.review_count,
                demand_trend=None,  # Not provided in manual entry
                success_probability=success_analysis.get("success_probability"),
                recommendation=success_analysis.get("recommendation"),
                confidence_level=success_analysis.get("confidence"),
                ai_analysis=success_analysis.get("action"),
                key_factors={"factors": success_analysis.get("factors", [])},
                warnings={"warnings": success_analysis.get("warnings", [])}
            )
            
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            saved_product_id = db_product.id
        
        return {
            "success": True,
            "analysis": analysis,
            "saved_product_id": saved_product_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/search")
def search_product(
    product_name: str,
    save_to_db: bool = False,
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    🔍 AUTO-FETCH PRODUCT DATA
    
    Enter just a product name and we automatically fetch:
    - Supplier cost (from AliExpress)
    - Average selling prices (from Amazon)
    - Competition level (seller count, reviews)
    - Shipping information
    - Market demand trend
    
    Returns pre-filled analysis ready to evaluate.
    Optionally saves to database if save_to_db=true
    """
    try:
        # Fetch all product data automatically
        product_data = fetch_product_auto(product_name)
        
        # Immediately analyze it
        analysis = analyze_product_complete(
            selling_price=product_data["selling_price"],
            product_cost=product_data["product_cost"],
            shipping_from_supplier=product_data["shipping_from_supplier"],
            shipping_to_customer=product_data["shipping_to_customer"],
            shipping_days=product_data["shipping_days"],
            seller_count=product_data["seller_count"],
            review_count=product_data["review_count"],
            platform=product_data["platform"],
            ad_cost_percent=product_data["ad_cost_percent"],
        )
        
        saved_product_id = None
        if save_to_db:
            # Save analysis to database
            profit_breakdown = analysis["profit_analysis"]
            success_analysis = analysis["success_analysis"]
            
            db_product = Product(
                name=product_name,
                supplier=product_data["data_sources"]["supplier"],
                niche="General",
                platform=product_data["platform"],
                cost=product_data["product_cost"],
                sale_price=product_data["selling_price"],
                shipping_from_supplier=product_data["shipping_from_supplier"],
                shipping_to_customer=product_data["shipping_to_customer"],
                packaging_cost=product_data.get("packaging_cost", 1.0),
                platform_fee=profit_breakdown.get("platform_fee"),
                payment_fee=profit_breakdown.get("payment_processing_fee"),
                ad_cost_estimate=profit_breakdown.get("ad_cost"),
                return_reserve=profit_breakdown.get("return_reserve"),
                gross_profit=profit_breakdown.get("gross_profit"),
                net_profit=profit_breakdown.get("net_profit"),
                gross_margin_percent=profit_breakdown.get("gross_margin_percent"),
                net_margin_percent=profit_breakdown.get("net_margin_percent"),
                margin_rating=profit_breakdown.get("margin_rating"),
                shipping_days=product_data["shipping_days"],
                competition_level=success_analysis.get("success_probability", 0) / 100.0,
                seller_count=product_data["seller_count"],
                review_count=product_data["review_count"],
                demand_trend=product_data.get("demand_trend"),
                success_probability=success_analysis.get("success_probability"),
                recommendation=success_analysis.get("recommendation"),
                confidence_level=success_analysis.get("confidence"),
                ai_analysis=success_analysis.get("action"),
                key_factors={"factors": success_analysis.get("factors", [])},
                warnings={"warnings": success_analysis.get("warnings", [])}
            )
            
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            saved_product_id = db_product.id
        
        return {
            "success": True,
            "product_name": product_name,
            "fetched_data": product_data,
            "analysis": analysis,
            "saved_product_id": saved_product_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/saved", response_model=List[ProductRead])
def get_saved_products(
    limit: int = Query(default=50, le=200),
    skip: int = Query(default=0, ge=0),
    recommendation: Optional[str] = Query(default=None, description="Filter by recommendation"),
    min_profit: Optional[float] = Query(default=None, description="Minimum net profit"),
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    📚 GET SAVED PRODUCTS
    
    Retrieve all products you've analyzed and saved.
    Filter by recommendation, minimum profit, etc.
    """
    try:
        query = db.query(Product).order_by(desc(Product.created_at))
        
        # Apply filters
        if recommendation:
            query = query.filter(Product.recommendation == recommendation)
        
        if min_profit is not None:
            query = query.filter(Product.net_profit >= min_profit)
        
        # Pagination
        products = query.offset(skip).limit(limit).all()
        
        return products
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/saved/{product_id}", response_model=ProductRead)
def get_saved_product(
    product_id: int,
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    📦 GET SINGLE SAVED PRODUCT
    
    Retrieve a specific saved product analysis by ID.
    """
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/saved/{product_id}")
def delete_saved_product(
    product_id: int,
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    🗑️ DELETE SAVED PRODUCT
    
    Remove a saved product from your database.
    """
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(product)
        db.commit()
        
        return {"success": True, "message": "Product deleted"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_analysis_stats(
    api_key=Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    📊 GET ANALYSIS STATISTICS
    
    Get overview statistics about your saved products.
    """
    try:
        total_products = db.query(Product).count()
        strong_buy = db.query(Product).filter(Product.recommendation.like("%STRONG BUY%")).count()
        buy = db.query(Product).filter(Product.recommendation.like("%BUY%")).filter(~Product.recommendation.like("%STRONG BUY%")).count()
        consider = db.query(Product).filter(Product.recommendation.like("%CONSIDER%")).count()
        skip = db.query(Product).filter(Product.recommendation.like("%SKIP%") | Product.recommendation.like("%AVOID%")).count()
        
        avg_profit = db.query(func.avg(Product.net_profit)).filter(Product.net_profit.isnot(None)).scalar()
        avg_score = db.query(func.avg(Product.success_probability)).filter(Product.success_probability.isnot(None)).scalar()
        
        return {
            "total_products": total_products,
            "recommendations": {
                "strong_buy": strong_buy,
                "buy": buy,
                "consider": consider,
                "skip": skip
            },
            "averages": {
                "net_profit": round(avg_profit, 2) if avg_profit else 0,
                "success_score": round(avg_score, 1) if avg_score else 0
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
