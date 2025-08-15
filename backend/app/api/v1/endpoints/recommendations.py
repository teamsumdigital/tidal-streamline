"""
Salary and Skills Recommendations API endpoints
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from loguru import logger

from app.core.ai_service import ai_service
from app.core.database import db

router = APIRouter()

class SalaryRequest(BaseModel):
    """Request for salary recommendations"""
    role_category: str
    experience_level: str
    complexity_score: int
    required_skills: List[str]
    preferred_regions: Optional[List[str]] = None

@router.post("/salary")
async def get_salary_recommendations(request: SalaryRequest):
    """
    Get salary recommendations based on role and requirements
    """
    try:
        # Get historical salary data for similar roles
        salary_benchmarks = await db.get_salary_benchmarks(
            role_category=request.role_category
        )
        
        # Create mock job analysis for AI processing
        job_analysis = {
            "role_category": request.role_category,
            "experience_level": request.experience_level,
            "complexity_score": request.complexity_score,
            "must_have_skills": request.required_skills
        }
        
        # Generate AI recommendations
        recommendations = await ai_service.generate_salary_recommendations(
            job_analysis=job_analysis,
            similar_scans=salary_benchmarks
        )
        
        return {
            "role_category": request.role_category,
            "experience_level": request.experience_level,
            "salary_recommendations": recommendations,
            "benchmark_data_points": len(salary_benchmarks),
            "confidence_level": "high" if len(salary_benchmarks) > 5 else "medium"
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get salary recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

@router.get("/salary/regional")
async def get_regional_salary_comparison(
    role_category: str = Query(..., description="Role category"),
    experience_level: str = Query("mid", description="Experience level")
):
    """
    Get regional salary comparison for a role
    """
    try:
        # Get salary data by region
        all_benchmarks = await db.get_salary_benchmarks(role_category=role_category)
        
        # Group by region
        regional_data = {}
        for benchmark in all_benchmarks:
            region = benchmark.get('region', 'Unknown')
            if region not in regional_data:
                regional_data[region] = []
            regional_data[region].append(benchmark)
        
        # Calculate averages by region
        regional_comparison = {}
        for region, data in regional_data.items():
            if data:
                avg_salary = sum(item.get('salary_mid', 0) for item in data) / len(data)
                regional_comparison[region] = {
                    "average_salary": avg_salary,
                    "currency": data[0].get('currency', 'USD'),
                    "data_points": len(data),
                    "salary_range": {
                        "low": min(item.get('salary_low', 0) for item in data),
                        "high": max(item.get('salary_high', 0) for item in data)
                    }
                }
        
        return {
            "role_category": role_category,
            "experience_level": experience_level,
            "regional_comparison": regional_comparison,
            "total_data_points": len(all_benchmarks)
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get regional comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get regional data: {str(e)}")

@router.get("/skills/{role_category}")
async def get_skills_recommendations(role_category: str):
    """
    Get skills recommendations for a specific role category
    """
    try:
        # Get historical market scans for this role
        historical_scans = await db.get_market_scans(limit=100)
        role_specific_scans = [
            scan for scan in historical_scans
            if scan.get('role_category') == role_category
        ]
        
        if not role_specific_scans:
            # Return default recommendations
            default_skills = get_default_skills_by_role(role_category)
            return {
                "role_category": role_category,
                "recommendations": default_skills,
                "data_source": "default_recommendations",
                "historical_data_points": 0
            }
        
        # Aggregate skills from historical data
        must_have_skills = {}
        nice_to_have_skills = {}
        
        for scan in role_specific_scans:
            job_analysis = scan.get('job_analysis', {})
            
            # Count frequency of must-have skills
            for skill in job_analysis.get('must_have_skills', []):
                must_have_skills[skill] = must_have_skills.get(skill, 0) + 1
                
            # Count frequency of nice-to-have skills  
            for skill in job_analysis.get('nice_to_have_skills', []):
                nice_to_have_skills[skill] = nice_to_have_skills.get(skill, 0) + 1
        
        # Sort by frequency and get top skills
        top_must_have = sorted(must_have_skills.items(), key=lambda x: x[1], reverse=True)[:8]
        top_nice_to_have = sorted(nice_to_have_skills.items(), key=lambda x: x[1], reverse=True)[:8]
        
        return {
            "role_category": role_category,
            "recommendations": {
                "must_have_skills": [
                    {"skill": skill, "frequency": freq, "percentage": round(freq/len(role_specific_scans)*100, 1)}
                    for skill, freq in top_must_have
                ],
                "nice_to_have_skills": [
                    {"skill": skill, "frequency": freq, "percentage": round(freq/len(role_specific_scans)*100, 1)}
                    for skill, freq in top_nice_to_have
                ]
            },
            "data_source": "historical_analysis",
            "historical_data_points": len(role_specific_scans)
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get skills recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get skills recommendations: {str(e)}")

@router.get("/market-insights/{role_category}")
async def get_market_insights(role_category: str):
    """
    Get market insights and trends for a role category
    """
    try:
        # Get recent market scans for trend analysis
        recent_scans = await db.get_market_scans(limit=50)
        role_scans = [
            scan for scan in recent_scans
            if scan.get('role_category') == role_category
        ]
        
        if len(role_scans) < 3:
            return {
                "role_category": role_category,
                "message": "Insufficient data for market insights",
                "data_points": len(role_scans),
                "recommendation": "Create more market scans to generate meaningful insights"
            }
        
        # Analyze trends
        regions_demand = {}
        complexity_scores = []
        salary_trends = []
        
        for scan in role_scans:
            # Track regional demand
            recommended_regions = scan.get('job_analysis', {}).get('recommended_regions', [])
            for region in recommended_regions:
                regions_demand[region] = regions_demand.get(region, 0) + 1
            
            # Track complexity
            complexity = scan.get('job_analysis', {}).get('complexity_score', 5)
            complexity_scores.append(complexity)
            
            # Track salary recommendations
            salary_rec = scan.get('salary_recommendations', {})
            if salary_rec:
                salary_trends.append(salary_rec.get('recommended_pay_band', 'mid'))
        
        # Calculate insights
        avg_complexity = sum(complexity_scores) / len(complexity_scores) if complexity_scores else 5
        most_demanded_regions = sorted(regions_demand.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "role_category": role_category,
            "market_insights": {
                "average_complexity_score": round(avg_complexity, 1),
                "most_in_demand_regions": [{"region": region, "demand_score": count} for region, count in most_demanded_regions],
                "salary_distribution": {
                    "low": salary_trends.count('low'),
                    "mid": salary_trends.count('mid'), 
                    "high": salary_trends.count('high')
                },
                "market_competitiveness": "high" if avg_complexity > 7 else "medium" if avg_complexity > 4 else "low",
                "hiring_difficulty": "challenging" if avg_complexity > 7 else "moderate"
            },
            "data_points": len(role_scans),
            "analysis_period": "last_50_scans"
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get market insights: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get market insights: {str(e)}")

def get_default_skills_by_role(role_category: str) -> Dict[str, List[str]]:
    """
    Default skills recommendations when no historical data is available
    """
    defaults = {
        "Brand Marketing Manager": {
            "must_have_skills": [
                {"skill": "Excel/Google Sheets (Advanced)", "frequency": 10, "percentage": 95.0},
                {"skill": "Project Management", "frequency": 9, "percentage": 85.0},
                {"skill": "Creative Coordination", "frequency": 8, "percentage": 80.0}
            ],
            "nice_to_have_skills": [
                {"skill": "Adobe Creative Suite", "frequency": 6, "percentage": 60.0},
                {"skill": "Project Management Tools", "frequency": 5, "percentage": 50.0},
                {"skill": "Brand Strategy", "frequency": 4, "percentage": 40.0}
            ]
        },
        "Ecommerce Manager": {
            "must_have_skills": [
                {"skill": "Shopify Admin Experience", "frequency": 10, "percentage": 95.0},
                {"skill": "E-commerce Operations", "frequency": 9, "percentage": 90.0},
                {"skill": "Data Analysis & Reporting", "frequency": 8, "percentage": 80.0}
            ],
            "nice_to_have_skills": [
                {"skill": "Google Analytics", "frequency": 6, "percentage": 60.0},
                {"skill": "Email Marketing", "frequency": 5, "percentage": 50.0},
                {"skill": "Inventory Management Systems", "frequency": 4, "percentage": 40.0}
            ]
        },
        "Data Analyst": {
            "must_have_skills": [
                {"skill": "Excel/Google Sheets (Advanced)", "frequency": 10, "percentage": 100.0},
                {"skill": "Data Analysis & Reporting", "frequency": 10, "percentage": 100.0},
                {"skill": "SQL/Database Knowledge", "frequency": 8, "percentage": 80.0}
            ],
            "nice_to_have_skills": [
                {"skill": "Python/R Programming", "frequency": 6, "percentage": 60.0},
                {"skill": "Tableau/Power BI", "frequency": 5, "percentage": 50.0},
                {"skill": "Statistical Analysis", "frequency": 4, "percentage": 40.0}
            ]
        }
    }
    
    return defaults.get(role_category, {
        "must_have_skills": [
            {"skill": "Microsoft Office Suite", "frequency": 8, "percentage": 80.0},
            {"skill": "Communication Skills", "frequency": 7, "percentage": 70.0}
        ],
        "nice_to_have_skills": [
            {"skill": "Industry Experience", "frequency": 5, "percentage": 50.0},
            {"skill": "Relevant Certifications", "frequency": 3, "percentage": 30.0}
        ]
    })