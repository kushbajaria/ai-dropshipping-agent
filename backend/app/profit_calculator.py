"""
True Profit Calculator - Accounts for ALL costs in dropshipping

This is what separates you from 90% of competitors who just show margin.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Optional
from enum import Enum


class Platform(Enum):
    """E-commerce platforms with different fee structures"""
    SHOPIFY = "shopify"
    AMAZON = "amazon"
    ETSY = "etsy"
    TIKTOK = "tiktok"
    EBAY = "ebay"
    CUSTOM = "custom"


class PaymentProcessor(Enum):
    """Payment processors with different fees"""
    STRIPE = "stripe"
    PAYPAL = "paypal"
    SHOPIFY_PAYMENTS = "shopify_payments"


@dataclass
class ProfitBreakdown:
    """Complete profit breakdown showing all costs"""
    
    # Revenue
    selling_price: float
    
    # Direct Costs
    product_cost: float
    shipping_from_supplier: float
    shipping_to_customer: float
    packaging_cost: float
    
    # Platform & Payment Fees
    platform_fee: float
    payment_processing_fee: float
    
    # Marketing & Risk
    estimated_ad_cost: float
    return_reserve: float
    
    # Calculated Values
    total_costs: float
    gross_profit: float
    net_profit: float
    gross_margin_percent: float
    net_margin_percent: float
    
    # Qualitative Assessment
    margin_rating: str
    is_profitable: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary with both raw and formatted values"""
        return {
            # Raw numeric values for calculations
            "selling_price": self.selling_price,
            "product_cost": self.product_cost,
            "shipping_from_supplier": self.shipping_from_supplier,
            "shipping_to_customer": self.shipping_to_customer,
            "packaging_cost": self.packaging_cost,
            "platform_fee": self.platform_fee,
            "payment_processing_fee": self.payment_processing_fee,
            "ad_cost": self.estimated_ad_cost,
            "return_reserve": self.return_reserve,
            "total_costs": self.total_costs,
            "gross_profit": self.gross_profit,
            "net_profit": self.net_profit,
            "gross_margin_percent": self.gross_margin_percent,
            "net_margin_percent": self.net_margin_percent,
            "margin_rating": self.margin_rating,
            "is_profitable": self.is_profitable,
            
            # Formatted for display
            "formatted": {
                "revenue": {
                    "selling_price": f"${self.selling_price:.2f}",
                },
                "costs": {
                    "product": f"${self.product_cost:.2f}",
                    "shipping_from_supplier": f"${self.shipping_from_supplier:.2f}",
                    "shipping_to_customer": f"${self.shipping_to_customer:.2f}",
                    "packaging": f"${self.packaging_cost:.2f}",
                    "platform_fee": f"${self.platform_fee:.2f}",
                    "payment_fee": f"${self.payment_processing_fee:.2f}",
                    "estimated_ads": f"${self.estimated_ad_cost:.2f}",
                    "return_reserve": f"${self.return_reserve:.2f}",
                    "total": f"${self.total_costs:.2f}",
                },
                "profit": {
                    "gross": f"${self.gross_profit:.2f}",
                    "net": f"${self.net_profit:.2f}",
                    "gross_margin": f"{self.gross_margin_percent:.1f}%",
                    "net_margin": f"{self.net_margin_percent:.1f}%",
                },
                "assessment": {
                    "rating": self.margin_rating,
                    "is_profitable": self.is_profitable,
                    "recommendation": self._get_recommendation()
                }
            }
        }
    
    def _get_recommendation(self) -> str:
        """Get actionable recommendation based on profitability"""
        if self.net_margin_percent >= 40:
            return "🟢 Excellent margins - strong opportunity"
        elif self.net_margin_percent >= 25:
            return "🟢 Good margins - proceed with confidence"
        elif self.net_margin_percent >= 15:
            return "🟡 Acceptable margins - watch your costs closely"
        elif self.net_margin_percent >= 10:
            return "🟡 Thin margins - requires high volume to be worthwhile"
        else:
            return "🔴 Margins too low - skip this product"


class ProfitCalculator:
    """
    Calculate true profit accounting for ALL dropshipping costs.
    
    This is your competitive advantage - most tools only show gross profit.
    """
    
    # Platform fee structures (as of 2024-2025)
    PLATFORM_FEES = {
        Platform.SHOPIFY: {
            "percent": 0.029,      # 2.9% + $0.30 (Basic plan)
            "fixed": 0.30,
            "description": "Shopify Payments (Basic plan)"
        },
        Platform.AMAZON: {
            "percent": 0.15,       # ~15% referral fee (average)
            "fixed": 0.0,
            "description": "Amazon Referral Fee"
        },
        Platform.ETSY: {
            "percent": 0.065,      # 6.5% transaction fee
            "fixed": 0.0,
            "description": "Etsy Transaction Fee"
        },
        Platform.TIKTOK: {
            "percent": 0.05,       # 5% platform fee
            "fixed": 0.0,
            "description": "TikTok Shop Fee"
        },
        Platform.EBAY: {
            "percent": 0.1275,     # 12.75% final value fee
            "fixed": 0.30,
            "description": "eBay Final Value Fee"
        },
    }
    
    # Payment processor fees
    PAYMENT_FEES = {
        PaymentProcessor.STRIPE: {
            "percent": 0.029,
            "fixed": 0.30,
            "description": "Stripe Standard"
        },
        PaymentProcessor.PAYPAL: {
            "percent": 0.0349,     # 3.49% for goods & services
            "fixed": 0.49,
            "description": "PayPal Goods & Services"
        },
        PaymentProcessor.SHOPIFY_PAYMENTS: {
            "percent": 0.029,
            "fixed": 0.30,
            "description": "Shopify Payments"
        },
    }
    
    @classmethod
    def calculate(
        cls,
        selling_price: float,
        product_cost: float,
        shipping_from_supplier: float = 0.0,
        shipping_to_customer: float = 0.0,
        platform: Platform = Platform.SHOPIFY,
        payment_processor: Optional[PaymentProcessor] = None,
        ad_cost_percent: float = 20.0,
        return_rate_percent: float = 3.0,
        packaging_cost: float = 1.0,
        custom_platform_fee_percent: Optional[float] = None,
        custom_payment_fee_percent: Optional[float] = None,
    ) -> ProfitBreakdown:
        """
        Calculate complete profit breakdown with all costs.
        
        Args:
            selling_price: Price you sell to customer
            product_cost: Cost from supplier
            shipping_from_supplier: Cost to ship from supplier to you
            shipping_to_customer: Cost to ship to customer
            platform: E-commerce platform (affects fees)
            payment_processor: Payment processor (defaults to platform default)
            ad_cost_percent: Expected ad spend as % of selling price (15-25% typical)
            return_rate_percent: Expected return/refund rate (2-5% typical)
            packaging_cost: Cost of packaging materials
            custom_platform_fee_percent: Override platform fee %
            custom_payment_fee_percent: Override payment fee %
        
        Returns:
            ProfitBreakdown with complete cost analysis
        """
        
        # Get platform fees
        if custom_platform_fee_percent is not None:
            platform_fee = selling_price * (custom_platform_fee_percent / 100)
        else:
            platform_config = cls.PLATFORM_FEES.get(platform, cls.PLATFORM_FEES[Platform.SHOPIFY])
            platform_fee = (selling_price * platform_config["percent"]) + platform_config["fixed"]
        
        # Get payment processing fees
        if custom_payment_fee_percent is not None:
            payment_fee = selling_price * (custom_payment_fee_percent / 100)
        else:
            # Default payment processor based on platform
            if payment_processor is None:
                if platform == Platform.SHOPIFY:
                    payment_processor = PaymentProcessor.SHOPIFY_PAYMENTS
                else:
                    payment_processor = PaymentProcessor.STRIPE
            
            payment_config = cls.PAYMENT_FEES.get(
                payment_processor, 
                cls.PAYMENT_FEES[PaymentProcessor.STRIPE]
            )
            payment_fee = (selling_price * payment_config["percent"]) + payment_config["fixed"]
        
        # Calculate marketing costs (typically 15-25% of selling price for profitable dropshipping)
        ad_cost = selling_price * (ad_cost_percent / 100)
        
        # Calculate return/refund reserve (typically 2-5%)
        return_reserve = selling_price * (return_rate_percent / 100)
        
        # Calculate total costs
        total_costs = (
            product_cost +
            shipping_from_supplier +
            shipping_to_customer +
            packaging_cost +
            platform_fee +
            payment_fee +
            ad_cost +
            return_reserve
        )
        
        # Calculate profits
        gross_profit = selling_price - product_cost  # Basic margin
        net_profit = selling_price - total_costs      # True profit
        
        # Calculate margin percentages
        gross_margin_percent = (gross_profit / selling_price * 100) if selling_price > 0 else 0
        net_margin_percent = (net_profit / selling_price * 100) if selling_price > 0 else 0
        
        # Determine margin rating
        margin_rating = cls._get_margin_rating(net_margin_percent)
        
        # Check if profitable (minimum 15% net margin recommended)
        is_profitable = net_margin_percent >= 15.0
        
        return ProfitBreakdown(
            selling_price=selling_price,
            product_cost=product_cost,
            shipping_from_supplier=shipping_from_supplier,
            shipping_to_customer=shipping_to_customer,
            packaging_cost=packaging_cost,
            platform_fee=platform_fee,
            payment_processing_fee=payment_fee,
            estimated_ad_cost=ad_cost,
            return_reserve=return_reserve,
            total_costs=total_costs,
            gross_profit=gross_profit,
            net_profit=net_profit,
            gross_margin_percent=gross_margin_percent,
            net_margin_percent=net_margin_percent,
            margin_rating=margin_rating,
            is_profitable=is_profitable,
        )
    
    @staticmethod
    def _get_margin_rating(net_margin_percent: float) -> str:
        """
        Get qualitative rating for profit margin.
        
        Industry benchmarks:
        - 40%+: Excellent (premium/unique products)
        - 25-40%: Good (healthy dropshipping margin)
        - 15-25%: Acceptable (need volume)
        - 10-15%: Thin (risky, requires optimization)
        - <10%: Too Low (unprofitable after real costs)
        """
        if net_margin_percent >= 40:
            return "EXCELLENT"
        elif net_margin_percent >= 25:
            return "GOOD"
        elif net_margin_percent >= 15:
            return "ACCEPTABLE"
        elif net_margin_percent >= 10:
            return "THIN"
        else:
            return "TOO_LOW"
    
    @classmethod
    def compare_platforms(
        cls,
        selling_price: float,
        product_cost: float,
        shipping_from_supplier: float = 0.0,
        shipping_to_customer: float = 0.0,
        ad_cost_percent: float = 20.0,
    ) -> Dict[str, ProfitBreakdown]:
        """
        Compare profitability across different platforms.
        
        This helps users decide which platform to sell on.
        """
        results = {}
        
        for platform in [Platform.SHOPIFY, Platform.AMAZON, Platform.ETSY, Platform.TIKTOK]:
            breakdown = cls.calculate(
                selling_price=selling_price,
                product_cost=product_cost,
                shipping_from_supplier=shipping_from_supplier,
                shipping_to_customer=shipping_to_customer,
                platform=platform,
                ad_cost_percent=ad_cost_percent,
            )
            results[platform.value] = breakdown
        
        return results
    
    @classmethod
    def recommend_price(
        cls,
        product_cost: float,
        shipping_from_supplier: float = 0.0,
        shipping_to_customer: float = 0.0,
        target_margin_percent: float = 30.0,
        platform: Platform = Platform.SHOPIFY,
    ) -> float:
        """
        Recommend selling price to achieve target margin.
        
        Useful for pricing new products.
        """
        # Get platform fee rate
        platform_config = cls.PLATFORM_FEES.get(platform, cls.PLATFORM_FEES[Platform.SHOPIFY])
        platform_fee_rate = platform_config["percent"]
        platform_fixed = platform_config["fixed"]
        
        # Get payment fee rate (use default)
        payment_config = cls.PAYMENT_FEES[PaymentProcessor.STRIPE]
        payment_fee_rate = payment_config["percent"]
        payment_fixed = payment_config["fixed"]
        
        # Assume 20% ad cost and 3% return rate
        ad_rate = 0.20
        return_rate = 0.03
        
        # Calculate required selling price
        # Formula: selling_price * (1 - all_rates - target_margin) = costs + fixed_fees
        all_rates = platform_fee_rate + payment_fee_rate + ad_rate + return_rate
        base_costs = product_cost + shipping_from_supplier + shipping_to_customer + 1.0  # +1 for packaging
        fixed_fees = platform_fixed + payment_fixed
        
        # Solve for selling_price
        target_margin_rate = target_margin_percent / 100
        selling_price = (base_costs + fixed_fees) / (1 - all_rates - target_margin_rate)
        
        # Round to nearest $0.99 (psychological pricing)
        return round(selling_price - 0.01, 2)


# Example usage
if __name__ == "__main__":
    # Example product
    breakdown = ProfitCalculator.calculate(
        selling_price=39.99,
        product_cost=12.00,
        shipping_from_supplier=3.50,
        shipping_to_customer=5.00,
        platform=Platform.SHOPIFY,
        ad_cost_percent=20.0,
    )
    
    print("Profit Breakdown:")
    print(f"Selling Price: ${breakdown.selling_price:.2f}")
    print(f"Total Costs: ${breakdown.total_costs:.2f}")
    print(f"Net Profit: ${breakdown.net_profit:.2f}")
    print(f"Net Margin: {breakdown.net_margin_percent:.1f}%")
    print(f"Rating: {breakdown.margin_rating}")
    print(f"Profitable: {breakdown.is_profitable}")
    print("\nFormatted:")
    import json
    print(json.dumps(breakdown.to_dict(), indent=2))
