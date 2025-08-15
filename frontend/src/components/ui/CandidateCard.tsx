import React from 'react'
import { CandidateProfile } from '../../services/types'

interface CandidateCardProps {
  candidate: CandidateProfile
  onContactClick: (candidate: CandidateProfile) => void
  regionalSavings?: number
  isLoading?: boolean
  className?: string
}

export const CandidateCard: React.FC<CandidateCardProps> = ({
  candidate,
  onContactClick,
  regionalSavings,
  isLoading = false,
  className = ''
}) => {
  const handleContactClick = () => {
    onContactClick(candidate)
  }

  const handleVideoClick = () => {
    if (candidate.video_url) {
      window.open(candidate.video_url, '_blank', 'noopener,noreferrer')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent, action: () => void) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      action()
    }
  }

  const formatHourlyRate = (rate: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(rate)
  }

  const formatRegionalSavings = (savings: number): string => {
    return `${savings}% savings vs US rates`
  }

  if (isLoading) {
    return (
      <div className={`card animate-pulse ${className}`} role="status" aria-label="Loading candidate">
        <div className="space-y-4">
          <div className="flex items-start justify-between">
            <div className="space-y-2 flex-1">
              <div className="h-6 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
            </div>
            <div className="h-10 bg-gray-200 rounded w-20"></div>
          </div>
          <div className="space-y-2">
            <div className="h-4 bg-gray-200 rounded w-1/4"></div>
            <div className="flex flex-wrap gap-2">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-6 bg-gray-200 rounded-full w-16"></div>
              ))}
            </div>
          </div>
          <div className="flex items-center justify-between pt-4 border-t border-gray-200">
            <div className="space-y-1">
              <div className="h-4 bg-gray-200 rounded w-20"></div>
              <div className="h-3 bg-gray-200 rounded w-24"></div>
            </div>
            <div className="h-10 bg-gray-200 rounded w-24"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`card hover:shadow-md transition-all duration-200 ${className}`}>
      {/* Header Section */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 truncate">
            {candidate.name}
          </h3>
          <p className="text-sm font-medium text-tidal-600 mt-1">
            {candidate.role_category}
          </p>
          <div className="flex items-center gap-4 mt-2 text-sm text-gray-600">
            <span className="flex items-center gap-1">
              <svg 
                className="w-4 h-4" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" 
                />
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" 
                />
              </svg>
              <span>{candidate.region}</span>
            </span>
            <span className="flex items-center gap-1">
              <svg 
                className="w-4 h-4" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" 
                />
              </svg>
              <span>{candidate.experience_years} experience</span>
            </span>
          </div>
        </div>

        {/* Video Introduction Link */}
        {candidate.video_url && (
          <button
            onClick={handleVideoClick}
            onKeyDown={(e) => handleKeyPress(e, handleVideoClick)}
            className="btn-outline text-xs px-3 py-1 flex items-center gap-1 ml-4 shrink-0"
            aria-label={`Watch ${candidate.name}'s video introduction`}
            title="Watch video introduction"
          >
            <svg 
              className="w-3 h-3" 
              fill="currentColor" 
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M8 5v14l11-7z"/>
            </svg>
            <span className="hidden sm:inline">Video</span>
          </button>
        )}
      </div>

      {/* Bio Section */}
      <div className="mb-4">
        <p className="text-sm text-gray-700 line-clamp-3 leading-relaxed">
          {candidate.bio}
        </p>
      </div>

      {/* Skills Section */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Skills</h4>
        <div className="flex flex-wrap gap-2">
          {candidate.skills.slice(0, 6).map((skill, index) => (
            <span 
              key={`${skill}-${index}`}
              className="badge badge-primary text-xs"
            >
              {skill}
            </span>
          ))}
          {candidate.skills.length > 6 && (
            <span className="badge bg-gray-100 text-gray-600 text-xs">
              +{candidate.skills.length - 6} more
            </span>
          )}
        </div>
      </div>

      {/* Footer Section */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <div className="space-y-1">
          {candidate.hourly_rate && (
            <div className="text-lg font-semibold text-gray-900">
              {formatHourlyRate(candidate.hourly_rate)}/hr
            </div>
          )}
          {regionalSavings && regionalSavings > 0 && (
            <div className="text-xs text-green-600 font-medium">
              {formatRegionalSavings(regionalSavings)}
            </div>
          )}
          {!candidate.hourly_rate && !regionalSavings && (
            <div className="text-sm text-gray-500">
              Rate upon inquiry
            </div>
          )}
        </div>

        <button
          onClick={handleContactClick}
          onKeyDown={(e) => handleKeyPress(e, handleContactClick)}
          className="btn-primary text-sm px-4 py-2 flex items-center gap-2"
          aria-label={`Contact ${candidate.name}`}
        >
          <svg 
            className="w-4 h-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" 
            />
          </svg>
          <span>Contact</span>
        </button>
      </div>

      {/* Additional Info Badges */}
      <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-gray-100">
        {candidate.english_proficiency && (
          <span className="badge bg-blue-50 text-blue-700 text-xs">
            {candidate.english_proficiency} English
          </span>
        )}
        {candidate.timezone && (
          <span className="badge bg-purple-50 text-purple-700 text-xs">
            {candidate.timezone}
          </span>
        )}
        {candidate.availability && (
          <span className="badge bg-green-50 text-green-700 text-xs">
            {candidate.availability}
          </span>
        )}
      </div>
    </div>
  )
}

export default CandidateCard