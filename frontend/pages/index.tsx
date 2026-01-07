import React, { useState } from 'react'
import Head from 'next/head'
import { AnalysisForm } from '../components/AnalysisForm'
import { ResultsDisplay } from '../components/ResultsDisplay'
import SearchProduct from '../components/SearchProduct'
import { analyzeProduct } from '../lib/api'
import { ProductData, AnalysisResult } from '../lib/types'

export default function Home() {
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'search' | 'manual'>('search')

  const handleAnalyze = async (data: ProductData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await analyzeProduct(data)
      setResult(response)
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Failed to analyze product. Make sure the backend is running!'
      )
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-500 to-purple-700 py-12 px-4">
      <Head>
        <title>Dropshipping Product Analyzer</title>
        <meta name="description" content="Find winning products with TRUE profit calculations" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">🎯 Product Analyzer</h1>
          <p className="text-xl text-purple-100 mb-2">
            Discover TRUE profit margins after ALL costs
          </p>
          <p className="text-purple-200">
            Analyze products in seconds, not hours. Find winners before you spend money.
          </p>
        </div>

        {/* Mobile Tabs */}
        <div className="flex gap-4 mb-8 lg:hidden">
          <button
            onClick={() => setActiveTab('search')}
            className={`flex-1 py-3 px-4 rounded-lg font-semibold transition ${
              activeTab === 'search'
                ? 'bg-white text-purple-600'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            🔍 Quick Search
          </button>
          <button
            onClick={() => setActiveTab('manual')}
            className={`flex-1 py-3 px-4 rounded-lg font-semibold transition ${
              activeTab === 'manual'
                ? 'bg-white text-purple-600'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            ✏️ Manual Entry
          </button>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Form Column */}
          <div className="lg:col-span-1">
            {/* Desktop: show search by default */}
            <div className="hidden lg:block">
              <SearchProduct onResults={setResult} />
            </div>

            {/* Mobile: show active tab */}
            {activeTab === 'search' && (
              <div className="lg:hidden">
                <SearchProduct onResults={setResult} />
              </div>
            )}

            {activeTab === 'manual' && (
              <AnalysisForm onSubmit={handleAnalyze} loading={loading} />
            )}
          </div>

          {/* Results Column */}
          <div className="lg:col-span-2">
            {error && (
              <div className="bg-red-100 border-2 border-red-300 rounded-lg p-6 mb-6">
                <h3 className="text-red-800 font-bold mb-2">❌ Error</h3>
                <p className="text-red-700">{error}</p>
                <p className="text-red-600 text-sm mt-2">
                  💡 Tip: Make sure the backend server is running at{' '}
                  <code className="bg-red-50 px-2 py-1 rounded">
                    {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
                  </code>
                </p>
              </div>
            )}

            {result && !loading && (
              <div className="space-y-6">
                <ResultsDisplay result={result} />
              </div>
            )}

            {!result && !error && !loading && (
              <div className="bg-white rounded-lg shadow-xl p-12 text-center">
                <p className="text-6xl mb-4">📊</p>
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Enter product details to get started</h3>
                <p className="text-gray-600">
                  Use the quick search to auto-fetch product data, or enter details manually
                </p>
              </div>
            )}

            {loading && (
              <div className="bg-white rounded-lg shadow-xl p-12 text-center">
                <div className="inline-block">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mb-4"></div>
                </div>
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Analyzing...</h3>
                <p className="text-gray-600">
                  Calculating TRUE profit, success probability, and market intelligence...
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-purple-100">
          <p className="text-sm">
            🚀 Accurate. Fast. Profitable. | Stop guessing. Start analyzing.
          </p>
        </div>
      </div>
    </div>
  )
}
