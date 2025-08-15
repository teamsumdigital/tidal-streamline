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
        return `$${Math.round(amount / 1000)}k`
      }
      return `$${amount.toLocaleString()}`
    }

    return `${formatCurrency(low)} - ${formatCurrency(high)}`
  }

  const getSavingsLabel = (savingsPercent: number): string => {
    return `${savingsPercent}% savings vs US`
  }

  if (isLoading) {
    return (
      <section className={`bg-white rounded-xl shadow-sm border border-[#E5E5E7] p-8 mb-8 ${className}`}>
        <div className="mb-8">
          <div className="w-64 h-8 bg-gray-200 rounded animate-pulse mb-2"></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map((index) => (
            <div key={index} className="bg-white rounded-xl border border-[#E5E5E7] p-6 animate-pulse">
              <div className="flex items-center justify-between mb-6">
                <div className="w-12 h-12 bg-gray-200 rounded-full"></div>
                <div className="w-24 h-6 bg-gray-200 rounded-full"></div>
              </div>
              <div className="space-y-4">
                <div className="w-32 h-6 bg-gray-200 rounded"></div>
                <div className="w-28 h-8 bg-gray-200 rounded"></div>
                <div className="w-full h-4 bg-gray-200 rounded"></div>
              </div>
            </div>
          ))}
        </div>
      </section>
    )
  }

  return (
    <section className={`bg-white rounded-xl shadow-sm border border-[#E5E5E7] p-8 mb-8 ${className}`}>
      {/* Section Header */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-[#1A1A1A] font-sans">Regional Pay Ranges</h2>
      </div>
      
      {/* Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {regionData.map((data, index) => (
          <div 
            key={data.region} 
            className="bg-white rounded-xl border border-[#E5E5E7] p-6 hover:shadow-md transition-all duration-300 group relative"
          >
            {/* Header with Flag and Savings - Consistent Position */}
            <div className="flex items-center justify-between mb-6">
              <div className="w-12 h-12 bg-[#F7F7F9] rounded-full flex items-center justify-center">
                <span className="text-2xl" role="img" aria-label={`${data.region} flag`}>
                  {data.flag}
                </span>
              </div>
              
              {/* Savings Badge - Always in same position */}
              <div className="h-7 flex items-center">
                {data.savingsPercent ? (
                  <div className="bg-[#00C6A2]/10 px-3 py-1 rounded-full flex items-center gap-1">
                    <span className="text-sm" role="img" aria-label="savings">👋</span>
                    <span className="text-[#00C6A2] text-sm font-medium">{data.savingsPercent}% savings</span>
                  </div>
                ) : (
                  <div className="bg-[#7B61FF]/10 px-3 py-1 rounded-full">
                    <span className="text-[#7B61FF] text-sm font-medium">Baseline</span>
                  </div>
                )}
              </div>
            </div>

            {/* Card Content */}
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-[#1A1A1A] font-sans">{data.region}</h3>
              <div className="space-y-1">
                <div className="text-3xl font-bold text-[#1A1A1A]">
                  {formatSalaryRange(data.payRange)}
                  <span className="text-sm font-normal text-[#555555] ml-1">/hour</span>
                </div>
              </div>
              <p className="text-[#555555] text-sm leading-relaxed">{data.description}</p>
              
              {/* Info Tooltip */}
              <div className="pt-2">
                <div className="group/tooltip relative inline-block">
                  <button className="text-[#7B61FF] text-xs font-medium hover:text-[#6B51E5] transition-colors">
                    Why choose this region? ℹ️
                  </button>
                  <div className="absolute bottom-full left-0 mb-2 hidden group-hover/tooltip:block bg-[#1A1A1A] text-white text-xs rounded-lg p-3 w-64 z-10">
                    {data.region === 'United States' && 'Same timezone, native English speakers, direct market knowledge. Best for complex roles requiring deep cultural understanding.'}
                    {data.region === 'Latin America' && 'Similar timezones to US, high English proficiency, strong work ethic. Great balance of cost savings and communication ease.'}
                    {data.region === 'Philippines' && 'Excellent English skills, cultural alignment with US business practices, tech-savvy workforce. Maximum cost savings without sacrificing quality.'}
                    <div className="absolute top-full left-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-[#1A1A1A]"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

export default RegionCards