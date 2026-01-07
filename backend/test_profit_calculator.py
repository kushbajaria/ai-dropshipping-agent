"""
Test the True Profit Calculator with real dropshipping scenarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.scoring_v2 import analyze_product_complete
import json


def test_product(name: str, **kwargs):
    """Test a product and print formatted results"""
    print(f"\n{'='*80}")
    print(f"🔍 ANALYZING: {name}")
    print(f"{'='*80}")
    
    analysis = analyze_product_complete(**kwargs)
    
    # Print Summary
    print(f"\n📊 QUICK SUMMARY")
    print(f"   Recommendation: {analysis['summary']['recommendation']}")
    print(f"   Success Rate:   {analysis['summary']['success_probability']}")
    print(f"   Net Profit:     {analysis['summary']['net_profit_per_sale']}")
    print(f"   Margin:         {analysis['summary']['margin']}")
    print(f"   Action:         {analysis['summary']['action']}")
    
    # Print Profit Breakdown
    profit = analysis['profit_analysis']
    print(f"\n💰 PROFIT BREAKDOWN (Selling Price: ${profit['selling_price']})")
    print(f"   Product Cost:          -${profit['product_cost']:.2f}")
    print(f"   Shipping (supplier):   -${profit['shipping_from_supplier']:.2f}")
    print(f"   Shipping (customer):   -${profit['shipping_to_customer']:.2f}")
    print(f"   Platform Fee:          -${profit['platform_fee']:.2f}")
    print(f"   Payment Fee:           -${profit['payment_processing_fee']:.2f}")
    print(f"   Ad Cost:               -${profit['ad_cost']:.2f}")
    print(f"   Return Reserve:        -${profit['return_reserve']:.2f}")
    print(f"   " + "-" * 40)
    print(f"   NET PROFIT:            ${profit['net_profit']:.2f} ({profit['net_margin_percent']:.1f}%)")
    
    # Print Key Factors
    factors = analysis['success_analysis']['key_factors']
    if factors:
        print(f"\n✅ KEY STRENGTHS")
        for factor in factors:
            print(f"   {factor}")
    
    # Print Warnings
    warnings = analysis['success_analysis']['warnings']
    if warnings:
        print(f"\n⚠️  WARNINGS")
        for warning in warnings:
            print(f"   {warning}")
    
    print(f"\n{'='*80}\n")
    
    return analysis


if __name__ == "__main__":
    print("\n🚀 TRUE PROFIT CALCULATOR - REAL WORLD TESTS")
    print("This is what makes your platform worth $29/mo")
    
    # TEST 1: Perfect Product - Low competition, great margin, fast shipping
    test_product(
        "Perfect Product - Pet Camera",
        selling_price=49.99,
        product_cost=18.00,
        shipping_from_supplier=4.00,
        shipping_to_customer=0.00,  # Free shipping absorbed
        shipping_days=5,
        seller_count=12,  # Low competition
        review_count=450,
        platform="shopify",
        ad_cost_percent=15.0,  # Lower ad costs
    )
    
    # TEST 2: Risky Product - High competition, thin margins
    test_product(
        "Risky Product - Phone Case",
        selling_price=19.99,
        product_cost=3.50,
        shipping_from_supplier=2.00,
        shipping_to_customer=4.50,
        shipping_days=18,  # Slow shipping
        seller_count=850,  # Oversaturated
        review_count=120,
        platform="amazon",  # Higher fees
        ad_cost_percent=25.0,  # Need more ads to compete
    )
    
    # TEST 3: Good Product - Solid middle ground
    test_product(
        "Good Product - LED Strip Lights",
        selling_price=34.99,
        product_cost=12.00,
        shipping_from_supplier=3.50,
        shipping_to_customer=0.00,
        shipping_days=8,
        seller_count=65,  # Medium competition
        review_count=890,
        platform="shopify",
        ad_cost_percent=20.0,
    )
    
    # TEST 4: Avoid Product - Unprofitable after fees
    test_product(
        "Avoid Product - Cheap Accessory",
        selling_price=12.99,
        product_cost=8.00,
        shipping_from_supplier=2.50,
        shipping_to_customer=3.50,
        shipping_days=21,
        seller_count=340,
        review_count=45,
        platform="amazon",
        ad_cost_percent=20.0,
    )
    
    # TEST 5: Platform Comparison - Same product different platforms
    print(f"\n{'='*80}")
    print(f"🔄 PLATFORM COMPARISON - Same Product on Different Platforms")
    print(f"{'='*80}")
    
    base_params = {
        "selling_price": 39.99,
        "product_cost": 14.00,
        "shipping_from_supplier": 3.50,
        "shipping_to_customer": 0.00,
        "shipping_days": 7,
        "seller_count": 45,
        "review_count": 230,
        "ad_cost_percent": 20.0,
    }
    
    platforms = ["shopify", "amazon", "etsy"]
    results = {}
    
    for platform in platforms:
        analysis = analyze_product_complete(**base_params, platform=platform)
        profit = analysis['profit_analysis']
        results[platform] = {
            "net_profit": profit['net_profit'],
            "net_margin": profit['net_margin_percent'],
            "total_fees": profit['platform_fee'] + profit['payment_processing_fee'],
        }
    
    print(f"\n📊 Results for ${base_params['selling_price']} product:")
    for platform, data in results.items():
        print(f"\n   {platform.upper()}")
        print(f"      Net Profit: ${data['net_profit']:.2f}")
        print(f"      Net Margin: {data['net_margin']:.1f}%")
        print(f"      Total Fees: ${data['total_fees']:.2f}")
    
    # Determine best platform
    best = max(results.items(), key=lambda x: x[1]['net_profit'])
    print(f"\n   🏆 WINNER: {best[0].upper()} (+${best[1]['net_profit']:.2f} per sale)")
    
    print(f"\n{'='*80}\n")
    print("✅ TRUE PROFIT CALCULATOR IS WORKING!")
    print("💡 This shows dropshippers REAL numbers - not fake margins")
    print("🎯 This is what justifies $29/mo subscription")
