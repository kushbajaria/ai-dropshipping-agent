from .domain import ProductData
from .scoring import calculate_viability, calculate_risk, calculate_competition
from .ai_insights import generate_product_insight
from .profit_calculator import ProfitCalculator, Platform
from .scoring_v2 import (
    analyze_product_complete,
    get_competition_level,
    get_demand_trend,
)


def ingest_products(raw_products: list[dict]) -> list[dict]:
    """
    Normalizes and scores a batch of raw products using the TRUE Profit Calculator.
    
    This is the enhanced version that provides complete profit analysis and success prediction.
    """
    processed = []

    for raw in raw_products:
        # Use new enhanced analysis
        analysis = analyze_product_complete(
            selling_price=raw["sale_price"],
            product_cost=raw["cost"],
            shipping_from_supplier=raw.get("shipping_from_supplier", 0.0),
            shipping_to_customer=raw.get("shipping_to_customer", 0.0),
            shipping_days=raw.get("shipping_days", 14),
            seller_count=raw.get("seller_count"),
            review_count=raw.get("review_count", 0),
            platform=raw.get("platform", "shopify"),
            ad_cost_percent=raw.get("ad_cost_percent", 20.0),
        )
        
        # Extract key info for response
        profit = analysis["profit_analysis"]
        success = analysis["success_analysis"]
        summary = analysis["summary"]
        
        # Legacy compatibility - keep old scores for backward compatibility
        review_count = raw.get("review_count", int(raw.get("competition_level", 0.5) * 2000))
        competition = calculate_competition(review_count)
        risk = calculate_risk(raw.get("shipping_days", 14))
        demand = raw["sale_price"] - raw["cost"]
        viability = calculate_viability(demand, competition, risk)
        
        # Create legacy product for insight generation
        product = ProductData(
            name=raw["name"],
            cost=raw["cost"],
            sale_price=raw["sale_price"],
            shipping_days=raw.get("shipping_days", 14),
            competition_level=raw.get("competition_level", 0.5)
        )
        
        scores = {
            "viability": viability,
            "risk": risk,
            "competition": competition,
        }
        
        insight = generate_product_insight(product, scores)
        
        # Return enhanced response with both legacy and new data
        processed.append({
            # Basic info
            "name": raw["name"],
            
            # Legacy scores (for backward compatibility)
            "viability_score": viability,
            "risk_score": risk,
            "competition_score": competition,
            "insight": insight,
            
            # NEW: Profit analysis
            "profit": {
                "selling_price": profit["selling_price"],
                "net_profit": profit["net_profit"],
                "net_margin_percent": profit["net_margin_percent"],
                "margin_rating": profit["margin_rating"],
                "is_profitable": profit["is_profitable"],
            },
            
            # NEW: Success prediction
            "success": {
                "probability": success["success_probability"],
                "recommendation": success["recommendation"],
                "action": success["action"],
                "confidence": success["confidence"],
            },
            
            # NEW: Summary
            "summary": summary,
            
            # NEW: Key factors and warnings
            "key_factors": success.get("key_factors", []),
            "warnings": success.get("warnings", []),
        })

    # Sort by success probability (new primary metric)
    return sorted(processed, key=lambda x: x["success"]["probability"], reverse=True)
