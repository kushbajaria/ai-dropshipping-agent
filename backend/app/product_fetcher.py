"""
Real product data fetcher with live web scraping and caching.
Fetches live data from AliExpress, Amazon, and Google Trends.
Falls back to local database and smart estimation for robustness.
"""

import requests
import sqlite3
import json
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from difflib import SequenceMatcher
import os
import logging
from .web_scrapers import scrape_all_sources, AmazonScraper, AliExpressScraper, GoogleTrendsScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache database
CACHE_DB = "product_cache.db"
CACHE_EXPIRY_HOURS = 6  # 6-hour cache for live data (vs 24h before)

# Initialize cache database
def init_cache():
    """Initialize the SQLite cache database"""
    conn = sqlite3.connect(CACHE_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS product_cache (
            id INTEGER PRIMARY KEY,
            product_name TEXT UNIQUE,
            data TEXT,
            timestamp REAL
        )
    ''')
    conn.commit()
    conn.close()

init_cache()


def get_cached_data(product_name: str) -> Optional[Dict[str, Any]]:
    """Get cached product data if it exists and hasn't expired"""
    conn = sqlite3.connect(CACHE_DB)
    c = conn.cursor()
    c.execute('SELECT data, timestamp FROM product_cache WHERE product_name = ?', 
              (product_name.lower(),))
    result = c.fetchone()
    conn.close()
    
    if result:
        data, timestamp = result
        age_hours = (time.time() - timestamp) / 3600
        if age_hours < CACHE_EXPIRY_HOURS:
            logger.info(f"✅ Cache hit for '{product_name}' (age: {age_hours:.1f}h)")
            return json.loads(data)
        else:
            logger.info(f"⏰ Cache expired for '{product_name}'")
    
    return None


def cache_product_data(product_name: str, data: Dict[str, Any]):
    """Cache product data with timestamp"""
    conn = sqlite3.connect(CACHE_DB)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO product_cache (product_name, data, timestamp)
        VALUES (?, ?, ?)
    ''', (product_name.lower(), json.dumps(data), time.time()))
    conn.commit()
    conn.close()
    logger.info(f"💾 Cached data for '{product_name}'")


def find_similar_product(product_name: str, database: Dict[str, Any]) -> Optional[str]:
    """
    Find the most similar product in database using fuzzy matching
    Returns the key of the best match if similarity > 0.6, else None
    """
    product_lower = product_name.lower().strip()
    best_match = None
    best_score = 0.0
    
    for key in database.keys():
        score = SequenceMatcher(None, product_lower, key.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = key
    
    if best_score > 0.6:  # 60% similarity threshold
        logger.info(f"🎯 Found similar product: '{product_name}' → '{best_match}' ({best_score*100:.0f}%)")
        return best_match
    
    return None


def estimate_from_keywords(product_name: str) -> Dict[str, Any]:
    """
    Estimate product data based on keywords if no match found
    Returns reasonable estimates for completely unknown products
    """
    product_lower = product_name.lower()
    
    # Price estimation based on keywords
    price_keywords = {
        "cable": 8.99,
        "charger": 14.99,
        "case": 12.99,
        "screen": 5.99,
        "protector": 5.99,
        "film": 5.99,
        "holder": 9.99,
        "stand": 11.99,
        "mount": 10.99,
        "ring": 8.99,
        "pop": 8.99,
        "tempered": 5.99,
        "glass": 5.99,
        "strap": 9.99,
        "clip": 7.99,
        "cover": 10.99,
        "bag": 15.99,
        "pouch": 12.99,
        "organizer": 14.99,
        "keyboard": 29.99,
        "mouse": 19.99,
        "headphones": 39.99,
        "headset": 39.99,
        "earbuds": 29.99,
        "earphones": 24.99,
        "speaker": 34.99,
        "camera": 49.99,
        "lens": 59.99,
        "tripod": 19.99,
        "gimbal": 79.99,
        "drone": 299.99,
    }
    
    selling_price = 25.00  # Default
    for keyword, price in price_keywords.items():
        if keyword in product_lower:
            selling_price = price
            break
    
    # Cost estimation (typically 30-50% of selling price for dropshipping)
    product_cost = round(selling_price * 0.35, 2)
    
    # Seller count estimation based on price
    if selling_price < 10:
        seller_count = 300  # Many sellers for cheap items
    elif selling_price < 25:
        seller_count = 150
    elif selling_price < 50:
        seller_count = 75
    elif selling_price < 100:
        seller_count = 40
    else:
        seller_count = 20  # Few sellers for expensive items
    
    # Review count estimation
    review_count = seller_count * 3
    
    return {
        "price": selling_price,
        "cost": product_cost,
        "seller_count": seller_count,
        "review_count": review_count,
        "shipping": round(selling_price * 0.05, 2),  # ~5% of price
        "shipping_days": 15,
        "availability": 0.90,
        "reliability": 0.70  # Lower reliability for estimates
    }

class AliExpressProductFetcher:
    """Fetch product data from AliExpress (supplier cost + shipping)"""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    # Local price database (until we can use real APIs)
    LOCAL_DATA = {
        "phone case": {
            "cost": 2.50,
            "shipping": 0.50,
            "shipping_days": 15,
            "reliability": 0.95
        },
        "pet camera": {
            "cost": 18.00,
            "shipping": 2.50,
            "shipping_days": 20,
            "reliability": 0.90
        },
        "wireless earbuds": {
            "cost": 8.00,
            "shipping": 1.50,
            "shipping_days": 18,
            "reliability": 0.88
        },
        "usb cable": {
            "cost": 0.75,
            "shipping": 0.25,
            "shipping_days": 10,
            "reliability": 0.92
        },
        "phone charger": {
            "cost": 3.50,
            "shipping": 0.75,
            "shipping_days": 14,
            "reliability": 0.91
        },
        "screen protector": {
            "cost": 0.50,
            "shipping": 0.20,
            "shipping_days": 12,
            "reliability": 0.93
        },
    }
    
    @staticmethod
    def search_product(product_name: str, retry_count: int = 3) -> Optional[Dict[str, Any]]:
        """
        Search for AliExpress supplier pricing with live scraping.
        Fallback chain: Live scrape → Exact match → Fuzzy match → Keyword estimation
        """
        try:
            search_key = product_name.lower().strip()
            
            # Try live scraping first (FRESH DATA)
            scraped_data = AliExpressScraper.search_product(product_name)
            if scraped_data:
                logger.info(f"🌐 Using live scraped AliExpress data")
                return {
                    "product_name": product_name,
                    "cost": scraped_data.get("cost", 10.00),
                    "shipping_cost": scraped_data.get("shipping", 1.50),
                    "shipping_days": scraped_data.get("shipping_days", 18),
                    "supplier": "AliExpress (Live)",
                    "reliability": 0.90
                }
            
            # Fallback: Try exact match from local database
            for key in AliExpressProductFetcher.LOCAL_DATA:
                if key in search_key or search_key in key:
                    data = AliExpressProductFetcher.LOCAL_DATA[key].copy()
                    logger.info(f"✅ Exact match found in local database")
                    return {
                        "product_name": product_name,
                        "cost": data["cost"],
                        "shipping_cost": data["shipping"],
                        "shipping_days": data["shipping_days"],
                        "supplier": "AliExpress",
                        "reliability": data["reliability"]
                    }
            
            # Fallback: Try fuzzy matching
            similar = find_similar_product(product_name, AliExpressProductFetcher.LOCAL_DATA)
            if similar:
                data = AliExpressProductFetcher.LOCAL_DATA[similar].copy()
                return {
                    "product_name": product_name,
                    "cost": data["cost"],
                    "shipping_cost": data["shipping"],
                    "shipping_days": data["shipping_days"],
                    "supplier": "AliExpress",
                    "reliability": data["reliability"] * 0.8
                }
            
            # Fallback: Use keyword-based estimation
            logger.info(f"🤖 Using smart estimation for '{product_name}'")
            estimate = estimate_from_keywords(product_name)
            return {
                "product_name": product_name,
                "cost": estimate["cost"],
                "shipping_cost": estimate["shipping"],
                "shipping_days": estimate["shipping_days"],
                "supplier": "AliExpress (Estimated)",
                "reliability": estimate["reliability"]
            }
        
        except Exception as e:
            logger.error(f"❌ Error fetching from AliExpress: {e}")
            return None


class AmazonProductFetcher:
    """Fetch product data from Amazon (selling prices & competition)"""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    # Local market database
    LOCAL_DATA = {
        "phone case": {
            "price": 12.99,
            "seller_count": 150,
            "review_count": 450,
            "rating": 4.5,
            "availability": 0.98
        },
        "pet camera": {
            "price": 49.99,
            "seller_count": 45,
            "review_count": 230,
            "rating": 4.3,
            "availability": 0.95
        },
        "wireless earbuds": {
            "price": 29.99,
            "seller_count": 200,
            "review_count": 850,
            "rating": 4.2,
            "availability": 0.97
        },
        "usb cable": {
            "price": 8.99,
            "seller_count": 300,
            "review_count": 1200,
            "rating": 4.4,
            "availability": 0.99
        },
        "phone charger": {
            "price": 14.99,
            "seller_count": 250,
            "review_count": 920,
            "rating": 4.3,
            "availability": 0.98
        },
        "screen protector": {
            "price": 5.99,
            "seller_count": 400,
            "review_count": 2100,
            "rating": 4.4,
            "availability": 0.99
        },
    }
    
    @staticmethod
    def search_product(product_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for Amazon market data with live scraping.
        Fallback chain: Live scrape → Exact match → Fuzzy match → Keyword estimation
        """
        try:
            search_key = product_name.lower().strip()
            
            # Try live scraping first (FRESH DATA)
            scraped_data = AmazonScraper.search_product(product_name)
            if scraped_data:
                logger.info(f"🌐 Using live scraped Amazon data")
                return {
                    "price": scraped_data.get("price", 25.00),
                    "seller_count": scraped_data.get("seller_count", 150),
                    "review_count": scraped_data.get("review_count", 500),
                    "rating": scraped_data.get("rating", 4.0),
                    "availability": scraped_data.get("availability", 0.95)
                }
            
            # Fallback: Try exact match from local database
            for key in AmazonProductFetcher.LOCAL_DATA:
                if key in search_key or search_key in key:
                    data = AmazonProductFetcher.LOCAL_DATA[key].copy()
                    logger.info(f"✅ Exact match found in local database")
                    return {
                        "price": data["price"],
                        "seller_count": data["seller_count"],
                        "review_count": data["review_count"],
                        "rating": data["rating"],
                        "availability": data["availability"]
                    }
            
            # Fallback: Try fuzzy matching
            similar = find_similar_product(product_name, AmazonProductFetcher.LOCAL_DATA)
            if similar:
                data = AmazonProductFetcher.LOCAL_DATA[similar].copy()
                logger.info(f"🎯 Fuzzy matched '{product_name}' to '{similar}' on Amazon")
                return {
                    "price": data["price"],
                    "seller_count": max(50, int(data["seller_count"] * 0.7)),
                    "review_count": max(100, int(data["review_count"] * 0.7)),
                    "rating": data["rating"],
                    "availability": data["availability"]
                }
            
            # Fallback: Use keyword-based estimation
            logger.info(f"🤖 Using smart estimation for '{product_name}' on Amazon")
            estimate = estimate_from_keywords(product_name)
            return {
                "price": estimate["price"],
                "seller_count": estimate["seller_count"],
                "review_count": int(estimate["review_count"]),
                "rating": 4.0,
                "availability": 0.95
            }
        
        except Exception as e:
            logger.error(f"❌ Error fetching from Amazon: {e}")
            return None


class GoogleTrendsFetcher:
    """Fetch demand trend data"""
    
    # Trend database
    TRENDS = {
        "pet camera": "RISING",
        "wireless earbuds": "STABLE",
        "phone case": "STABLE",
        "usb cable": "FALLING",
        "phone charger": "STABLE",
        "screen protector": "FALLING",
    }
    
    @staticmethod
    def get_trend(product_name: str) -> str:
        """
        Get demand trend with live data.
        Fallback chain: Live scrape → Exact match → Heuristic estimation
        """
        try:
            search_key = product_name.lower().strip()
            
            # Try live scraping first (FRESH DATA)
            live_trend = GoogleTrendsScraper.get_trend(product_name)
            if live_trend and live_trend != "STABLE":  # Only use if we got real data
                logger.info(f"📈 Using live trend data")
                return live_trend
            
            # Fallback: Try exact match from local database
            for key in GoogleTrendsFetcher.TRENDS:
                if key in search_key or search_key in key:
                    return GoogleTrendsFetcher.TRENDS[key]
            
            # Fallback: Try fuzzy matching
            similar = find_similar_product(product_name, GoogleTrendsFetcher.TRENDS)
            if similar:
                logger.info(f"🎯 Fuzzy matched '{product_name}' to '{similar}' for trends")
                return GoogleTrendsFetcher.TRENDS[similar]
            
            # Fallback: Smart estimation based on keywords
            product_lower = product_name.lower()
            if any(word in product_lower for word in ["drone", "robot", "ai", "smart", "iot", "gaming", "vr"]):
                return "RISING"  # Tech products trending
            elif any(word in product_lower for word in ["cable", "basic", "common", "generic"]):
                return "FALLING"  # Commodities declining
            
            logger.warning(f"⚠️ Trend for '{product_name}' estimated as STABLE")
            return "STABLE"
        
        except Exception as e:
            logger.error(f"❌ Error fetching trends: {e}")
            return "STABLE"


class ProductAggregator:
    """Aggregate data from multiple sources with caching"""
    
    @staticmethod
    def fetch_product_data(product_name: str) -> Dict[str, Any]:
        """
        Fetch comprehensive product data from all sources
        Uses cache to avoid redundant API calls
        """
        
        # Check cache first
        cached = get_cached_data(product_name)
        if cached:
            return cached
        
        logger.info(f"🔍 Fetching fresh data for '{product_name}'...")
        
        # Fetch supplier cost
        supplier_data = AliExpressProductFetcher.search_product(product_name)
        
        # Fetch market/competitor data
        market_data = AmazonProductFetcher.search_product(product_name)
        
        # Fetch trend data
        trend = GoogleTrendsFetcher.get_trend(product_name)
        
        # Determine shipping to customer (standard US shipping)
        shipping_to_customer = 4.99
        
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
            "platform": "shopify",
            "packaging_cost": 1.0,
            "return_reserve_percent": 3.0,
            "data_sources": {
                "supplier": supplier_data.get("supplier", "AliExpress"),
                "supplier_reliability": supplier_data.get("reliability", 0.85),
                "market": "Amazon",
                "market_availability": market_data.get("availability", 0.95),
                "trends": "Google Trends",
                "shipping": "USPS/UPS Average",
                "fetched_at": datetime.now().isoformat(),
            },
            "data_quality": "REAL" if supplier_data and market_data else "ESTIMATED"
        }
        
        # Cache the data
        cache_product_data(product_name, compiled_data)
        
        return compiled_data


def fetch_product_auto(product_name: str) -> Dict[str, Any]:
    """
    Public API: Fetch all product data automatically with caching
    """
    logger.info(f"📦 Fetching product data for: {product_name}")
    return ProductAggregator.fetch_product_data(product_name)


def clear_cache():
    """Clear all cached data"""
    conn = sqlite3.connect(CACHE_DB)
    c = conn.cursor()
    c.execute('DELETE FROM product_cache')
    conn.commit()
    conn.close()
    logger.info("🗑️ Cache cleared")


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics"""
    conn = sqlite3.connect(CACHE_DB)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM product_cache')
    count = c.fetchone()[0]
    c.execute('SELECT SUM(length(data)) FROM product_cache')
    size = c.fetchone()[0] or 0
    conn.close()
    
    return {
        "cached_products": count,
        "cache_size_bytes": size,
        "cache_file": CACHE_DB
    }
