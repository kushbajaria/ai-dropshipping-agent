"""
Quick API test for the /products/analyze endpoint
"""

import requests
import json

# Test the instant product analysis endpoint
BASE_URL = "http://localhost:8000"
API_KEY = "test-key-123"  # Replace with actual API key from your database

def test_analyze_endpoint():
    """Test the /products/analyze endpoint"""
    
    url = f"{BASE_URL}/products/analyze"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Test data - good product
    payload = {
        "selling_price": 39.99,
        "product_cost": 14.00,
        "shipping_from_supplier": 3.50,
        "shipping_to_customer": 0.00,
        "shipping_days": 7,
        "seller_count": 45,
        "review_count": 230,
        "platform": "shopify",
        "ad_cost_percent": 20.0
    }
    
    print("🧪 Testing /products/analyze endpoint...")
    print(f"Request: {json.dumps(payload, indent=2)}\n")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!\n")
            print(json.dumps(result, indent=2))
            
            # Extract key info
            if result.get("success"):
                analysis = result["analysis"]
                summary = analysis["summary"]
                
                print(f"\n{'='*60}")
                print(f"📊 RECOMMENDATION: {summary['recommendation']}")
                print(f"💯 Success Probability: {summary['success_probability']}")
                print(f"💰 Net Profit: {summary['net_profit_per_sale']}")
                print(f"📈 Margin: {summary['margin']}")
                print(f"🎯 Action: {summary['action']}")
                print(f"{'='*60}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API")
        print("💡 Make sure FastAPI server is running:")
        print("   cd backend && uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    test_analyze_endpoint()
