from .domain import ProductData
from .scoring import calculate_viability, calculate_risk, calculate_competition
from .ai_insights import generate_product_insight


def ingest_products(raw_products: list[dict]) -> list[dict]:
    """
    Normalizes and scores a batch of raw products.
    """
    processed = []

    for raw in raw_products:
        product = ProductData(
            name=raw["name"],
            cost=raw["cost"],
            sale_price=raw["sale_price"],
            shipping_days=raw["shipping_days"],
            competition_level=raw["competition_level"]
        )

        # Map competition_level (0–1) to review count
        review_count = int(product.competition_level * 2000)
        competition = calculate_competition(review_count)

        # Risk based on shipping_days
        risk = calculate_risk(product.shipping_days)

        # Demand as numeric metric
        demand = product.sale_price - product.cost

        # Compute viability
        viability = calculate_viability(demand, competition, risk)


        scores = {
            "viability": viability,
            "risk": risk,
            "competition": competition,
        }

        insight = generate_product_insight(product, scores)

        processed.append({
            "name": product.name,
            "viability_score": viability,
            "risk_score": risk,
            "competition_score": competition,
            "insight": insight
        })

    return sorted(processed, key=lambda x: x["viability_score"], reverse=True)
