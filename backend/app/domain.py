class ProductData:
    def __init__(
        self,
        name: str,
        cost: float,
        sale_price: float,
        shipping_days: int,
        competition_level: float
    ):
        self.name = name
        self.cost = cost
        self.sale_price = sale_price
        self.shipping_days = shipping_days
        self.competition_level = competition_level
