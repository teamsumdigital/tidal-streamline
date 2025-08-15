import React, { useState } from 'react'
import { RegionCards } from './RegionCards'
import { SkillsSection } from './SkillsSection'
import { JobAnalysisSection } from './JobAnalysisSection'
import { NextStepsSection } from './NextStepsSection'
import { CTASection } from './CTASection'
import { SalaryRange, SkillsRecommendation, JobAnalysis } from '../../services/types'

/**
 * Demo component showcasing the complete MarketScanResults page components
 * following exact Tidal PRD design system requirements and section hierarchy
 */
export const MarketScanResultsDemo: React.FC = () => {
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

  // Sample skills data
  const sampleSkillsData: SkillsRecommendation = {
    must_have_skills: [
      'Digital Marketing Strategy',
      'Google Analytics',
      'Facebook Ads Manager',
      'Email Marketing',
      'Data Analysis',
      'Campaign Optimization',
      'A/B Testing'
    ],
    nice_to_have_skills: [
      'Shopify Plus',
      'Klaviyo',
      'TikTok Ads',
      'Influencer Marketing',
      'Video Production',
      'SEO/SEM',
      'Marketing Automation',
      'Customer Segmentation'
    ],
    skill_categories: {
      'Advertising Platforms': ['Facebook Ads', 'Google Ads', 'TikTok Ads'],
      'Analytics Tools': ['Google Analytics', 'Mixpanel', 'Hotjar'],
      'Marketing Automation': ['Klaviyo', 'Mailchimp', 'HubSpot']
    },
    certification_recommendations: [
      'Google Analytics Certified',
      'Facebook Blueprint Certified',
      'Google Ads Certified',
      'HubSpot Content Marketing Certified'
    ]
  }

  // Sample job analysis data
  const sampleJobAnalysis: JobAnalysis = {
    role_category: 'Brand Marketing Manager',
    experience_level: 'mid',
    years_experience_required: '3-5 years',
    must_have_skills: ['Digital Marketing', 'Brand Strategy', 'Analytics'],
    nice_to_have_skills: ['Video Production', 'Influencer Marketing'],
    key_responsibilities: [
      'Develop and execute comprehensive brand marketing strategies across digital channels',
      'Manage multi-platform advertising campaigns with $50K+ monthly budgets',
      'Analyze campaign performance metrics and optimize for 4+ ROAS targets',
      'Collaborate with creative teams on brand content and visual identity',
      'Track brand awareness and sentiment metrics using advanced analytics tools',
      'Lead cross-functional projects with design, content, and product teams'
    ],
    remote_work_suitability: 'Highly suitable for remote work',
    complexity_score: 78,
    recommended_regions: ['Philippines', 'Latin America'],
    unique_challenges: 'Requires strong analytical skills combined with creative thinking and ability to manage large advertising budgets while maintaining brand consistency',
    salary_factors: [
      'Experience with premium ecommerce brands',
      'Proven track record with ROAS improvement (4.0+ preferred)',
      'Multi-platform advertising expertise (Facebook, Google, TikTok)',
      'Advanced analytics and attribution modeling experience',
      'Team leadership and project management skills'
    ]
  }

  const toggleLoading = () => {
    setIsLoading(!isLoading)
  }

  const handleBookCall = () => {
    alert('Book Strategy Call clicked - would open calendar widget')
  }

  const handleContactTidal = () => {
    alert('Contact Tidal clicked - would open contact form')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Demo Header */}
      <div className="bg-white border-b border-gray-200 py-8">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-dark-navy-text mb-4">
              Market Scan Results Demo
            </h1>
            <p className="text-lg text-medium-gray-text mb-8 max-w-3xl mx-auto">
              Complete MarketScanResults page showcase following Tidal PRD section hierarchy and design system. 
              Features responsive layouts, exact brand colors, smooth animations, and accessibility compliance.
            </p>
            
            {/* Demo Controls */}
            <div className="flex justify-center gap-4">
              <button 
                onClick={toggleLoading}
                className="btn-primary"
              >
                {isLoading ? 'Hide Loading States' : 'Show Loading States'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* PRD Section Hierarchy - STRICT ORDER */}
      
      {/* 1. Region Cards (Pay Ranges) - FIRST */}
      <section className="py-16 bg-light-gray-bg">
        <div className="max-w-7xl mx-auto px-6 mb-8">
          <h2 className="text-3xl font-bold text-dark-navy-text text-center mb-4">
            Regional Pay Ranges
          </h2>
          <p className="text-lg text-medium-gray-text text-center max-w-2xl mx-auto">
            Based on your Brand Marketing Manager role analysis, here are the recommended pay ranges by region.
          </p>
        </div>
        
        <RegionCards 
          salaryRecommendations={sampleSalaryData}
          isLoading={isLoading}
        />
      </section>

      {/* 2. Recommended Skills & Tools - SECOND */}
      <SkillsSection 
        skillsRecommendation={sampleSkillsData}
        isLoading={isLoading}
      />

      {/* 3. Job Analysis Summary - THIRD */}
      <JobAnalysisSection 
        jobAnalysis={sampleJobAnalysis}
        isLoading={isLoading}
      />

      {/* 4. Next Steps - FOURTH */}
      <NextStepsSection 
        isLoading={isLoading}
        onBookCall={handleBookCall}
        onContactTidal={handleContactTidal}
      />

      {/* 5. Call-to-Action Blocks - FIFTH */}
      <CTASection 
        isLoading={isLoading}
        layout="horizontal"
        ctaItems={[
          {
            id: 'book-strategy-call',
            title: 'Book a Strategy Call',
            description: 'Get personalized hiring recommendations and meet pre-screened candidates who match your exact requirements.',
            buttonText: 'Schedule Free Call',
            icon: '📅',
            type: 'primary',
            onClick: handleBookCall,
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
            onClick: handleContactTidal,
            features: [
              'Pre-vetted professionals',
              'Video interviews available',
              'Skills assessments included',
              'Multiple experience levels'
            ]
          }
        ]}
      />

      {/* PRD Implementation Status */}
      <section className="py-16 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-dark-navy-text text-center mb-12">
            PRD Requirements Implementation
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-light-gray-bg rounded-xl p-6">
              <div className="w-12 h-12 bg-tidal-purple/10 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">📱</span>
              </div>
              <h3 className="text-xl font-bold text-dark-navy-text mb-3">Responsive Design</h3>
              <ul className="text-medium-gray-text space-y-2">
                <li>• Desktop: 1200px+ (3 cards horizontal)</li>
                <li>• Tablet: 768-1199px (2+1 layout)</li>
                <li>• Mobile: &lt;768px (stacked)</li>
                <li>• Generous 40px+ padding on desktop</li>
              </ul>
            </div>

            <div className="bg-light-gray-bg rounded-xl p-6">
              <div className="w-12 h-12 bg-tidal-aqua/10 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🎨</span>
              </div>
              <h3 className="text-xl font-bold text-dark-navy-text mb-3">Exact Brand Colors</h3>
              <ul className="text-medium-gray-text space-y-2">
                <li>• Tidal Purple: #7B61FF</li>
                <li>• Tidal Aqua: #00C6A2</li>
                <li>• Dark Navy Text: #1A1A1A</li>
                <li>• Purple gradients for CTAs</li>
              </ul>
            </div>

            <div className="bg-light-gray-bg rounded-xl p-6">
              <div className="w-12 h-12 bg-success-green/10 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">📋</span>
              </div>
              <h3 className="text-xl font-bold text-dark-navy-text mb-3">Section Hierarchy</h3>
              <ul className="text-medium-gray-text space-y-2">
                <li>1. Region cards (pay ranges)</li>
                <li>2. Recommended skills & tools</li>
                <li>3. Job analysis summary</li>
                <li>4. Next steps</li>
                <li>5. Call-to-action blocks</li>
              </ul>
            </div>

            <div className="bg-light-gray-bg rounded-xl p-6">
              <div className="w-12 h-12 bg-dark-navy-text/10 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">⚡</span>
              </div>
              <h3 className="text-xl font-bold text-dark-navy-text mb-3">Animations & Interactions</h3>
              <ul className="text-medium-gray-text space-y-2">
                <li>• Smooth slide-in animations</li>
                <li>• Hover scale effects</li>
                <li>• Staggered component reveals</li>
                <li>• Loading skeleton states</li>
              </ul>
            </div>

            <div className="bg-light-gray-bg rounded-xl p-6">
              <div className="w-12 h-12 bg-tidal-purple/10 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🏷️</span>
              </div>
              <h3 className="text-xl font-bold text-dark-navy-text mb-3">Skills & Analysis</h3>
              <ul className="text-medium-gray-text space-y-2">
                <li>• Must-have vs nice-to-have categorization</li>
                <li>• Pill-shaped skill badges</li>
                <li>• Most important insights first</li>
                <li>• Scannable format with icons</li>
              </ul>
            </div>

            <div className="bg-light-gray-bg rounded-xl p-6">
              <div className="w-12 h-12 bg-tidal-aqua/10 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">♿</span>
              </div>
              <h3 className="text-xl font-bold text-dark-navy-text mb-3">Accessibility</h3>
              <ul className="text-medium-gray-text space-y-2">
                <li>• ARIA labels on all interactive elements</li>
                <li>• Semantic HTML structure</li>
                <li>• Keyboard navigation support</li>
                <li>• Color contrast compliance</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-16 bg-light-gray-bg">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-dark-navy-text mb-8">
            Built with Modern Tech Stack
          </h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg p-4">
              <div className="text-2xl mb-2">⚛️</div>
              <div className="font-medium text-dark-navy-text">React 18</div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="text-2xl mb-2">🎨</div>
              <div className="font-medium text-dark-navy-text">Tailwind CSS</div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="text-2xl mb-2">📘</div>
              <div className="font-medium text-dark-navy-text">TypeScript</div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="text-2xl mb-2">🏗️</div>
              <div className="font-medium text-dark-navy-text">Vite</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default MarketScanResultsDemo