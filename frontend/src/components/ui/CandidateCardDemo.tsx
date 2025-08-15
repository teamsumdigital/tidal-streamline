import React, { useState } from 'react'
import { CandidateCard } from './CandidateCard'
import { CandidateProfile } from '../../services/types'

// Demo data for testing the component
const mockCandidates: CandidateProfile[] = [
  {
    id: '1',
    name: 'Maria Santos',
    role_category: 'Ecommerce Manager',
    experience_years: '5-7 years',
    region: 'Philippines',
    skills: ['Shopify', 'Google Ads', 'Facebook Ads', 'Email Marketing', 'Analytics', 'Conversion Optimization', 'SEO', 'PPC'],
    bio: 'Experienced ecommerce manager with 6+ years driving online sales growth for D2C brands. Specialized in Shopify optimization, paid advertising campaigns, and data-driven conversion improvements. Led teams that increased revenue by 150% year-over-year.',
    video_url: 'https://example.com/video1',
    resume_url: 'https://example.com/resume1',
    portfolio_url: 'https://example.com/portfolio1',
    hourly_rate: 25,
    availability: 'Full-time',
    english_proficiency: 'Fluent',
    timezone: 'GMT+8'
  },
  {
    id: '2',
    name: 'Carlos Rodriguez',
    role_category: 'Data Analyst',
    experience_years: '3-5 years',
    region: 'Latin America',
    skills: ['Python', 'SQL', 'Tableau', 'Google Analytics', 'Excel', 'Power BI'],
    bio: 'Detail-oriented data analyst with expertise in e-commerce analytics and business intelligence. Proven track record of identifying growth opportunities through data visualization and statistical analysis.',
    video_url: 'https://example.com/video2',
    hourly_rate: 22,
    availability: 'Full-time',
    english_proficiency: 'Advanced',
    timezone: 'GMT-5'
  },
  {
    id: '3',
    name: 'Thandiwe Mbeki',
    role_category: 'Community Manager',
    experience_years: '2-4 years',
    region: 'South Africa',
    skills: ['Social Media', 'Content Creation', 'Brand Management', 'Customer Service', 'Engagement Strategy'],
    bio: 'Creative community manager passionate about building authentic brand relationships. Expert in social media strategy, content creation, and community engagement across multiple platforms.',
    hourly_rate: 18,
    availability: 'Part-time',
    english_proficiency: 'Native',
    timezone: 'GMT+2'
  }
]

export const CandidateCardDemo: React.FC = () => {
  const [selectedCandidate, setSelectedCandidate] = useState<CandidateProfile | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleContactClick = (candidate: CandidateProfile) => {
    setSelectedCandidate(candidate)
    // In a real app, this would open a contact modal or navigate to a contact page
    console.log('Contact clicked for:', candidate.name)
  }

  const handleLoadingDemo = () => {
    setIsLoading(true)
    setTimeout(() => {
      setIsLoading(false)
    }, 2000)
  }

  const calculateRegionalSavings = (region: string): number => {
    // Mock savings calculation based on region
    const savingsMap: Record<string, number> = {
      'Philippines': 65,
      'Latin America': 55,
      'South Africa': 60,
      'United States': 0
    }
    return savingsMap[region] || 0
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-bold text-gray-900">CandidateCard Component Demo</h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          This demo showcases the CandidateCard component with various states and configurations.
          The component follows Tidal's design system and includes accessibility features.
        </p>
        
        <div className="flex justify-center gap-4">
          <button
            onClick={handleLoadingDemo}
            className="btn-secondary"
          >
            Demo Loading State
          </button>
        </div>
      </div>

      {/* Loading State Demo */}
      {isLoading && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900">Loading State</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <CandidateCard
                key={i}
                candidate={{} as CandidateProfile}
                onContactClick={() => {}}
                isLoading={true}
              />
            ))}
          </div>
        </div>
      )}

      {/* Regular Candidates Grid */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Candidate Profiles</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockCandidates.map((candidate) => (
            <CandidateCard
              key={candidate.id}
              candidate={candidate}
              onContactClick={handleContactClick}
              regionalSavings={calculateRegionalSavings(candidate.region)}
            />
          ))}
        </div>
      </div>

      {/* Single Card Variations */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Component Variations</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Without video link */}
          <div className="space-y-2">
            <h3 className="text-sm font-medium text-gray-700">Without Video Link</h3>
            <CandidateCard
              candidate={{
                ...mockCandidates[0],
                video_url: undefined
              }}
              onContactClick={handleContactClick}
              regionalSavings={65}
            />
          </div>

          {/* Without hourly rate */}
          <div className="space-y-2">
            <h3 className="text-sm font-medium text-gray-700">Rate Upon Inquiry</h3>
            <CandidateCard
              candidate={{
                ...mockCandidates[1],
                hourly_rate: undefined
              }}
              onContactClick={handleContactClick}
            />
          </div>
        </div>
      </div>

      {/* Selected Candidate Display */}
      {selectedCandidate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">Contact Request</h3>
            <p className="text-gray-600 mb-4">
              You clicked contact for <strong>{selectedCandidate.name}</strong> ({selectedCandidate.role_category}).
            </p>
            <p className="text-sm text-gray-500 mb-4">
              In a real application, this would open a contact form or initiate the hiring process.
            </p>
            <button
              onClick={() => setSelectedCandidate(null)}
              className="btn-primary w-full"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Implementation Notes */}
      <div className="bg-gray-50 rounded-lg p-6 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Implementation Features</h2>
        <ul className="space-y-2 text-sm text-gray-700">
          <li className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span><strong>Accessibility:</strong> Proper ARIA labels, keyboard navigation, and semantic HTML</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span><strong>TypeScript:</strong> Fully typed with CandidateProfile interface</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span><strong>Responsive Design:</strong> Mobile-first approach with responsive breakpoints</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span><strong>Loading States:</strong> Skeleton loading animation</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span><strong>Brand Consistency:</strong> Uses Tidal color palette and design tokens</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span><strong>Atomic Design:</strong> Follows single responsibility principle</span>
          </li>
        </ul>
      </div>
    </div>
  )
}

export default CandidateCardDemo