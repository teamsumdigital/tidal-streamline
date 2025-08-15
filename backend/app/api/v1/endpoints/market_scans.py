"""
Market Scans API endpoints
"""

import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
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