import React from 'react'
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts'

interface ProfitBreakdownChartProps {
  selling_price: number
  product_cost: number
  platform_fee: number
  payment_processing_fee: number
  ad_cost: number
  shipping_from_supplier: number
  shipping_to_customer: number
  return_reserve: number
  net_profit: number
}

export const ProfitBreakdownChart: React.FC<ProfitBreakdownChartProps> = ({
  selling_price,
  product_cost,
  platform_fee,
  payment_processing_fee,
  ad_cost,
  shipping_from_supplier,
  shipping_to_customer,
  return_reserve,
  net_profit,
}) => {
  const data = [
    { name: 'Net Profit', value: net_profit, color: '#10b981' },
    { name: 'Product Cost', value: product_cost, color: '#ef4444' },
    { name: 'Ads', value: ad_cost, color: '#f59e0b' },
    { name: 'Platform Fee', value: platform_fee, color: '#8b5cf6' },
    { name: 'Payment Fee', value: payment_processing_fee, color: '#06b6d4' },
    {
      name: 'Shipping Total',
      value: shipping_from_supplier + shipping_to_customer,
      color: '#ec4899',
    },
    { name: 'Returns', value: return_reserve, color: '#6b7280' },
  ].filter((item) => item.value > 0)

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value }) => `${name}: $${value.toFixed(2)}`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `$${Number(value).toFixed(2)}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
