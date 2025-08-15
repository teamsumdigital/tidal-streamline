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
  jobTitle?: string
  className?: string
  isLoading?: boolean
}

export const NextStepsSection: React.FC<NextStepsSectionProps> = ({
  jobTitle = '',
  className = '',
  isLoading = false
}) => {
  if (isLoading) {
    return (
      <div className={`bg-white rounded-xl shadow-sm border border-[#E5E5E7] p-8 ${className}`}>
        <div className="animate-pulse space-y-6">
          <div className="w-48 h-6 bg-gray-200 rounded"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((index) => (
              <div key={index} className="w-full h-32 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-[#E5E5E7] p-8 ${className}`}>
      {/* Numbered Steps */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Step 1: Book Strategy Call */}
        <div className="relative">
          <div className="absolute -top-3 -left-3 w-8 h-8 bg-[#7B61FF] text-white rounded-full flex items-center justify-center text-sm font-bold">
            1
          </div>
          <div className="bg-[#7B61FF]/5 border border-[#7B61FF]/20 rounded-lg p-6">
            <h3 className="font-semibold text-[#1A1A1A] mb-2">Book Strategy Call</h3>
            <p className="text-sm text-[#555555] mb-4">
              Schedule a 15-minute call to see qualified {jobTitle} candidates.
            </p>
            <a 
              href={`mailto:connect@hiretidal.com?subject=Strategy Call - ${jobTitle}&body=Hi! I'd like to schedule a call to discuss hiring for the ${jobTitle} role and see qualified candidates.`}
              className="inline-flex items-center justify-center w-full bg-[#7B61FF] text-white font-medium px-4 py-2 rounded-lg hover:bg-[#6B51E5] transition-colors text-sm"
            >
              Book Call
              <span className="ml-2">→</span>
            </a>
          </div>
        </div>

        {/* Step 2: Share Report */}
        <div className="relative">
          <div className="absolute -top-3 -left-3 w-8 h-8 bg-[#00C6A2] text-white rounded-full flex items-center justify-center text-sm font-bold">
            2
          </div>
          <div className="bg-[#00C6A2]/5 border border-[#00C6A2]/20 rounded-lg p-6">
            <h3 className="font-semibold text-[#1A1A1A] mb-2">Share This Report</h3>
            <p className="text-sm text-[#555555] mb-4">
              Forward these insights to your team for review and decision-making.
            </p>
            <button 
              onClick={() => {
                if (navigator.share) {
                  navigator.share({
                    title: `${jobTitle} Hiring Insights - Tidal`,
                    text: 'Check out these hiring insights from Tidal',
                    url: window.location.href
                  })
                } else {
                  navigator.clipboard.writeText(window.location.href)
                  alert('Link copied to clipboard!')
                }
              }}
              className="inline-flex items-center justify-center w-full bg-white border border-[#00C6A2] text-[#00C6A2] font-medium px-4 py-2 rounded-lg hover:bg-[#00C6A2]/5 transition-colors text-sm"
            >
              Share Report
              <span className="ml-2">↗</span>
            </button>
          </div>
        </div>

        {/* Step 3: Explore More Roles */}
        <div className="relative">
          <div className="absolute -top-3 -left-3 w-8 h-8 bg-[#555555] text-white rounded-full flex items-center justify-center text-sm font-bold">
            3
          </div>
          <div className="bg-[#F7F7F9] border border-[#E5E5E7] rounded-lg p-6">
            <h3 className="font-semibold text-[#1A1A1A] mb-2">Explore Other Roles</h3>
            <p className="text-sm text-[#555555] mb-4">
              Run additional market scans for other positions you need to fill.
            </p>
            <a 
              href="/"
              className="inline-flex items-center justify-center w-full bg-white border border-[#E5E5E7] text-[#555555] font-medium px-4 py-2 rounded-lg hover:bg-[#F7F7F9] transition-colors text-sm"
            >
              New Scan
              <span className="ml-2">+</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default NextStepsSection