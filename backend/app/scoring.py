def calculate_demand(review_count: int | None) -> float:
    if not review_count:
        return 0.2
    return min(review_count / 1000, 1.0)

def calculate_competition(review_count: int | None) -> float:
    if not review_count:
        return 0.8
    return max(1.0 - (review_count / 2000), 0.0)

def calculate_risk(shipping_time_days: int) -> float:
    if shipping_time_days <= 7:
        return 0.1
    if shipping_time_days <= 14:
        return 0.4
    return 0.8

def calculate_viability(demand: float, competition: float, risk: float) -> float:
    return round((demand * 0.4 + competition * 0.4 + (1 - risk) * 0.2), 2)
