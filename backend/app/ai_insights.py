def generate_product_insight(product, scores: dict) -> str:
    """
    Generates a human-readable insight explaining product viability.
    """
    margin = product.sale_price - product.cost
    shipping_days = product.shipping_days
    viability = scores["viability"]
    competition = scores["competition"]
    risk = scores["risk"]

    reasons = []
    warnings = []

    if margin >= 15:
        reasons.append("healthy profit margin")
    else:
        warnings.append("low profit margin")

    if shipping_days <= 7:
        reasons.append("fast shipping time")
    else:
        warnings.append("slow shipping may reduce conversion rates")

    if competition > 0.7:
        warnings.append("high market competition")

    if risk > 0.6:
        warnings.append("elevated business risk")

    if viability >= 0.7:
        summary = "This product shows strong overall viability"
    elif viability >= 0.5:
        summary = "This product shows moderate viability"
    else:
        summary = "This product shows low viability"

    details = []

    if reasons:
        details.append("due to " + ", ".join(reasons))

    if warnings:
        details.append("however there are concerns such as " + ", ".join(warnings))

    return summary + " " + ". ".join(details) + "."
