"""
Enhanced Product Scoring System v2
Uses True Profit Calculator to give accurate success predictions
"""

from enum import Enum
from typing import Dict, List, Optional
from .profit_calculator import ProfitCalculator, Platform


class CompetitionLevel(str, Enum):
    """Competition levels based on seller count"""
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class DemandTrend(str, Enum):
    """Market demand trend direction"""
    RISING = "RISING"
    STABLE = "STABLE"
    FALLING = "FALLING"


class Recommendation(str, Enum):
    """Product recommendation levels"""
    STRONG_BUY = "🟢 STRONG BUY"
    BUY = "🟢 BUY"
    CONSIDER = "🟡 CONSIDER"
    RISKY = "🟡 RISKY"
    SKIP = "🔴 SKIP"
    AVOID = "🔴 AVOID"


def get_competition_level(seller_count: Optional[int]) -> CompetitionLevel:
    """
    Determine competition level based on number of sellers.
    
    Benchmarks:
    - <10 sellers: Very easy to enter
    - 10-50: Still good opportunity
    - 50-200: Need differentiation
    - 200-500: Very competitive
    - 500+: Oversaturated
    """
    if seller_count is None:
        return CompetitionLevel.MEDIUM  # Default if unknown
    
    if seller_count < 10:
        return CompetitionLevel.VERY_LOW
    elif seller_count < 50:
        return CompetitionLevel.LOW
    elif seller_count < 200:
        return CompetitionLevel.MEDIUM
    elif seller_count < 500:
        return CompetitionLevel.HIGH
    else:
        return CompetitionLevel.VERY_HIGH


def get_demand_trend(review_velocity: Optional[float], review_count: int) -> DemandTrend:
    """
    Determine if demand is rising, stable, or falling.
    
    Args:
        review_velocity: Reviews per day (if available)
        review_count: Total reviews
    
    Returns:
        RISING if accelerating, STABLE if steady, FALLING if declining
    """
    if review_velocity is None:
        # Fall back to review count
        if review_count > 1000:
            return DemandTrend.STABLE  # Mature product
        elif review_count > 100:
            return DemandTrend.RISING  # Growing
        else:
            return DemandTrend.STABLE  # Unknown
    
    # Use velocity if available
    if review_velocity > 10:  # 10+ reviews/day = hot product
        return DemandTrend.RISING
    elif review_velocity > 1:  # Steady reviews
        return DemandTrend.STABLE
    else:  # Slowing down
        return DemandTrend.FALLING


def calculate_success_probability(
    net_profit: float,
    net_margin_percent: float,
    competition_level: CompetitionLevel,
    demand_trend: DemandTrend,
    shipping_days: int,
    review_count: int,
    price_point: float,
    is_profitable: bool,
) -> Dict:
    """
    Calculate probability of success (0-100%) based on multiple factors.
    
    This is the CORE VALUE of your platform - one clear answer.
    
    Weighting:
    - Profit Margin: 40% (most important - can't succeed without profit)
    - Competition: 30% (affects ability to get traffic)
    - Demand Trend: 15% (market timing matters)
    - Shipping: 10% (affects conversion rate)
    - Social Proof: 5% (validation that product works)
    """
    
    score = 0
    factors = []
    warnings = []
    
    # 1. PROFIT MARGIN (40% weight) - Most critical factor
    if not is_profitable:
        # Product is fundamentally unprofitable
        score += 0
        warnings.append("❌ Not profitable after all costs - AVOID")
    elif net_margin_percent >= 40:
        score += 40
        factors.append(f"✅ Excellent {net_margin_percent:.0f}% profit margin")
    elif net_margin_percent >= 30:
        score += 35
        factors.append(f"✅ Great {net_margin_percent:.0f}% margin")
    elif net_margin_percent >= 25:
        score += 28
        factors.append(f"✅ Good {net_margin_percent:.0f}% margin")
    elif net_margin_percent >= 20:
        score += 22
        factors.append(f"✅ Decent {net_margin_percent:.0f}% margin")
    elif net_margin_percent >= 15:
        score += 15
        factors.append(f"⚠️ Acceptable {net_margin_percent:.0f}% margin")
        warnings.append("⚠️ Thin margins - need high volume")
    else:
        score += 5
        warnings.append(f"❌ Low {net_margin_percent:.0f}% margin - risky")
    
    # Show actual profit per sale
    if net_profit > 0:
        factors.append(f"💰 ${net_profit:.2f} profit per sale")
    
    # 2. COMPETITION (30% weight)
    comp_scores = {
        CompetitionLevel.VERY_LOW: 30,
        CompetitionLevel.LOW: 25,
        CompetitionLevel.MEDIUM: 15,
        CompetitionLevel.HIGH: 5,
        CompetitionLevel.VERY_HIGH: 0,
    }
    comp_score = comp_scores[competition_level]
    score += comp_score
    
    comp_labels = {
        CompetitionLevel.VERY_LOW: "Very low competition (<10 sellers)",
        CompetitionLevel.LOW: "Low competition (10-50 sellers)",
        CompetitionLevel.MEDIUM: "Medium competition (50-200 sellers)",
        CompetitionLevel.HIGH: "High competition (200-500 sellers)",
        CompetitionLevel.VERY_HIGH: "Very high competition (500+ sellers)",
    }
    
    if competition_level in [CompetitionLevel.VERY_LOW, CompetitionLevel.LOW]:
        factors.append(f"✅ {comp_labels[competition_level]}")
    elif competition_level == CompetitionLevel.MEDIUM:
        factors.append(f"⚠️ {comp_labels[competition_level]}")
        warnings.append("⚠️ Need unique angle to stand out")
    elif competition_level == CompetitionLevel.HIGH:
        warnings.append(f"⚠️ {comp_labels[competition_level]}")
        warnings.append("⚠️ Difficult market - strong marketing required")
    else:
        warnings.append(f"❌ {comp_labels[competition_level]}")
        warnings.append("❌ Oversaturated - very hard to compete")
    
    # 3. DEMAND TREND (15% weight)
    trend_scores = {
        DemandTrend.RISING: 15,
        DemandTrend.STABLE: 10,
        DemandTrend.FALLING: 0,
    }
    trend_score = trend_scores[demand_trend]
    score += trend_score
    
    if demand_trend == DemandTrend.RISING:
        factors.append("🔥 Growing market demand")
    elif demand_trend == DemandTrend.STABLE:
        factors.append("📊 Stable market demand")
    else:
        warnings.append("📉 Declining demand - market may be dying")
    
    # 4. SHIPPING SPEED (10% weight)
    if shipping_days <= 5:
        score += 10
        factors.append("⚡ Express shipping (≤5 days)")
    elif shipping_days <= 10:
        score += 7
        factors.append("✅ Fast shipping (≤10 days)")
    elif shipping_days <= 14:
        score += 4
        factors.append("⚠️ Standard shipping (≤14 days)")
    elif shipping_days <= 21:
        score += 2
        warnings.append("⚠️ Slow shipping (14-21 days)")
    else:
        score += 0
        warnings.append("❌ Very slow shipping - will hurt conversions")
    
    # 5. MARKET VALIDATION (5% weight) - Reviews = proven demand
    if review_count >= 1000:
        score += 5
        factors.append("✅ Strong validation (1000+ reviews)")
    elif review_count >= 500:
        score += 4
        factors.append("✅ Good validation (500+ reviews)")
    elif review_count >= 100:
        score += 3
        factors.append("✅ Proven product (100+ reviews)")
    elif review_count >= 20:
        score += 1
    else:
        warnings.append("⚠️ Unproven - limited market validation")
    
    # BONUS/PENALTY FACTORS
    
    # Impulse buy price point (<$30) - easier to convert
    if price_point <= 30:
        score += 5
        factors.append("💳 Impulse buy price point")
    
    # Premium price (>$100) - harder to convert, longer sales cycle
    if price_point > 100:
        score -= 5
        warnings.append("⚠️ Premium pricing - longer decision time")
    
    # Ensure score stays 0-100
    score = max(0, min(100, score))
    
    # DETERMINE RECOMMENDATION
    if score >= 80:
        recommendation = Recommendation.STRONG_BUY
        confidence = "Very High"
        action = "🚀 Launch immediately - strong opportunity"
    elif score >= 70:
        recommendation = Recommendation.BUY
        confidence = "High"
        action = "✅ Proceed with confidence"
    elif score >= 60:
        recommendation = Recommendation.CONSIDER
        confidence = "Medium"
        action = "🧪 Test with small batch first"
    elif score >= 45:
        recommendation = Recommendation.RISKY
        confidence = "Low"
        action = "⚠️ High risk - only if you have competitive edge"
    elif score >= 30:
        recommendation = Recommendation.SKIP
        confidence = "Very Low"
        action = "🛑 Not recommended - too risky"
    else:
        recommendation = Recommendation.AVOID
        confidence = "None"
        action = "❌ Definitely skip this product"
    
    return {
        "success_probability": score,
        "probability_text": f"{score}%",
        "recommendation": recommendation.value,
        "confidence": confidence,
        "action": action,
        "key_factors": factors,
        "warnings": warnings,
        "score_breakdown": {
            "margin_contribution": min(net_margin_percent, 40),
            "competition_contribution": comp_score,
            "trend_contribution": trend_score,
            "shipping_contribution": min(10, 10 - (shipping_days / 3)),
            "validation_contribution": min(5, review_count / 200),
        }
    }


def analyze_product_complete(
    selling_price: float,
    product_cost: float,
    shipping_from_supplier: float = 0.0,
    shipping_to_customer: float = 0.0,
    shipping_days: int = 14,
    seller_count: Optional[int] = None,
    review_count: int = 0,
    review_velocity: Optional[float] = None,
    platform: str = "shopify",
    ad_cost_percent: float = 20.0,
) -> Dict:
    """
    Complete product analysis combining profit calculation and success scoring.
    
    This is the main function that powers your platform's recommendations.
    
    Returns:
        Complete analysis with profit breakdown, success probability, and recommendation
    """
    
    # Convert platform string to enum
    platform_enum = Platform.SHOPIFY
    if platform.lower() == "amazon":
        platform_enum = Platform.AMAZON
    elif platform.lower() == "etsy":
        platform_enum = Platform.ETSY
    elif platform.lower() == "tiktok":
        platform_enum = Platform.TIKTOK
    
    # 1. Calculate True Profit
    profit_breakdown = ProfitCalculator.calculate(
        selling_price=selling_price,
        product_cost=product_cost,
        shipping_from_supplier=shipping_from_supplier,
        shipping_to_customer=shipping_to_customer,
        platform=platform_enum,
        ad_cost_percent=ad_cost_percent,
    )
    
    # 2. Determine market factors
    competition_level = get_competition_level(seller_count)
    demand_trend = get_demand_trend(review_velocity, review_count)
    
    # 3. Calculate success probability
    success_analysis = calculate_success_probability(
        net_profit=profit_breakdown.net_profit,
        net_margin_percent=profit_breakdown.net_margin_percent,
        competition_level=competition_level,
        demand_trend=demand_trend,
        shipping_days=shipping_days,
        review_count=review_count,
        price_point=selling_price,
        is_profitable=profit_breakdown.is_profitable,
    )
    
    # 4. Combine into complete analysis
    return {
        "product_info": {
            "selling_price": selling_price,
            "product_cost": product_cost,
            "platform": platform,
        },
        "profit_analysis": profit_breakdown.to_dict(),
        "market_intelligence": {
            "competition_level": competition_level.value,
            "seller_count": seller_count,
            "demand_trend": demand_trend.value,
            "review_count": review_count,
            "shipping_days": shipping_days,
        },
        "success_analysis": success_analysis,
        "summary": {
            "recommendation": success_analysis["recommendation"],
            "success_probability": f"{success_analysis['success_probability']}%",
            "net_profit_per_sale": f"${profit_breakdown.net_profit:.2f}",
            "margin": f"{profit_breakdown.net_margin_percent:.1f}%",
            "action": success_analysis["action"],
        }
    }


# Example usage
if __name__ == "__main__":
    # Test with example product
    analysis = analyze_product_complete(
        selling_price=39.99,
        product_cost=12.00,
        shipping_from_supplier=3.50,
        shipping_to_customer=5.00,
        shipping_days=7,
        seller_count=45,
        review_count=230,
        platform="shopify",
    )
    
    import json
    print(json.dumps(analysis, indent=2))
