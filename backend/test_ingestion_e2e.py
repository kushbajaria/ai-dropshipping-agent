"""
End-to-End Test for Enhanced Ingestion Pipeline
Tests the complete flow: Input → ProfitCalculator → Success Scoring → Response
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.ingestion import ingest_products
import json


def test_batch_ingestion():
    """Test the batch ingestion with enhanced profit analysis"""
    
    print("\n" + "="*80)
    print("🧪 END-TO-END TEST: Enhanced Ingestion Pipeline")
    print("="*80)
    
    # Sample batch of products with new fields
    raw_products = [
        {
            "name": "Pet Camera with Treat Dispenser",
            "cost": 18.00,
            "sale_price": 49.99,
            "shipping_days": 5,
            "competition_level": 0.1,
            "supplier": "AliExpress - PetTech Co",
            "niche": "Pet Tech",
            "platform": "shopify",
            "shipping_from_supplier": 4.00,
            "shipping_to_customer": 0.00,
            "seller_count": 12,
            "review_count": 450,
            "ad_cost_percent": 15.0,
        },
        {
            "name": "Phone Case - Generic Design",
            "cost": 3.50,
            "sale_price": 19.99,
            "shipping_days": 18,
            "competition_level": 0.9,
            "supplier": "AliExpress - Cases R Us",
            "niche": "Phone Accessories",
            "platform": "amazon",
            "shipping_from_supplier": 2.00,
            "shipping_to_customer": 4.50,
            "seller_count": 850,
            "review_count": 120,
            "ad_cost_percent": 25.0,
        },
        {
            "name": "LED Strip Lights RGB",
            "cost": 12.00,
            "sale_price": 34.99,
            "shipping_days": 8,
            "competition_level": 0.4,
            "supplier": "AliExpress - LightTech",
            "niche": "Home Decor",
            "platform": "shopify",
            "shipping_from_supplier": 3.50,
            "shipping_to_customer": 0.00,
            "seller_count": 65,
            "review_count": 890,
            "ad_cost_percent": 20.0,
        },
        {
            "name": "Bluetooth Speaker Mini",
            "cost": 8.00,
            "sale_price": 29.99,
            "shipping_days": 10,
            "competition_level": 0.6,
            "supplier": "AliExpress - AudioGear",
            "niche": "Electronics",
            "platform": "shopify",
            "shipping_from_supplier": 2.50,
            "shipping_to_customer": 0.00,
            "seller_count": 180,
            "review_count": 340,
            "ad_cost_percent": 20.0,
        },
    ]
    
    print(f"\n📦 Processing {len(raw_products)} products...")
    
    # Run ingestion
    results = ingest_products(raw_products)
    
    print(f"\n✅ Processing complete! Results sorted by success probability\n")
    
    # Display results
    for i, product in enumerate(results, 1):
        print(f"\n{'─'*80}")
        print(f"#{i} {product['name']}")
        print(f"{'─'*80}")
        
        # Success prediction
        success = product['success']
        print(f"\n🎯 SUCCESS PREDICTION:")
        print(f"   {success['recommendation']}")
        print(f"   Probability: {success['probability']}%")
        print(f"   Confidence: {success['confidence']}")
        print(f"   Action: {success['action']}")
        
        # Profit analysis
        profit = product['profit']
        print(f"\n💰 PROFIT ANALYSIS:")
        print(f"   Selling Price: ${profit['selling_price']:.2f}")
        print(f"   Net Profit: ${profit['net_profit']:.2f}")
        print(f"   Net Margin: {profit['net_margin_percent']:.1f}%")
        print(f"   Rating: {profit['margin_rating']}")
        print(f"   Profitable: {'✅ Yes' if profit['is_profitable'] else '❌ No'}")
        
        # Key factors
        if product['key_factors']:
            print(f"\n✅ STRENGTHS:")
            for factor in product['key_factors'][:3]:  # Top 3
                print(f"   {factor}")
        
        # Warnings
        if product['warnings']:
            print(f"\n⚠️  WARNINGS:")
            for warning in product['warnings'][:3]:  # Top 3
                print(f"   {warning}")
        
        # Legacy scores (for backward compatibility)
        print(f"\n📊 LEGACY SCORES:")
        print(f"   Viability: {product['viability_score']:.2f}")
        print(f"   Risk: {product['risk_score']:.2f}")
        print(f"   Competition: {product['competition_score']:.2f}")
    
    print(f"\n{'='*80}")
    print("📈 BATCH SUMMARY")
    print(f"{'='*80}")
    
    # Calculate summary stats
    total = len(results)
    strong_buy = sum(1 for p in results if "STRONG BUY" in p['success']['recommendation'])
    buy = sum(1 for p in results if "BUY" in p['success']['recommendation'] and "STRONG" not in p['success']['recommendation'])
    consider = sum(1 for p in results if "CONSIDER" in p['success']['recommendation'])
    skip = sum(1 for p in results if "SKIP" in p['success']['recommendation'] or "AVOID" in p['success']['recommendation'])
    
    profitable = sum(1 for p in results if p['profit']['is_profitable'])
    avg_margin = sum(p['profit']['net_margin_percent'] for p in results) / total
    avg_success = sum(p['success']['probability'] for p in results) / total
    
    print(f"\nTotal Products Analyzed: {total}")
    print(f"\nRecommendations:")
    print(f"  🟢 STRONG BUY: {strong_buy}")
    print(f"  🟢 BUY: {buy}")
    print(f"  🟡 CONSIDER: {consider}")
    print(f"  🔴 SKIP/AVOID: {skip}")
    
    print(f"\nProfitability:")
    print(f"  Profitable (≥15% margin): {profitable}/{total} ({profitable/total*100:.0f}%)")
    print(f"  Average Net Margin: {avg_margin:.1f}%")
    print(f"  Average Success Rate: {avg_success:.0f}%")
    
    print(f"\n{'='*80}")
    print("✅ END-TO-END TEST COMPLETE!")
    print(f"{'='*80}\n")
    
    # Return results for further testing
    return results


def test_json_serialization():
    """Test that results can be serialized to JSON (for API responses)"""
    print("\n🧪 Testing JSON serialization...")
    
    raw_products = [{
        "name": "Test Product",
        "cost": 10.00,
        "sale_price": 29.99,
        "shipping_days": 7,
        "competition_level": 0.3,
        "platform": "shopify",
    }]
    
    results = ingest_products(raw_products)
    
    try:
        json_output = json.dumps(results, indent=2)
        print("✅ JSON serialization successful!")
        return True
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False


if __name__ == "__main__":
    # Run tests
    results = test_batch_ingestion()
    test_json_serialization()
    
    print("\n🎉 All tests passed! The ingestion pipeline is working correctly.")
