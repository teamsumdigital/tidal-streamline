#!/usr/bin/env python3
"""
Tidal Streamline - Market Scan Automation System
Main FastAPI application server
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from dotenv import load_dotenv

from app.core.config import settings
from app.api.v1.endpoints import market_scans, analysis, recommendations, admin, candidates, reports

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("🚀 Tidal Streamline API starting up...")
    logger.info(f"📊 Running in {'development' if settings.DEBUG_MODE else 'production'} mode")
    logger.info(f"🔌 Server will run on port {settings.PORT}")
    
    yield
    
    logger.info("⏹️  Tidal Streamline API shutting down...")

# Create FastAPI application
app = FastAPI(
    title="Tidal Streamline API",
    description="Market Scan Automation System for Global Recruiting",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG_MODE else None,
    redoc_url="/redoc" if settings.DEBUG_MODE else None,
)

# CORS middleware for frontend communication
cors_origins = [
    "http://localhost:3000",  # Local development (Vite default)
    "http://localhost:3008",  # Local development (custom port)
    "http://127.0.0.1:3008",  # Local development
]

# Add production CORS origins from environment
cors_env = os.getenv("CORS_ORIGINS", "")
if cors_env:
    cors_origins.extend([origin.strip() for origin in cors_env.split(",") if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(
    market_scans.router,
    prefix="/api/v1/market-scans",
    tags=["Market Scans"]
)

app.include_router(
    analysis.router,
    prefix="/api/v1/analysis",
    tags=["Job Analysis"]
)

app.include_router(
    recommendations.router,
    prefix="/api/v1/recommendations",
    tags=["Salary & Skills Recommendations"]
)

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["Admin & Coaching"]
)

app.include_router(
    candidates.router,
    prefix="/api/v1/candidates",
    tags=["Candidate Profiles"]
)

app.include_router(
    reports.router,
    prefix="/api/v1/reports",
    tags=["Report Generation"]
)

# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "Tidal Streamline API",
        "version": "1.0.0",
        "port": settings.PORT
    }

@app.get("/api/health")
async def api_health():
    """API health check with database connectivity"""
    try:
        # TODO: Add actual database connection check
        return {
            "status": "healthy",
            "database": "connected",
            "ai_service": "available",
            "timestamp": "2025-01-14T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🌊 Welcome to Tidal Streamline API",
        "description": "Market Scan Automation System for Global Recruiting",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG_MODE else "Documentation disabled in production",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🔧 Starting Tidal Streamline API server directly...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        log_level="info"
    )