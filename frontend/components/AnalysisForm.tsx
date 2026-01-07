import React, { useState } from 'react'
import { PLATFORMS, ProductData } from '../lib/types'

interface AnalysisFormProps {
  onSubmit: (data: ProductData) => void
  loading?: boolean
}

export const AnalysisForm: React.FC<AnalysisFormProps> = ({ onSubmit, loading = false }) => {
  const [formData, setFormData] = useState<ProductData>({
    selling_price: 39.99,
    product_cost: 14.0,
    shipping_from_supplier: 3.5,
    shipping_to_customer: 0,
    shipping_days: 7,
    seller_count: 45,
    review_count: 230,
    platform: 'shopify',
    ad_cost_percent: 20.0,
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: isNaN(Number(value)) ? value : Number(value),
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-xl p-8">
      <h2 className="text-3xl font-bold mb-8 gradient-text">Analyze Product</h2>

      {/* Pricing Section */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">💰 Pricing</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="label-text">Selling Price ($)</label>
            <input
              type="number"
              name="selling_price"
              step="0.01"
              value={formData.selling_price}
              onChange={handleChange}
              className="input-field"
              placeholder="39.99"
              required
            />
          </div>
          <div>
            <label className="label-text">Product Cost ($)</label>
            <input
              type="number"
              name="product_cost"
              step="0.01"
              value={formData.product_cost}
              onChange={handleChange}
              className="input-field"
              placeholder="14.00"
              required
            />
          </div>
          <div>
            <label className="label-text">Ad Cost (%)</label>
            <input
              type="number"
              name="ad_cost_percent"
              step="0.1"
              value={formData.ad_cost_percent}
              onChange={handleChange}
              className="input-field"
              placeholder="20"
            />
          </div>
        </div>
      </div>

      {/* Shipping Section */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">🚚 Shipping</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="label-text">From Supplier ($)</label>
            <input
              type="number"
              name="shipping_from_supplier"
              step="0.01"
              value={formData.shipping_from_supplier}
              onChange={handleChange}
              className="input-field"
              placeholder="3.50"
            />
          </div>
          <div>
            <label className="label-text">To Customer ($)</label>
            <input
              type="number"
              name="shipping_to_customer"
              step="0.01"
              value={formData.shipping_to_customer}
              onChange={handleChange}
              className="input-field"
              placeholder="5.00"
            />
          </div>
          <div>
            <label className="label-text">Shipping Days</label>
            <input
              type="number"
              name="shipping_days"
              value={formData.shipping_days}
              onChange={handleChange}
              className="input-field"
              placeholder="7"
            />
          </div>
        </div>
      </div>

      {/* Market Section */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">📊 Market</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="label-text">Platform</label>
            <select
              name="platform"
              value={formData.platform}
              onChange={handleChange}
              className="input-field"
            >
              {PLATFORMS.map((p) => (
                <option key={p.value} value={p.value}>
                  {p.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="label-text">Seller Count</label>
            <input
              type="number"
              name="seller_count"
              value={formData.seller_count}
              onChange={handleChange}
              className="input-field"
              placeholder="45"
            />
          </div>
          <div>
            <label className="label-text">Review Count</label>
            <input
              type="number"
              name="review_count"
              value={formData.review_count}
              onChange={handleChange}
              className="input-field"
              placeholder="230"
            />
          </div>
        </div>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full btn-primary ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        {loading ? '⏳ Analyzing...' : '🚀 Analyze Product'}
      </button>
    </form>
  )
}
