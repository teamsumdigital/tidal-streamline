// API Service for Tidal Streamline Frontend

import { 
  MarketScanRequest, 
  MarketScanResponse, 
  MarketScanSummary,
  CandidateProfile,
  QuickAnalysisResponse,
  RoleCategory,
  SystemStats,
  RegionalSalaryComparison,
  API_ENDPOINTS
} from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8008'

class APIService {
  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new APIError(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
          response.status
        )
      }

      return await response.json()
    } catch (error) {
      if (error instanceof APIError) {
        throw error
      }
      
      // Network or other errors
      throw new APIError(
        error instanceof Error ? error.message : 'An unexpected error occurred'
      )
    }
  }

  // Market Scans API
  async createMarketScan(data: MarketScanRequest): Promise<MarketScanResponse> {
    return this.request(`${API_ENDPOINTS.MARKET_SCANS}/analyze`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async getMarketScan(scanId: string): Promise<MarketScanResponse> {
    return this.request(`${API_ENDPOINTS.MARKET_SCANS}/${scanId}`)
  }

  async getMarketScans(params: {
    page?: number
    page_size?: number
    status?: string
    role_category?: string
    client_name?: string
  } = {}): Promise<{
    scans: MarketScanSummary[]
    total_count: number
    page: number
    page_size: number
    has_next: boolean
  }> {
    const searchParams = new URLSearchParams()
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value.toString())
      }
    })

    return this.request(`${API_ENDPOINTS.MARKET_SCANS}?${searchParams}`)
  }

  async getSimilarScans(scanId: string, limit: number = 5): Promise<{
    scan_id: string
    similar_scans: MarketScanResponse[]
    total_found: number
  }> {
    return this.request(`${API_ENDPOINTS.MARKET_SCANS}/${scanId}/similar?limit=${limit}`)
  }

  async deleteMarketScan(scanId: string): Promise<{ message: string }> {
    return this.request(`${API_ENDPOINTS.MARKET_SCANS}/${scanId}`, {
      method: 'DELETE',
    })
  }

  // Analysis API
  async quickJobAnalysis(data: {
    job_title: string
    job_description: string
    hiring_challenges?: string
  }): Promise<QuickAnalysisResponse> {
    return this.request(`${API_ENDPOINTS.ANALYSIS}/quick`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async compareJobToHistorical(data: {
    job_title: string
    job_description: string
    hiring_challenges?: string
  }): Promise<{
    similar_roles_found: number
    comparisons: Array<{
      scan_id: string
      job_title: string
      company: string
      similarity_score: number
      role_category: string
      salary_range: string
      created_date: string
    }>
    average_similarity: number
    recommendation: string
  }> {
    return this.request(`${API_ENDPOINTS.ANALYSIS}/compare`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async getRoleCategories(): Promise<{ categories: RoleCategory[] }> {
    return this.request(`${API_ENDPOINTS.ANALYSIS}/role-categories`)
  }

  async getCommonSkillsForRole(roleCategory: string): Promise<{
    role_category: string
    historical_scans_analyzed: number
    most_common_must_have: Array<{ skill: string; frequency: number }>
    most_common_nice_to_have: Array<{ skill: string; frequency: number }>
  }> {
    return this.request(`${API_ENDPOINTS.ANALYSIS}/skills/${encodeURIComponent(roleCategory)}`)
  }

  // Recommendations API
  async getSalaryRecommendations(data: {
    role_category: string
    experience_level: string
    complexity_score: number
    required_skills: string[]
    preferred_regions?: string[]
  }): Promise<{
    role_category: string
    experience_level: string
    salary_recommendations: any
    benchmark_data_points: number
    confidence_level: string
  }> {
    return this.request(`${API_ENDPOINTS.RECOMMENDATIONS}/salary`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async getRegionalSalaryComparison(
    roleCategory: string, 
    experienceLevel: string = 'mid'
  ): Promise<RegionalSalaryComparison> {
    const params = new URLSearchParams({
      role_category: roleCategory,
      experience_level: experienceLevel,
    })

    return this.request(`${API_ENDPOINTS.RECOMMENDATIONS}/salary/regional?${params}`)
  }

  async getSkillsRecommendations(roleCategory: string): Promise<{
    role_category: string
    recommendations: {
      must_have_skills: Array<{ skill: string; frequency: number; percentage: number }>
      nice_to_have_skills: Array<{ skill: string; frequency: number; percentage: number }>
    }
    data_source: string
    historical_data_points: number
  }> {
    return this.request(`${API_ENDPOINTS.RECOMMENDATIONS}/skills/${encodeURIComponent(roleCategory)}`)
  }

  async getMarketInsights(roleCategory: string): Promise<{
    role_category: string
    market_insights: {
      average_complexity_score: number
      most_in_demand_regions: Array<{ region: string; demand_score: number }>
      salary_distribution: { low: number; mid: number; high: number }
      market_competitiveness: string
      hiring_difficulty: string
    }
    data_points: number
    analysis_period: string
  }> {
    return this.request(`${API_ENDPOINTS.RECOMMENDATIONS}/market-insights/${encodeURIComponent(roleCategory)}`)
  }

  // Candidates API
  async getCandidateProfiles(params: {
    role_category?: string
    region?: string
    max_rate?: number
    limit?: number
  } = {}): Promise<CandidateProfile[]> {
    const searchParams = new URLSearchParams()
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value.toString())
      }
    })

    return this.request(`${API_ENDPOINTS.CANDIDATES}?${searchParams}`)
  }

  async getCandidateProfile(candidateId: string): Promise<CandidateProfile> {
    return this.request(`${API_ENDPOINTS.CANDIDATES}/${candidateId}`)
  }

  async getCandidatesForRole(roleCategory: string, limit: number = 10): Promise<{
    role_category: string
    candidates_found: number
    candidates: Array<{
      candidate: CandidateProfile
      matching_score: number
      key_strengths: string[]
      experience_highlight: string
    }>
  }> {
    return this.request(`${API_ENDPOINTS.CANDIDATES}/for-role/${encodeURIComponent(roleCategory)}?limit=${limit}`)
  }

  async getCandidatesByRegion(region: string, params: {
    role_category?: string
    limit?: number
  } = {}): Promise<{
    regional_insights: {
      region: string
      total_candidates: number
      average_experience: string
      common_skills: string[]
      salary_range: { min: number; max: number; average: number }
      timezone_info: string
    }
    candidates: CandidateProfile[]
  }> {
    const searchParams = new URLSearchParams(params as Record<string, string>)
    return this.request(`${API_ENDPOINTS.CANDIDATES}/regions/${encodeURIComponent(region)}?${searchParams}`)
  }

  // Admin API
  async getSystemStats(): Promise<SystemStats> {
    return this.request(`${API_ENDPOINTS.ADMIN}/stats`)
  }

  async getQualityMetrics(): Promise<{
    total_completed_scans: number
    confidence_metrics: {
      average_confidence: number
      high_confidence_count: number
      low_confidence_count: number
    }
    complexity_analysis: {
      average_complexity: number
      high_complexity_count: number
      low_complexity_count: number
    }
    performance_metrics: {
      average_processing_time: number
      fastest_processing: number
      slowest_processing: number
    }
  }> {
    return this.request(`${API_ENDPOINTS.ADMIN}/quality-metrics`)
  }

  async getFailedScans(): Promise<{
    total_failed: number
    failed_scans: Array<{
      id: string
      client_name: string
      job_title: string
      error_message: string
      created_at: string
      job_description_length: number
      has_hiring_challenges: boolean
    }>
    common_issues: Array<{
      pattern: string
      count: number
      percentage: number
      recommendation: string
    }>
  }> {
    return this.request(`${API_ENDPOINTS.ADMIN}/failed-scans`)
  }

  async retrainRecommendations(): Promise<{
    status: string
    message: string
    training_data_quality: {
      total_training_samples: number
      role_distribution: Record<string, number>
      region_coverage: Record<string, number>
      quality_score: number
    }
    estimated_completion: string
  }> {
    return this.request(`${API_ENDPOINTS.ADMIN}/retrain-recommendations`, {
      method: 'POST',
    })
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return this.request('/health')
  }

  async apiHealthCheck(): Promise<{
    status: string
    database: string
    ai_service: string
    timestamp: string
  }> {
    return this.request('/api/health')
  }
}

// Custom error class for API errors
class APIError extends Error {
  constructor(message: string, public status_code?: number) {
    super(message)
    this.name = 'APIError'
  }
}

// Export singleton instance
export const apiService = new APIService()
export { APIError }