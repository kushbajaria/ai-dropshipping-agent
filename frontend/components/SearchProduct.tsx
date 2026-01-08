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
    <form onSubmit={handleSearch} className="space-y-4">
      <div>
        <label className="block text-sm font-semibold text-slate-900 mb-2">Product Name</label>
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="e.g., phone case, gaming mouse, bluetooth speaker..."
          className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white text-slate-900 placeholder-slate-400"
          disabled={loading}
        />
        <p className="text-xs text-slate-600 mt-2">
          💡 We'll fetch live prices from Amazon & AliExpress automatically
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700 text-sm"><span className="font-semibold">Error:</span> {error}</p>
        </div>
      )}

      <button
        type="submit"
        disabled={loading || !productName.trim()}
        className={`w-full py-3 px-4 rounded-lg font-semibold transition ${
          loading || !productName.trim()
            ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
            : 'bg-emerald-600 text-white hover:bg-emerald-700'
        }`}
      >
        {loading ? '⏳ Searching...' : '🔍 Search & Analyze'}
      </button>

      <div className="mt-4 p-4 bg-slate-50 rounded-lg border border-slate-200">
        <p className="text-sm font-semibold text-slate-800 mb-2">
          🌐 What we fetch:
        </p>
        <ul className="text-sm text-slate-700 list-disc list-inside space-y-1">
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
