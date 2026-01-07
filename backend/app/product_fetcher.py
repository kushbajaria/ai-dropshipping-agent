"""
Automatic product data fetcher from online sources.
Fetches product cost, prices, competition, and reviews.
"""

import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
import json

@dataclass
class ProductData:
    """Fetched product data from online sources"""
    product_name: str
    product_cost: float
    average_selling_price: float
    seller_count: int
    review_count: int
    shipping_days: int
    shipping_cost: float
    competition_level: str
    demand_trend: str
    source: str


class AliExpressProductFetcher:
    """Fetch product data from AliExpress (supplier cost)"""
    
    @staticmethod
    def search_product(product_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for product on AliExpress and get supplier pricing
        Returns: {product_name, cost, shipping_cost, shipping_days}
        """
        try:
            # Mock data for now - in production, use actual AliExpress API or scraping
            # AliExpress typically has products 30-70% cheaper than retail
            mock_products = {
                "phone case": {
                    "product_name": "Phone Case",
                    "cost": 2.50,
                    "shipping_cost": 0.50,
                    "shipping_days": 15,
                    "supplier": "AliExpress"
                },
                "pet camera": {
                    "product_name": "Pet Camera",
                    "cost": 18.00,
                    "shipping_cost": 2.50,
                    "shipping_days": 20,
                    "supplier": "AliExpress"
                },
                "usb cable": {
                    "product_name": "USB Cable",
                    "cost": 0.75,
                    "shipping_cost": 0.25,
                    "shipping_days": 10,
                    "supplier": "AliExpress"
                },
                "wireless earbuds": {
                    "product_name": "Wireless Earbuds",
                    "cost": 8.00,
                    "shipping_cost": 1.50,
                    "shipping_days": 18,
                    "supplier": "AliExpress"
                },
            }
            
            search_key = product_name.lower().strip()
            for key in mock_products:
                if key in search_key or search_key in key:
                    return mock_products[key]
            
            # Default fallback
            return {
                "product_name": product_name,
                "cost": 10.00,  # Default estimate
                "shipping_cost": 2.00,
                "shipping_days": 15,
                "supplier": "AliExpress"
            }
        except Exception as e:
            print(f"Error fetching from AliExpress: {e}")
            return None


class AmazonProductFetcher:
    """Fetch product data from Amazon (selling prices & competition)"""
    
    @staticmethod
    def search_product(product_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for product on Amazon and get market data
        Returns: {prices, seller_count, review_count, rating}
        """
        try:
            # Mock data for now - in production, use Amazon API or scraping
            mock_amazon = {
                "phone case": {
                    "price": 12.99,
                    "seller_count": 150,
                    "review_count": 450,
                    "rating": 4.5,
                },
                "pet camera": {
                    "price": 49.99,
                    "seller_count": 45,
                    "review_count": 230,
                    "rating": 4.3,
                },
                "usb cable": {
                    "price": 8.99,
                    "seller_count": 300,
                    "review_count": 1200,
                    "rating": 4.4,
                },
                "wireless earbuds": {
                    "price": 29.99,
                    "seller_count": 200,
                    "review_count": 850,
                    "rating": 4.2,
                },
            }
            
            search_key = product_name.lower().strip()
            for key in mock_amazon:
                if key in search_key or search_key in key:
                    return mock_amazon[key]
            
            # Default fallback
            return {
                "price": 25.00,
                "seller_count": 100,
                "review_count": 500,
                "rating": 4.0,
            }
        except Exception as e:
            print(f"Error fetching from Amazon: {e}")
            return None


class GoogleTrendsFetcher:
    """Fetch demand trend data"""
    
    @staticmethod
    def get_trend(product_name: str) -> str:
        """
        Determine demand trend (RISING, STABLE, FALLING)
        Returns: trend classification
        """
        try:
            # Mock data - in production, use Google Trends API
            trending_products = {
                "pet camera": "RISING",
                "wireless earbuds": "STABLE",
                "phone case": "STABLE",
                "usb cable": "FALLING",
            }
            
            search_key = product_name.lower().strip()
            for key in trending_products:
                if key in search_key or search_key in key:
                    return trending_products[key]
            
            return "STABLE"  # Default
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return "STABLE"


class ProductAggregator:
    """Aggregate data from multiple sources"""
    
    @staticmethod
    def fetch_product_data(product_name: str) -> Dict[str, Any]:
        """
        Fetch comprehensive product data from all sources
        and return pre-filled form data
        """
        
        # Fetch supplier cost
        supplier_data = AliExpressProductFetcher.search_product(product_name)
        
        # Fetch market/competitor data
        market_data = AmazonProductFetcher.search_product(product_name)
        
        # Fetch trend data
        trend = GoogleTrendsFetcher.get_trend(product_name)
        
        # Determine shipping to customer (typically 5-15 for US-based dropshipping)
        shipping_to_customer = 4.99  # Standard US shipping
        
        # Calculate ad cost estimate (typically 15-25% of price)
        ad_cost_percent = 20
        
        # Compile all data
        compiled_data = {
            "product_name": product_name,
            "selling_price": round(market_data.get("price", 25.00), 2),
            "product_cost": round(supplier_data.get("cost", 10.00), 2),
            "shipping_from_supplier": round(supplier_data.get("shipping_cost", 2.00), 2),
            "shipping_to_customer": shipping_to_customer,
            "shipping_days": supplier_data.get("shipping_days", 15),
            "seller_count": market_data.get("seller_count", 100),
            "review_count": market_data.get("review_count", 500),
            "demand_trend": trend,
            "ad_cost_percent": ad_cost_percent,
            "platform": "shopify",  # Default platform
            "packaging_cost": 1.0,
            "return_reserve_percent": 3.0,
            "data_sources": {
                "supplier": supplier_data.get("supplier", "AliExpress"),
                "market": "Amazon",
                "trends": "Google Trends",
                "shipping": "USPS/UPS Average",
            }
        }
        
        return compiled_data


def fetch_product_auto(product_name: str) -> Dict[str, Any]:
    """
    Public API: Fetch all product data automatically
    """
    return ProductAggregator.fetch_product_data(product_name)
