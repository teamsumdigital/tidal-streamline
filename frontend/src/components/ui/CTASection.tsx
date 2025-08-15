import React from 'react'

interface CTAItem {
  id: string
  title: string
  description: string
  buttonText: string
  icon: string
  type: 'primary' | 'secondary' | 'outline'
  href?: string
  onClick?: () => void
  features?: string[]
  badge?: string
}

interface CTASectionProps {
  title?: string
  subtitle?: string
  ctaItems?: CTAItem[]
  className?: string
  isLoading?: boolean
  layout?: 'horizontal' | 'vertical' | 'grid'
}

export const CTASection: React.FC<CTASectionProps> = ({
  title = "Ready to Find Your Perfect Candidate?",
  subtitle = "Join hundreds of companies who've streamlined their hiring with Tidal",
  ctaItems,
  className = '',
  isLoading = false,
  layout = 'horizontal'
}) => {
  // Default CTA items following Tidal design patterns
  const defaultCTAItems: CTAItem[] = [
    {
      id: 'book-strategy-call',
      title: 'Book a Strategy Call',
      description: 'Get personalized hiring recommendations and meet pre-screened candidates who match your exact requirements.',
      buttonText: 'Schedule Free Call',
      icon: '📅',
      type: 'primary',
      features: [
        'Free 30-minute consultation',
        'Personalized hiring strategy',
        'Pre-screened candidate introductions',
        'No commitment required'
      ],
      badge: 'Most Popular'
    },
    {
      id: 'browse-candidates',
      title: 'Browse Our Talent Pool',
      description: 'Access our curated database of vetted candidates from the Philippines, Latin America, and other top regions.',
      buttonText: 'View Candidates',
      icon: '👥',
      type: 'secondary',
      features: [
        'Pre-vetted professionals',
        'Video interviews available',
        'Skills assessments included',
        'Multiple experience levels'
      ]
    },
    {
      id: 'get-custom-quote',
      title: 'Get a Custom Quote',
      description: 'Receive detailed pricing based on your specific role, region preferences, and hiring timeline.',
      buttonText: 'Get Quote',
      icon: '💰',
      type: 'outline',
      features: [
        'Transparent pricing',
        'Flexible engagement models',
        'Volume discounts available',
        'No hidden fees'
      ]
    }
  ]

  const ctas = ctaItems || defaultCTAItems.slice(0, layout === 'horizontal' ? 2 : 3)

  const getButtonClasses = (type: CTAItem['type']) => {
    switch (type) {
      case 'primary':
        return 'cta-button-primary'
      case 'secondary':
        return 'cta-button-secondary'
      case 'outline':
        return 'cta-button-outline'
      default:
        return 'cta-button-primary'
    }
  }

  const getLayoutClasses = () => {
    switch (layout) {
      case 'horizontal':
        return 'cta-layout-horizontal'
      case 'vertical':
        return 'cta-layout-vertical'
      case 'grid':
        return 'cta-layout-grid'
      default:
        return 'cta-layout-horizontal'
    }
  }

  if (isLoading) {
    return (
      <section className={`cta-section ${className}`}>
        <div className="cta-container">
          <div className="cta-header animate-pulse">
            <div className="cta-title-skeleton bg-gray-200 w-96 h-10 rounded mb-4"></div>
            <div className="cta-subtitle-skeleton bg-gray-200 w-80 h-6 rounded"></div>
          </div>
          
          <div className={`cta-content ${getLayoutClasses()}`}>
            {[1, 2].map((index) => (
              <div key={index} className="cta-card animate-pulse">
                <div className="cta-card-header">
                  <div className="cta-icon-skeleton bg-gray-200 w-16 h-16 rounded mb-4"></div>
                  <div className="cta-card-title-skeleton bg-gray-200 w-48 h-7 rounded mb-2"></div>
                  <div className="cta-card-description-skeleton bg-gray-200 w-full h-16 rounded mb-4"></div>
                </div>
                <div className="cta-button-skeleton bg-gray-200 w-full h-12 rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className={`cta-section ${className}`}>
      <div className="cta-container">
        <div className="cta-header">
          <h2 className="cta-title">{title}</h2>
          <p className="cta-subtitle">{subtitle}</p>
        </div>
        
        <div className={`cta-content ${getLayoutClasses()}`}>
          {ctas.map((cta, index) => (
            <div 
              key={cta.id}
              className={`cta-card ${cta.type === 'primary' ? 'cta-card-featured' : ''}`}
              style={{ animationDelay: `${index * 200}ms` }}
            >
              {cta.badge && (
                <div className="cta-badge">
                  <span className="cta-badge-text">{cta.badge}</span>
                </div>
              )}
              
              <div className="cta-card-header">
                <div className="cta-icon-container">
                  <span className="cta-icon" role="img" aria-label={cta.title}>
                    {cta.icon}
                  </span>
                </div>
                <h3 className="cta-card-title">{cta.title}</h3>
                <p className="cta-card-description">{cta.description}</p>
              </div>

              {cta.features && cta.features.length > 0 && (
                <div className="cta-features">
                  <ul className="cta-features-list">
                    {cta.features.slice(0, 4).map((feature, featureIndex) => (
                      <li 
                        key={featureIndex} 
                        className="cta-feature-item"
                        style={{ animationDelay: `${(index * 200) + (featureIndex * 100)}ms` }}
                      >
                        <span className="cta-feature-check" role="img" aria-label="included">✓</span>
                        <span className="cta-feature-text">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="cta-card-footer">
                <button 
                  className={`cta-button ${getButtonClasses(cta.type)}`}
                  onClick={() => {
                    if (cta.onClick) {
                      cta.onClick()
                    } else if (cta.href) {
                      window.open(cta.href, '_blank', 'noopener,noreferrer')
                    }
                  }}
                >
                  <span className="cta-button-icon" role="img" aria-label="action">
                    {cta.icon}
                  </span>
                  <span className="cta-button-text">{cta.buttonText}</span>
                  <span className="cta-button-arrow" role="img" aria-label="go">→</span>
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Trust Indicators */}
        <div className="cta-trust-section">
          <div className="cta-trust-content">
            <div className="cta-trust-stats">
              <div className="cta-trust-stat">
                <span className="cta-trust-number">500+</span>
                <span className="cta-trust-label">Companies Served</span>
              </div>
              <div className="cta-trust-stat">
                <span className="cta-trust-number">95%</span>
                <span className="cta-trust-label">Client Satisfaction</span>
              </div>
              <div className="cta-trust-stat">
                <span className="cta-trust-number">60%</span>
                <span className="cta-trust-label">Average Savings</span>
              </div>
            </div>
            
            <div className="cta-trust-badges">
              <div className="cta-trust-badge">
                <span role="img" aria-label="security">🔒</span>
                <span>SOC 2 Compliant</span>
              </div>
              <div className="cta-trust-badge">
                <span role="img" aria-label="guarantee">💯</span>
                <span>30-Day Guarantee</span>
              </div>
              <div className="cta-trust-badge">
                <span role="img" aria-label="support">🚀</span>
                <span>24/7 Support</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default CTASection