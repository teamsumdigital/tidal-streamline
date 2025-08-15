#!/usr/bin/env python3
"""
Database setup script for Tidal Streamline
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from loguru import logger

# Add parent directory to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings

def main():
    """
    Setup and initialize the Tidal Streamline database
    """
    logger.info("🚀 Setting up Tidal Streamline database...")
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Verify environment variables
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            logger.error("❌ Missing required environment variables:")
            logger.error("   - SUPABASE_URL")
            logger.error("   - SUPABASE_SERVICE_KEY")
            logger.error("   Please check your .env file")
            return False
        
        # Connect to Supabase
        logger.info("🔌 Connecting to Supabase...")
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        
        # Test connection
        logger.info("🧪 Testing database connection...")
        test_result = supabase.table('market_scans').select("count", count="exact").execute()
        logger.info("✅ Database connection successful!")
        
        # Read and execute schema
        schema_file = Path(__file__).parent.parent.parent / "database" / "schema.sql"
        
        if not schema_file.exists():
            logger.error(f"❌ Schema file not found: {schema_file}")
            return False
        
        logger.info("📄 Reading database schema...")
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Note: Supabase Python client doesn't directly execute SQL
        # Users need to run the SQL in the Supabase dashboard
        logger.info("📋 Database schema ready!")
        logger.info("👉 Please execute the following SQL in your Supabase dashboard:")
        logger.info(f"   File location: {schema_file}")
        logger.info("   Dashboard: https://app.supabase.com -> SQL Editor")
        
        # Verify tables exist (basic check)
        logger.info("🔍 Checking if tables exist...")
        try:
            tables_to_check = ['market_scans', 'roles', 'salary_benchmarks', 'candidate_profiles']
            for table in tables_to_check:
                result = supabase.table(table).select("count", count="exact").execute()
                count = result.count if hasattr(result, 'count') else 0
                logger.info(f"   ✅ {table}: {count} records")
        except Exception as e:
            logger.warning(f"⚠️  Tables may not exist yet: {e}")
            logger.info("   This is normal if you haven't run the schema SQL yet")
        
        logger.info("✅ Database setup completed!")
        logger.info("🎯 Next steps:")
        logger.info("   1. Copy .env.example to .env")
        logger.info("   2. Update .env with your actual credentials")
        logger.info("   3. Run the schema.sql in Supabase dashboard")
        logger.info("   4. Start the API server with: uvicorn main:app --reload --port 8008")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)