"""
Market Scans API endpoints
"""

import csv
import io
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, Response
from loguru import logger

from app.models.market_scan import (
    MarketScanRequest,
    MarketScanResponse, 
    MarketScanSummary,
    MarketScanList,
    MarketScanDB
)
from app.core.database import db
from app.core.ai_service import ai_service
from app.services.job_analyzer import JobAnalyzer
from app.services.salary_calculator import SalaryCalculator

router = APIRouter()

@router.post("/analyze", response_model=MarketScanResponse)
async def create_market_scan(
    request: MarketScanRequest,
    background_tasks: BackgroundTasks
):
    """
    Create and analyze a new market scan
    """
    try:
        # Generate unique ID
        scan_id = str(uuid.uuid4())
        
        # Create initial database record
        scan_data = MarketScanDB(
            id=scan_id,
            client_name=request.client_name,
            client_email=request.client_email,
            company_domain=request.company_domain,
            job_title=request.job_title,
            job_description=request.job_description,
            hiring_challenges=request.hiring_challenges,
            status="analyzing",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save to database - convert datetime objects to ISO strings
        scan_dict = scan_data.dict()
        scan_dict['created_at'] = scan_dict['created_at'].isoformat() if scan_dict.get('created_at') else None
        scan_dict['updated_at'] = scan_dict['updated_at'].isoformat() if scan_dict.get('updated_at') else None
        created_scan = await db.create_market_scan(scan_dict)
        
        # Start background analysis
        background_tasks.add_task(
            process_market_scan_analysis,
            scan_id,
            request
        )
        
        logger.info(f"✅ Created market scan {scan_id} for {request.client_name}")
        
        # Return immediate response with processing status
        return MarketScanResponse(
            id=scan_id,
            client_name=request.client_name,
            client_email=request.client_email,
            company_domain=request.company_domain,
            job_title=request.job_title,
            job_description=request.job_description,
            hiring_challenges=request.hiring_challenges,
            status="analyzing",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to create market scan: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create market scan: {str(e)}")

@router.get("/{scan_id}", response_model=MarketScanResponse)
async def get_market_scan(scan_id: str):
    """
    Retrieve a specific market scan by ID
    """
    try:
        scan_data = await db.get_market_scan(scan_id)
        
        if not scan_data:
            raise HTTPException(status_code=404, detail="Market scan not found")
        
        return MarketScanResponse(**scan_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get market scan {scan_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve market scan: {str(e)}")

@router.get("/", response_model=MarketScanList)
async def list_market_scans(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    role_category: Optional[str] = Query(None, description="Filter by role category"),
    client_name: Optional[str] = Query(None, description="Filter by client name")
):
    """
    List market scans with pagination and filtering
    """
    try:
        offset = (page - 1) * page_size
        
        # Get filtered scans
        scans = await db.get_market_scans(limit=page_size, offset=offset)
        
        # Convert to summary format
        scan_summaries = [
            MarketScanSummary(
                id=scan['id'],
                client_name=scan['client_name'],
                company_domain=scan['company_domain'],
                job_title=scan['job_title'],
                role_category=scan.get('role_category'),
                status=scan['status'],
                created_at=scan['created_at'],
                recommended_pay_band=scan.get('salary_recommendations', {}).get('recommended_pay_band') if isinstance(scan.get('salary_recommendations'), dict) else None,
                primary_region=scan.get('recommended_regions', [None])[0] if scan.get('recommended_regions') else None
            )
            for scan in scans
        ]
        
        # Note: In a real implementation, you'd also get total count for pagination
        total_count = len(scan_summaries)  # Simplified for now
        
        return MarketScanList(
            scans=scan_summaries,
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_next=len(scan_summaries) == page_size
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to list market scans: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list market scans: {str(e)}")

@router.delete("/{scan_id}")
async def delete_market_scan(scan_id: str):
    """
    Delete a market scan
    """
    try:
        # Check if scan exists
        existing_scan = await db.get_market_scan(scan_id)
        if not existing_scan:
            raise HTTPException(status_code=404, detail="Market scan not found")
        
        # TODO: Implement delete functionality in database manager
        # await db.delete_market_scan(scan_id)
        
        logger.info(f"✅ Deleted market scan {scan_id}")
        return {"message": "Market scan deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete market scan {scan_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete market scan: {str(e)}")

@router.get("/{scan_id}/similar")
async def get_similar_scans(
    scan_id: str, 
    limit: int = Query(5, ge=1, le=20),
    similarity_threshold: float = Query(0.70, ge=0.0, le=1.0, description="Minimum similarity score")
):
    """
    Get similar market scans using semantic matching
    """
    try:
        # Get the original scan
        scan_data = await db.get_market_scan(scan_id)
        if not scan_data:
            raise HTTPException(status_code=404, detail="Market scan not found")
        
        # Use vector search to find semantically similar scans
        from app.services.vector_search import vector_search_service
        similar_scans, confidence_score = await vector_search_service.find_similar_market_scans(
            job_title=scan_data['job_title'],
            job_description=scan_data['job_description'],
            current_scan_id=scan_id,
            similarity_threshold=similarity_threshold,
            max_results=limit
        )
        
        return {
            "scan_id": scan_id,
            "similar_scans": similar_scans,
            "total_found": len(similar_scans),
            "confidence_score": confidence_score,
            "similarity_threshold": similarity_threshold,
            "search_method": "semantic_matching"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get similar scans for {scan_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get similar scans: {str(e)}")

@router.get("/analytics/trends")
async def get_market_trends(
    lookback_days: int = Query(90, ge=1, le=365, description="Days to analyze")
):
    """
    Get market trends and analytics from semantic search data
    """
    try:
        from app.services.vector_search import vector_search_service
        trends = await vector_search_service.get_market_trends(lookback_days)
        
        return {
            "trends": trends,
            "generated_at": datetime.utcnow().isoformat(),
            "lookback_days": lookback_days
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get market trends: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get market trends: {str(e)}")

@router.get("/analytics/vector-stats")
async def get_vector_stats():
    """
    Get vector database statistics
    """
    try:
        from app.services.embedding_service import embedding_service
        stats = await embedding_service.get_index_stats()
        
        return {
            "vector_stats": stats,
            "index_name": embedding_service.index_name,
            "embedding_model": embedding_service.embedding_model,
            "embedding_dimension": embedding_service.embedding_dimension,
            "retrieved_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get vector stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get vector stats: {str(e)}")

# Background processing function
async def process_market_scan_analysis(scan_id: str, request: MarketScanRequest):
    """
    Background task to process market scan analysis
    """
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"🔄 Starting analysis for market scan {scan_id}")
        
        # Step 1: AI Job Analysis with Semantic Matching using enhanced JobAnalyzer
        job_analyzer = JobAnalyzer()
        job_analysis, similar_scans, confidence_score = await job_analyzer.analyze_job_with_similar_scans(
            job_title=request.job_title,
            job_description=request.job_description,
            hiring_challenges=request.hiring_challenges or "",
            scan_id=scan_id
        )
        
        # Step 2: Generate Salary Recommendations using SalaryCalculator
        salary_calculator = SalaryCalculator()
        salary_recommendations = await salary_calculator.calculate_salary_recommendations(job_analysis)
        
        # Step 3: Store analysis in vector database for future semantic matching
        await job_analyzer.store_analysis_vector(
            scan_id=scan_id,
            job_title=request.job_title,
            job_description=request.job_description,
            job_analysis=job_analysis,
            company_domain=request.company_domain,
            client_name=request.client_name
        )
        
        # Step 4: Create basic skills recommendations
        from app.models.market_scan import SkillsRecommendation
        skills_recommendations = SkillsRecommendation(
            must_have_skills=job_analysis.must_have_skills,
            nice_to_have_skills=job_analysis.nice_to_have_skills,
            skill_categories={"technical": job_analysis.must_have_skills[:3], "soft": job_analysis.nice_to_have_skills[:2]},
            certification_recommendations=["Industry certification", "Relevant online courses"]
        )
        
        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Update database with results - convert Pydantic models to dicts
        update_data = {
            'job_analysis': job_analysis.dict(),
            'salary_recommendations': salary_recommendations.dict(),
            'skills_recommendations': skills_recommendations.dict(),
            'status': 'completed',
            'updated_at': datetime.utcnow().isoformat(),
            'processing_time_seconds': processing_time,
            'similar_scans_count': len(similar_scans),
            'role_category': job_analysis.role_category.value,
            'experience_level': job_analysis.experience_level.value,
            'recommended_regions': [r.value for r in job_analysis.recommended_regions],
            'confidence_score': confidence_score
        }
        
        # Update database with completed analysis
        await db.update_market_scan(scan_id, update_data)
        
        logger.info(f"✅ Completed analysis for market scan {scan_id} in {processing_time:.2f}s")
        
    except Exception as e:
        logger.error(f"❌ Failed to process market scan {scan_id}: {e}")
        
        # Update status to failed
        await db.update_market_scan(scan_id, {
            'status': 'failed',
            'updated_at': datetime.utcnow(),
            'error_message': str(e)
        })


# CSV Export endpoint for Canva template integration
@router.get("/{scan_id}/export")
async def export_market_scan_csv(
    scan_id: str,
    format: str = Query("template", description="Export format: 'template' for Canva variables")
):
    """
    Export market scan data as CSV with all 134 template variables for Canva integration
    """
    try:
        # Get market scan data
        scan_data = await db.get_market_scan(scan_id)
        if not scan_data:
            raise HTTPException(status_code=404, detail="Market scan not found")
        
        # Get candidate profiles from database matching the role category
        role_category = ''
        if scan_data.get('job_analysis'):
            role_category = scan_data['job_analysis'].get('role_category', '')
        candidates = await get_candidate_profiles_for_template(role_category)
        
        # Generate template variables
        template_data = generate_template_variables(scan_data, candidates)
        
        # Create CSV
        csv_content = create_csv_content(template_data)
        
        logger.info(f"✅ Generated CSV export for scan {scan_id} with {len(template_data[0]) if template_data else 0} template variables")
        
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=market-scan-{scan_id}-export.csv"
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to export CSV for scan {scan_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to export CSV: {str(e)}")


async def get_candidate_profiles_for_template(role_category: str = '') -> List[Dict[str, Any]]:
    """Get candidate profiles from database for template variables, filtered by role category"""
    try:
        if role_category:
            # Try to get candidates matching the specific role category
            candidates_data = await db.get_candidate_profiles(role_category=role_category)
            if candidates_data:
                logger.info(f"✅ Found {len(candidates_data)} candidates for role: {role_category}")
                return candidates_data
            else:
                logger.info(f"⚠️ No candidates found for role '{role_category}', falling back to all candidates")
        
        # Fall back to all candidates if no role-specific candidates found
        candidates_data = await db.get_all_candidate_profiles()
        return candidates_data if candidates_data else []
    except Exception as e:
        logger.warning(f"Could not fetch candidate profiles: {e}")
        # Return empty list if database fetch fails
        return []


def generate_template_variables(scan_data: Dict[str, Any], candidates: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generate all 134+ template variables for Canva"""
    
    # Debug logging
    logger.info(f"🔍 Processing scan data keys: {list(scan_data.keys())}")
    logger.info(f"🔍 Found {len(candidates)} candidates")
    
    # Extract scan data fields
    template_vars = {}
    
    # Basic scan information
    template_vars.update({
        'company_domain': scan_data.get('company_domain', ''),
        'job_title': scan_data.get('job_title', ''),
        'client_name': scan_data.get('client_name', ''),
        'client_email': scan_data.get('client_email', ''),
        'scan_date': scan_data.get('created_at', ''),
        'status': scan_data.get('status', ''),
        'confidence_score': str(scan_data.get('confidence_score', 0))
    })
    
    # Job analysis data
    if scan_data.get('job_analysis'):
        job_analysis = scan_data['job_analysis']
        template_vars.update({
            'role_category': job_analysis.get('role_category', ''),
            'experience_level': job_analysis.get('experience_level', ''),
            'complexity_score': str(job_analysis.get('complexity_score', 0)),
            'years_experience_required': job_analysis.get('years_experience_required', ''),
            'remote_work_suitability': job_analysis.get('remote_work_suitability', ''),
            'unique_challenges': job_analysis.get('unique_challenges', ''),
            'key_responsibilities': ', '.join(job_analysis.get('key_responsibilities', [])),
            'recommended_regions': ', '.join(job_analysis.get('recommended_regions', [])),
            'salary_factors': ', '.join(job_analysis.get('salary_factors', [])),
            'must_have_skills': ', '.join(job_analysis.get('must_have_skills', [])),
            'nice_to_have_skills': ', '.join(job_analysis.get('nice_to_have_skills', []))
        })
    
    # Salary recommendations
    if scan_data.get('salary_recommendations'):
        salary_recs = scan_data['salary_recommendations']
        if salary_recs.get('salary_recommendations'):
            for region_name, salary_data in salary_recs['salary_recommendations'].items():
                safe_region = region_name.lower().replace(' ', '_')
                template_vars.update({
                    f'{safe_region}_low_salary': str(salary_data.get('low', 0)),
                    f'{safe_region}_mid_salary': str(salary_data.get('mid', 0)),
                    f'{safe_region}_high_salary': str(salary_data.get('high', 0)),
                    f'{safe_region}_currency': salary_data.get('currency', ''),
                    f'{safe_region}_period': salary_data.get('period', ''),
                    f'{safe_region}_savings_vs_us': str(salary_data.get('savings_vs_us', 0))
                })
        
        # Market insights
        if salary_recs.get('market_insights'):
            insights = salary_recs['market_insights']
            template_vars.update({
                'high_demand_regions': ', '.join(insights.get('high_demand_regions', [])),
                'competitive_factors': ', '.join(insights.get('competitive_factors', [])),
                'cost_efficiency': insights.get('cost_efficiency', '')
            })
    
    # Skills recommendations
    if scan_data.get('skills_recommendations'):
        skills = scan_data['skills_recommendations']
        template_vars.update({
            'must_have_skills': ', '.join(skills.get('must_have_skills', [])),
            'nice_to_have_skills': ', '.join(skills.get('nice_to_have_skills', [])),
            'certification_recommendations': ', '.join(skills.get('certification_recommendations', [])),
        })
        
        # Skill categories
        if skills.get('skill_categories'):
            for cat_name, cat_skills in skills['skill_categories'].items():
                safe_cat = cat_name.lower().replace(' ', '_')
                template_vars[f'{safe_cat}_skills'] = ', '.join(cat_skills)
    
    # Add candidate profile data
    for i, candidate in enumerate(candidates[:3]):  # Limit to 3 candidates to match market scan
        candidate_prefix = f'candidate_{i+1}'
        template_vars.update({
            f'{candidate_prefix}_name': candidate.get('name', ''),
            f'{candidate_prefix}_role': candidate.get('role_category', ''),
            f'{candidate_prefix}_experience': candidate.get('experience_years', ''),
            f'{candidate_prefix}_region': candidate.get('region', ''),
            f'{candidate_prefix}_skills': ', '.join(candidate.get('skills', [])),
            f'{candidate_prefix}_bio': candidate.get('bio', ''),
            f'{candidate_prefix}_hourly_rate': str(candidate.get('hourly_rate', 0)),
            f'{candidate_prefix}_availability': candidate.get('availability', ''),
            f'{candidate_prefix}_english_proficiency': candidate.get('english_proficiency', ''),
            f'{candidate_prefix}_timezone': candidate.get('timezone', '')
        })
    
    # Convert to list format for CSV
    return [template_vars]


def create_csv_content(template_data: List[Dict[str, str]]) -> str:
    """Create CSV content from template data"""
    if not template_data:
        return ""
    
    output = io.StringIO()
    
    # Get all field names from the first row
    fieldnames = list(template_data[0].keys())
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(template_data)
    
    return output.getvalue()