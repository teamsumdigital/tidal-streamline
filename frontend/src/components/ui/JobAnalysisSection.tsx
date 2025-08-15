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
    if (score >= 60) return { label: 'Standard Complexity', color: 'text-[#16A34A]', icon: '✅' }
    return { label: 'Standard Complexity', color: 'text-[#16A34A]', icon: '✅' }
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
    <section className={`bg-white rounded-xl shadow-sm border border-[#E5E5E7] p-8 mb-8 ${className}`}>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-[#1A1A1A] mb-2 font-sans">Job Analysis Summary</h2>
        <p className="text-[#555555] text-base">
          Key insights about this role and what to expect during hiring
        </p>
      </div>
      
      {/* Key Insights Grid - Clean 4-column layout */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Role Complexity Card */}
        <div className="bg-[#F7F7F9] rounded-xl p-6 text-center border border-[#E5E5E7]">
          <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
            <span className="text-2xl" role="img" aria-label="complexity">{complexity.icon}</span>
          </div>
          <h3 className="text-sm font-medium text-[#555555] mb-2 uppercase tracking-wide">ROLE<br/>COMPLEXITY</h3>
          <div className={`text-lg font-bold ${complexity.color} mb-1`}>
            {complexity.label.replace(' Complexity', '')}
          </div>
          <div className="text-xs text-[#555555]">({analysis.complexity_score}/10)</div>
        </div>

        {/* Experience Level Card */}
        <div className="bg-[#F7F7F9] rounded-xl p-6 text-center border border-[#E5E5E7]">
          <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
            <span className="text-2xl" role="img" aria-label="experience">{experience.icon}</span>
          </div>
          <h3 className="text-sm font-medium text-[#555555] mb-2 uppercase tracking-wide">EXPERIENCE<br/>LEVEL</h3>
          <div className="text-lg font-bold text-[#1A1A1A] mb-1">
            {experience.label.replace(' Level', '')}
          </div>
          <div className="text-xs text-[#555555]">{analysis.years_experience_required}</div>
        </div>

        {/* Remote Suitability Card */}
        <div className="bg-[#F7F7F9] rounded-xl p-6 text-center border border-[#E5E5E7]">
          <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
            <span className="text-2xl" role="img" aria-label="remote work">🌍</span>
          </div>
          <h3 className="text-sm font-medium text-[#555555] mb-2 uppercase tracking-wide">REMOTE<br/>SUITABILITY</h3>
          <div className="text-lg font-bold text-[#16A34A]">
            {analysis.remote_work_suitability === 'Highly suitable for remote work' ? 'High' : 'Medium'}
          </div>
        </div>

        {/* Best Regions Card */}
        <div className="bg-[#F7F7F9] rounded-xl p-6 text-center border border-[#E5E5E7]">
          <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
            <span className="text-2xl" role="img" aria-label="recommended regions">🗺️</span>
          </div>
          <h3 className="text-sm font-medium text-[#555555] mb-2 uppercase tracking-wide">BEST<br/>REGIONS</h3>
          <div className="space-y-1">
            {analysis.recommended_regions.slice(0, 2).map((region, index) => (
              <div key={region} className="text-sm font-medium text-[#00C6A2]">
                {region}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Detailed Analysis Sections - Two Column Layout */}
      <div className="space-y-8">
        {/* Key Responsibilities and Salary Factors - Side by Side */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Key Responsibilities */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 bg-[#7B61FF]/10 rounded-lg flex items-center justify-center">
                <span className="text-lg" role="img" aria-label="responsibilities">📋</span>
              </div>
              <h3 className="text-lg font-semibold text-[#1A1A1A] font-sans">Key Responsibilities</h3>
            </div>
            <ul className="space-y-3">
              {analysis.key_responsibilities.map((responsibility, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="text-[#7B61FF] mt-1.5 text-sm">•</span>
                  <span className="text-[#555555] leading-relaxed">{responsibility}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Salary Factors */}
          {analysis.salary_factors.length > 0 && (
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 bg-[#00C6A2]/10 rounded-lg flex items-center justify-center">
                  <span className="text-lg" role="img" aria-label="salary factors">💰</span>
                </div>
                <h3 className="text-lg font-semibold text-[#1A1A1A] font-sans">Salary Influencing Factors</h3>
              </div>
              <ul className="space-y-3">
                {analysis.salary_factors.map((factor, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="text-[#00C6A2] mt-1.5 text-sm">✓</span>
                    <span className="text-[#555555] leading-relaxed">{factor}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Unique Challenges - Full Width */}
        {analysis.unique_challenges && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <span className="text-lg" role="img" aria-label="challenges">⚠️</span>
              </div>
              <h3 className="text-lg font-semibold text-[#1A1A1A] font-sans">Unique Challenges</h3>
            </div>
            <p className="text-[#555555] leading-relaxed">{analysis.unique_challenges}</p>
          </div>
        )}
      </div>
    </section>
  )
}

export default JobAnalysisSection