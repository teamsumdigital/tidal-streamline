import React from 'react'
import { JobAnalysis } from '../../services/types'

interface JobAnalysisSectionProps {
  jobAnalysis?: JobAnalysis
  className?: string
  isLoading?: boolean
}

export const JobAnalysisSection: React.FC<JobAnalysisSectionProps> = ({
  jobAnalysis,
  className = '',
  isLoading = false
}) => {
  // Default job analysis data following Tidal design patterns
  const defaultAnalysis: JobAnalysis = {
    role_category: 'Brand Marketing Manager',
    experience_level: 'mid',
    years_experience_required: '3-5 years',
    must_have_skills: ['Digital Marketing', 'Brand Strategy', 'Analytics'],
    nice_to_have_skills: ['Video Production', 'Influencer Marketing'],
    key_responsibilities: [
      'Develop and execute comprehensive brand marketing strategies',
      'Manage digital advertising campaigns across multiple platforms',
      'Analyze campaign performance and optimize for ROI',
      'Collaborate with creative teams on brand content',
      'Track brand awareness and sentiment metrics'
    ],
    remote_work_suitability: 'Highly suitable for remote work',
    complexity_score: 75,
    recommended_regions: ['Philippines', 'Latin America'],
    unique_challenges: 'Requires strong analytical skills combined with creative thinking',
    salary_factors: [
      'Experience with premium brands',
      'Proven track record with ROAS improvement',
      'Multi-platform advertising expertise'
    ]
  }

  const analysis = jobAnalysis || defaultAnalysis

  const getComplexityLevel = (score: number): { label: string; color: string; icon: string } => {
    if (score >= 80) return { label: 'High Complexity', color: 'text-red-600', icon: '🔥' }
    if (score >= 60) return { label: 'Medium Complexity', color: 'text-yellow-600', icon: '⚡' }
    return { label: 'Standard Complexity', color: 'text-green-600', icon: '✅' }
  }

  const getExperienceLabel = (level: string): { label: string; icon: string } => {
    switch (level) {
      case 'junior': return { label: 'Junior Level', icon: '🌱' }
      case 'mid': return { label: 'Mid Level', icon: '🚀' }
      case 'senior': return { label: 'Senior Level', icon: '🎯' }
      case 'expert': return { label: 'Expert Level', icon: '💎' }
      default: return { label: 'Mid Level', icon: '🚀' }
    }
  }

  const complexity = getComplexityLevel(analysis.complexity_score)
  const experience = getExperienceLabel(analysis.experience_level)

  if (isLoading) {
    return (
      <section className={`job-analysis-section ${className}`}>
        <div className="job-analysis-container">
          <div className="job-analysis-header animate-pulse">
            <div className="job-analysis-title-skeleton bg-gray-200 w-64 h-8 rounded mb-3"></div>
            <div className="job-analysis-subtitle-skeleton bg-gray-200 w-96 h-5 rounded"></div>
          </div>
          
          <div className="job-analysis-content">
            <div className="job-analysis-grid">
              {[1, 2, 3, 4].map((index) => (
                <div key={index} className="job-analysis-insight animate-pulse">
                  <div className="insight-icon-skeleton bg-gray-200 w-8 h-8 rounded"></div>
                  <div className="insight-content">
                    <div className="insight-title-skeleton bg-gray-200 w-32 h-5 rounded mb-2"></div>
                    <div className="insight-value-skeleton bg-gray-200 w-24 h-6 rounded"></div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="job-analysis-details animate-pulse">
              <div className="detail-section">
                <div className="detail-title-skeleton bg-gray-200 w-40 h-6 rounded mb-3"></div>
                <div className="detail-list">
                  {[1, 2, 3].map((index) => (
                    <div key={index} className="detail-item-skeleton bg-gray-200 w-full h-4 rounded mb-2"></div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className={`job-analysis-section ${className}`}>
      <div className="job-analysis-container">
        <div className="job-analysis-header">
          <h2 className="job-analysis-title">Job Analysis Summary</h2>
          <p className="job-analysis-subtitle">
            Key insights about this role and what to expect during hiring
          </p>
        </div>
        
        <div className="job-analysis-content">
          {/* Key Insights Grid - Most Important First */}
          <div className="job-analysis-grid">
            <div className="job-analysis-insight featured">
              <div className="insight-icon">
                <span role="img" aria-label="complexity">{complexity.icon}</span>
              </div>
              <div className="insight-content">
                <h3 className="insight-title">Role Complexity</h3>
                <div className="insight-value-wrapper">
                  <span className={`insight-value ${complexity.color}`}>
                    {complexity.label}
                  </span>
                  <span className="insight-score">({analysis.complexity_score}/100)</span>
                </div>
              </div>
            </div>

            <div className="job-analysis-insight">
              <div className="insight-icon">
                <span role="img" aria-label="experience">{experience.icon}</span>
              </div>
              <div className="insight-content">
                <h3 className="insight-title">Experience Level</h3>
                <span className="insight-value">{experience.label}</span>
                <span className="insight-detail">{analysis.years_experience_required}</span>
              </div>
            </div>

            <div className="job-analysis-insight">
              <div className="insight-icon">
                <span role="img" aria-label="remote work">🌍</span>
              </div>
              <div className="insight-content">
                <h3 className="insight-title">Remote Suitability</h3>
                <span className="insight-value text-success-green">
                  {analysis.remote_work_suitability}
                </span>
              </div>
            </div>

            <div className="job-analysis-insight">
              <div className="insight-icon">
                <span role="img" aria-label="recommended regions">🗺️</span>
              </div>
              <div className="insight-content">
                <h3 className="insight-title">Best Regions</h3>
                <div className="insight-regions">
                  {analysis.recommended_regions.slice(0, 2).map((region, index) => (
                    <span key={region} className="region-tag">
                      {region}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Analysis */}
          <div className="job-analysis-details">
            {/* Key Responsibilities */}
            <div className="detail-section">
              <h3 className="detail-title">
                <span className="detail-icon" role="img" aria-label="responsibilities">📋</span>
                Key Responsibilities
              </h3>
              <ul className="detail-list responsibilities-list">
                {analysis.key_responsibilities.map((responsibility, index) => (
                  <li 
                    key={index} 
                    className="detail-item responsibility-item"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <span className="responsibility-bullet">•</span>
                    {responsibility}
                  </li>
                ))}
              </ul>
            </div>

            {/* Unique Challenges */}
            {analysis.unique_challenges && (
              <div className="detail-section challenge-section">
                <h3 className="detail-title">
                  <span className="detail-icon" role="img" aria-label="challenges">⚠️</span>
                  Unique Challenges
                </h3>
                <div className="challenge-content">
                  <p className="challenge-text">{analysis.unique_challenges}</p>
                </div>
              </div>
            )}

            {/* Salary Factors */}
            {analysis.salary_factors.length > 0 && (
              <div className="detail-section">
                <h3 className="detail-title">
                  <span className="detail-icon" role="img" aria-label="salary factors">💰</span>
                  Salary Influencing Factors
                </h3>
                <ul className="detail-list factors-list">
                  {analysis.salary_factors.map((factor, index) => (
                    <li 
                      key={index} 
                      className="detail-item factor-item"
                      style={{ animationDelay: `${index * 100}ms` }}
                    >
                      <span className="factor-bullet">✓</span>
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}

export default JobAnalysisSection