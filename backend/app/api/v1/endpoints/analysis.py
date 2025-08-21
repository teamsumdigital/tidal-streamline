"""
Job Analysis API endpoints
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

from app.core.ai_service import ai_service
from app.core.database import get_database

router = APIRouter()

class JobAnalysisRequest(BaseModel):
    """Request for standalone job analysis"""
    job_title: str
    job_description: str
    hiring_challenges: str = ""

class QuickAnalysisResponse(BaseModel):
    """Quick analysis response"""
    role_category: str
    experience_level: str
    complexity_score: int
    must_have_skills: List[str]
    recommended_regions: List[str]
    analysis_confidence: float

@router.post("/quick", response_model=QuickAnalysisResponse)
async def quick_job_analysis(request: JobAnalysisRequest):
    """
    Perform quick job analysis without creating a full market scan
    """
    try:
        logger.info(f"🔄 Starting quick analysis for: {request.job_title}")
        
        # Perform AI analysis
        analysis = await ai_service.analyze_job_description(
            job_title=request.job_title,
            job_description=request.job_description,
            hiring_challenges=request.hiring_challenges
        )
        
        # Return simplified response
        return QuickAnalysisResponse(
            role_category=analysis.get('role_category', 'Unknown'),
            experience_level=analysis.get('experience_level', 'mid'),
            complexity_score=analysis.get('complexity_score', 5),
            must_have_skills=analysis.get('must_have_skills', []),
            recommended_regions=analysis.get('recommended_regions', []),
            analysis_confidence=0.85  # TODO: Calculate actual confidence
        )
        
    except Exception as e:
        logger.error(f"❌ Quick analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/compare")
async def compare_job_to_historical(request: JobAnalysisRequest):
    """
    Compare a job description to historical market scans
    """
    try:
        # Find similar historical scans
        similar_scans = await get_database().search_similar_scans(
            job_title=request.job_title,
            job_description=request.job_description
        )
        
        if not similar_scans:
            return {
                "message": "No similar roles found in historical data",
                "similar_count": 0,
                "recommendations": "This appears to be a unique role. Consider creating a comprehensive market scan."
            }
        
        # Analyze similarities
        comparison_results = []
        for scan in similar_scans[:5]:  # Limit to top 5
            similarity_score = calculate_job_similarity(request, scan)
            comparison_results.append({
                "scan_id": scan['id'],
                "job_title": scan['job_title'],
                "company": scan.get('company_domain', 'Unknown'),
                "similarity_score": similarity_score,
                "role_category": scan.get('role_category'),
                "salary_range": scan.get('salary_recommendations', {}).get('recommended_pay_band'),
                "created_date": scan.get('created_at')
            })
        
        return {
            "similar_roles_found": len(comparison_results),
            "comparisons": comparison_results,
            "average_similarity": sum(r['similarity_score'] for r in comparison_results) / len(comparison_results),
            "recommendation": "Based on similar roles, consider reviewing salary expectations and skill requirements."
        }
        
    except Exception as e:
        logger.error(f"❌ Comparison analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@router.get("/role-categories")
async def get_role_categories():
    """
    Get available role categories and their common titles
    """
    try:
        role_mappings = await get_database().get_role_mappings()
        
        if not role_mappings:
            # Return default categories if no data in database
            return {
                "categories": [
                    {
                        "core_role": "Brand Marketing Manager",
                        "common_titles": ["Creative Project Manager", "Marketing Project Manager", "Production Manager", "Marketing Operations Manager"],
                        "description": "Manages brand marketing campaigns and creative projects"
                    },
                    {
                        "core_role": "Community Manager", 
                        "common_titles": ["Social Media Manager", "Influencer Coordinator", "Affiliate Manager", "Partnerships Coordinator"],
                        "description": "Manages online communities and social media presence"
                    },
                    {
                        "core_role": "Content Marketer",
                        "common_titles": ["Brand Content Manager", "Content Strategist", "Digital Content Manager", "Creative Content Manager"],
                        "description": "Creates and manages content marketing strategies"
                    },
                    {
                        "core_role": "Retention Manager",
                        "common_titles": ["Email Marketing Manager", "Lifecycle Marketing Manager", "CRM Manager"],
                        "description": "Focuses on customer retention and lifecycle marketing"
                    },
                    {
                        "core_role": "Ecommerce Manager",
                        "common_titles": ["E-commerce Manager", "Shopify Manager", "E-commerce Operations Manager", "E-commerce Project Manager", "Digital Commerce Manager"],
                        "description": "Manages online store operations and e-commerce strategy"
                    },
                    {
                        "core_role": "Sales Operations Manager",
                        "common_titles": ["Operations Manager", "RevOps Manager", "Amazon/Shopify/Sales Channel Manager"],
                        "description": "Optimizes sales processes and revenue operations"
                    },
                    {
                        "core_role": "Data Analyst",
                        "common_titles": ["Data Engineer", "Marketing Data Analyst", "Business Intelligence Analyst", "Digital Analytics Specialist", "Reporting Analyst", "Performance Marketing Analyst"],
                        "description": "Analyzes data to drive business insights and decisions"
                    },
                    {
                        "core_role": "Logistics Manager",
                        "common_titles": ["Supply Chain Coordinator", "Operations Manager", "Fulfillment Operations Manager", "Freight Coordinator", "EDI/ERP Coordinator"],
                        "description": "Manages supply chain and logistics operations"
                    }
                ]
            }
        
        return {"categories": role_mappings}
        
    except Exception as e:
        logger.error(f"❌ Failed to get role categories: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve role categories: {str(e)}")

@router.get("/skills/{role_category}")
async def get_common_skills_for_role(role_category: str):
    """
    Get common skills and tools for a specific role category
    """
    try:
        # Get historical data for this role
        historical_scans = await get_database().get_market_scans(limit=50)
        role_scans = [
            scan for scan in historical_scans 
            if scan.get('role_category') == role_category
        ]
        
        if not role_scans:
            return {
                "role_category": role_category,
                "message": "No historical data found for this role",
                "suggested_skills": get_default_skills_for_role(role_category)
            }
        
        # Aggregate skills from historical scans
        all_must_have = []
        all_nice_to_have = []
        
        for scan in role_scans:
            job_analysis = scan.get('job_analysis', {})
            all_must_have.extend(job_analysis.get('must_have_skills', []))
            all_nice_to_have.extend(job_analysis.get('nice_to_have_skills', []))
        
        # Count frequency and return most common
        must_have_freq = {}
        nice_to_have_freq = {}
        
        for skill in all_must_have:
            must_have_freq[skill] = must_have_freq.get(skill, 0) + 1
            
        for skill in all_nice_to_have:
            nice_to_have_freq[skill] = nice_to_have_freq.get(skill, 0) + 1
        
        # Sort by frequency
        top_must_have = sorted(must_have_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        top_nice_to_have = sorted(nice_to_have_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "role_category": role_category,
            "historical_scans_analyzed": len(role_scans),
            "most_common_must_have": [{"skill": skill, "frequency": freq} for skill, freq in top_must_have],
            "most_common_nice_to_have": [{"skill": skill, "frequency": freq} for skill, freq in top_nice_to_have]
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get skills for role {role_category}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve skills: {str(e)}")

# Helper functions
def calculate_job_similarity(request: JobAnalysisRequest, historical_scan: Dict[str, Any]) -> float:
    """
    Calculate similarity score between job request and historical scan
    """
    # Simple similarity calculation based on title and description keywords
    # In production, this would use vector similarity or more sophisticated NLP
    
    title_words = set(request.job_title.lower().split())
    hist_title_words = set(historical_scan.get('job_title', '').lower().split())
    
    desc_words = set(request.job_description.lower().split())
    hist_desc_words = set(historical_scan.get('job_description', '').lower().split())
    
    # Calculate Jaccard similarity
    title_similarity = len(title_words.intersection(hist_title_words)) / len(title_words.union(hist_title_words)) if title_words.union(hist_title_words) else 0
    desc_similarity = len(desc_words.intersection(hist_desc_words)) / len(desc_words.union(hist_desc_words)) if desc_words.union(hist_desc_words) else 0
    
    # Weighted average (title weighted more heavily)
    return (title_similarity * 0.7 + desc_similarity * 0.3)

def get_default_skills_for_role(role_category: str) -> Dict[str, List[str]]:
    """
    Get default skills when no historical data is available
    """
    defaults = {
        "Brand Marketing Manager": {
            "must_have": ["Excel/Google Sheets (Advanced)", "Project Management", "Creative Coordination"],
            "nice_to_have": ["Adobe Creative Suite", "Project Management Tools", "Brand Strategy"]
        },
        "Ecommerce Manager": {
            "must_have": ["Shopify Admin Experience", "E-commerce Operations", "Data Analysis"],
            "nice_to_have": ["Google Analytics", "Email Marketing", "Inventory Management"]
        },
        "Data Analyst": {
            "must_have": ["Excel/Google Sheets (Advanced)", "Data Analysis & Reporting", "SQL/Database Knowledge"],
            "nice_to_have": ["Python/R", "Tableau/Power BI", "Statistical Analysis"]
        }
    }
    
    return defaults.get(role_category, {
        "must_have": ["Microsoft Office", "Communication Skills", "Problem Solving"],
        "nice_to_have": ["Industry Experience", "Relevant Certifications"]
    })