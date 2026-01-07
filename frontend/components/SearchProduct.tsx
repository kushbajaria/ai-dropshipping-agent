import { useState } from 'react'
import { analyzeProduct } from '@/lib/api'
import { AnalysisResult } from '@/lib/types'

interface SearchProductProps {
  onResults: (result: AnalysisResult) => void
}

export default function SearchProduct({ onResults }: SearchProductProps) {
  const [productName, setProductName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!productName.trim()) return

    setLoading(true)
    setError(null)

    try {
      const url = `${process.env.NEXT_PUBLIC_API_URL}/products/search?product_name=${encodeURIComponent(productName)}`
      console.log('🔍 Searching:', url)
      
      const response = await fetch(
        url,
        {
          method: 'POST',
          headers: {
            'X-API-Key': process.env.NEXT_PUBLIC_API_KEY || 'test-key-123',
            'Content-Type': 'application/json',
          },
        }
      )

      console.log('📊 Response status:', response.status)
      
      if (!response.ok) {
        throw new Error('Failed to search product')
      }

      const data = await response.json()
      console.log('✅ Data received:', data)
      
      // Pass the full data structure (analysis is nested inside)
      onResults(data.analysis || data)
      console.log('✅ Results sent to parent')
    } catch (err: any) {
      console.error('❌ Error:', err)
      setError(err.message || 'Failed to search product')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSearch} className="bg-white rounded-lg shadow-xl p-8">
      <h2 className="text-3xl font-bold mb-8 gradient-text">🔍 Quick Search</h2>
      
      <div className="mb-6">
        <label className="label-text">Product Name</label>
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="e.g., phone case, pet camera, wireless earbuds..."
          className="input-field"
          disabled={loading}
        />
        <p className="text-sm text-gray-500 mt-2">
          💡 Just enter the product name and we'll fetch all data automatically
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      <button
        type="submit"
        disabled={loading || !productName.trim()}
        className={`w-full btn-primary ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        {loading ? '🔍 Searching...' : '🚀 Search & Analyze'}
      </button>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-gray-700 font-semibold mb-2">
          What we fetch:
        </p>
        <ul className="text-sm text-gray-700 list-disc list-inside">
          <li>💰 Supplier cost (from AliExpress)</li>
          <li>💸 Market prices (from Amazon)</li>
          <li>👥 Competition level (seller counts)</li>
          <li>⭐ Reviews & ratings</li>
          <li>📈 Demand trends</li>
        </ul>
      </div>
    </form>
  )
}
