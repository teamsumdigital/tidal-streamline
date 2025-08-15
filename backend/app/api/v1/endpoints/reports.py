"""
Report Generation API Endpoints
Generate professional Tidal-branded market scan reports
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json

from ....core.database import get_database
from ....services.report_generator import TidalReportGenerator
from ....core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

class ReportGenerationRequest(BaseModel):
    scan_id: str
    client_name: Optional[str] = None
    report_format: str = "canva"  # canva, pdf, pptx
    include_candidate_profiles: bool = True
    custom_branding: Optional[Dict[str, Any]] = None

class ReportGenerationResponse(BaseModel):
    success: bool
    report_id: Optional[str] = None
    report_url: Optional[str] = None
    preview_url: Optional[str] = None
    download_url: Optional[str] = None
    pages: Optional[int] = None
    generated_at: str
    client_name: Optional[str] = None
    role_title: Optional[str] = None
    error: Optional[str] = None

@router.post("/generate", response_model=ReportGenerationResponse)
async def generate_market_scan_report(
    request: ReportGenerationRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_database)
):
    """
    Generate professional market scan report from scan data
    
    Args:
        request: Report generation parameters
        background_tasks: FastAPI background task handler
        db: Database connection
        
    Returns:
        Report generation response with URLs and metadata
    """
    try:
        logger.info(f"Starting report generation for scan ID: {request.scan_id}")
        
        # Fetch market scan data from database
        scan_data = await get_market_scan_data(db, request.scan_id)
        if not scan_data:
            raise HTTPException(status_code=404, detail="Market scan not found")
        
        # Override client name if provided
        if request.client_name:
            if 'client_info' not in scan_data:
                scan_data['client_info'] = {}
            scan_data['client_info']['client_name'] = request.client_name
        
        # Apply custom branding if provided
        if request.custom_branding:
            scan_data['custom_branding'] = request.custom_branding
        
        # Initialize report generator
        report_generator = TidalReportGenerator()
        
        # Generate report asynchronously
        report_result = await report_generator.generate_market_scan_report(scan_data)
        
        if report_result['success']:
            # Store report metadata in database
            report_record = await save_report_record(db, {
                "scan_id": request.scan_id,
                "report_url": report_result['report_url'],
                "preview_url": report_result['preview_url'],
                "client_name": report_result['client_name'],
                "role_title": report_result['role_title'],
                "pages": report_result['pages'],
                "generated_at": report_result['generated_at'],
                "format": request.report_format
            })
            
            return ReportGenerationResponse(
                success=True,
                report_id=str(report_record['id']),
                report_url=report_result['report_url'],
                preview_url=report_result['preview_url'],
                download_url=report_result['report_url'],
                pages=report_result['pages'],
                generated_at=report_result['generated_at'],
                client_name=report_result['client_name'],
                role_title=report_result['role_title']
            )
        else:
            logger.error(f"Report generation failed: {report_result.get('error')}")
            return ReportGenerationResponse(
                success=False,
                generated_at=report_result['generated_at'],
                error=report_result.get('error', 'Unknown error occurred')
            )
            
    except Exception as e:
        logger.error(f"Report generation endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/status/{report_id}")
async def get_report_status(report_id: str, db=Depends(get_database)):
    """
    Get status and details of generated report
    
    Args:
        report_id: Report record ID
        db: Database connection
        
    Returns:
        Report status and metadata
    """
    try:
        report_record = await get_report_record(db, report_id)
        if not report_record:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "report_id": report_id,
            "status": "completed",
            "report_url": report_record['report_url'],
            "preview_url": report_record.get('preview_url'),
            "client_name": report_record['client_name'],
            "role_title": report_record['role_title'],
            "pages": report_record['pages'],
            "generated_at": report_record['generated_at'],
            "format": report_record['format']
        }
        
    except Exception as e:
        logger.error(f"Get report status error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get report status: {str(e)}")

@router.get("/download/{report_id}")
async def download_report(report_id: str, db=Depends(get_database)):
    """
    Get download URL for generated report
    
    Args:
        report_id: Report record ID
        db: Database connection
        
    Returns:
        Direct download URL
    """
    try:
        report_record = await get_report_record(db, report_id)
        if not report_record:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "download_url": report_record['report_url'],
            "filename": f"tidal-market-scan-{report_record['client_name']}-{report_id}.pdf",
            "generated_at": report_record['generated_at']
        }
        
    except Exception as e:
        logger.error(f"Download report error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get download URL: {str(e)}")

@router.get("/scan/{scan_id}/reports")
async def list_scan_reports(scan_id: str, db=Depends(get_database)):
    """
    List all reports generated for a specific market scan
    
    Args:
        scan_id: Market scan ID
        db: Database connection
        
    Returns:
        List of reports for the scan
    """
    try:
        reports = await get_scan_reports(db, scan_id)
        
        return {
            "success": True,
            "scan_id": scan_id,
            "reports": [
                {
                    "report_id": str(report['id']),
                    "report_url": report['report_url'],
                    "preview_url": report.get('preview_url'),
                    "client_name": report['client_name'],
                    "pages": report['pages'],
                    "generated_at": report['generated_at'],
                    "format": report['format']
                }
                for report in reports
            ],
            "total_reports": len(reports)
        }
        
    except Exception as e:
        logger.error(f"List scan reports error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list reports: {str(e)}")

@router.post("/template/preview")
async def preview_template_data(scan_id: str, db=Depends(get_database)):
    """
    Preview template data mapping without generating actual report
    Useful for debugging and template development
    
    Args:
        scan_id: Market scan ID
        db: Database connection
        
    Returns:
        Template data mapping preview
    """
    try:
        # Fetch market scan data
        scan_data = await get_market_scan_data(db, scan_id)
        if not scan_data:
            raise HTTPException(status_code=404, detail="Market scan not found")
        
        # Initialize report generator
        report_generator = TidalReportGenerator()
        
        # Get template data mapping
        template_data = report_generator._prepare_template_data(scan_data)
        
        return {
            "success": True,
            "scan_id": scan_id,
            "template_data": template_data,
            "data_fields": {
                "client_name": template_data['client_name'],
                "role_title": template_data['role_title'],
                "regions_count": len(template_data['regions']),
                "candidate_profiles_count": len(template_data['candidate_profiles']),
                "similar_roles_count": len(template_data['role_insights']['similar_roles']),
                "required_tools_count": len(template_data['role_insights']['required_tools'])
            }
        }
        
    except Exception as e:
        logger.error(f"Template preview error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to preview template: {str(e)}")

# Database helper functions

async def get_market_scan_data(db, scan_id: str) -> Optional[Dict[str, Any]]:
    """Fetch complete market scan data from database"""
    try:
        # Query market scan with all related data
        query = """
            SELECT 
                ms.*,
                ms.job_analysis::jsonb as job_analysis,
                ms.salary_recommendations::jsonb as salary_recommendations,
                ms.skills_recommendations::jsonb as skills_recommendations
            FROM market_scans ms 
            WHERE ms.id = %s
        """
        
        result = await db.fetch_one(query, [scan_id])
        if result:
            return dict(result)
        return None
        
    except Exception as e:
        logger.error(f"Database error fetching scan data: {str(e)}")
        raise

async def save_report_record(db, report_data: Dict[str, Any]) -> Dict[str, Any]:
    """Save generated report record to database"""
    try:
        query = """
            INSERT INTO generated_reports 
            (scan_id, report_url, preview_url, client_name, role_title, pages, generated_at, format)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, *
        """
        
        result = await db.fetch_one(query, [
            report_data['scan_id'],
            report_data['report_url'],
            report_data.get('preview_url'),
            report_data['client_name'],
            report_data['role_title'],
            report_data['pages'],
            report_data['generated_at'],
            report_data['format']
        ])
        
        return dict(result)
        
    except Exception as e:
        logger.error(f"Database error saving report record: {str(e)}")
        raise

async def get_report_record(db, report_id: str) -> Optional[Dict[str, Any]]:
    """Get report record by ID"""
    try:
        query = "SELECT * FROM generated_reports WHERE id = %s"
        result = await db.fetch_one(query, [report_id])
        if result:
            return dict(result)
        return None
        
    except Exception as e:
        logger.error(f"Database error fetching report record: {str(e)}")
        raise

async def get_scan_reports(db, scan_id: str) -> List[Dict[str, Any]]:
    """Get all reports for a specific scan"""
    try:
        query = """
            SELECT * FROM generated_reports 
            WHERE scan_id = %s 
            ORDER BY generated_at DESC
        """
        
        results = await db.fetch_all(query, [scan_id])
        return [dict(result) for result in results]
        
    except Exception as e:
        logger.error(f"Database error fetching scan reports: {str(e)}")
        raise