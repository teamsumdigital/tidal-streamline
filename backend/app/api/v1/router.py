"""
API v1 Router
Main router configuration for Tidal Streamline API endpoints
"""

from fastapi import APIRouter

from .endpoints import (
    market_scans,
    analysis, 
    recommendations,
    candidates,
    admin,
    reports
)

api_router = APIRouter()

# Market Scans endpoints
api_router.include_router(
    market_scans.router,
    prefix="/market-scans",
    tags=["market-scans"]
)

# Analysis endpoints  
api_router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["analysis"]
)

# Recommendations endpoints
api_router.include_router(
    recommendations.router,
    prefix="/recommendations", 
    tags=["recommendations"]
)

# Candidates endpoints
api_router.include_router(
    candidates.router,
    prefix="/candidates",
    tags=["candidates"]
)

# Admin endpoints
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"]
)

# Reports endpoints - NEW
api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["reports"]
)

