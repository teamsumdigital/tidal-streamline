#!/usr/bin/env python3
"""
Pinecone Index Setup Script for Tidal Streamline
Creates and configures the Pinecone vector index for market scan similarity search.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from pinecone import Pinecone, ServerlessSpec
from loguru import logger
from app.core.config import settings

class PineconeIndexSetup:
    """Handle Pinecone index creation and configuration"""
    
    def __init__(self):
        """Initialize Pinecone client"""
        try:
            self.pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index_name = settings.PINECONE_INDEX_NAME
            self.embedding_dimension = settings.EMBEDDING_DIMENSION
            logger.info("Pinecone client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone client: {e}")
            raise
    
    def check_index_exists(self) -> bool:
        """Check if the index already exists"""
        try:
            existing_indexes = [index.name for index in self.pinecone_client.list_indexes()]
            return self.index_name in existing_indexes
        except Exception as e:
            logger.error(f"Failed to check existing indexes: {e}")
            return False
    
    def create_index(self, force_recreate: bool = False) -> bool:
        """Create the Pinecone index"""
        try:
            # Check if index exists
            if self.check_index_exists():
                if not force_recreate:
                    logger.info(f"Index '{self.index_name}' already exists. Use --force-recreate to delete and recreate.")
                    return True
                else:
                    logger.info(f"Deleting existing index '{self.index_name}'...")
                    self.pinecone_client.delete_index(self.index_name)
                    
                    # Wait for deletion to complete
                    import time
                    logger.info("Waiting for index deletion to complete...")
                    time.sleep(30)
            
            logger.info(f"Creating Pinecone index '{self.index_name}' with {self.embedding_dimension} dimensions...")
            
            # Create index with serverless configuration
            self.pinecone_client.create_index(
                name=self.index_name,
                dimension=self.embedding_dimension,
                metric="cosine",  # Best for semantic similarity
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"  # Choose region closest to your users
                )
            )
            
            logger.info("Index created successfully. Waiting for it to be ready...")
            
            # Wait for index to be ready
            import time
            time.sleep(20)
            
            # Verify index is ready
            if self.verify_index():
                logger.success(f"✅ Pinecone index '{self.index_name}' is ready!")
                return True
            else:
                logger.error("❌ Index creation failed verification")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to create index: {e}")
            return False
    
    def verify_index(self) -> bool:
        """Verify the index is working correctly"""
        try:
            index = self.pinecone_client.Index(self.index_name)
            
            # Get index stats
            stats = index.describe_index_stats()
            logger.info(f"Index stats - Total vectors: {stats.total_vector_count}, Dimension: {stats.dimension}")
            
            # Verify dimension matches our configuration
            if stats.dimension != self.embedding_dimension:
                logger.error(f"Dimension mismatch: expected {self.embedding_dimension}, got {stats.dimension}")
                return False
            
            logger.success("✅ Index verification successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Index verification failed: {e}")
            return False
    
    def get_index_info(self) -> dict:
        """Get detailed index information"""
        try:
            if not self.check_index_exists():
                return {"error": "Index does not exist"}
            
            index = self.pinecone_client.Index(self.index_name)
            stats = index.describe_index_stats()
            
            return {
                "name": self.index_name,
                "dimension": stats.dimension,
                "total_vector_count": stats.total_vector_count,
                "index_fullness": stats.index_fullness,
                "status": "ready" if stats.dimension > 0 else "initializing"
            }
            
        except Exception as e:
            logger.error(f"Failed to get index info: {e}")
            return {"error": str(e)}
    
    def delete_index(self) -> bool:
        """Delete the index (use with caution!)"""
        try:
            if not self.check_index_exists():
                logger.warning(f"Index '{self.index_name}' does not exist")
                return True
            
            logger.warning(f"Deleting index '{self.index_name}'...")
            self.pinecone_client.delete_index(self.index_name)
            
            logger.info("Index deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete index: {e}")
            return False


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Pinecone index for Tidal Streamline")
    parser.add_argument("--create", action="store_true", help="Create the index")
    parser.add_argument("--force-recreate", action="store_true", help="Delete and recreate the index")
    parser.add_argument("--info", action="store_true", help="Show index information")
    parser.add_argument("--delete", action="store_true", help="Delete the index (DANGEROUS)")
    parser.add_argument("--verify", action="store_true", help="Verify index is working")
    
    args = parser.parse_args()
    
    # Setup logging
    logger.add(
        "logs/pinecone_setup.log",
        rotation="1 day",
        retention="7 days",
        level="INFO"
    )
    
    setup = PineconeIndexSetup()
    
    try:
        if args.info:
            logger.info("Getting index information...")
            info = setup.get_index_info()
            
            if "error" in info:
                logger.error(f"Error: {info['error']}")
                return 1
            
            logger.info("📊 Index Information:")
            logger.info(f"  Name: {info['name']}")
            logger.info(f"  Dimension: {info['dimension']}")
            logger.info(f"  Total Vectors: {info['total_vector_count']:,}")
            logger.info(f"  Index Fullness: {info['index_fullness']:.2%}")
            logger.info(f"  Status: {info['status']}")
            
        elif args.delete:
            logger.warning("⚠️  DELETE OPERATION - This will permanently remove all vectors!")
            confirm = input("Type 'DELETE' to confirm: ")
            if confirm == "DELETE":
                if setup.delete_index():
                    logger.success("✅ Index deleted successfully")
                    return 0
                else:
                    logger.error("❌ Failed to delete index")
                    return 1
            else:
                logger.info("Delete operation cancelled")
                return 0
                
        elif args.verify:
            logger.info("Verifying index...")
            if setup.verify_index():
                logger.success("✅ Index verification passed")
                return 0
            else:
                logger.error("❌ Index verification failed")
                return 1
                
        elif args.create or args.force_recreate:
            logger.info("Creating Pinecone index...")
            if setup.create_index(force_recreate=args.force_recreate):
                logger.success("✅ Index setup completed successfully!")
                
                # Show final info
                info = setup.get_index_info()
                logger.info("\n📊 Final Index Configuration:")
                logger.info(f"  Name: {info['name']}")
                logger.info(f"  Dimension: {info['dimension']}")
                logger.info(f"  Ready for embeddings: {info['status'] == 'ready'}")
                
                return 0
            else:
                logger.error("❌ Index setup failed")
                return 1
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())