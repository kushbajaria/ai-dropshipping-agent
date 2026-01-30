"""
Test database integration with product analysis
"""

from sqlalchemy import func
from app.database import SessionLocal
from app.product_fetcher import fetch_product_auto
from app.scoring_v2 import analyze_product_complete
from app.models import Product
import json

def test_save_analysis():
    """Test saving a product analysis to the database"""
    
    db = SessionLocal()
    
    try:
        print("🔍 Fetching product data for 'wireless earbuds'...")
        product_data = fetch_product_auto("wireless earbuds")
        
        print("\n📊 Analyzing product...")
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
        
        print(f"\n✅ Analysis complete!")
        print(f"   Recommendation: {analysis['success_analysis']['recommendation']}")
        print(f"   Success Score: {analysis['success_analysis']['success_probability']}%")
        print(f"   Net Profit: ${analysis['profit_analysis']['net_profit']:.2f}")
        
        print("\n💾 Saving to database...")
        profit_breakdown = analysis["profit_analysis"]
        success_analysis = analysis["success_analysis"]
        
        db_product = Product(
            name="wireless earbuds",
            supplier=product_data["data_sources"]["supplier"],
            niche="Electronics",
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
        
        print(f"✅ Saved to database with ID: {db_product.id}")
        
        # Retrieve and verify
        print("\n🔄 Retrieving from database...")
        retrieved = db.query(Product).filter(Product.id == db_product.id).first()
        
        if retrieved:
            print(f"✅ Retrieved successfully!")
            print(f"   Name: {retrieved.name}")
            print(f"   Net Profit: ${retrieved.net_profit:.2f}")
            print(f"   Recommendation: {retrieved.recommendation}")
            print(f"   Success Score: {retrieved.success_probability}%")
            print(f"   Key Factors: {len(retrieved.key_factors.get('factors', []))} factors")
        
        # Get stats
        print("\n📊 Database Statistics:")
        total = db.query(Product).count()
        avg_profit = db.query(func.avg(Product.net_profit)).filter(Product.net_profit.isnot(None)).scalar()
        
        print(f"   Total products: {total}")
        print(f"   Average profit: ${avg_profit:.2f}" if avg_profit else "   Average profit: N/A")
        
        print("\n✅ DATABASE INTEGRATION TEST PASSED!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_save_analysis()
