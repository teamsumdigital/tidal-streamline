import React from 'react'
import { SkillsRecommendation } from '../../services/types'

interface SkillsSectionProps {
  skillsRecommendations?: SkillsRecommendation
  className?: string
  isLoading?: boolean
}

export const SkillsSection: React.FC<SkillsSectionProps> = ({
  skillsRecommendations,
  className = '',
  isLoading = false
}) => {
  if (isLoading) {
    return (
      <section className={`bg-white rounded-xl shadow-sm border border-[#E5E5E7] p-8 mb-8 ${className}`}>
        <div className="mb-8">
          <div className="w-64 h-8 bg-gray-200 rounded animate-pulse mb-2"></div>
          <div className="w-96 h-5 bg-gray-200 rounded animate-pulse"></div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {[1, 2].map((index) => (
            <div key={index}>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-gray-200 rounded-lg animate-pulse"></div>
                <div className="space-y-2">
                  <div className="w-24 h-5 bg-gray-200 rounded animate-pulse"></div>
                  <div className="w-32 h-4 bg-gray-200 rounded animate-pulse"></div>
                </div>
              </div>
              <div className="space-y-3">
                {[1, 2, 3, 4].map((skillIndex) => (
                  <div key={skillIndex} className="w-full h-12 bg-gray-200 rounded-lg animate-pulse"></div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    )
  }

  if (!skillsRecommendations) {
    return null
  }

  return (
    <section className={`bg-white rounded-xl shadow-sm border border-[#E5E5E7] p-8 mb-8 ${className}`}>
      {/* Section Header */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-[#1A1A1A] mb-2 font-sans">Recommended Skills & Tools</h2>
        <p className="text-[#555555] text-base">
          Based on similar successful hires in your industry
        </p>
      </div>
      
      {/* Skills Grid - Clean 2-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Must Have Skills */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center">
                <span className="text-xl" role="img" aria-label="star">⭐</span>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-[#1A1A1A] font-sans">Must Have</h3>
                <p className="text-sm text-[#555555]">Essential requirements</p>
              </div>
            </div>
            <button className="flex items-center gap-2 text-sm text-[#555555] hover:text-[#7B61FF] transition-colors">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Update
            </button>
          </div>
          
          <div className="space-y-3">
            {skillsRecommendations.must_have_skills.map((skill, index) => {
              const isShopifySkill = skill.toLowerCase().includes('shopify') || skill.toLowerCase().includes('platform')
              return (
                <div 
                  key={index} 
                  className={`flex items-center justify-between rounded-lg px-4 py-3 ${
                    isShopifySkill 
                      ? 'bg-[#7B61FF]/10 border border-[#7B61FF]/30' 
                      : 'bg-red-50 border border-red-200'
                  }`}
                >
                  <span className={`font-medium ${
                    isShopifySkill ? 'text-[#7B61FF]' : 'text-red-800'
                  }`}>
                    {skill}
                  </span>
                  <div className="flex items-center gap-2">
                    {isShopifySkill && <span className="text-xs text-[#7B61FF]">Platform</span>}
                    <div className={`w-2 h-2 rounded-full ${
                      isShopifySkill ? 'bg-[#7B61FF]' : 'bg-red-500'
                    }`}></div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Nice to Have Skills */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center">
                <span className="text-xl" role="img" aria-label="plus">➕</span>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-[#1A1A1A] font-sans">Nice to Have</h3>
                <p className="text-sm text-[#555555]">Bonus qualifications</p>
              </div>
            </div>
            <button className="flex items-center gap-2 text-sm text-[#555555] hover:text-[#7B61FF] transition-colors">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Update
            </button>
          </div>
          
          <div className="space-y-3">
            {skillsRecommendations.nice_to_have_skills.map((skill, index) => {
              const isBusinessSkill = skill.toLowerCase().includes('marketing') || skill.toLowerCase().includes('design') || skill.toLowerCase().includes('logistics')
              return (
                <div 
                  key={index} 
                  className={`flex items-center justify-between rounded-lg px-4 py-3 ${
                    isBusinessSkill 
                      ? 'bg-[#00C6A2]/10 border border-[#00C6A2]/30' 
                      : 'bg-blue-50 border border-blue-200'
                  }`}
                >
                  <span className={`font-medium ${
                    isBusinessSkill ? 'text-[#00C6A2]' : 'text-blue-800'
                  }`}>
                    {skill}
                  </span>
                  <div className="flex items-center gap-2">
                    {isBusinessSkill && <span className="text-xs text-[#00C6A2]">Business</span>}
                    <div className={`w-2 h-2 rounded-full ${
                      isBusinessSkill ? 'bg-[#00C6A2]' : 'bg-blue-500'
                    }`}></div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Certification Recommendations */}
      {skillsRecommendations.certification_recommendations && 
       skillsRecommendations.certification_recommendations.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-[#1A1A1A] mb-4 font-sans">Recommended Certifications</h3>
          <div className="flex flex-wrap gap-3">
            {skillsRecommendations.certification_recommendations.map((cert, index) => (
              <div 
                key={index} 
                className="flex items-center gap-2 bg-[#7B61FF]/10 border border-[#7B61FF]/20 rounded-lg px-4 py-2"
              >
                <span className="text-lg" role="img" aria-label="certificate">🏆</span>
                <span className="text-[#7B61FF] font-medium">{cert}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  )
}

export default SkillsSection