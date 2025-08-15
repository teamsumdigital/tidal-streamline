import React from 'react'
import { SalaryRange, Region } from '../../services/types'

interface RegionCardData {
  region: Region
  payRange: SalaryRange
  savingsPercent?: number
  flag: string
  description: string
}

interface RegionCardsProps {
  salaryRecommendations?: Record<string, SalaryRange>
  className?: string
  isLoading?: boolean
}

export const RegionCards: React.FC<RegionCardsProps> = ({
  salaryRecommendations,
  className = '',
  isLoading = false
}) => {
  // Default pay range data based on PRD requirements
  const defaultRegionData: RegionCardData[] = [
    {
      region: 'United States',
      payRange: {
        low: 85000,
        mid: 110000,
        high: 140000,
        currency: 'USD',
        period: 'annual'
      },
      flag: '🇺🇸',
      description: 'Premium US talent for complex roles'
    },
    {
      region: 'Latin America',
      payRange: {
        low: 35000,
        mid: 50000,
        high: 65000,
        currency: 'USD',
        period: 'annual'
      },
      savingsPercent: 54,
      flag: '🇲🇽',
      description: 'Skilled professionals in your timezone'
    },
    {
      region: 'Philippines',
      payRange: {
        low: 18000,
        mid: 32000,
        high: 45000,
        currency: 'USD',
        period: 'annual'
      },
      savingsPercent: 71,
      flag: '🇵🇭',
      description: 'Exceptional value with English fluency'
    }
  ]

  // Merge salary recommendations with default data
  const regionData = defaultRegionData.map(region => {
    const recommendedSalary = salaryRecommendations?.[region.region]
    return recommendedSalary ? { ...region, payRange: recommendedSalary } : region
  })

  const formatSalaryRange = (payRange: SalaryRange): string => {
    const { low, high } = payRange
    
    const formatCurrency = (amount: number): string => {
      if (amount >= 1000) {
        return `${Math.round(amount / 1000)}k`
      }
      return amount.toLocaleString()
    }

    return `$${formatCurrency(low)} - $${formatCurrency(high)}`
  }

  const getSavingsLabel = (savingsPercent: number): string => {
    return `${savingsPercent}% savings vs US`
  }

  if (isLoading) {
    return (
      <div className={`region-cards-container ${className}`}>
        <div className="region-cards-grid">
          {[1, 2, 3].map((index) => (
            <div key={index} className="region-card animate-pulse">
              <div className="region-card-header">
                <div className="region-flag-container skeleton">
                  <div className="region-flag-circle bg-gray-200"></div>
                </div>
                <div className="savings-badge-skeleton bg-gray-200 w-24 h-6 rounded-full"></div>
              </div>
              <div className="region-card-content">
                <div className="region-title-skeleton bg-gray-200 w-32 h-6 rounded mb-2"></div>
                <div className="salary-range-skeleton bg-gray-200 w-28 h-8 rounded mb-3"></div>
                <div className="description-skeleton bg-gray-200 w-full h-4 rounded"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className={`region-cards-container ${className}`}>
      <div className="region-cards-grid">
        {regionData.map((data, index) => (
          <div 
            key={data.region} 
            className="region-card group"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            {/* Header with Flag and Savings */}
            <div className="region-card-header">
              <div className="region-flag-container">
                <div className="region-flag-circle">
                  <span className="region-flag-emoji" role="img" aria-label={`${data.region} flag`}>
                    {data.flag}
                  </span>
                </div>
              </div>
              
              {data.savingsPercent && (
                <div className="savings-badge" aria-label={getSavingsLabel(data.savingsPercent)}>
                  <span className="savings-emoji" role="img" aria-label="savings">👋</span>
                  <span className="savings-text">{data.savingsPercent}% savings</span>
                </div>
              )}
            </div>

            {/* Card Content */}
            <div className="region-card-content">
              <h3 className="region-title">{data.region}</h3>
              <div className="salary-range">
                {formatSalaryRange(data.payRange)}
                <span className="salary-period">/{data.payRange.period === 'annual' ? 'year' : 'hour'}</span>
              </div>
              <p className="region-description">{data.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default RegionCards