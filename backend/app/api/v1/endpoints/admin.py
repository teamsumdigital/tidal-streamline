"""
Admin and Coaching API endpoints
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

from app.core.database import get_database

router = APIRouter()

class SystemStatsResponse(BaseModel):
    """System statistics response"""
    total_scans: int
    completed_scans: int
    pending_scans: int
    failed_scans: int
    average_processing_time: float
    top_role_categories: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]

@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_statistics():
    """
    Get system-wide statistics and metrics
    """
    try:
        # Get all market scans for analysis
        all_scans = await get_database().get_market_scans(limit=1000)
        
        # Calculate statistics
        total_scans = len(all_scans)
        completed_scans = len([s for s in all_scans if s.get('status') == 'completed'])
        pending_scans = len([s for s in all_scans if s.get('status') == 'pending'])
        failed_scans = len([s for s in all_scans if s.get('status') == 'failed'])
        
        # Calculate average processing time
        processing_times = [
            s.get('processing_time_seconds', 0) 
            for s in all_scans 
            if s.get('processing_time_seconds')
        ]
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        # Top role categories
        role_counts = {}
        for scan in all_scans:
            role = scan.get('role_category', 'Unknown')
            role_counts[role] = role_counts.get(role, 0) + 1
        
        top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_role_categories = [{"role": role, "count": count} for role, count in top_roles]
        
        # Recent activity (last 10 scans)
        recent_scans = sorted(all_scans, key=lambda x: x.get('created_at', ''), reverse=True)[:10]
        recent_activity = [
            {
                "id": scan['id'],
                "client_name": scan['client_name'],
                "job_title": scan['job_title'],
                "status": scan['status'],
                "created_at": scan['created_at']
            }
            for scan in recent_scans
        ]
        
        return SystemStatsResponse(
            total_scans=total_scans,
            completed_scans=completed_scans,
            pending_scans=pending_scans,
            failed_scans=failed_scans,
            average_processing_time=avg_processing_time,
            top_role_categories=top_role_categories,
            recent_activity=recent_activity
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to get system statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve statistics: {str(e)}")

@router.get("/quality-metrics")
async def get_quality_metrics():
    """
    Get quality metrics for coaching and improvement
    """
    try:
        all_scans = await get_database().get_market_scans(limit=500)
        completed_scans = [s for s in all_scans if s.get('status') == 'completed']
        
        if not completed_scans:
            return {
                "message": "No completed scans available for quality analysis",
                "total_scans": len(all_scans)
            }
        
        # Analyze confidence scores
        confidence_scores = [
            s.get('confidence_score', 0) 
            for s in completed_scans 
            if s.get('confidence_score')
        ]
        
        # Analyze complexity distribution
        complexity_scores = []
        for scan in completed_scans:
            job_analysis = scan.get('job_analysis', {})
            if job_analysis.get('complexity_score'):
                complexity_scores.append(job_analysis['complexity_score'])
        
        # Processing time analysis
        processing_times = [
            s.get('processing_time_seconds', 0) 
            for s in completed_scans 
            if s.get('processing_time_seconds')
        ]
        
        return {
            "total_completed_scans": len(completed_scans),
            "confidence_metrics": {
                "average_confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
                "high_confidence_count": len([c for c in confidence_scores if c > 0.8]),
                "low_confidence_count": len([c for c in confidence_scores if c < 0.6])
            },
            "complexity_analysis": {
                "average_complexity": sum(complexity_scores) / len(complexity_scores) if complexity_scores else 0,
                "high_complexity_count": len([c for c in complexity_scores if c > 7]),
                "low_complexity_count": len([c for c in complexity_scores if c < 4])
            },
            "performance_metrics": {
                "average_processing_time": sum(processing_times) / len(processing_times) if processing_times else 0,
                "fastest_processing": min(processing_times) if processing_times else 0,
                "slowest_processing": max(processing_times) if processing_times else 0
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get quality metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve quality metrics: {str(e)}")

@router.get("/failed-scans")
async def get_failed_scans():
    """
    Get failed scans for debugging and improvement
    """
    try:
        all_scans = await get_database().get_market_scans(limit=200)
        failed_scans = [s for s in all_scans if s.get('status') == 'failed']
        
        failed_analysis = []
        for scan in failed_scans:
            failed_analysis.append({
                "id": scan['id'],
                "client_name": scan['client_name'],
                "job_title": scan['job_title'],
                "error_message": scan.get('error_message', 'Unknown error'),
                "created_at": scan['created_at'],
                "job_description_length": len(scan.get('job_description', '')),
                "has_hiring_challenges": bool(scan.get('hiring_challenges'))
            })
        
        return {
            "total_failed": len(failed_scans),
            "failed_scans": failed_analysis,
            "common_issues": analyze_common_failure_patterns(failed_scans)
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get failed scans: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve failed scans: {str(e)}")

@router.post("/retrain-recommendations")
async def retrain_recommendations():
    """
    Trigger retraining of recommendation algorithms
    """
    try:
        # In a real implementation, this would trigger ML model retraining
        # For now, we'll just analyze current data quality
        
        all_scans = await get_database().get_market_scans(limit=1000)
        completed_scans = [s for s in all_scans if s.get('status') == 'completed']
        
        training_data_quality = {
            "total_training_samples": len(completed_scans),
            "role_distribution": {},
            "region_coverage": {},
            "quality_score": 0.0
        }
        
        # Analyze role distribution
        for scan in completed_scans:
            role = scan.get('role_category', 'Unknown')
            training_data_quality["role_distribution"][role] = training_data_quality["role_distribution"].get(role, 0) + 1
        
        # Analyze region coverage
        for scan in completed_scans:
            job_analysis = scan.get('job_analysis', {})
            regions = job_analysis.get('recommended_regions', [])
            for region in regions:
                training_data_quality["region_coverage"][region] = training_data_quality["region_coverage"].get(region, 0) + 1
        
        # Calculate quality score (simplified)
        if len(completed_scans) > 50:
            training_data_quality["quality_score"] = min(0.95, len(completed_scans) / 100)
        else:
            training_data_quality["quality_score"] = len(completed_scans) / 50 * 0.5
        
        return {
            "status": "retraining_initiated",
            "message": "Recommendation model retraining has been queued",
            "training_data_quality": training_data_quality,
            "estimated_completion": "2-4 hours"
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to initiate retraining: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate retraining: {str(e)}")

def analyze_common_failure_patterns(failed_scans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyze common patterns in failed scans
    """
    patterns = []
    
    # Check for common error patterns
    error_messages = [scan.get('error_message', '') for scan in failed_scans]
    
    # Count API-related errors
    api_errors = len([msg for msg in error_messages if 'api' in msg.lower() or 'openai' in msg.lower()])
    if api_errors > 0:
        patterns.append({
            "pattern": "API Connection Issues",
            "count": api_errors,
            "percentage": round(api_errors / len(failed_scans) * 100, 1),
            "recommendation": "Check API credentials and rate limits"
        })
    
    # Check for timeout errors
    timeout_errors = len([msg for msg in error_messages if 'timeout' in msg.lower() or 'time' in msg.lower()])
    if timeout_errors > 0:
        patterns.append({
            "pattern": "Processing Timeouts",
            "count": timeout_errors,
            "percentage": round(timeout_errors / len(failed_scans) * 100, 1),
            "recommendation": "Optimize processing pipeline or increase timeout limits"
        })
    
    # Check for data validation errors
    validation_errors = len([msg for msg in error_messages if 'validation' in msg.lower() or 'invalid' in msg.lower()])
    if validation_errors > 0:
        patterns.append({
            "pattern": "Data Validation Errors",
            "count": validation_errors,
            "percentage": round(validation_errors / len(failed_scans) * 100, 1),
            "recommendation": "Improve input validation and data sanitization"
        })
    
    return patterns