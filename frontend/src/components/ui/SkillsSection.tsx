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
      <div className={`skills-section ${className}`}>
        <div className="skills-header-skeleton">
          <div className="w-64 h-8 bg-gray-200 rounded animate-pulse mb-8"></div>
        </div>
        
        <div className="skills-grid">
          {[1, 2].map((index) => (
            <div key={index} className="skills-card animate-pulse">
              <div className="skills-card-header-skeleton">
                <div className="w-32 h-6 bg-gray-200 rounded mb-4"></div>
              </div>
              <div className="skills-list-skeleton space-y-3">
                {[1, 2, 3, 4].map((skillIndex) => (
                  <div key={skillIndex} className="w-full h-10 bg-gray-200 rounded"></div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (!skillsRecommendations) {
    return null
  }

  return (
    <div className={`skills-section ${className}`}>
      <div className="skills-header">
        <h2 className="skills-title">Recommended Skills & Tools</h2>
        <p className="skills-subtitle">
          Based on similar successful hires in your industry
        </p>
      </div>
      
      <div className="skills-grid">
        {/* Must Have Skills */}
        <div className="skills-card must-have">
          <div className="skills-card-header">
            <div className="skills-icon must-have-icon">
              <span role="img" aria-label="star">⭐</span>
            </div>
            <div className="skills-card-title-group">
              <h3 className="skills-card-title">Must Have</h3>
              <p className="skills-card-subtitle">Essential requirements</p>
            </div>
            <button className="skills-update-btn" aria-label="Update must-have skills">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Update
            </button>
          </div>
          
          <div className="skills-list">
            {skillsRecommendations.must_have_skills.map((skill, index) => (
              <div 
                key={index} 
                className="skill-pill must-have-pill"
                style={{ animationDelay: `${index * 50}ms` }}
              >
                <span className="skill-text">{skill}</span>
                <div className="skill-priority-indicator must-have-indicator"></div>
              </div>
            ))}
          </div>
        </div>

        {/* Nice to Have Skills */}
        <div className="skills-card nice-to-have">
          <div className="skills-card-header">
            <div className="skills-icon nice-to-have-icon">
              <span role="img" aria-label="plus">➕</span>
            </div>
            <div className="skills-card-title-group">
              <h3 className="skills-card-title">Nice to Have</h3>
              <p className="skills-card-subtitle">Bonus qualifications</p>
            </div>
            <button className="skills-update-btn" aria-label="Update nice-to-have skills">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Update
            </button>
          </div>
          
          <div className="skills-list">
            {skillsRecommendations.nice_to_have_skills.map((skill, index) => (
              <div 
                key={index} 
                className="skill-pill nice-to-have-pill"
                style={{ animationDelay: `${(index + skillsRecommendations.must_have_skills.length) * 50}ms` }}
              >
                <span className="skill-text">{skill}</span>
                <div className="skill-priority-indicator nice-to-have-indicator"></div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Certification Recommendations */}
      {skillsRecommendations.certification_recommendations && 
       skillsRecommendations.certification_recommendations.length > 0 && (
        <div className="certifications-section">
          <h3 className="certifications-title">Recommended Certifications</h3>
          <div className="certifications-list">
            {skillsRecommendations.certification_recommendations.map((cert, index) => (
              <div 
                key={index} 
                className="certification-badge"
                style={{ animationDelay: `${index * 75}ms` }}
              >
                <span className="certification-icon" role="img" aria-label="certificate">🏆</span>
                <span className="certification-text">{cert}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default SkillsSection