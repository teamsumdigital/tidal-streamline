#!/usr/bin/env python3
"""
Historical Data Population Script for Tidal Streamline
Populates Pinecone index with existing market scans from Supabase database.

This script:
1. Fetches all existing market_scans from the database
2. Generates embeddings for job titles and descriptions  
3. Upserts vectors to Pinecone with proper metadata
4. Handles batch processing for efficiency
5. Provides progress tracking and error recovery
"""

import sys
import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

# Add app directory to path for imports
sys.path.append(str(Path(__file__).parent))

from loguru import logger
from app.core.database import DatabaseManager
from app.services.embedding_service import EmbeddingService
from app.core.config import settings


class HistoricalDataPopulator:
    """Populate Pinecone with historical market scan data"""
    
    def __init__(self, dry_run: bool = False, batch_size: int = 50):
        """Initialize populator with database and embedding service"""
        self.dry_run = dry_run
        self.batch_size = batch_size
        
        # Initialize services
        self.db = DatabaseManager()
        self.embedding_service = EmbeddingService() if not dry_run else None
        
        # Statistics tracking
        self.stats = {
            "total_scans": 0,
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": None,
            "end_time": None
        }
        
        # Progress tracking
        self.processed_scan_ids = set()
        self.failed_scan_ids = set()
        
        logger.info(f"Initialized HistoricalDataPopulator (dry_run={dry_run}, batch_size={batch_size})")
    
    async def get_all_market_scans(self) -> List[Dict[str, Any]]:
        """Fetch all market scans from the database"""
        try:
            logger.info("Fetching all market scans from database...")
            
            # Get total count first
            count_result = self.db.client.table('market_scans').select('*', count='exact').execute()
            total_count = count_result.count
            
            logger.info(f"Found {total_count:,} total market scans")
            
            # Fetch all scans in batches to avoid memory issues
            all_scans = []
            offset = 0
            fetch_batch_size = 1000  # Larger batch for fetching
            
            while offset < total_count:
                logger.info(f"Fetching scans {offset:,} to {min(offset + fetch_batch_size, total_count):,}")
                
                batch_result = (
                    self.db.client
                    .table('market_scans')
                    .select('*')
                    .order('created_at', desc=False)  # Process oldest first
                    .range(offset, offset + fetch_batch_size - 1)
                    .execute()
                )
                
                if not batch_result.data:
                    break
                
                all_scans.extend(batch_result.data)
                offset += fetch_batch_size
                
                # Small delay to be nice to the database
                await asyncio.sleep(0.1)
            
            logger.info(f"Successfully fetched {len(all_scans):,} market scans")
            return all_scans
            
        except Exception as e:
            logger.error(f"Failed to fetch market scans: {e}")
            return []
    
    def validate_scan_data(self, scan: Dict[str, Any]) -> bool:
        """Validate that a scan has required data for embedding"""
        required_fields = ['id', 'job_title', 'job_description']
        
        for field in required_fields:
            if not scan.get(field):
                logger.warning(f"Scan {scan.get('id', 'unknown')} missing required field: {field}")
                return False
        
        # Check for minimum content length
        job_title = scan.get('job_title', '').strip()
        job_description = scan.get('job_description', '').strip()
        
        if len(job_title) < 3:
            logger.warning(f"Scan {scan['id']} has job_title too short: '{job_title}'")
            return False
            
        if len(job_description) < 10:
            logger.warning(f"Scan {scan['id']} has job_description too short")
            return False
        
        return True
    
    def extract_metadata_from_scan(self, scan: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant metadata from a market scan for Pinecone"""
        job_analysis = scan.get('job_analysis', {}) or {}
        
        # Handle job_analysis being stored as JSON string
        if isinstance(job_analysis, str):
            try:
                job_analysis = json.loads(job_analysis)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse job_analysis for scan {scan['id']}")
                job_analysis = {}
        
        return {
            "scan_id": scan['id'],
            "job_title": scan['job_title'],
            "company_domain": scan.get('company_domain', ''),
            "client_name": scan.get('client_name', ''),
            "client_email": scan.get('client_email', ''),
            "role_category": scan.get('role_category') or job_analysis.get('role_category', ''),
            "experience_level": scan.get('experience_level') or job_analysis.get('experience_level', ''),
            "complexity_score": scan.get('complexity_score') or job_analysis.get('complexity_score', 5),
            "status": scan.get('status', 'unknown'),
            "created_at": scan.get('created_at', ''),
            "processing_time_seconds": scan.get('processing_time_seconds', 0),
            "confidence_score": scan.get('confidence_score', 0),
            "similar_scans_count": scan.get('similar_scans_count', 0),
            # Extract arrays from job_analysis
            "must_have_skills": json.dumps(job_analysis.get('must_have_skills', [])),
            "recommended_regions": json.dumps(scan.get('recommended_regions', []) or job_analysis.get('recommended_regions', [])),
            "remote_work_suitability": job_analysis.get('remote_work_suitability', ''),
            "hiring_challenges": scan.get('hiring_challenges', '')[:500]  # Truncate long text
        }
    
    async def process_batch(self, batch: List[Dict[str, Any]]) -> Dict[str, int]:
        """Process a batch of market scans"""
        batch_stats = {"successful": 0, "failed": 0, "skipped": 0}
        
        for scan in batch:
            try:
                # Validate scan data
                if not self.validate_scan_data(scan):
                    batch_stats["skipped"] += 1
                    self.stats["skipped"] += 1
                    continue
                
                scan_id = scan['id']
                
                # Skip if already processed
                if scan_id in self.processed_scan_ids:
                    logger.debug(f"Skipping already processed scan: {scan_id}")
                    batch_stats["skipped"] += 1
                    self.stats["skipped"] += 1
                    continue
                
                job_title = scan['job_title']
                job_description = scan['job_description']
                
                logger.debug(f"Processing scan: {scan_id} - {job_title}")
                
                if self.dry_run:
                    # In dry run, just log what we would do
                    logger.info(f"[DRY RUN] Would process: {scan_id} - {job_title}")
                    batch_stats["successful"] += 1
                    self.stats["successful"] += 1
                    self.processed_scan_ids.add(scan_id)
                else:
                    # Extract metadata
                    metadata = self.extract_metadata_from_scan(scan)
                    
                    # Create embedding text
                    embedding_text = f"Job Title: {job_title}\n\nJob Description: {job_description}"
                    
                    # Generate embedding
                    embedding = await self.embedding_service.generate_embedding(embedding_text)
                    
                    # Prepare vector for Pinecone
                    vector_data = {
                        "id": scan_id,
                        "values": embedding,
                        "metadata": {
                            **metadata,
                            "embedding_text_preview": embedding_text[:200] + ("..." if len(embedding_text) > 200 else "")
                        }
                    }
                    
                    # Upsert to Pinecone
                    self.embedding_service.index.upsert(vectors=[vector_data])
                    
                    logger.debug(f"Successfully processed scan: {scan_id}")
                    batch_stats["successful"] += 1
                    self.stats["successful"] += 1
                    self.processed_scan_ids.add(scan_id)
                
            except Exception as e:
                logger.error(f"Failed to process scan {scan.get('id', 'unknown')}: {e}")
                batch_stats["failed"] += 1
                self.stats["failed"] += 1
                if scan.get('id'):
                    self.failed_scan_ids.add(scan['id'])
        
        return batch_stats
    
    async def populate_historical_data(self, resume_from_scan_id: Optional[str] = None) -> bool:
        """Main method to populate historical data"""
        try:
            self.stats["start_time"] = datetime.now()
            
            logger.info("🚀 Starting historical data population...")
            
            # Fetch all market scans
            all_scans = await self.get_all_market_scans()
            
            if not all_scans:
                logger.error("No market scans found to process")
                return False
            
            self.stats["total_scans"] = len(all_scans)
            
            # Filter scans if resuming from a specific point
            if resume_from_scan_id:
                logger.info(f"Resuming from scan ID: {resume_from_scan_id}")
                resume_index = None
                for i, scan in enumerate(all_scans):
                    if scan['id'] == resume_from_scan_id:
                        resume_index = i
                        break
                
                if resume_index is not None:
                    all_scans = all_scans[resume_index:]
                    logger.info(f"Resuming with {len(all_scans):,} remaining scans")
                else:
                    logger.warning(f"Resume scan ID {resume_from_scan_id} not found, processing all scans")
            
            # Process in batches
            total_batches = (len(all_scans) + self.batch_size - 1) // self.batch_size
            
            logger.info(f"Processing {len(all_scans):,} scans in {total_batches:,} batches of {self.batch_size}")
            
            for batch_num in range(total_batches):
                batch_start = batch_num * self.batch_size
                batch_end = min(batch_start + self.batch_size, len(all_scans))
                batch = all_scans[batch_start:batch_end]
                
                logger.info(f"Processing batch {batch_num + 1}/{total_batches} ({len(batch)} scans)")
                
                # Process batch
                batch_stats = await self.process_batch(batch)
                
                # Update overall stats
                self.stats["processed"] += len(batch)
                
                # Show progress
                progress_pct = (self.stats["processed"] / self.stats["total_scans"]) * 100
                logger.info(
                    f"Progress: {self.stats['processed']:,}/{self.stats['total_scans']:,} "
                    f"({progress_pct:.1f}%) - "
                    f"Successful: {batch_stats['successful']}, "
                    f"Failed: {batch_stats['failed']}, "
                    f"Skipped: {batch_stats['skipped']}"
                )
                
                # Small delay between batches to avoid overwhelming services
                if batch_num < total_batches - 1:
                    await asyncio.sleep(1)
            
            self.stats["end_time"] = datetime.now()
            
            # Log final results
            self._log_final_results()
            
            return self.stats["successful"] > 0
            
        except Exception as e:
            logger.error(f"Fatal error during historical data population: {e}")
            return False
    
    def _log_final_results(self):
        """Log final processing results"""
        duration = self.stats["end_time"] - self.stats["start_time"]
        
        logger.info("=" * 60)
        logger.info("📊 FINAL RESULTS")
        logger.info("=" * 60)
        logger.info(f"Total Scans Found: {self.stats['total_scans']:,}")
        logger.info(f"Scans Processed: {self.stats['processed']:,}")
        logger.info(f"Successfully Uploaded: {self.stats['successful']:,}")
        logger.info(f"Failed: {self.stats['failed']:,}")
        logger.info(f"Skipped: {self.stats['skipped']:,}")
        logger.info(f"Processing Time: {duration}")
        
        if self.stats["successful"] > 0:
            rate = self.stats["successful"] / duration.total_seconds()
            logger.info(f"Processing Rate: {rate:.2f} scans/second")
        
        if self.failed_scan_ids:
            logger.warning(f"Failed scan IDs ({len(self.failed_scan_ids)}): {list(self.failed_scan_ids)[:10]}...")
        
        success_rate = (self.stats["successful"] / max(self.stats["processed"], 1)) * 100
        logger.info(f"Success Rate: {success_rate:.1f}%")
        
        if self.dry_run:
            logger.info("🧪 DRY RUN COMPLETED - No data was actually uploaded to Pinecone")
        else:
            logger.success("✅ Historical data population completed!")
    
    async def verify_upload(self, sample_size: int = 5) -> bool:
        """Verify that data was uploaded correctly by checking a sample"""
        if self.dry_run:
            logger.info("Skipping verification in dry run mode")
            return True
        
        try:
            logger.info(f"Verifying upload by checking {sample_size} random samples...")
            
            # Get index stats
            stats = await self.embedding_service.get_index_stats()
            logger.info(f"Pinecone index now contains {stats.get('total_vector_count', 0):,} vectors")
            
            # Sample some processed scan IDs
            sample_ids = list(self.processed_scan_ids)[:sample_size]
            
            verification_passed = 0
            for scan_id in sample_ids:
                try:
                    # Try to retrieve the vector
                    vector_data = await self.embedding_service.get_scan_by_id(scan_id)
                    if vector_data:
                        logger.debug(f"✅ Verified scan {scan_id} exists in Pinecone")
                        verification_passed += 1
                    else:
                        logger.warning(f"❌ Scan {scan_id} not found in Pinecone")
                except Exception as e:
                    logger.error(f"❌ Error verifying scan {scan_id}: {e}")
            
            success_rate = (verification_passed / len(sample_ids)) * 100
            logger.info(f"Verification success rate: {verification_passed}/{len(sample_ids)} ({success_rate:.1f}%)")
            
            return success_rate >= 80  # Consider 80%+ success rate as passing
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return False


async def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Populate Pinecone with historical market scan data")
    parser.add_argument("--dry-run", action="store_true", help="Run without actually uploading to Pinecone")
    parser.add_argument("--batch-size", type=int, default=50, help="Number of scans to process per batch")
    parser.add_argument("--resume-from", type=str, help="Resume processing from specific scan ID")
    parser.add_argument("--verify", action="store_true", help="Verify upload after completion")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Log level")
    
    args = parser.parse_args()
    
    # Setup logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        level=args.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
    )
    
    # Also log to file
    log_file = Path(__file__).parent / "logs" / "populate_pinecone_historical.log"
    log_file.parent.mkdir(exist_ok=True)
    
    logger.add(
        log_file,
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
    )
    
    # Initialize populator
    populator = HistoricalDataPopulator(
        dry_run=args.dry_run,
        batch_size=args.batch_size
    )
    
    try:
        # Check database connection
        logger.info("Testing database connection...")
        if not await populator.db.test_connection():
            logger.error("❌ Database connection failed")
            return 1
        
        # Check Pinecone connection (if not dry run)
        if not args.dry_run:
            logger.info("Testing Pinecone connection...")
            try:
                stats = await populator.embedding_service.get_index_stats()
                logger.info(f"✅ Connected to Pinecone index with {stats.get('total_vector_count', 0):,} vectors")
            except Exception as e:
                logger.error(f"❌ Pinecone connection failed: {e}")
                logger.info("Hint: Run 'python scripts/setup_pinecone_index.py --create' first")
                return 1
        
        # Run population
        success = await populator.populate_historical_data(resume_from_scan_id=args.resume_from)
        
        if not success:
            logger.error("❌ Historical data population failed")
            return 1
        
        # Run verification if requested
        if args.verify and not args.dry_run:
            if await populator.verify_upload():
                logger.success("✅ Upload verification passed")
            else:
                logger.warning("⚠️  Upload verification had issues")
        
        logger.success("🎉 Population script completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("⚠️  Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    # Run the main function
    sys.exit(asyncio.run(main()))