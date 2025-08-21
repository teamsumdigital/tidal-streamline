"""
Database connection and management for Tidal Streamline
"""

from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from loguru import logger
from app.core.config import settings

class DatabaseManager:
    """Manages Supabase database connections and operations"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client connection"""
        try:
            # Validate required environment variables first
            if not settings.SUPABASE_URL:
                raise ValueError("SUPABASE_URL environment variable is required")
            if not settings.SUPABASE_SERVICE_KEY:
                raise ValueError("SUPABASE_SERVICE_KEY environment variable is required")
                
            self.client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_KEY
            )
            logger.info("✅ Database connection initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize database connection: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Test database connectivity"""
        try:
            if not self.client:
                return False
            
            # Simple test query
            result = self.client.table('market_scans').select("count", count="exact").execute()
            logger.info("✅ Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection test failed: {e}")
            return False
    
    # Market Scans Operations
    async def create_market_scan(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new market scan record"""
        try:
            result = self.client.table('market_scans').insert(scan_data).execute()
            logger.info(f"✅ Created market scan: {result.data[0]['id']}")
            return result.data[0]
        except Exception as e:
            logger.error(f"❌ Failed to create market scan: {e}")
            raise
    
    async def get_market_scan(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a market scan by ID"""
        try:
            result = self.client.table('market_scans').select("*").eq('id', scan_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"❌ Failed to get market scan {scan_id}: {e}")
            return None
    
    async def get_market_scans(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieve multiple market scans with pagination"""
        try:
            result = (
                self.client
                .table('market_scans')
                .select("*")
                .order('created_at', desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            return result.data
        except Exception as e:
            logger.error(f"❌ Failed to get market scans: {e}")
            return []
    
    async def search_similar_scans(self, job_title: str, job_description: str) -> List[Dict[str, Any]]:
        """Search for similar market scans based on job details"""
        try:
            # Simple text search - can be enhanced with vector similarity later
            # Simple text search using ilike - simplified for now
            result = (
                self.client
                .table('market_scans')
                .select("*")
                .ilike('job_title', f'%{job_title}%')
                .limit(10)
                .execute()
            )
            return result.data
        except Exception as e:
            logger.error(f"❌ Failed to search similar scans: {e}")
            return []
    
    # Salary Benchmarks Operations
    async def get_salary_benchmarks(self, role_category: str, region: str = None) -> List[Dict[str, Any]]:
        """Get salary benchmarks for a role and region"""
        try:
            query = self.client.table('salary_benchmarks').select("*").eq('role_category', role_category)
            
            if region:
                query = query.eq('region', region)
            
            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"❌ Failed to get salary benchmarks: {e}")
            return []
    
    async def create_salary_benchmark(self, benchmark_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new salary benchmark"""
        try:
            result = self.client.table('salary_benchmarks').insert(benchmark_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"❌ Failed to create salary benchmark: {e}")
            raise
    
    async def update_market_scan(self, scan_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing market scan"""
        try:
            result = self.client.table('market_scans').update(update_data).eq('id', scan_id).execute()
            logger.info(f"✅ Updated market scan {scan_id}")
            return result.data[0] if result.data else {}
        except Exception as e:
            logger.error(f"❌ Failed to update market scan {scan_id}: {e}")
            raise
    
    # Role Management Operations
    async def get_role_mappings(self) -> List[Dict[str, Any]]:
        """Get all role mappings and standardizations"""
        try:
            result = self.client.table('roles').select("*").execute()
            return result.data
        except Exception as e:
            logger.error(f"❌ Failed to get role mappings: {e}")
            return []
    
    async def find_role_by_title(self, job_title: str) -> Optional[Dict[str, Any]]:
        """Find role mapping by job title"""
        try:
            result = (
                self.client
                .table('roles')
                .select("*")
                .or_(f"core_role.ilike.%{job_title}%,common_titles.cs.{{{job_title}}}")
                .limit(1)
                .execute()
            )
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"❌ Failed to find role by title: {e}")
            return None
    
    # Candidate Profiles Operations
    async def get_candidate_profiles(self, role_category: str = None) -> List[Dict[str, Any]]:
        """Get candidate profiles, optionally filtered by role"""
        try:
            query = self.client.table('candidate_profiles').select("*")
            
            if role_category:
                query = query.eq('role_category', role_category)
            
            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"❌ Failed to get candidate profiles: {e}")
            return []
    
    # Generated Reports Operations
    async def save_report_record(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save generated report record to database"""
        try:
            result = self.client.table('generated_reports').insert(report_data).execute()
            logger.info(f"✅ Saved report record: {result.data[0]['id']}")
            return result.data[0]
        except Exception as e:
            logger.error(f"❌ Failed to save report record: {e}")
            raise
    
    async def get_report_record(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get report record by ID"""
        try:
            result = self.client.table('generated_reports').select("*").eq('id', report_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"❌ Failed to get report record {report_id}: {e}")
            return None
    
    async def get_scan_reports(self, scan_id: str) -> List[Dict[str, Any]]:
        """Get all reports for a specific scan"""
        try:
            result = (
                self.client
                .table('generated_reports')
                .select("*")
                .eq('scan_id', scan_id)
                .order('created_at', desc=True)
                .execute()
            )
            return result.data
        except Exception as e:
            logger.error(f"❌ Failed to get scan reports for {scan_id}: {e}")
            return []
    
    async def get_all_candidate_profiles(self) -> List[Dict[str, Any]]:
        """Get all candidate profiles from database for template generation"""
        try:
            result = (
                self.client
                .table('candidate_profiles')
                .select("*")
                .execute()
            )
            return result.data
        except Exception as e:
            logger.error(f"❌ Failed to get candidate profiles: {e}")
            return []

# Global database instance (lazy initialization)
_db_instance = None

def get_database() -> DatabaseManager:
    """Get or create the database manager instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance

def get_supabase_client() -> Client:
    """Get the Supabase client instance"""
    return get_database().client

# Maintain backward compatibility
db = None  # Will be initialized when first accessed