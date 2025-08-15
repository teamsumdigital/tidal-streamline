import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { MarketScanForm } from '../components/forms/MarketScanForm'
import { apiService, APIError } from '../services/api'
import { MarketScanRequest } from '../services/types'

export const ClientPortal: React.FC = () => {
  const navigate = useNavigate()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleFormSubmit = async (formData: MarketScanRequest) => {
    setIsSubmitting(true)
    setError(null)

    try {
      const response = await apiService.createMarketScan({
        client_name: formData.client_name,
        client_email: formData.client_email,
        company_domain: formData.company_domain,
        job_title: formData.job_title,
        job_description: formData.job_description,
        hiring_challenges: formData.hiring_challenges
      })

      // Navigate to results page
      navigate(`/scan/${response.id}`)
    } catch (err) {
      if (err instanceof APIError) {
        setError(err.message)
      } else {
        setError('An unexpected error occurred. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#F7F7F9]">
      {/* Hero Section - Purple Gradient Background */}
      <div className="relative overflow-hidden bg-gradient-to-br from-[#7B61FF] to-[#9F7FFF]">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-6 lg:px-8 py-20 sm:py-28">
          <div className="text-center">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-8 leading-tight font-sans">
              Hire World-Class<br />
              <span className="text-transparent bg-gradient-to-r from-[#00C6A2] to-[#00E5B8] bg-clip-text">
                E-Commerce Talent
              </span>
            </h1>
            
            <p className="text-xl sm:text-2xl text-white/90 mb-6 max-w-3xl mx-auto font-medium">
              Save up to 71% on payroll while accessing the top 1% of global talent
            </p>
            
            <p className="text-lg text-white/80 mb-16 max-w-2xl mx-auto">
              Get your personalized market scan in under 2 minutes. Discover what world-class talent costs in your market.
            </p>

            {/* Hero Stats - Aqua Highlights */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 max-w-5xl mx-auto mb-20">
              <div className="text-center">
                <div className="text-4xl font-bold text-white mb-2">💰 71%</div>
                <div className="text-sm text-white/80 font-medium">Average Savings vs US</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-white mb-2">🌍 50+</div>
                <div className="text-sm text-white/80 font-medium">Countries Sourced</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-white mb-2">⚡ 2min</div>
                <div className="text-sm text-white/80 font-medium">Market Scan Time</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-white mb-2">🎯 98%</div>
                <div className="text-sm text-white/80 font-medium">Client Satisfaction</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Market Scan Form Section */}
      <div className="relative -mt-12 pb-20">
        <div className="max-w-4xl mx-auto px-6 lg:px-8">
          <div id="market-scan-form" className="bg-white rounded-xl shadow-xl border border-[#E5E5E7] overflow-hidden">
            {/* Form Header */}
            <div className="bg-gradient-to-r from-[#7B61FF]/5 to-[#00C6A2]/5 px-8 py-8 border-b border-[#E5E5E7]">
              <h2 className="text-3xl font-bold text-[#1A1A1A] mb-3 font-sans">
                What role are you looking to hire? 🚀
              </h2>
              <p className="text-lg text-[#555555]">
                Get instant salary insights across 3 regions plus vetted candidate recommendations
              </p>
            </div>

            {/* Error Display */}
            {error && (
              <div className="mx-8 mt-6 p-6 bg-red-50 border border-red-200 rounded-xl">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-6 w-6 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-semibold text-red-800">
                      Something went wrong
                    </h3>
                    <div className="mt-2 text-sm text-red-700">
                      {error}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Market Scan Form */}
            <div className="p-8">
              <MarketScanForm 
                onSubmit={handleFormSubmit}
                isSubmitting={isSubmitting}
              />
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-[#1A1A1A] mb-6 font-sans">
              Why Tidal Delivers Results 📈
            </h2>
            <p className="text-xl text-[#555555] max-w-3xl mx-auto">
              Our battle-tested process connects you with pre-vetted, top-tier talent who've already proven themselves at scale
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-12">
            {/* Rigorous Vetting */}
            <div className="text-center group hover:transform hover:scale-105 transition-all duration-300">
              <div className="w-20 h-20 bg-gradient-to-br from-[#7B61FF] to-[#9F7FFF] rounded-xl flex items-center justify-center mx-auto mb-6 group-hover:shadow-lg transition-shadow">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-[#1A1A1A] mb-4 font-sans">
                Rigorous Vetting Process
              </h3>
              <ul className="text-[#555555] space-y-3 text-left max-w-xs mx-auto">
                <li className="flex items-start">
                  <span className="text-[#00C6A2] mr-3 mt-1">✓</span>
                  <span>Video interviews with every candidate</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[#00C6A2] mr-3 mt-1">✓</span>
                  <span>Skills assessments already completed</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[#00C6A2] mr-3 mt-1">✓</span>
                  <span>Reference checks verified</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[#00C6A2] mr-3 mt-1">✓</span>
                  <span>Portfolio reviews for technical roles</span>
                </li>
              </ul>
            </div>

            {/* Quality Over Quantity */}
            <div className="text-center group hover:transform hover:scale-105 transition-all duration-300">
              <div className="w-20 h-20 bg-gradient-to-br from-[#00C6A2] to-[#00E5B8] rounded-xl flex items-center justify-center mx-auto mb-6 group-hover:shadow-lg transition-shadow">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-[#1A1A1A] mb-4 font-sans">
                The Intangibles We Find
              </h3>
              <ul className="text-[#555555] space-y-3 text-left max-w-xs mx-auto">
                <li className="flex items-start">
                  <span className="text-[#00C6A2] mr-3 mt-1">✓</span>
                  <span>Curious & hungry to learn</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[#00C6A2] mr-3 mt-1">✓</span>
                  <span>Proactive problem-solvers</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[#00C6A2] mr-3 mt-1">✓</span>
                  <span>Cultural fit for your brand</span>
                </li>
                <li className="flex items-start">
                  <span className="text-[#00C6A2] mr-3 mt-1">✓</span>
                  <span>Proven track records at scale</span>
                </li>
              </ul>
            </div>

            {/* Global Network */}
            <div className="text-center group hover:transform hover:scale-105 transition-all duration-300">
              <div className="w-20 h-20 bg-gradient-to-br from-[#7B61FF] to-[#00C6A2] rounded-xl flex items-center justify-center mx-auto mb-6 group-hover:shadow-lg transition-shadow">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-[#1A1A1A] mb-4 font-sans">
                Global Talent Network
              </h3>
              <div className="text-[#555555] space-y-4 text-left max-w-xs mx-auto">
                <p>Access to the top 1% of global e-commerce talent across 50+ countries.</p>
                <div className="bg-[#F7F7F9] p-4 rounded-lg">
                  <div className="text-sm text-[#555555] mb-2">Popular regions:</div>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-[#7B61FF]/10 text-[#7B61FF] rounded-full text-xs font-medium">🇺🇸 United States</span>
                    <span className="px-3 py-1 bg-[#00C6A2]/10 text-[#00C6A2] rounded-full text-xs font-medium">🌎 Latin America</span>
                    <span className="px-3 py-1 bg-[#7B61FF]/10 text-[#7B61FF] rounded-full text-xs font-medium">🇵🇭 Philippines</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sample Results Preview */}
      <div className="bg-[#F7F7F9] py-20">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-[#1A1A1A] mb-6 font-sans">
              Here's what you'll get 📊
            </h2>
            <p className="text-xl text-[#555555] max-w-3xl mx-auto">
              A comprehensive market analysis with region-specific salary data and hand-picked candidate recommendations
            </p>
          </div>

          {/* Sample Region Cards Preview */}
          <div className="grid lg:grid-cols-3 gap-8 mb-16">
            {/* United States Card */}
            <div className="bg-white rounded-xl shadow-lg border border-[#E5E5E7] p-8 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">🇺🇸</span>
                  <h3 className="text-xl font-bold text-[#1A1A1A] font-sans">United States</h3>
                </div>
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              </div>
              <div className="space-y-4">
                <div className="text-3xl font-bold text-[#1A1A1A]">$75k - $120k</div>
                <div className="text-sm text-[#555555]">Annual salary range</div>
                <div className="bg-[#F7F7F9] p-3 rounded-lg">
                  <div className="text-xs text-[#555555] mb-1">Key benefits:</div>
                  <ul className="text-xs text-[#555555] space-y-1">
                    <li>• Same timezone</li>
                    <li>• Native English speakers</li>
                    <li>• Direct market knowledge</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Latin America Card */}
            <div className="bg-white rounded-xl shadow-lg border border-[#E5E5E7] p-8 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">🌎</span>
                  <h3 className="text-xl font-bold text-[#1A1A1A] font-sans">Latin America</h3>
                </div>
                <div className="bg-[#00C6A2]/10 px-3 py-1 rounded-full">
                  <span className="text-[#00C6A2] text-xs font-bold">45% savings</span>
                </div>
              </div>
              <div className="space-y-4">
                <div className="text-3xl font-bold text-[#1A1A1A]">$40k - $65k</div>
                <div className="text-sm text-[#555555]">Annual salary range</div>
                <div className="bg-[#F7F7F9] p-3 rounded-lg">
                  <div className="text-xs text-[#555555] mb-1">Key benefits:</div>
                  <ul className="text-xs text-[#555555] space-y-1">
                    <li>• Similar timezones</li>
                    <li>• High English proficiency</li>
                    <li>• Strong work ethic</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Philippines Card */}
            <div className="bg-white rounded-xl shadow-lg border border-[#E5E5E7] p-8 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">🇵🇭</span>
                  <h3 className="text-xl font-bold text-[#1A1A1A] font-sans">Philippines</h3>
                </div>
                <div className="bg-[#00C6A2]/10 px-3 py-1 rounded-full">
                  <span className="text-[#00C6A2] text-xs font-bold">👋 71% savings</span>
                </div>
              </div>
              <div className="space-y-4">
                <div className="text-3xl font-bold text-[#1A1A1A]">$22k - $35k</div>
                <div className="text-sm text-[#555555]">Annual salary range</div>
                <div className="bg-[#F7F7F9] p-3 rounded-lg">
                  <div className="text-xs text-[#555555] mb-1">Key benefits:</div>
                  <ul className="text-xs text-[#555555] space-y-1">
                    <li>• Excellent English</li>
                    <li>• Cultural alignment with US</li>
                    <li>• Tech-savvy workforce</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Final CTA Section */}
      <div className="bg-gradient-to-r from-[#7B61FF] to-[#9F7FFF] py-20">
        <div className="max-w-4xl mx-auto text-center px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-6 font-sans">
            Ready to save 71% on your next hire? 🚀
          </h2>
          <p className="text-xl text-white/90 mb-10">
            Join hundreds of brands who've scaled their teams with Tidal. Get your market scan in under 2 minutes.
          </p>
          <button 
            onClick={() => document.getElementById('market-scan-form')?.scrollIntoView({ behavior: 'smooth' })}
            className="bg-white text-[#7B61FF] font-bold px-10 py-4 rounded-xl hover:bg-gray-50 hover:scale-105 transition-all duration-300 shadow-lg text-lg"
          >
            Get My Market Scan Now →
          </button>
          <div className="mt-6 text-white/80 text-sm">
            ⚡ 2-minute setup • 📊 Instant results • 🎯 Zero commitment
          </div>
        </div>
      </div>
    </div>
  )
}