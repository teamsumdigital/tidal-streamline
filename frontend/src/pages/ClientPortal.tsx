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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
              Market<br />
              <span className="text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text">
                Scan
              </span>
            </h1>
            
            <p className="text-xl sm:text-2xl text-blue-100 mb-4 max-w-3xl mx-auto">
              Precision Placement for E-Commerce Teams
            </p>
            
            <p className="text-lg text-blue-200 mb-12 max-w-2xl mx-auto">
              Increase Output. Save on Payroll. Scale Confidently.
            </p>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto mb-16">
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">200+</div>
                <div className="text-sm text-blue-200">Market Scans</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">71%</div>
                <div className="text-sm text-blue-200">Savings vs US</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">4</div>
                <div className="text-sm text-blue-200">Global Regions</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">50+</div>
                <div className="text-sm text-blue-200">Vetted Candidates</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Market Scan Form Section */}
      <div className="relative -mt-8 pb-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden">
            {/* Form Header */}
            <div className="bg-gradient-to-r from-slate-50 to-blue-50 px-8 py-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                What Role Are You Looking to Hire?
              </h2>
              <p className="text-gray-600">
                Get instant salary recommendations and candidate insights for your next hire.
              </p>
            </div>

            {/* Error Display */}
            {error && (
              <div className="mx-8 mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">
                      Analysis Failed
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

      {/* Features Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How Tidal Hires
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our proven process ensures you get the right talent at the right price.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Robust Evaluation Process */}
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Robust Evaluation Process
              </h3>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>✓ Video introductions for every candidate</li>
                <li>✓ Skills assessments already completed</li>
                <li>✓ Reference checks verified</li>
              </ul>
            </div>

            {/* Intangibles We Look For */}
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Intangibles We Look For
              </h3>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>✓ Curious & motivated to learn</li>
                <li>✓ Proactive self-starters</li>
                <li>✓ Hungry for more</li>
              </ul>
            </div>

            {/* Global Talent Pool */}
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Global Talent Access
              </h3>
              <p className="text-sm text-gray-600">
                Connecting brands to the best global talent with proven track records in e-commerce operations.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-slate-900 to-blue-900 py-16">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Scale Your Team?
          </h2>
          <p className="text-xl text-blue-200 mb-8">
            Get your market scan results and start building your dream team today.
          </p>
          <button 
            onClick={() => document.getElementById('market-scan-form')?.scrollIntoView({ behavior: 'smooth' })}
            className="bg-white text-slate-900 font-semibold px-8 py-3 rounded-lg hover:bg-gray-100 transition-colors duration-200"
          >
            Start Your Market Scan
          </button>
        </div>
      </div>
    </div>
  )
}