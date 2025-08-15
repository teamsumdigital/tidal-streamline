"""
Data models for market scan operations
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class ExperienceLevel(str, Enum):
    """Experience level options"""
    JUNIOR = "junior"
    MID = "mid" 
    SENIOR = "senior"
    EXPERT = "expert"

class Region(str, Enum):
    """Supported regions"""
    UNITED_STATES = "United States"
    PHILIPPINES = "Philippines"
    LATIN_AMERICA = "Latin America"
    SOUTH_AFRICA = "South Africa"

class RoleCategory(str, Enum):
    """Core role categories"""
    BRAND_MARKETING_MANAGER = "Brand Marketing Manager"
    COMMUNITY_MANAGER = "Community Manager" 
    CONTENT_MARKETER = "Content Marketer"
    RETENTION_MANAGER = "Retention Manager"
    ECOMMERCE_MANAGER = "Ecommerce Manager"
    SALES_OPERATIONS_MANAGER = "Sales Operations Manager"
    DATA_ANALYST = "Data Analyst"
    LOGISTICS_MANAGER = "Logistics Manager"
    OPERATIONS_MANAGER = "Operations Manager"

# Request Models
class MarketScanRequest(BaseModel):
    """Request model for creating a market scan"""
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    company_domain: str = Field(..., max_length=100)
    job_title: str = Field(..., min_length=1, max_length=200)
    job_description: str = Field(..., min_length=10, max_length=5000)
    hiring_challenges: Optional[str] = Field(None, max_length=1000)
    
    @validator('company_domain')
    def validate_domain(cls, v):
        # Remove protocol if present
        if v.startswith(('http://', 'https://')):
            v = v.split('://', 1)[1]
        return v.lower()

class SalaryRange(BaseModel):
    """Salary range for a specific region"""
    low: int = Field(..., ge=0)
    mid: int = Field(..., ge=0) 
    high: int = Field(..., ge=0)
    currency: str = Field(default="USD")
    period: str = Field(default="monthly")
    savings_vs_us: Optional[int] = Field(None, ge=0, le=100)
    
    @validator('high')
    def validate_range(cls, v, values):
        if 'low' in values and v < values['low']:
            raise ValueError('High salary must be greater than low salary')
        return v

class SkillsRecommendation(BaseModel):
    """Skills and tools recommendations"""
    must_have_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)
    skill_categories: Dict[str, List[str]] = Field(default_factory=dict)
    certification_recommendations: List[str] = Field(default_factory=list)

class JobAnalysis(BaseModel):
    """AI analysis results for a job posting"""
    role_category: RoleCategory
    experience_level: ExperienceLevel  
    years_experience_required: str
    must_have_skills: List[str]
    nice_to_have_skills: List[str]
    key_responsibilities: List[str]
    remote_work_suitability: str = Field(..., pattern=r'^(high|medium|low)$')
    complexity_score: int = Field(..., ge=1, le=10)
    recommended_regions: List[Region]
    unique_challenges: str
    salary_factors: List[str]

class MarketInsights(BaseModel):
    """Market insights and analysis"""
    high_demand_regions: List[str]
    competitive_factors: List[str] 
    cost_efficiency: str

class SalaryRecommendations(BaseModel):
    """Complete salary recommendations"""
    salary_recommendations: Dict[str, SalaryRange]
    recommended_pay_band: str = Field(..., pattern=r'^(low|mid|high)$')
    factors_considered: List[str]
    market_insights: MarketInsights

# Response Models  
class MarketScanResponse(BaseModel):
    """Complete market scan response"""
    id: str
    client_name: str
    client_email: str
    company_domain: str
    job_title: str
    job_description: str
    hiring_challenges: Optional[str]
    
    # Analysis Results
    job_analysis: Optional[JobAnalysis] = None
    salary_recommendations: Optional[SalaryRecommendations] = None
    skills_recommendations: Optional[SkillsRecommendation] = None
    
    # Metadata
    status: str = Field(default="pending")  # pending, analyzing, completed, failed
    created_at: datetime
    updated_at: datetime
    processing_time_seconds: Optional[float] = None
    
    # Similar Scans
    similar_scans_count: int = Field(default=0)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class MarketScanSummary(BaseModel):
    """Summary view of market scan"""
    id: str
    client_name: str
    company_domain: str
    job_title: str
    role_category: Optional[str]
    status: str
    created_at: datetime
    recommended_pay_band: Optional[str]
    primary_region: Optional[str]

class MarketScanList(BaseModel):
    """List of market scans with pagination"""
    scans: List[MarketScanSummary]
    total_count: int
    page: int
    page_size: int
    has_next: bool

# Database Models
class MarketScanDB(BaseModel):
    """Database representation of market scan"""
    id: Optional[str] = None
    client_name: str
    client_email: str
    company_domain: str
    job_title: str
    job_description: str
    hiring_challenges: Optional[str] = None
    
    # Analysis Results (stored as JSON)
    job_analysis: Optional[Dict[str, Any]] = None
    salary_recommendations: Optional[Dict[str, Any]] = None
    skills_recommendations: Optional[Dict[str, Any]] = None
    
    # Metadata
    status: str = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    processing_time_seconds: Optional[float] = None
    similar_scans_count: int = 0
    confidence_score: Optional[float] = None
    
    # Additional fields for search and filtering
    role_category: Optional[str] = None
    experience_level: Optional[str] = None
    recommended_regions: Optional[List[str]] = None