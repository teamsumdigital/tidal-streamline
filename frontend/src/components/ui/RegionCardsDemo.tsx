import React, { useState } from 'react'
import { RegionCards } from './RegionCards'
import { SalaryRange } from '../../services/types'

/**
 * Demo component showcasing the RegionCards component
 * following exact Tidal PRD design system requirements
 */
export const RegionCardsDemo: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false)
  
  // Sample salary data following the API structure
  const sampleSalaryData: Record<string, SalaryRange> = {
    'United States': {
      low: 85000,
      mid: 110000,
      high: 140000,
      currency: 'USD',
      period: 'annual'
    },
    'Latin America': {
      low: 35000,
      mid: 50000,
      high: 65000,
      currency: 'USD',
      period: 'annual',
      savings_vs_us: 54
    },
    'Philippines': {
      low: 18000,
      mid: 32000,
      high: 45000,
      currency: 'USD', 
      period: 'annual',
      savings_vs_us: 71
    }
  }

  const toggleLoading = () => {
    setIsLoading(!isLoading)
  }

  return (
    <div className="min-h-screen bg-light-gray-bg py-16">
      <div className="max-w-7xl mx-auto px-6">
        {/* Demo Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-dark-navy-text mb-4">
            RegionCards Component Demo
          </h1>
          <p className="text-lg text-medium-gray-text mb-8 max-w-3xl mx-auto">
            Showcasing the new RegionCards component following the exact Tidal PRD design system. 
            Features responsive breakpoints, exact brand colors, circular flags with glow effects, 
            and savings percentage pill labels.
          </p>
          
          {/* Demo Controls */}
          <div className="flex justify-center gap-4 mb-12">
            <button 
              onClick={toggleLoading}
              className="btn-primary"
            >
              {isLoading ? 'Hide Loading State' : 'Show Loading State'}
            </button>
          </div>
        </div>

        {/* Design System Showcase */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-dark-navy-text mb-8 text-center">
            Regional Pay Ranges
          </h2>
          
          <RegionCards 
            salaryRecommendations={sampleSalaryData}
            isLoading={isLoading}
            className="mb-12"
          />
        </div>

        {/* Features Highlight */}
        <div className="bg-white rounded-xl shadow-sm border border-card-border-gray p-8 mb-12">
          <h3 className="text-xl font-bold text-dark-navy-text mb-6">PRD Requirements Implemented</h3>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-tidal-purple/10 rounded-lg flex items-center justify-center shrink-0">
                <span className="text-tidal-purple">📱</span>
              </div>
              <div>
                <h4 className="font-semibold text-dark-navy-text mb-1">Responsive Design</h4>
                <p className="text-sm text-medium-gray-text">
                  Desktop: 3 cards horizontal, Tablet: 2+1 layout, Mobile: Stacked
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-tidal-aqua/10 rounded-lg flex items-center justify-center shrink-0">
                <span className="text-tidal-aqua">🎨</span>
              </div>
              <div>
                <h4 className="font-semibold text-dark-navy-text mb-1">Exact Brand Colors</h4>
                <p className="text-sm text-medium-gray-text">
                  Tidal Purple (#7B61FF), Tidal Aqua (#00C6A2), exact PRD palette
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-success-green/10 rounded-lg flex items-center justify-center shrink-0">
                <span className="text-success-green">💡</span>
              </div>
              <div>
                <h4 className="font-semibold text-dark-navy-text mb-1">Savings Pills</h4>
                <p className="text-sm text-medium-gray-text">
                  Green pill labels with 👋 emoji showing cost savings vs US
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-gradient-to-r from-tidal-purple/20 to-tidal-aqua/20 rounded-lg flex items-center justify-center shrink-0">
                <span>🌟</span>
              </div>
              <div>
                <h4 className="font-semibold text-dark-navy-text mb-1">Circular Flags</h4>
                <p className="text-sm text-medium-gray-text">
                  Glow effects on hover, country flags with proper accessibility
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-dark-navy-text/10 rounded-lg flex items-center justify-center shrink-0">
                <span>⚡</span>
              </div>
              <div>
                <h4 className="font-semibold text-dark-navy-text mb-1">Animations</h4>
                <p className="text-sm text-medium-gray-text">
                  Smooth slide-in animations, hover states, scale transforms
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-medium-gray-text/10 rounded-lg flex items-center justify-center shrink-0">
                <span>♿</span>
              </div>
              <div>
                <h4 className="font-semibold text-dark-navy-text mb-1">Accessibility</h4>
                <p className="text-sm text-medium-gray-text">
                  ARIA labels, semantic HTML, keyboard navigation support
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Responsive Breakpoints Info */}
        <div className="bg-white rounded-xl shadow-sm border border-card-border-gray p-8">
          <h3 className="text-xl font-bold text-dark-navy-text mb-6">Responsive Breakpoints</h3>
          
          <div className="grid sm:grid-cols-3 gap-6">
            <div className="text-center p-4 bg-light-gray-bg rounded-lg">
              <h4 className="font-semibold text-dark-navy-text mb-2">Desktop</h4>
              <p className="text-2xl font-bold text-tidal-purple mb-1">1200px+</p>
              <p className="text-sm text-medium-gray-text">All 3 cards horizontal</p>
            </div>
            
            <div className="text-center p-4 bg-light-gray-bg rounded-lg">
              <h4 className="font-semibold text-dark-navy-text mb-2">Tablet</h4>
              <p className="text-2xl font-bold text-tidal-purple mb-1">768-1199px</p>
              <p className="text-sm text-medium-gray-text">2 cards + 1 card layout</p>
            </div>
            
            <div className="text-center p-4 bg-light-gray-bg rounded-lg">
              <h4 className="font-semibold text-dark-navy-text mb-2">Mobile</h4>
              <p className="text-2xl font-bold text-tidal-purple mb-1">&lt;768px</p>
              <p className="text-sm text-medium-gray-text">Stacked vertically</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RegionCardsDemo