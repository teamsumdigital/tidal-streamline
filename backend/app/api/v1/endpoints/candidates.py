"""
Candidate Profiles API endpoints
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from loguru import logger

from app.core.database import db

router = APIRouter()

class CandidateProfile(BaseModel):
    """Candidate profile model"""
    id: str
    name: str
    role_category: str
    experience_years: str
    region: str
    skills: List[str]
    bio: str
    video_url: Optional[str] = None
    resume_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    hourly_rate: Optional[int] = None
    availability: str
    english_proficiency: str
    timezone: str

@router.get("/", response_model=List[CandidateProfile])
async def get_candidate_profiles(
    role_category: Optional[str] = Query(None, description="Filter by role category"),
    region: Optional[str] = Query(None, description="Filter by region"),
    max_rate: Optional[int] = Query(None, description="Maximum hourly rate"),
    limit: int = Query(20, ge=1, le=100, description="Number of candidates to return")
):
    """
    Get candidate profiles with optional filtering
    """
    try:
        # Get candidate profiles from database
        profiles = await db.get_candidate_profiles(role_category=role_category)
        
        # Apply additional filters
        if region:
            profiles = [p for p in profiles if p.get('region', '').lower() == region.lower()]
        
        if max_rate:
            profiles = [p for p in profiles if p.get('hourly_rate', 0) <= max_rate]
        
        # Limit results
        profiles = profiles[:limit]
        
        # Convert to response format
        candidate_list = []
        for profile in profiles:
            candidate_list.append(CandidateProfile(
                id=profile.get('id', ''),
                name=profile.get('name', ''),
                role_category=profile.get('role_category', ''),
                experience_years=profile.get('experience_years', ''),
                region=profile.get('region', ''),
                skills=profile.get('skills', []),
                bio=profile.get('bio', ''),
                video_url=profile.get('video_url'),
                resume_url=profile.get('resume_url'),
                portfolio_url=profile.get('portfolio_url'),
                hourly_rate=profile.get('hourly_rate'),
                availability=profile.get('availability', 'Available'),
                english_proficiency=profile.get('english_proficiency', 'Fluent'),
                timezone=profile.get('timezone', 'UTC')
            ))
        
        return candidate_list
        
    except Exception as e:
        logger.error(f"❌ Failed to get candidate profiles: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve candidates: {str(e)}")

@router.get("/{candidate_id}", response_model=CandidateProfile)
async def get_candidate_profile(candidate_id: str):
    """
    Get a specific candidate profile by ID
    """
    try:
        # In a real implementation, this would fetch from database
        # For now, return mock data
        mock_candidates = get_mock_candidates()
        candidate = next((c for c in mock_candidates if c['id'] == candidate_id), None)
        
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        return CandidateProfile(**candidate)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get candidate {candidate_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve candidate: {str(e)}")

@router.get("/for-role/{role_category}")
async def get_candidates_for_role(
    role_category: str,
    limit: int = Query(10, ge=1, le=50, description="Number of candidates to return")
):
    """
    Get candidate profiles specifically matching a role category
    """
    try:
        # Get candidates for specific role
        profiles = await db.get_candidate_profiles(role_category=role_category)
        
        if not profiles:
            # Return mock candidates if no data available
            mock_candidates = get_mock_candidates_for_role(role_category)
            profiles = mock_candidates[:limit]
        
        # Add matching score based on role alignment
        candidates_with_scores = []
        for profile in profiles[:limit]:
            matching_score = calculate_role_match_score(profile, role_category)
            candidates_with_scores.append({
                "candidate": profile,
                "matching_score": matching_score,
                "key_strengths": extract_key_strengths(profile, role_category),
                "experience_highlight": profile.get('bio', '')[:200] + "..." if len(profile.get('bio', '')) > 200 else profile.get('bio', '')
            })
        
        # Sort by matching score
        candidates_with_scores.sort(key=lambda x: x['matching_score'], reverse=True)
        
        return {
            "role_category": role_category,
            "candidates_found": len(candidates_with_scores),
            "candidates": candidates_with_scores
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get candidates for role {role_category}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get candidates for role: {str(e)}")

@router.get("/regions/{region}")
async def get_candidates_by_region(
    region: str,
    role_category: Optional[str] = Query(None, description="Filter by role"),
    limit: int = Query(20, ge=1, le=100, description="Number of candidates to return")
):
    """
    Get candidates from a specific region
    """
    try:
        # Get all candidates and filter by region
        all_profiles = await db.get_candidate_profiles()
        
        if not all_profiles:
            # Return mock data if no database data
            all_profiles = get_mock_candidates()
        
        # Filter by region
        regional_candidates = [
            p for p in all_profiles 
            if p.get('region', '').lower() == region.lower()
        ]
        
        # Additional role filter if specified
        if role_category:
            regional_candidates = [
                p for p in regional_candidates
                if p.get('role_category', '').lower() == role_category.lower()
            ]
        
        # Limit results
        regional_candidates = regional_candidates[:limit]
        
        # Add regional insights
        regional_insights = {
            "region": region,
            "total_candidates": len(regional_candidates),
            "average_experience": calculate_average_experience(regional_candidates),
            "common_skills": get_common_skills(regional_candidates),
            "salary_range": get_salary_range(regional_candidates),
            "timezone_info": get_timezone_info(region)
        }
        
        return {
            "regional_insights": regional_insights,
            "candidates": regional_candidates
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get candidates for region {region}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get regional candidates: {str(e)}")

# Helper functions
def get_mock_candidates() -> List[Dict[str, Any]]:
    """
    Mock candidate data for demonstration
    """
    return [
        {
            "id": "candidate_1",
            "name": "Maria Santos",
            "role_category": "Ecommerce Manager",
            "experience_years": "5-8 years",
            "region": "Philippines",
            "skills": ["Shopify Admin", "Google Analytics", "Email Marketing", "Project Management"],
            "bio": "Experienced e-commerce manager with 6 years of experience managing Shopify stores for US-based brands. Specialized in conversion optimization and customer retention strategies.",
            "video_url": "https://example.com/videos/maria_intro.mp4",
            "resume_url": "https://example.com/resumes/maria_santos.pdf",
            "hourly_rate": 15,
            "availability": "Available",
            "english_proficiency": "Fluent",
            "timezone": "GMT+8"
        },
        {
            "id": "candidate_2", 
            "name": "Carlos Rodriguez",
            "role_category": "Data Analyst",
            "experience_years": "3-6 years",
            "region": "Latin America",
            "skills": ["Excel Advanced", "SQL", "Python", "Tableau", "Google Analytics"],
            "bio": "Data analyst with strong background in e-commerce analytics and reporting. Experience with large datasets and automated reporting systems.",
            "video_url": "https://example.com/videos/carlos_intro.mp4",
            "resume_url": "https://example.com/resumes/carlos_rodriguez.pdf",
            "hourly_rate": 18,
            "availability": "Available",
            "english_proficiency": "Advanced",
            "timezone": "GMT-3"
        },
        {
            "id": "candidate_3",
            "name": "Thandiwe Mokwena", 
            "role_category": "Content Marketer",
            "experience_years": "2-4 years",
            "region": "South Africa",
            "skills": ["Content Creation", "Social Media", "SEO", "Adobe Creative Suite"],
            "bio": "Creative content marketer with experience in B2C brands. Strong background in social media content and email marketing campaigns.",
            "video_url": "https://example.com/videos/thandiwe_intro.mp4",
            "resume_url": "https://example.com/resumes/thandiwe_mokwena.pdf",
            "hourly_rate": 20,
            "availability": "Available",
            "english_proficiency": "Native",
            "timezone": "GMT+2"
        }
    ]

def get_mock_candidates_for_role(role_category: str) -> List[Dict[str, Any]]:
    """
    Get mock candidates filtered by role
    """
    all_candidates = get_mock_candidates()
    return [c for c in all_candidates if c['role_category'] == role_category]

def calculate_role_match_score(candidate: Dict[str, Any], role_category: str) -> float:
    """
    Calculate how well a candidate matches a role
    """
    # Simple scoring based on role match and experience
    base_score = 0.8 if candidate.get('role_category') == role_category else 0.4
    
    # Boost score based on experience
    experience = candidate.get('experience_years', '')
    if '5-8' in experience or '9+' in experience:
        base_score += 0.15
    elif '3-6' in experience:
        base_score += 0.1
    
    return min(base_score, 1.0)

def extract_key_strengths(candidate: Dict[str, Any], role_category: str) -> List[str]:
    """
    Extract key strengths relevant to the role
    """
    skills = candidate.get('skills', [])
    return skills[:4]  # Return top 4 skills

def calculate_average_experience(candidates: List[Dict[str, Any]]) -> str:
    """
    Calculate average experience level
    """
    if not candidates:
        return "No data"
    
    experience_levels = [c.get('experience_years', '') for c in candidates]
    # Simplified calculation
    return "3-6 years average"

def get_common_skills(candidates: List[Dict[str, Any]]) -> List[str]:
    """
    Get most common skills across candidates
    """
    skill_counts = {}
    for candidate in candidates:
        for skill in candidate.get('skills', []):
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    return sorted(skill_counts.keys(), key=lambda x: skill_counts[x], reverse=True)[:5]

def get_salary_range(candidates: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Get salary range for candidates
    """
    rates = [c.get('hourly_rate', 0) for c in candidates if c.get('hourly_rate')]
    if not rates:
        return {"min": 0, "max": 0, "average": 0}
    
    return {
        "min": min(rates),
        "max": max(rates),
        "average": sum(rates) // len(rates)
    }

def get_timezone_info(region: str) -> str:
    """
    Get timezone information for region
    """
    timezone_map = {
        "Philippines": "GMT+8 (Manila) - Good overlap with US West Coast",
        "Latin America": "GMT-3 to GMT-5 - Excellent overlap with US time zones", 
        "South Africa": "GMT+2 (Cape Town) - Good overlap with European hours",
        "United States": "Various time zones - Local talent"
    }
    
    return timezone_map.get(region, "Contact for specific timezone information")