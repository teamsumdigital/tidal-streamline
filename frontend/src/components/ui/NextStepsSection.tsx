import React from 'react'

interface NextStep {
  id: string
  title: string
  description: string
  icon: string
  actionText?: string
  priority: 'high' | 'medium' | 'low'
  timeframe?: string
}

interface NextStepsSectionProps {
  customSteps?: NextStep[]
  className?: string
  isLoading?: boolean
  onContactTidal?: () => void
  onBookCall?: () => void
}

export const NextStepsSection: React.FC<NextStepsSectionProps> = ({
  customSteps,
  className = '',
  isLoading = false,
  onContactTidal,
  onBookCall
}) => {
  // Default next steps following Tidal design patterns
  const defaultSteps: NextStep[] = [
    {
      id: 'refine-requirements',
      title: 'Refine Your Job Requirements',
      description: 'Review the skills analysis and adjust your job posting to attract the right candidates. Focus on must-have vs nice-to-have skills.',
      icon: '📝',
      actionText: 'Download JD Template',
      priority: 'high',
      timeframe: '15 minutes'
    },
    {
      id: 'choose-region',
      title: 'Select Your Preferred Region',
      description: 'Based on the salary analysis, decide which region aligns best with your budget and quality requirements.',
      icon: '🗺️',
      actionText: 'View Region Details',
      priority: 'high',
      timeframe: '10 minutes'
    },
    {
      id: 'connect-with-tidal',
      title: 'Connect with Tidal',
      description: 'Schedule a strategy call to discuss your specific needs and get personalized candidate recommendations.',
      icon: '🤝',
      actionText: 'Book Strategy Call',
      priority: 'medium',
      timeframe: '30 minutes'
    },
    {
      id: 'review-candidates',
      title: 'Review Pre-Screened Candidates',
      description: 'Access our curated talent pool of candidates who match your role requirements and budget.',
      icon: '👥',
      actionText: 'Browse Candidates',
      priority: 'medium',
      timeframe: 'Ongoing'
    }
  ]

  const steps = customSteps || defaultSteps

  const getPriorityStyles = (priority: 'high' | 'medium' | 'low') => {
    switch (priority) {
      case 'high': return 'border-tidal-purple bg-tidal-purple/5'
      case 'medium': return 'border-tidal-aqua bg-tidal-aqua/5'
      case 'low': return 'border-gray-300 bg-gray-50'
      default: return 'border-gray-300 bg-gray-50'
    }
  }

  const getPriorityIcon = (priority: 'high' | 'medium' | 'low') => {
    switch (priority) {
      case 'high': return '🚀'
      case 'medium': return '⭐'
      case 'low': return '💡'
      default: return '💡'
    }
  }

  if (isLoading) {
    return (
      <section className={`next-steps-section ${className}`}>
        <div className="next-steps-container">
          <div className="next-steps-header animate-pulse">
            <div className="next-steps-title-skeleton bg-gray-200 w-48 h-8 rounded mb-3"></div>
            <div className="next-steps-subtitle-skeleton bg-gray-200 w-80 h-5 rounded"></div>
          </div>
          
          <div className="next-steps-content">
            <div className="steps-grid">
              {[1, 2, 3, 4].map((index) => (
                <div key={index} className="step-card animate-pulse">
                  <div className="step-header">
                    <div className="step-icon-skeleton bg-gray-200 w-12 h-12 rounded"></div>
                    <div className="step-priority-skeleton bg-gray-200 w-16 h-5 rounded-full"></div>
                  </div>
                  <div className="step-content">
                    <div className="step-title-skeleton bg-gray-200 w-40 h-6 rounded mb-2"></div>
                    <div className="step-description-skeleton bg-gray-200 w-full h-16 rounded mb-3"></div>
                    <div className="step-action-skeleton bg-gray-200 w-32 h-8 rounded"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className={`next-steps-section ${className}`}>
      <div className="next-steps-container">
        <div className="next-steps-header">
          <h2 className="next-steps-title">Your Next Steps</h2>
          <p className="next-steps-subtitle">
            Ready to find your perfect candidate? Here's how to get started.
          </p>
        </div>
        
        <div className="next-steps-content">
          <div className="steps-grid">
            {steps.map((step, index) => (
              <div 
                key={step.id}
                className={`step-card ${getPriorityStyles(step.priority)}`}
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <div className="step-header">
                  <div className="step-icon-container">
                    <span className="step-icon" role="img" aria-label={step.title}>
                      {step.icon}
                    </span>
                  </div>
                  <div className="step-meta">
                    <span className="step-priority">
                      <span role="img" aria-label="priority">{getPriorityIcon(step.priority)}</span>
                      {step.priority.charAt(0).toUpperCase() + step.priority.slice(1)} Priority
                    </span>
                    {step.timeframe && (
                      <span className="step-timeframe">
                        <span role="img" aria-label="time">⏱️</span>
                        {step.timeframe}
                      </span>
                    )}
                  </div>
                </div>

                <div className="step-content">
                  <h3 className="step-title">{step.title}</h3>
                  <p className="step-description">{step.description}</p>
                  
                  {step.actionText && (
                    <button 
                      className="step-action-button"
                      onClick={() => {
                        if (step.id === 'connect-with-tidal' && onBookCall) {
                          onBookCall()
                        } else if (onContactTidal) {
                          onContactTidal()
                        }
                      }}
                    >
                      <span className="step-action-text">{step.actionText}</span>
                      <span className="step-action-arrow" role="img" aria-label="go">→</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Contact Section */}
          <div className="contact-section">
            <div className="contact-card">
              <div className="contact-icon">
                <span role="img" aria-label="contact">💬</span>
              </div>
              <div className="contact-content">
                <h3 className="contact-title">Need Personalized Guidance?</h3>
                <p className="contact-description">
                  Our team can help you navigate the hiring process and find the perfect candidate for your specific needs.
                </p>
                <div className="contact-actions">
                  <button 
                    className="contact-primary-button"
                    onClick={onBookCall}
                  >
                    <span>📅</span>
                    Book Strategy Call
                  </button>
                  <button 
                    className="contact-secondary-button"
                    onClick={onContactTidal}
                  >
                    <span>✉️</span>
                    Send Message
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default NextStepsSection