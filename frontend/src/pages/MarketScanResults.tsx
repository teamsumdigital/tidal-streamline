import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { MarketScanResponse } from '../services/types'
import { RegionCards } from '../components/ui'


export const MarketScanResults: React.FC = () => {
  const { scanId } = useParams<{ scanId: string }>()
  const [scan, setScan] = useState<MarketScanResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchScan = async () => {
      if (!scanId) return

      try {
        const response = await apiService.getMarketScan(scanId)
        setScan(response)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load scan results')
      } finally {
        setLoading(false)
      }
    }

    fetchScan()
    
    // Poll for updates if scan is still processing
    const interval = scan?.status === 'analyzing' || scan?.status === 'pending' 
      ? setInterval(fetchScan, 3000) 
      : null

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [scanId, scan?.status])

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-tidal-purple mx-auto mb-4"></div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Loading Market Scan Results</h2>
          <p className="text-gray-600">Analyzing your job requirements and market data...</p>
        </div>
      </div>
    )
  }

  if (error || !scan) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Scan Not Found</h2>
          <p className="text-gray-600 mb-8">{error || 'The market scan you requested could not be found.'}</p>
          <Link to="/" className="btn-primary">
            Create New Market Scan
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{scan.job_title}</h1>
            <p className="text-gray-600 mt-1">{scan.company_domain}</p>
          </div>
          <div className="text-right">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
              scan.status === 'completed' ? 'bg-green-100 text-green-800' :
              scan.status === 'analyzing' ? 'bg-yellow-100 text-yellow-800' :
              scan.status === 'failed' ? 'bg-red-100 text-red-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {scan.status.charAt(0).toUpperCase() + scan.status.slice(1)}
            </span>
          </div>
        </div>
      </div>

      {/* Processing Status */}
      {(scan.status === 'analyzing' || scan.status === 'pending') && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-yellow-600 mr-3"></div>
            <div>
              <h3 className="text-lg font-semibold text-yellow-800">Analysis in Progress</h3>
              <p className="text-yellow-700">
                We're analyzing your job requirements and comparing against our database of 200+ market scans. 
                This typically takes 30-60 seconds.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Results Content - Two Column Layout */}
      {scan.status === 'completed' && scan.salary_recommendations && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 320px',
          gap: '2rem',
          width: '100%',
          alignItems: 'start'
        }}>
          {/* Main Content - Left Side */}
          <div style={{minWidth: 0}}>
            {/* Regional Pay Range Cards - Using New Tidal PRD Component */}
            <div className="mb-12">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-bold text-dark-navy-text">Regional Pay Ranges</h2>
                <div className="flex items-center text-sm text-medium-gray-text">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Last updated: {scan.processing_time_seconds ? `${Math.round(scan.processing_time_seconds)} seconds ago` : '2 minutes ago'}
                </div>
              </div>
              
              <RegionCards 
                salaryRecommendations={scan.salary_recommendations.salary_recommendations}
                className="mb-8"
              />
            </div>

          {/* Skills Recommendations - Improved Layout */}
          {scan.skills_recommendations && (
            <div className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-8">Recommended Skills & Tools</h2>
              
              <div className="grid md:grid-cols-2 gap-8">
                {/* Must Have Skills */}
                <div className="bg-white rounded-2xl border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-gray-900 flex items-center">
                      <span className="text-red-500 mr-3">⭐</span>
                      Must Have
                    </h3>
                    <button className="text-sm text-gray-500 hover:text-gray-700 flex items-center">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      Update
                    </button>
                  </div>
                  <div className="space-y-3">
                    {scan.skills_recommendations.must_have_skills.map((skill, index) => (
                      <div key={index} className="bg-gray-50 rounded-lg px-4 py-3 border border-gray-200">
                        <span className="text-gray-900 font-medium">{skill}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Nice to Have Skills */}
                <div className="bg-white rounded-2xl border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-gray-900 flex items-center">
                      <span className="text-blue-500 mr-3">➕</span>
                      Nice to Have
                    </h3>
                    <button className="text-sm text-gray-500 hover:text-gray-700 flex items-center">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      Update
                    </button>
                  </div>
                  <div className="space-y-3">
                    {scan.skills_recommendations.nice_to_have_skills.map((skill, index) => (
                      <div key={index} className="bg-gray-50 rounded-lg px-4 py-3 border border-gray-200">
                        <span className="text-gray-900 font-medium">{skill}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Job Analysis */}
          {scan.job_analysis && (
            <div className="card mb-12">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Job Analysis Summary</h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Role Category</h3>
                  <p className="text-gray-700">{scan.job_analysis.role_category}</p>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Experience Level</h3>
                  <p className="text-gray-700">{scan.job_analysis.experience_level}</p>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Complexity Score</h3>
                  <div className="flex items-center">
                    <span className="text-2xl font-bold text-tidal-purple">{scan.job_analysis.complexity_score}</span>
                    <span className="text-gray-500 ml-1">/10</span>
                  </div>
                </div>
              </div>
              
              {scan.job_analysis.unique_challenges && (
                <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                  <h3 className="font-semibold text-amber-800 mb-2">Unique Challenges</h3>
                  <p className="text-amber-700">{scan.job_analysis.unique_challenges}</p>
                </div>
              )}
            </div>
          )}

          {/* Next Steps */}
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Next Steps</h2>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-tidal-purple/10 text-tidal-purple rounded-full flex items-center justify-center text-sm font-bold">1</div>
                <div>
                  <h3 className="font-semibold text-gray-900">Review Salary Recommendations</h3>
                  <p className="text-gray-600">Consider the regional options and cost savings for your budget.</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-tidal-purple/10 text-tidal-purple rounded-full flex items-center justify-center text-sm font-bold">2</div>
                <div>
                  <h3 className="font-semibold text-gray-900">Refine Job Requirements</h3>
                  <p className="text-gray-600">Use the skills recommendations to update your job posting.</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-tidal-purple/10 text-tidal-purple rounded-full flex items-center justify-center text-sm font-bold">3</div>
                <div>
                  <h3 className="font-semibold text-gray-900">Connect with Tidal</h3>
                  <p className="text-gray-600">Ready to start hiring? Contact us to see qualified candidates.</p>
                </div>
              </div>
            </div>
            
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="flex flex-col sm:flex-row gap-4">
                <a 
                  href="mailto:connect@hiretidal.com?subject=Market Scan Follow-up"
                  className="btn-primary text-center"
                >
                  Connect with Tidal Team
                </a>
                <Link to="/" className="btn-outline text-center">
                  Create Another Scan
                </Link>
              </div>
            </div>
          </div>

          {/* Sidebar - Right Side */}
          <div style={{width: '320px'}}>
            <div className="sticky top-8 space-y-6">
              {/* How Tidal Hires */}
              <div className="bg-white rounded-2xl border border-gray-200 p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-6">How Tidal Hires</h3>
                  
                  {/* Robust Evaluation Process */}
                  <div className="bg-blue-50 rounded-xl p-4 mb-4">
                    <div className="flex items-center mb-3">
                      <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                        <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <h4 className="font-semibold text-gray-900">Robust Evaluation Process</h4>
                    </div>
                    <div className="space-y-2 text-sm text-gray-700">
                      <div className="flex items-center">
                        <svg className="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Video introductions for every candidate
                      </div>
                      <div className="flex items-center">
                        <svg className="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Skills assessments already completed
                      </div>
                      <div className="flex items-center">
                        <svg className="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Reference checks verified
                      </div>
                    </div>
                  </div>

                  {/* Intangibles We Look For */}
                  <div className="bg-green-50 rounded-xl p-4 mb-4">
                    <div className="flex items-center mb-3">
                      <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                        <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      </div>
                      <h4 className="font-semibold text-gray-900">Intangibles We Look For</h4>
                    </div>
                    <div className="space-y-2 text-sm text-gray-700">
                      <div className="flex items-center">
                        <svg className="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Curious & motivated to learn
                      </div>
                      <div className="flex items-center">
                        <svg className="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Proactive self-starters
                      </div>
                      <div className="flex items-center">
                        <svg className="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Hungry for more
                      </div>
                    </div>
                  </div>

                  {/* 6 Month Guarantee */}
                  <div className="bg-purple-50 rounded-xl p-4">
                    <div className="flex items-center mb-3">
                      <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                        <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                        </svg>
                      </div>
                      <h4 className="font-semibold text-gray-900">6 Month Guarantee</h4>
                    </div>
                    <p className="text-sm text-gray-700">
                      If your hire doesn't work out within 6 months, we'll find you another candidate at no additional cost.
                    </p>
                  </div>
                </div>

                {/* Analysis Complete CTA */}
                <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl p-6 text-white">
                  <div className="mb-4">
                    <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-white bg-opacity-20 text-white mb-2">
                      Analysis Complete
                    </div>
                    <h3 className="text-lg font-bold">Your salary analysis completed successfully.</h3>
                  </div>
                  <p className="text-white text-opacity-90 text-sm mb-4">
                    Book a 15-minute strategy call to discuss your shopify admin needs and get a custom hiring plan.
                  </p>
                  <a 
                    href="mailto:connect@hiretidal.com?subject=Strategy Call - Shopify Admin Role"
                    className="inline-flex items-center justify-center w-full px-4 py-2 bg-white text-purple-600 font-medium rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Book Strategy Call
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Error State */}
      {scan.status === 'failed' && (
        <div className="card">
          <div className="text-center py-8">
            <h2 className="text-xl font-bold text-red-600 mb-4">Analysis Failed</h2>
            <p className="text-gray-600 mb-6">
              We encountered an issue analyzing your job requirements. Our team has been notified.
            </p>
            <div className="flex justify-center gap-4">
              <Link to="/" className="btn-primary">
                Try Again
              </Link>
              <a 
                href="mailto:connect@hiretidal.com?subject=Market Scan Error"
                className="btn-outline"
              >
                Contact Support
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}