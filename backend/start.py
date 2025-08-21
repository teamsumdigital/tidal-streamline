"""
Production startup script for Render deployment
"""
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Tidal Streamline API on port {port}")
    print(f"📊 Debug mode: {os.getenv('DEBUG_MODE', 'true')}")
    print(f"🔗 CORS origins: {os.getenv('CORS_ORIGINS', 'localhost')}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        access_log=True,
        log_level="info"
    )