"""
Salary Calculator Service - Regional salary calculations and recommendations
"""

from typing import Dict, List, Optional
from app.models.market_scan import SalaryRange, SalaryRecommendations, MarketInsights, JobAnalysis, Region, RoleCategory
from app.core.database import get_supabase_client

class SalaryCalculator:
    """Regional salary calculator and recommendations service"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        
        # Regional savings percentages vs US baseline
        self.regional_savings = {
            Region.UNITED_STATES: 0,
            Region.PHILIPPINES: 71,
            Region.LATIN_AMERICA: 58, 
            Region.SOUTH_AFRICA: 48
        }
    
    async def calculate_salary_recommendations(self, job_analysis: JobAnalysis) -> SalaryRecommendations:
        """Calculate salary recommendations based on job analysis"""
        
        # Get salary benchmarks from database
        salary_data = await self._get_salary_benchmarks(
            job_analysis.role_category,
            job_analysis.experience_level
        )
        
        # Calculate recommendations for each region
        salary_recommendations = {}
        
        for region in job_analysis.recommended_regions:
            if region in salary_data:
                salary_recommendations[region.value] = salary_data[region]
            else:
                # Calculate estimated salary if no data exists
                salary_recommendations[region.value] = await self._estimate_salary(
                    job_analysis.role_category,
                    job_analysis.experience_level,
                    region,
                    job_analysis.complexity_score
                )
        
        # Determine recommended pay band
        pay_band = self._determine_pay_band(job_analysis.complexity_score, job_analysis.experience_level)
        
        # Generate market insights
        market_insights = self._generate_market_insights(job_analysis, salary_recommendations)
        
        return SalaryRecommendations(
            salary_recommendations=salary_recommendations,
            recommended_pay_band=pay_band,
            factors_considered=job_analysis.salary_factors,
            market_insights=market_insights
        )
    
    async def _get_salary_benchmarks(self, role_category: RoleCategory, experience_level: str) -> Dict[Region, SalaryRange]:
        """Get salary benchmarks from database"""
        
        # Map experience level to database format
        exp_map = {
            "junior": ["1-2 years", "2-4 years"],
            "mid": ["2-4 years", "3-6 years"],
            "senior": ["5-8 years", "7-10 years"],
            "expert": ["9+ years", "10+ years"]
        }
        
        exp_levels = exp_map.get(experience_level, ["2-4 years"])
        
        try:
            response = self.supabase.table('salary_benchmarks').select('*').eq(
                'role_category', role_category.value
            ).in_('experience_level', exp_levels).execute()
            
            salary_data = {}
            for row in response.data:
                region = Region(row['region'])
                salary_data[region] = SalaryRange(
                    low=row['salary_low'],
                    mid=row['salary_mid'],
                    high=row['salary_high'],
                    currency=row.get('currency', 'USD'),
                    period=row.get('period', 'monthly'),
                    savings_vs_us=row.get('savings_vs_us', 0)
                )
            
            return salary_data
            
        except Exception as e:
            print(f"Error fetching salary benchmarks: {e}")
            return {}
    
    async def _estimate_salary(self, role_category: RoleCategory, experience_level: str, 
                             region: Region, complexity_score: int) -> SalaryRange:
        """Estimate salary when no benchmark data exists"""
        
        # Base salary estimates (monthly USD)
        base_salaries = {
            RoleCategory.BRAND_MARKETING_MANAGER: {"junior": 5000, "mid": 6000, "senior": 7500, "expert": 9000},
            RoleCategory.ECOMMERCE_MANAGER: {"junior": 4500, "mid": 5500, "senior": 7000, "expert": 8500},
            RoleCategory.DATA_ANALYST: {"junior": 4000, "mid": 5000, "senior": 6500, "expert": 8000},
            RoleCategory.CONTENT_MARKETER: {"junior": 3500, "mid": 4500, "senior": 6000, "expert": 7500},
            RoleCategory.COMMUNITY_MANAGER: {"junior": 3000, "mid": 4000, "senior": 5500, "expert": 7000},
            RoleCategory.RETENTION_MANAGER: {"junior": 4000, "mid": 5000, "senior": 6500, "expert": 8000},
            RoleCategory.SALES_OPERATIONS_MANAGER: {"junior": 4500, "mid": 5500, "senior": 7000, "expert": 8500},
            RoleCategory.LOGISTICS_MANAGER: {"junior": 4000, "mid": 5000, "senior": 6500, "expert": 8000},
            RoleCategory.OPERATIONS_MANAGER: {"junior": 4200, "mid": 5200, "senior": 6700, "expert": 8200}
        }
        
        # Get base salary for US
        us_base = base_salaries.get(role_category, {}).get(experience_level, 5000)
        
        # Apply complexity multiplier (0.8x to 1.2x)
        complexity_multiplier = 0.8 + (complexity_score - 1) * 0.04  # 1-10 scale to 0.8-1.2
        us_adjusted = int(us_base * complexity_multiplier)
        
        if region == Region.UNITED_STATES:
            base_salary = us_adjusted
        else:
            # Apply regional savings
            savings_percent = self.regional_savings.get(region, 50)
            base_salary = int(us_adjusted * (100 - savings_percent) / 100)
        
        # Create salary range (±15% around base)
        return SalaryRange(
            low=int(base_salary * 0.85),
            mid=base_salary,
            high=int(base_salary * 1.15),
            currency="USD",
            period="monthly",
            savings_vs_us=self.regional_savings.get(region, 0)
        )
    
    def _determine_pay_band(self, complexity_score: int, experience_level: str) -> str:
        """Determine recommended pay band"""
        
        # Experience level scoring
        exp_score = {"junior": 1, "mid": 2, "senior": 3, "expert": 4}.get(experience_level, 2)
        
        # Combined scoring (1-14 scale)
        total_score = complexity_score + exp_score
        
        if total_score <= 6:
            return "low"
        elif total_score <= 10:
            return "mid"
        else:
            return "high"
    
    def _generate_market_insights(self, job_analysis: JobAnalysis, 
                                 salary_recommendations: Dict[str, SalaryRange]) -> MarketInsights:
        """Generate market insights based on analysis"""
        
        # Determine high demand regions based on savings and complexity
        high_demand = []
        competitive_factors = []
        
        # Analyze salary recommendations for insights
        if salary_recommendations:
            savings_data = [(region, data.savings_vs_us or 0) for region, data in salary_recommendations.items()]
            savings_data.sort(key=lambda x: x[1], reverse=True)
            
            # Top savings regions are high demand
            high_demand = [region for region, _ in savings_data[:2]]
        
        # Generate competitive factors based on role
        if job_analysis.complexity_score >= 7:
            competitive_factors.append("High complexity role requires experienced candidates")
        
        if "technical" in [skill.lower() for skill in job_analysis.must_have_skills]:
            competitive_factors.append("Technical skills increase market competition")
        
        if len(job_analysis.must_have_skills) >= 5:
            competitive_factors.append("Multiple required skills narrow candidate pool")
        
        # Cost efficiency analysis
        if any(region in ["Philippines", "Latin America"] for region in salary_recommendations.keys()):
            cost_efficiency = "High cost savings available through strategic regional hiring"
        else:
            cost_efficiency = "Moderate cost optimization possible with current regional focus"
        
        return MarketInsights(
            high_demand_regions=high_demand or ["Philippines", "Latin America"],
            competitive_factors=competitive_factors or ["Standard market competition"],
            cost_efficiency=cost_efficiency
        )