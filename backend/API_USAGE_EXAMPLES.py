"""
Quick reference for using the new database-integrated API
"""

import requests
import json

# Base URL (update if your server runs on different port)
BASE_URL = "http://localhost:8000"
API_KEY = "test-key"

# Headers
headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

print("=" * 80)
print("🎯 DATABASE INTEGRATION - API USAGE EXAMPLES")
print("=" * 80)

# Example 1: Search for a product and SAVE to database
print("\n📦 Example 1: Search and Save Product")
print("-" * 80)
print("POST /products/search?save_to_db=true")
print("Product: pet camera")
print("\nThis will:")
print("  1. Fetch data from AliExpress, Amazon, Google Trends")
print("  2. Calculate true profit and success probability")
print("  3. Save complete analysis to database")
print("  4. Return saved_product_id for later retrieval")

example_url = f"{BASE_URL}/products/search?product_name=pet+camera&save_to_db=true"
print(f"\nFull URL:\n{example_url}")

# Example 2: Manual analyze and save
print("\n\n📊 Example 2: Manual Analysis with Save")
print("-" * 80)
print("POST /products/analyze")

example_payload = {
    "product_name": "Wireless Charger",
    "selling_price": 24.99,
    "product_cost": 8.50,
    "shipping_from_supplier": 2.00,
    "shipping_to_customer": 0.00,
    "shipping_days": 12,
    "seller_count": 85,
    "review_count": 420,
    "platform": "shopify",
    "ad_cost_percent": 20.0,
    "save_to_db": True  # <-- KEY: Set to true to save
}

print(f"\nPayload:")
print(json.dumps(example_payload, indent=2))

# Example 3: Get all saved products
print("\n\n📚 Example 3: Retrieve Saved Products")
print("-" * 80)
print("GET /products/saved")
print("\nOptional query parameters:")
print("  - limit: Number of results (default: 50, max: 200)")
print("  - skip: Pagination offset")
print("  - recommendation: Filter by recommendation (e.g., 'STRONG BUY')")
print("  - min_profit: Minimum net profit filter")

example_urls = [
    f"{BASE_URL}/products/saved",
    f"{BASE_URL}/products/saved?limit=10",
    f"{BASE_URL}/products/saved?recommendation=🟢%20STRONG%20BUY",
    f"{BASE_URL}/products/saved?min_profit=10.00",
]

for url in example_urls:
    print(f"\n  {url}")

# Example 4: Get single product
print("\n\n📦 Example 4: Get Single Product by ID")
print("-" * 80)
print("GET /products/saved/{product_id}")
example_url = f"{BASE_URL}/products/saved/1"
print(f"\nFull URL:\n{example_url}")

# Example 5: Delete saved product
print("\n\n🗑️ Example 5: Delete Saved Product")
print("-" * 80)
print("DELETE /products/saved/{product_id}")
example_url = f"{BASE_URL}/products/saved/1"
print(f"\nFull URL:\n{example_url}")

# Example 6: Get statistics
print("\n\n📊 Example 6: Get Analysis Statistics")
print("-" * 80)
print("GET /products/stats")
print("\nReturns:")
print("  - Total products analyzed")
print("  - Breakdown by recommendation (STRONG BUY, BUY, CONSIDER, SKIP)")
print("  - Average net profit across all products")
print("  - Average success score")

example_url = f"{BASE_URL}/products/stats"
print(f"\nFull URL:\n{example_url}")

print("\n" + "=" * 80)
print("💡 TIP: Run your FastAPI server first with:")
print("   cd backend && uvicorn app.main:app --reload")
print("=" * 80)
print("\n✅ Database integration is ready to use!")
print("\nYou can now:")
print("  ✓ Save product analyses to database")
print("  ✓ Retrieve and filter saved products")
print("  ✓ Track analysis history")
print("  ✓ Get statistics and insights")
print("  ✓ Delete products you don't need")
print("\n")
