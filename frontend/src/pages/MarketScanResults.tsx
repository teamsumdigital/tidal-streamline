import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { MarketScanResponse } from '../services/types'
import { RegionCards, SkillsSection, JobAnalysisSection, NextStepsSection } from '../components/ui'

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
    <div className="market-scan-results">
      {/* Header Section - Improved with Tidal branding */}
      <div className="scan-header">
        <div className="header-content">
          <div className="header-info">
            <div className="breadcrumb">
              <Link to="/" className="breadcrumb-link">Market Scans</Link>
              <span className="breadcrumb-separator">/</span>
              <span className="breadcrumb-current">Results</span>
            </div>
            <h1 className="scan-title">{scan.job_title}</h1>
            <div className="scan-meta">
              <span className="company-info">
                <span className="company-icon" role="img" aria-label="company">🏢</span>
                {scan.company_domain}
              </span>
              <span className="scan-date">
                <span className="date-icon" role="img" aria-label="calendar">📅</span>
                {new Date(scan.created_at).toLocaleDateString('en-US', { 
                  month: 'long', 
                  day: 'numeric', 
                  year: 'numeric' 
                })}
              </span>
            </div>
          </div>
          <div className="header-status">
            <div className={`status-badge ${scan.status}`}>
              {scan.status === 'completed' && <span className="status-icon">✅</span>}
              {scan.status === 'analyzing' && <span className="status-icon animate-spin">⚙️</span>}
              {scan.status === 'failed' && <span className="status-icon">❌</span>}
              {scan.status === 'pending' && <span className="status-icon">⏳</span>}
              <span className="status-text">
                {scan.status.charAt(0).toUpperCase() + scan.status.slice(1)}
              </span>
            </div>
            {scan.confidence_score && (
              <div className="confidence-score">
                <span className="confidence-label">Confidence</span>
                <span className="confidence-value">{Math.round(scan.confidence_score * 100)}%</span>
              </div>
            )}
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

      {/* Main Results Content - Following Tidal PRD Section Order */}
      {scan.status === 'completed' && scan.salary_recommendations && (
        <div className="results-layout">
          {/* Main Content Column */}
          <div className="main-content">
            {/* 1. Region Cards (First per PRD requirements) */}
            <section className="results-section region-section">
              <div className="section-header">
                <h2 className="section-title">Regional Pay Ranges</h2>
                <div className="section-meta">
                  <span className="meta-icon" role="img" aria-label="updated">🔄</span>
                  <span className="meta-text">
                    Updated {scan.processing_time_seconds ? `${Math.round(scan.processing_time_seconds)}s ago` : 'recently'}
                  </span>
                </div>
              </div>
              
              <RegionCards 
                salaryRecommendations={scan.salary_recommendations.salary_recommendations}
                isLoading={false}
              />
            </section>

            {/* 2. Skills Section (Second per PRD requirements) */}
            {scan.skills_recommendations && (
              <SkillsSection 
                skillsRecommendations={scan.skills_recommendations}
                isLoading={false}
              />
            )}

            {/* 3. Job Analysis Section (Third per PRD requirements) */}
            {scan.job_analysis && (
              <JobAnalysisSection 
                jobAnalysis={scan.job_analysis}
                isLoading={false}
              />
            )}

            {/* 4. Next Steps Section (Fourth per PRD requirements) */}
            <NextStepsSection 
              jobTitle={scan.job_title}
              isLoading={false}
            />
          </div>

          {/* Sidebar - Right Column */}
          <div className="sidebar-content">
            <div className="sidebar-sticky">
              {/* How Tidal Hires Card */}
              <div className="tidal-process-card">
                <h3 className="process-card-title">How Tidal Hires</h3>
                
                {/* Evaluation Process */}
                <div className="process-section evaluation">
                  <div className="process-header">
                    <div className="process-icon">
                      <span role="img" aria-label="evaluation">🎯</span>
                    </div>
                    <h4 className="process-title">Robust Evaluation Process</h4>
                  </div>
                  <div className="process-features">
                    <div className="feature-item">
                      <span className="feature-check">✅</span>
                      <span className="feature-text">Video introductions for every candidate</span>
                    </div>
                    <div className="feature-item">
                      <span className="feature-check">✅</span>
                      <span className="feature-text">Skills assessments already completed</span>
                    </div>
                    <div className="feature-item">
                      <span className="feature-check">✅</span>
                      <span className="feature-text">Reference checks verified</span>
                    </div>
                  </div>
                </div>

                {/* Intangibles */}
                <div className="process-section intangibles">
                  <div className="process-header">
                    <div className="process-icon">
                      <span role="img" aria-label="personality">✨</span>
                    </div>
                    <h4 className="process-title">Intangibles We Look For</h4>
                  </div>
                  <div className="process-features">
                    <div className="feature-item">
                      <span className="feature-check">✅</span>
                      <span className="feature-text">Curious & motivated to learn</span>
                    </div>
                    <div className="feature-item">
                      <span className="feature-check">✅</span>
                      <span className="feature-text">Proactive self-starters</span>
                    </div>
                    <div className="feature-item">
                      <span className="feature-check">✅</span>
                      <span className="feature-text">Hungry for growth</span>
                    </div>
                  </div>
                </div>

                {/* 6 Month Guarantee */}
                <div className="process-section guarantee">
                  <div className="process-header">
                    <div className="process-icon">
                      <span role="img" aria-label="guarantee">🛡️</span>
                    </div>
                    <h4 className="process-title">6 Month Guarantee</h4>
                  </div>
                  <p className="guarantee-text">
                    If your hire doesn't work out within 6 months, we'll find you another 
                    candidate at no additional cost.
                  </p>
                </div>
              </div>

              {/* CTA Card - Analysis Complete */}
              <div className="cta-card">
                <div className="cta-status">
                  <span className="cta-badge">Analysis Complete</span>
                  <h3 className="cta-title">Ready to Start Hiring?</h3>
                </div>
                <p className="cta-description">
                  Book a 15-minute strategy call to discuss your {scan.job_title} role 
                  and see qualified candidates from our pre-vetted talent pool.
                </p>
                <a 
                  href={`mailto:connect@hiretidal.com?subject=Strategy Call - ${scan.job_title}`}
                  className="cta-button"
                >
                  <span className="cta-button-text">Book Strategy Call</span>
                  <span className="cta-button-icon" role="img" aria-label="arrow">→</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Failed State */}
      {scan.status === 'failed' && (
        <div className="failed-state">
          <div className="failed-container">
            <div className="failed-icon">
              <span role="img" aria-label="failed">❌</span>
            </div>
            <h2 className="failed-title">Analysis Failed</h2>
            <p className="failed-description">
              We encountered an issue analyzing your job requirements. Our team has been 
              notified and will investigate. Please try creating a new scan or contact support.
            </p>
            <div className="failed-actions">
              <Link to="/" className="btn-primary">
                Create New Scan
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