import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { MarketScanResponse } from '../services/types'
import { RegionCards, SkillsSection, JobAnalysisSection, NextStepsSection, ReportGenerationButton } from '../components/ui'

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

  // Loading State with Tidal branding
  if (loading) {
    return (
      <div className="market-scan-loading">
        <div className="loading-container">
          <div className="loading-spinner">
            <div className="spinner-circle"></div>
          </div>
          <h2 className="loading-title">Analyzing Your Market Scan</h2>
          <p className="loading-description">
            Comparing against 200+ similar roles to find the perfect talent strategy for you
          </p>
          <div className="loading-progress">
            <div className="progress-bar">
              <div className="progress-fill"></div>
            </div>
            <p className="progress-text">This typically takes 30-60 seconds</p>
          </div>
        </div>
      </div>
    )
  }

  // Error State with improved messaging
  if (error || !scan) {
    return (
      <div className="market-scan-error">
        <div className="error-container">
          <div className="error-icon">
            <span role="img" aria-label="error">⚠️</span>
          </div>
          <h2 className="error-title">Scan Not Found</h2>
          <p className="error-description">
            {error || 'We couldn\'t locate the market scan you requested. It may have expired or been removed.'}
          </p>
          <div className="error-actions">
            <Link to="/" className="btn-primary">
              Create New Market Scan
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
    )
  }

  return (
    <div className="min-h-screen bg-[#F7F7F9]">
      {/* Page Header - Clear Purpose & Benefits */}
      <div className="bg-white border-b border-[#E5E5E7]">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
          {/* Breadcrumb */}
          <div className="flex items-center gap-2 text-sm text-[#555555] mb-4">
            <Link to="/" className="hover:text-[#7B61FF] transition-colors">Market Scans</Link>
            <span>/</span>
            <span className="text-[#1A1A1A] font-medium">Results</span>
          </div>
          
          {/* Clear Page Purpose */}
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <h1 className="text-3xl font-bold text-[#1A1A1A] mb-2 font-sans">
                Your {scan.job_title} Hiring Insights
              </h1>
              <p className="text-lg text-[#555555] mb-4">
                Review salary ranges, skill requirements, and candidate recommendations below, then book a call to see qualified candidates.
              </p>
              <div className="flex items-center gap-6 text-sm text-[#555555]">
                <div className="flex items-center gap-2">
                  <span role="img" aria-label="company">🏢</span>
                  <span>{scan.company_domain}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span role="img" aria-label="calendar">📅</span>
                  <span>{new Date(scan.created_at).toLocaleDateString('en-US', { 
                    month: 'long', 
                    day: 'numeric', 
                    year: 'numeric' 
                  })}</span>
                </div>
              </div>
            </div>
            
            {/* Status & Confidence */}
            <div className="flex items-center gap-4">
              <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${
                scan.status === 'completed' ? 'bg-green-50 text-green-700' :
                scan.status === 'analyzing' ? 'bg-blue-50 text-blue-700' :
                scan.status === 'failed' ? 'bg-red-50 text-red-700' :
                'bg-yellow-50 text-yellow-700'
              }`}>
                {scan.status === 'completed' && <span>✅</span>}
                {scan.status === 'analyzing' && <span className="animate-spin">⚙️</span>}
                {scan.status === 'failed' && <span>❌</span>}
                {scan.status === 'pending' && <span>⏳</span>}
                <span className="font-medium capitalize">{scan.status}</span>
              </div>
              
              {scan.confidence_score && (
                <div className="text-right">
                  <div className="text-sm text-[#555555]">Confidence</div>
                  <div className="text-xl font-bold text-[#1A1A1A]">{Math.round(scan.confidence_score * 100)}%</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Processing Status Banner */}
      {(scan.status === 'analyzing' || scan.status === 'pending') && (
        <div className="processing-banner">
          <div className="processing-content">
            <div className="processing-spinner">
              <div className="spinner-circle analyzing"></div>
            </div>
            <div className="processing-info">
              <h3 className="processing-title">
                {scan.status === 'analyzing' ? 'Analysis in Progress' : 'Scan Queued'}
              </h3>
              <p className="processing-description">
                We're analyzing your job requirements and comparing against our database of 
                {scan.similar_scans_count ? ` ${scan.similar_scans_count}+` : ' 200+'} market scans. 
                Results will update automatically.
              </p>
              <div className="processing-stats">
                <div className="stat-item">
                  <span className="stat-icon" role="img" aria-label="database">🗄️</span>
                  <span className="stat-text">
                    {scan.similar_scans_count || 200}+ similar roles analyzed
                  </span>
                </div>
                <div className="stat-item">
                  <span className="stat-icon" role="img" aria-label="time">⏱️</span>
                  <span className="stat-text">Typically completes in 60 seconds</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Results Content */}
      {scan.status === 'completed' && scan.salary_recommendations && (
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
            {/* Main Content - 3/4 width */}
            <div className="xl:col-span-3 space-y-12">
              
              {/* Section 1: Salary Insights */}
              <section>
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-[#1A1A1A] mb-2 font-sans">💰 Salary Insights</h2>
                  <p className="text-[#555555]">Compare regional pay rates and potential savings</p>
                </div>
                <RegionCards 
                  salaryRecommendations={scan.salary_recommendations.salary_recommendations}
                  isLoading={false}
                />
              </section>

              {/* Section 2: Skills & Tools */}
              {scan.skills_recommendations && (
                <section>
                  <div className="mb-6">
                    <h2 className="text-2xl font-bold text-[#1A1A1A] mb-2 font-sans">🛠️ Skills & Tools</h2>
                    <p className="text-[#555555]">Must-have requirements and nice-to-have qualifications</p>
                  </div>
                  <SkillsSection 
                    skillsRecommendations={scan.skills_recommendations}
                    isLoading={false}
                  />
                </section>
              )}

              {/* Section 3: Job Analysis */}
              {scan.job_analysis && (
                <section>
                  <div className="mb-6">
                    <h2 className="text-2xl font-bold text-[#1A1A1A] mb-2 font-sans">📊 Job Analysis</h2>
                    <p className="text-[#555555]">Role complexity, responsibilities, and key factors</p>
                  </div>
                  <JobAnalysisSection 
                    jobAnalysis={scan.job_analysis}
                    isLoading={false}
                  />
                </section>
              )}

              {/* Section 4: Next Steps */}
              <section>
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-[#1A1A1A] mb-2 font-sans">🚀 Your Next Steps</h2>
                  <p className="text-[#555555]">Ready to find your perfect candidate? Here's how to get started</p>
                </div>
                <NextStepsSection 
                  jobTitle={scan.job_title}
                  isLoading={false}
                />
              </section>
            </div>

            {/* Sidebar - Right Column */}
            <div className="space-y-6">
              
              {/* Report Generation CTA */}
              <div className="bg-gradient-to-r from-[#7B61FF] to-[#9F7FFF] rounded-xl p-6 text-white">
                <h3 className="text-lg font-semibold mb-2">Generate Professional Report</h3>
                <p className="text-white/90 text-sm mb-4">
                  Create a branded Tidal report matching your client's format with all analysis data.
                </p>
                <ReportGenerationButton 
                  scanId={scan.id}
                  clientName={scan.company_domain.replace('.com', '').toUpperCase()}
                  roleTitle={scan.job_title}
                />
              </div>

              {/* Primary CTA */}
              <div className="bg-white rounded-xl border border-[#E5E5E7] p-6">
                <h3 className="text-lg font-semibold text-[#1A1A1A] mb-2">Ready to Start Hiring?</h3>
                <p className="text-[#555555] text-sm mb-4">
                  Book a 15-minute call to see qualified {scan.job_title} candidates from our vetted talent pool.
                </p>
                <a 
                  href={`mailto:connect@hiretidal.com?subject=Strategy Call - ${scan.job_title}&body=Hi! I'd like to schedule a call to discuss hiring for the ${scan.job_title} role and see qualified candidates.`}
                  className="inline-flex items-center justify-center w-full bg-[#7B61FF] text-white font-semibold px-4 py-3 rounded-lg hover:bg-[#6B51E5] transition-colors"
                >
                  Book Strategy Call
                  <span className="ml-2">→</span>
                </a>
              </div>

              {/* How Tidal Works - Simplified */}
              <div className="bg-white rounded-xl border border-[#E5E5E7] p-6">
                <h3 className="font-semibold text-[#1A1A1A] mb-4">Why Choose Tidal</h3>
                
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-[#7B61FF]/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-sm">🎯</span>
                    </div>
                    <div>
                      <div className="font-medium text-[#1A1A1A] text-sm">Pre-Vetted Talent</div>
                      <div className="text-xs text-[#555555]">Video interviews, skills assessments, and reference checks completed</div>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-[#00C6A2]/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-sm">💰</span>
                    </div>
                    <div>
                      <div className="font-medium text-[#1A1A1A] text-sm">Cost Savings</div>
                      <div className="text-xs text-[#555555]">Save 48-71% vs US rates while maintaining quality</div>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-[#7B61FF]/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-sm">🛡️</span>
                    </div>
                    <div>
                      <div className="font-medium text-[#1A1A1A] text-sm">6-Month Guarantee</div>
                      <div className="text-xs text-[#555555]">Risk-free replacement if hire doesn't work out</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Quick Contact */}
              <div className="bg-[#F7F7F9] rounded-xl border border-[#E5E5E7] p-6">
                <h3 className="font-semibold text-[#1A1A1A] mb-2">Have Questions?</h3>
                <p className="text-sm text-[#555555] mb-3">
                  Speak with our hiring experts about your specific needs.
                </p>
                <a 
                  href="mailto:connect@hiretidal.com?subject=Questions about Hiring"
                  className="inline-flex items-center text-[#7B61FF] font-medium text-sm hover:text-[#6B51E5] transition-colors"
                >
                  connect@hiretidal.com
                  <span className="ml-1">↗</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Failed State */}
      {scan.status === 'failed' && (
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
          <div className="bg-white rounded-xl border border-red-200 p-8 text-center">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-2xl" role="img" aria-label="failed">❌</span>
            </div>
            <h2 className="text-2xl font-bold text-[#1A1A1A] mb-4">Analysis Failed</h2>
            <p className="text-[#555555] mb-8 max-w-2xl mx-auto">
              We encountered an issue analyzing your job requirements. Our team has been 
              notified and will investigate. Please try creating a new scan or contact support.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/" 
                className="bg-[#7B61FF] text-white font-semibold px-6 py-3 rounded-lg hover:bg-[#6B51E5] transition-colors"
              >
                Create New Scan
              </Link>
              <a 
                href="mailto:connect@hiretidal.com?subject=Market Scan Error"
                className="border border-[#7B61FF] text-[#7B61FF] font-semibold px-6 py-3 rounded-lg hover:bg-[#7B61FF]/5 transition-colors"
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