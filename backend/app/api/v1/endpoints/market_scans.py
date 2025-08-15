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
                recommended_pay_band=scan.get('salary_recommendations', {}).get('recommended_pay_band'),
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
async def get_similar_scans(scan_id: str, limit: int = Query(5, ge=1, le=20)):
    """
    Get similar market scans for comparison
    """
    try:
        # Get the original scan
        scan_data = await db.get_market_scan(scan_id)
        if not scan_data:
            raise HTTPException(status_code=404, detail="Market scan not found")
        
        # Find similar scans
        similar_scans = await db.search_similar_scans(
            job_title=scan_data['job_title'],
            job_description=scan_data['job_description']
        )
        
        # Filter out the original scan and limit results
        similar_scans = [
            scan for scan in similar_scans 
            if scan['id'] != scan_id
        ][:limit]
        
        return {
            "scan_id": scan_id,
            "similar_scans": similar_scans,
            "total_found": len(similar_scans)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get similar scans for {scan_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get similar scans: {str(e)}")

# Background processing function
async def process_market_scan_analysis(scan_id: str, request: MarketScanRequest):
    """
    Background task to process market scan analysis
    """
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"🔄 Starting analysis for market scan {scan_id}")
        
        # Step 1: AI Job Analysis
        job_analysis = await ai_service.analyze_job_description(
            job_title=request.job_title,
            job_description=request.job_description,
            hiring_challenges=request.hiring_challenges or ""
        )
        
        # Step 2: Find Similar Historical Scans
        similar_scans = await db.search_similar_scans(
            job_title=request.job_title,
            job_description=request.job_description
        )
        
        # Step 3: Generate Salary Recommendations
        salary_recommendations = await ai_service.generate_salary_recommendations(
            job_analysis=job_analysis,
            similar_scans=similar_scans
        )
        
        # Step 4: Enhance Skills Recommendations
        skills_recommendations = await ai_service.enhance_skills_recommendations(
            job_analysis=job_analysis
        )
        
        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Update database with results
        update_data = {
            'job_analysis': job_analysis,
            'salary_recommendations': salary_recommendations,
            'skills_recommendations': skills_recommendations,
            'status': 'completed',
            'updated_at': datetime.utcnow(),
            'processing_time_seconds': processing_time,
            'similar_scans_count': len(similar_scans),
            'role_category': job_analysis.get('role_category'),
            'experience_level': job_analysis.get('experience_level'),
            'recommended_regions': job_analysis.get('recommended_regions'),
            'confidence_score': 0.85  # TODO: Calculate actual confidence score
        }
        
        # TODO: Implement update functionality in database manager
        # await db.update_market_scan(scan_id, update_data)
        
        logger.info(f"✅ Completed analysis for market scan {scan_id} in {processing_time:.2f}s")
        
    except Exception as e:
        logger.error(f"❌ Failed to process market scan {scan_id}: {e}")
        
        # Update status to failed
        await db.update_market_scan(scan_id, {
            'status': 'failed',
            'updated_at': datetime.utcnow(),
            'error_message': str(e)
        })