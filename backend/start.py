"""
Production startup script for Render deployment
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_required_env_vars():
    """Validate that all required environment variables are present"""
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_KEY", 
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Print first few chars for verification (security safe)
            print(f"✅ {var}: {'*' * (len(value) - 8)}{value[-4:]}")
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please configure these in your Render dashboard:")
        for var in missing_vars:
            print(f"  - {var}")
        sys.exit(1)
    
    print("✅ All required environment variables are present")

if __name__ == "__main__":
    print("🔧 Validating environment configuration...")
    validate_required_env_vars()
    
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Tidal Streamline API on port {port}")
    print(f"📊 Debug mode: {os.getenv('DEBUG_MODE', 'false')}")
    print(f"🔗 CORS origins: {os.getenv('CORS_ORIGINS', 'localhost')}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        access_log=True,
        log_level="info"
    )