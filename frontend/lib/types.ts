export interface ProductData {
  selling_price: number
  product_cost: number
  shipping_from_supplier?: number
  shipping_to_customer?: number
  shipping_days?: number
  seller_count?: number
  review_count?: number
  platform?: string
  ad_cost_percent?: number
}

export interface AnalysisResult {
  success: boolean
  analysis: {
    summary: {
      recommendation: string
      success_probability: string
      net_profit_per_sale: string
      margin: string
      action: string
    }
    profit_analysis: {
      selling_price: number
      product_cost: number
      net_profit: number
      net_margin_percent: number
      margin_rating: string
      is_profitable: boolean
      [key: string]: any
    }
    market_intelligence: {
      competition_level: string
      seller_count: number
      demand_trend: string
      review_count: number
      shipping_days: number
    }
    success_analysis: {
      success_probability: number
      recommendation: string
      confidence: string
      action: string
      key_factors: string[]
      warnings: string[]
    }
  }
}

export const PLATFORMS = [
  { value: 'shopify', label: 'Shopify' },
  { value: 'amazon', label: 'Amazon' },
  { value: 'etsy', label: 'Etsy' },
  { value: 'tiktok', label: 'TikTok Shop' },
  { value: 'ebay', label: 'eBay' },
]

export const getRecommendationColor = (recommendation: string): string => {
  if (recommendation.includes('STRONG BUY')) return '#10b981'
  if (recommendation.includes('BUY')) return '#10b981'
  if (recommendation.includes('CONSIDER')) return '#f59e0b'
  if (recommendation.includes('RISKY')) return '#f59e0b'
  return '#ef4444'
}

export const getRecommendationBgColor = (recommendation: string): string => {
  if (recommendation.includes('STRONG BUY')) return 'bg-green-50'
  if (recommendation.includes('BUY')) return 'bg-green-50'
  if (recommendation.includes('CONSIDER')) return 'bg-yellow-50'
  if (recommendation.includes('RISKY')) return 'bg-yellow-50'
  return 'bg-red-50'
}
