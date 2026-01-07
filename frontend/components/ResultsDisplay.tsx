import React from 'react'
import { AnalysisResult } from '../lib/types'
import { RecommendationBadge } from './RecommendationBadge'
import { FactorsList } from './FactorsList'
import { ProfitBreakdownChart } from './ProfitBreakdownChart'

interface ResultsDisplayProps {
  result: AnalysisResult
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result }) => {
  // Handle both wrapped and unwrapped analysis objects
  const analysis = result.analysis || result
  const { profit_analysis, success_analysis, market_intelligence, summary } = analysis

  return (
    <div className="space-y-8">
      {/* Recommendation */}
      <div>
        <RecommendationBadge
          recommendation={success_analysis.recommendation}
          probability={success_analysis.success_probability}
        />
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <p className="text-gray-600 text-sm mb-2">Net Profit Per Sale</p>
          <p className="text-3xl font-bold text-green-600">{summary.net_profit_per_sale}</p>
        </div>
        <div className="card text-center">
          <p className="text-gray-600 text-sm mb-2">Net Margin</p>
          <p className="text-3xl font-bold text-blue-600">{summary.margin}</p>
        </div>
        <div className="card text-center">
          <p className="text-gray-600 text-sm mb-2">Competition</p>
          <p className="text-2xl font-bold text-purple-600">{market_intelligence.competition_level}</p>
          <p className="text-xs text-gray-500">{market_intelligence.seller_count} sellers</p>
        </div>
        <div className="card text-center">
          <p className="text-gray-600 text-sm mb-2">Demand Trend</p>
          <p className="text-2xl font-bold text-orange-600">{market_intelligence.demand_trend}</p>
        </div>
      </div>

      {/* Profit Breakdown */}
      <div className="card">
        <h3 className="text-2xl font-bold mb-6">💰 Profit Breakdown</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <ProfitBreakdownChart
              selling_price={profit_analysis.selling_price}
              product_cost={profit_analysis.product_cost}
              platform_fee={profit_analysis.platform_fee}
              payment_processing_fee={profit_analysis.payment_processing_fee}
              ad_cost={profit_analysis.ad_cost}
              shipping_from_supplier={profit_analysis.shipping_from_supplier}
              shipping_to_customer={profit_analysis.shipping_to_customer}
              return_reserve={profit_analysis.return_reserve}
              net_profit={profit_analysis.net_profit}
            />
          </div>
          <div className="space-y-4">
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-700">Selling Price</span>
              <span className="font-semibold">${profit_analysis.selling_price.toFixed(2)}</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-700">- Product Cost</span>
              <span className="font-semibold">-${profit_analysis.product_cost.toFixed(2)}</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-700">- Platform Fee</span>
              <span className="font-semibold">-${profit_analysis.platform_fee.toFixed(2)}</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-700">- Payment Fee</span>
              <span className="font-semibold">-${profit_analysis.payment_processing_fee.toFixed(2)}</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-700">- Ads (20%)</span>
              <span className="font-semibold">-${profit_analysis.ad_cost.toFixed(2)}</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-700">- Shipping (Total)</span>
              <span className="font-semibold">
                -${(profit_analysis.shipping_from_supplier + profit_analysis.shipping_to_customer).toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-700">- Returns (3%)</span>
              <span className="font-semibold">-${profit_analysis.return_reserve.toFixed(2)}</span>
            </div>
            <div className="flex justify-between pt-4 bg-green-50 px-4 py-3 rounded-lg">
              <span className="text-lg font-bold">NET PROFIT</span>
              <span className="text-lg font-bold text-green-600">${profit_analysis.net_profit.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Key Factors & Warnings */}
      <div>
        <h3 className="text-2xl font-bold mb-6">📋 Analysis Details</h3>
        <FactorsList factors={success_analysis.key_factors} warnings={success_analysis.warnings} />
      </div>

      {/* Action */}
      <div className="card bg-gradient-to-r from-purple-600 to-blue-600 text-white text-center">
        <h3 className="text-2xl font-bold mb-2">🎯 Recommendation</h3>
        <p className="text-xl mb-4">{success_analysis.action}</p>
        <p className="text-sm opacity-90">
          Based on {success_analysis.success_probability}% success probability
        </p>
      </div>
    </div>
  )
}
