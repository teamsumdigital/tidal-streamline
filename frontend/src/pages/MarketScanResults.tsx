import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { MarketScanResponse } from '../services/types'

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
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-tidal-600 mx-auto mb-4"></div>
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

      {/* Results Content */}
      {scan.status === 'completed' && scan.salary_recommendations && (
        <>
          {/* Salary Analysis */}
          <div className="grid lg:grid-cols-2 gap-8 mb-12">
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Salary Analysis Results</h2>
              <div className="space-y-4">
                {Object.entries(scan.salary_recommendations.salary_recommendations).map(([region, salary]) => (
                  <div key={region} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-gray-900">{region}</h3>
                      {salary.savings_vs_us && (
                        <span className="badge badge-success">{salary.savings_vs_us}% savings vs US</span>
                      )}
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-bold text-gray-900">
                        ${salary.low.toLocaleString()} - ${salary.high.toLocaleString()}
                      </span>
                      <span className="text-sm text-gray-500">{salary.period}</span>
                    </div>
                    <div className="text-sm text-gray-600 mt-1">
                      Mid-point: ${salary.mid.toLocaleString()} {salary.currency}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Skills Recommendations */}
            {scan.skills_recommendations && (
              <div className="card">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Recommended Skills & Tools</h2>
                
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                    <span className="text-red-500 mr-2">★</span>
                    Must Have
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {scan.skills_recommendations.must_have_skills.map((skill, index) => (
                      <span key={index} className="badge bg-red-100 text-red-800">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                    <span className="text-blue-500 mr-2">+</span>
                    Nice to Have
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {scan.skills_recommendations.nice_to_have_skills.map((skill, index) => (
                      <span key={index} className="badge bg-blue-100 text-blue-800">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

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
                    <span className="text-2xl font-bold text-tidal-600">{scan.job_analysis.complexity_score}</span>
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
                <div className="w-6 h-6 bg-tidal-100 text-tidal-700 rounded-full flex items-center justify-center text-sm font-bold">1</div>
                <div>
                  <h3 className="font-semibold text-gray-900">Review Salary Recommendations</h3>
                  <p className="text-gray-600">Consider the regional options and cost savings for your budget.</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-tidal-100 text-tidal-700 rounded-full flex items-center justify-center text-sm font-bold">2</div>
                <div>
                  <h3 className="font-semibold text-gray-900">Refine Job Requirements</h3>
                  <p className="text-gray-600">Use the skills recommendations to update your job posting.</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-tidal-100 text-tidal-700 rounded-full flex items-center justify-center text-sm font-bold">3</div>
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
        </>
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