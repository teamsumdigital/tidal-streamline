#!/usr/bin/env python3
"""
Pinecone Data Management Utility for Tidal Streamline
Provides easy commands to manage Pinecone index and data population.
"""

import sys
import asyncio
from pathlib import Path

# Add app directory to path for imports
sys.path.append(str(Path(__file__).parent))

from loguru import logger
from app.core.database import DatabaseManager
from app.services.embedding_service import EmbeddingService
from scripts.setup_pinecone_index import PineconeIndexSetup


class PineconeDataManager:
    """Utility class for managing Pinecone data operations"""
    
    def __init__(self):
        """Initialize manager with services"""
        self.db = DatabaseManager()
        self.embedding_service = None
        self.index_setup = PineconeIndexSetup()
    
    async def get_database_stats(self) -> dict:
        """Get statistics about data in the database"""
        try:
            # Total market scans
            total_result = self.db.client.table('market_scans').select('*', count='exact').execute()
            total_scans = total_result.count
            
            # Completed scans
            completed_result = (
                self.db.client
                .table('market_scans')
                .select('*', count='exact')
                .eq('status', 'completed')
                .execute()
            )
            completed_scans = completed_result.count
            
            # Scans by status
            status_counts = {}
            status_result = (
                self.db.client
                .rpc('get_scan_status_counts')
                .execute()
            )
            
            # If the RPC doesn't exist, get status counts manually
            if not status_result.data:
                statuses = ['pending', 'analyzing', 'completed', 'failed']
                for status in statuses:
                    count_result = (
                        self.db.client
                        .table('market_scans')
                        .select('*', count='exact')
                        .eq('status', status)
                        .execute()
                    )
                    status_counts[status] = count_result.count
            else:
                status_counts = {item['status']: item['count'] for item in status_result.data}
            
            # Recent scans (last 7 days)
            from datetime import datetime, timedelta
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            recent_result = (
                self.db.client
                .table('market_scans')
                .select('*', count='exact')
                .gte('created_at', week_ago)
                .execute()
            )
            recent_scans = recent_result.count
            
            return {
                'total_scans': total_scans,
                'completed_scans': completed_scans,
                'recent_scans': recent_scans,
                'status_counts': status_counts
            }
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}
    
    async def get_pinecone_stats(self) -> dict:
        """Get statistics about data in Pinecone"""
        try:
            # Initialize embedding service if not already done
            if not self.embedding_service:
                self.embedding_service = EmbeddingService()
            
            stats = await self.embedding_service.get_index_stats()
            
            # Get index info from setup utility
            index_info = self.index_setup.get_index_info()
            
            return {
                'index_exists': not ('error' in index_info),
                'total_vectors': stats.get('total_vector_count', 0),
                'index_fullness': stats.get('index_fullness', 0),
                'dimension': stats.get('dimension', 0),
                'index_name': self.index_setup.index_name
            }
            
        except Exception as e:
            logger.error(f"Failed to get Pinecone stats: {e}")
            return {
                'index_exists': False,
                'error': str(e)
            }
    
    async def show_status(self):
        """Show comprehensive status of database and Pinecone"""
        logger.info("🔍 Tidal Streamline - Pinecone Data Status")
        logger.info("=" * 50)
        
        # Database stats
        logger.info("📊 Database Statistics:")
        db_stats = await self.get_database_stats()
        
        if db_stats:
            logger.info(f"  Total Market Scans: {db_stats['total_scans']:,}")
            logger.info(f"  Completed Scans: {db_stats['completed_scans']:,}")
            logger.info(f"  Recent Scans (7 days): {db_stats['recent_scans']:,}")
            logger.info("  Status Breakdown:")
            for status, count in db_stats['status_counts'].items():
                logger.info(f"    {status.title()}: {count:,}")
        else:
            logger.error("  ❌ Failed to retrieve database statistics")
        
        logger.info("")
        
        # Pinecone stats
        logger.info("📊 Pinecone Statistics:")
        pinecone_stats = await self.get_pinecone_stats()
        
        if 'error' in pinecone_stats:
            logger.error(f"  ❌ Error: {pinecone_stats['error']}")
        elif pinecone_stats.get('index_exists'):
            logger.info(f"  Index Name: {pinecone_stats['index_name']}")
            logger.info(f"  Total Vectors: {pinecone_stats['total_vectors']:,}")
            logger.info(f"  Index Fullness: {pinecone_stats['index_fullness']:.2%}")
            logger.info(f"  Dimension: {pinecone_stats['dimension']}")
            
            # Calculate sync status
            if db_stats and pinecone_stats['total_vectors'] > 0:
                sync_pct = (pinecone_stats['total_vectors'] / max(db_stats['completed_scans'], 1)) * 100
                logger.info(f"  Sync Status: {sync_pct:.1f}% of completed scans")
                
                if sync_pct < 50:
                    logger.warning("  ⚠️  Low sync percentage - consider running population script")
                elif sync_pct >= 95:
                    logger.success("  ✅ Well synchronized with database")
        else:
            logger.warning("  ⚠️  Pinecone index does not exist")
            logger.info("  Run: python scripts/setup_pinecone_index.py --create")
        
        logger.info("")
        
        # Recommendations
        logger.info("💡 Recommendations:")
        
        if not pinecone_stats.get('index_exists'):
            logger.info("  1. Create Pinecone index: python scripts/setup_pinecone_index.py --create")
            logger.info("  2. Populate with data: python populate_pinecone_historical.py")
        elif db_stats and pinecone_stats.get('total_vectors', 0) < db_stats['completed_scans']:
            missing = db_stats['completed_scans'] - pinecone_stats['total_vectors']
            logger.info(f"  1. Populate missing {missing:,} scans: python populate_pinecone_historical.py")
        elif pinecone_stats.get('total_vectors', 0) == 0:
            logger.info("  1. Index is empty - populate with data: python populate_pinecone_historical.py")
        else:
            logger.success("  ✅ System appears to be well configured!")
    
    async def quick_test(self):
        """Run a quick test of the system"""
        logger.info("🧪 Running Quick System Test")
        logger.info("=" * 30)
        
        # Test database connection
        logger.info("Testing database connection...")
        if await self.db.test_connection():
            logger.success("  ✅ Database connection OK")
        else:
            logger.error("  ❌ Database connection failed")
            return False
        
        # Test Pinecone connection
        logger.info("Testing Pinecone connection...")
        try:
            if not self.embedding_service:
                self.embedding_service = EmbeddingService()
            
            stats = await self.embedding_service.get_index_stats()
            logger.success(f"  ✅ Pinecone connection OK ({stats.get('total_vector_count', 0):,} vectors)")
        except Exception as e:
            logger.error(f"  ❌ Pinecone connection failed: {e}")
            return False
        
        # Test embedding generation
        logger.info("Testing embedding generation...")
        try:
            test_embedding = await self.embedding_service.generate_embedding("Test job posting content")
            logger.success(f"  ✅ Embedding generation OK ({len(test_embedding)} dimensions)")
        except Exception as e:
            logger.error(f"  ❌ Embedding generation failed: {e}")
            return False
        
        logger.success("🎉 All tests passed!")
        return True


async def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage Pinecone data for Tidal Streamline")
    parser.add_argument("command", choices=["status", "test"], help="Command to run")
    
    args = parser.parse_args()
    
    # Setup logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
    )
    
    manager = PineconeDataManager()
    
    try:
        if args.command == "status":
            await manager.show_status()
        elif args.command == "test":
            success = await manager.quick_test()
            if not success:
                return 1
        
        return 0
        
    except KeyboardInterrupt:
        logger.warning("⚠️  Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))