// API Types for Tidal Streamline Frontend

export interface MarketScanRequest {
  client_name: string
  client_email: string
  company_domain: string
  job_title: string
  job_description: string
  hiring_challenges?: string
}

export interface SalaryRange {
  low: number
  mid: number
  high: number
  currency: string
  period: string
  savings_vs_us?: number
}

export interface MarketInsights {
  high_demand_regions: string[]
  competitive_factors: string[]
  cost_efficiency: string
}

export interface SalaryRecommendations {
  salary_recommendations: Record<string, SalaryRange>
  recommended_pay_band: 'low' | 'mid' | 'high'
  factors_considered: string[]
  market_insights: MarketInsights
}

export interface SkillsRecommendation {
  must_have_skills: string[]
  nice_to_have_skills: string[]
  skill_categories: Record<string, string[]>
  certification_recommendations: string[]
}

export interface JobAnalysis {
  role_category: string
  experience_level: string
  years_experience_required: string
  must_have_skills: string[]
  nice_to_have_skills: string[]
  key_responsibilities: string[]
  remote_work_suitability: string
  complexity_score: number
  recommended_regions: string[]
  unique_challenges: string
  salary_factors: string[]
}

export interface MarketScanResponse {
  id: string
  client_name: string
  client_email: string
  company_domain: string
  job_title: string
  job_description: string
  hiring_challenges?: string
  job_analysis?: JobAnalysis
  salary_recommendations?: SalaryRecommendations
  skills_recommendations?: SkillsRecommendation
  status: 'pending' | 'analyzing' | 'completed' | 'failed'
  created_at: string
  updated_at: string
  processing_time_seconds?: number
  similar_scans_count: number
  confidence_score?: number
}

export interface MarketScanSummary {
  id: string
  client_name: string
  company_domain: string
  job_title: string
  role_category?: string
  status: string
  created_at: string
  recommended_pay_band?: string
  primary_region?: string
}

export interface CandidateProfile {
  id: string
  name: string
  role_category: string
  experience_years: string
  region: string
  skills: string[]
  bio: string
  video_url?: string
  resume_url?: string
  portfolio_url?: string
  hourly_rate?: number
  availability: string
  english_proficiency: string
  timezone: string
}

export interface RegionalSalaryComparison {
  role_category: string
  experience_level: string
  regional_comparison: Record<string, {
    average_salary: number
    currency: string
    data_points: number
    salary_range: {
      low: number
      high: number
    }
  }>
  total_data_points: number
}

export interface QuickAnalysisResponse {
  role_category: string
  experience_level: string
  complexity_score: number
  must_have_skills: string[]
  recommended_regions: string[]
  analysis_confidence: number
}

export interface RoleCategory {
  core_role: string
  common_titles: string[]
  description: string
  category?: string
}

export interface SystemStats {
  total_scans: number
  completed_scans: number
  pending_scans: number
  failed_scans: number
  average_processing_time: number
  top_role_categories: Array<{
    role: string
    count: number
  }>
  recent_activity: Array<{
    id: string
    client_name: string
    job_title: string
    status: string
    created_at: string
  }>
}

export interface APIError {
  detail: string
  status_code?: number
}

export interface APIResponse<T> {
  data?: T
  error?: APIError
  loading: boolean
}

// Form types
export interface MarketScanFormData {
  clientName: string
  clientEmail: string
  companyDomain: string
  jobTitle: string
  jobDescription: string
  hiringChallenges: string
}

export interface FormErrors {
  [key: string]: string | undefined
}

// UI State types
export interface UIState {
  isLoading: boolean
  error: string | null
  success: string | null
}

// Region types for easier management
export type Region = 'United States' | 'Philippines' | 'Latin America' | 'South Africa'

export const REGIONS: Region[] = [
  'United States',
  'Philippines', 
  'Latin America',
  'South Africa'
]

// Role categories for type safety
export type RoleCategoryType = 
  | 'Brand Marketing Manager'
  | 'Community Manager'
  | 'Content Marketer'
  | 'Retention Manager'
  | 'Ecommerce Manager'
  | 'Sales Operations Manager'
  | 'Data Analyst'
  | 'Logistics Manager'
  | 'Operations Manager'

export const ROLE_CATEGORIES: RoleCategoryType[] = [
  'Brand Marketing Manager',
  'Community Manager',
  'Content Marketer', 
  'Retention Manager',
  'Ecommerce Manager',
  'Sales Operations Manager',
  'Data Analyst',
  'Logistics Manager',
  'Operations Manager'
]

// Experience levels
export type ExperienceLevel = 'junior' | 'mid' | 'senior' | 'expert'

export const EXPERIENCE_LEVELS: ExperienceLevel[] = [
  'junior',
  'mid', 
  'senior',
  'expert'
]

// Status types for better type checking
export type ScanStatus = 'pending' | 'analyzing' | 'completed' | 'failed'

// API endpoints configuration
export const API_ENDPOINTS = {
  MARKET_SCANS: '/api/v1/market-scans',
  ANALYSIS: '/api/v1/analysis',
  RECOMMENDATIONS: '/api/v1/recommendations',
  CANDIDATES: '/api/v1/candidates',
  ADMIN: '/api/v1/admin',
  REPORTS: '/api/v1/reports'
} as const