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
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
      <Head>
        <title>Dropshipping Profit Analyzer | Real Data, Real Profits</title>
        <meta name="description" content="Discover TRUE profit margins after ALL costs. Join dropshippers making data-driven decisions." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      {/* Navigation Bar */}
      <nav className="border-b border-slate-200 bg-white sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-2xl">📊</span>
            <h2 className="text-xl font-bold text-slate-800">Profit Analyzer</h2>
          </div>
          <p className="text-sm text-slate-600 hidden sm:block">Real data. Real profit calculations. No BS.</p>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-slate-900 mb-4">
            Know Your True Profit Before You Start
          </h1>
          <p className="text-xl text-slate-600 mb-6 max-w-3xl mx-auto">
            Most tools show fake margins. We show <span className="font-semibold text-emerald-600">ALL costs</span> — platform fees, payment processing, shipping, ads, returns. 
            Make confident decisions with real numbers.
          </p>
          
          {/* Trust Badges */}
          <div className="flex justify-center gap-8 mb-12 flex-wrap">
            <div className="flex items-center gap-2 text-slate-700">
              <span className="text-lg">✓</span> <span className="text-sm">Live Market Data</span>
            </div>
            <div className="flex items-center gap-2 text-slate-700">
              <span className="text-lg">✓</span> <span className="text-sm">8 Cost Factors</span>
            </div>
            <div className="flex items-center gap-2 text-slate-700">
              <span className="text-lg">✓</span> <span className="text-sm">Industry Rates</span>
            </div>
            <div className="flex items-center gap-2 text-slate-700">
              <span className="text-lg">✓</span> <span className="text-sm">Honest Results</span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-slate-200">
          <button
            onClick={() => setActiveTab('search')}
            className={`px-6 py-3 font-semibold transition border-b-2 ${
              activeTab === 'search'
                ? 'text-emerald-600 border-emerald-600'
                : 'text-slate-600 border-transparent hover:text-slate-900'
            }`}
          >
            🔍 Quick Search
          </button>
          <button
            onClick={() => setActiveTab('manual')}
            className={`px-6 py-3 font-semibold transition border-b-2 ${
              activeTab === 'manual'
                ? 'text-emerald-600 border-emerald-600'
                : 'text-slate-600 border-transparent hover:text-slate-900'
            }`}
          >
            📝 Manual Entry
          </button>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Input Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm hover:shadow-md transition">
              <div className="mb-6">
                <h2 className="text-lg font-bold text-slate-900 mb-1">
                  {activeTab === 'search' ? '🔍 Search Product' : '📝 Enter Details'}
                </h2>
                <p className="text-sm text-slate-600">
                  {activeTab === 'search' 
                    ? 'Type any product name. We\'ll fetch live data.' 
                    : 'Enter your product details manually.'}
                </p>
              </div>

              {activeTab === 'search' ? (
                <SearchProduct 
                  onResults={setResult}
                  isLoading={loading}
                />
              ) : (
                <AnalysisForm 
                  onSubmit={handleAnalyze}
                  isLoading={loading}
                />
              )}

              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-700 text-sm"><span className="font-semibold">Error:</span> {error}</p>
                </div>
              )}
            </div>

            {/* Info Card */}
            <div className="mt-6 bg-blue-50 rounded-2xl p-6 border border-blue-200">
              <h3 className="font-semibold text-blue-900 mb-3">💡 What We Calculate</h3>
              <ul className="space-y-2 text-sm text-blue-800">
                <li>✓ Product cost from suppliers</li>
                <li>✓ Shipping (supplier → you → customer)</li>
                <li>✓ Platform fees (Shopify, Amazon, etc)</li>
                <li>✓ Payment processing fees</li>
                <li>✓ Advertising costs (20% default)</li>
                <li>✓ Return/refund reserves</li>
                <li>✓ Packaging materials</li>
                <li>✓ <strong>TRUE net profit</strong></li>
              </ul>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2">
            {result ? (
              <ResultsDisplay result={result} />
            ) : (
              <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-2xl p-12 border-2 border-dashed border-slate-300 text-center">
                <div className="text-6xl mb-4">📈</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Enter a product to get started</h3>
                <p className="text-slate-600 max-w-md mx-auto">
                  Search for any product name or enter details manually. We'll instantly show you the true profit potential.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-20 pt-12 border-t border-slate-200">
          <h2 className="text-3xl font-bold text-slate-900 mb-12 text-center">Why Choose Us?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl p-8 border border-slate-200">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">Real Data</h3>
              <p className="text-slate-600 text-sm">
                Live scraping from Amazon & AliExpress. Fresh prices, real competition data, actual trends.
              </p>
            </div>
            <div className="bg-white rounded-xl p-8 border border-slate-200">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">ALL Costs Included</h3>
              <p className="text-slate-600 text-sm">
                Unlike fake tools showing 40% margins, we show TRUE profit after every expense. Industry-standard rates.
              </p>
            </div>
            <div className="bg-white rounded-xl p-8 border border-slate-200">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">Instant Insights</h3>
              <p className="text-slate-600 text-sm">
                Analyze 100s of products in minutes. Get success scores, profitability ratings, and honest recommendations.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 bg-gradient-to-r from-emerald-50 to-blue-50 rounded-2xl p-12 border border-emerald-200 text-center">
          <h2 className="text-2xl font-bold text-slate-900 mb-2">Ready to Make Better Decisions?</h2>
          <p className="text-slate-700 mb-6">Join dropshippers using real profit analysis to build sustainable businesses.</p>
          <button 
            onClick={() => setActiveTab('search')}
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3 px-8 rounded-lg transition shadow-md"
          >
            Search Your First Product →
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-200 mt-20 py-8 bg-white">
        <div className="max-w-6xl mx-auto px-4 text-center text-slate-600 text-sm">
          <p>We show TRUE profit. No fluff. No fake margins. Just honest analysis.</p>
          <p className="mt-2 text-slate-500">Built for dropshippers who want to win the right way.</p>
        </div>
      </footer>
    </div>
  )
}

