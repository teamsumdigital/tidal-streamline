"""
Embedding Service - Handle OpenAI embeddings and Pinecone operations
"""

import asyncio
from typing import List, Dict, Any, Optional, Tuple
import openai
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings
from loguru import logger
import hashlib
import json


class EmbeddingService:
    """Service for generating embeddings and managing vector operations"""
    
    def __init__(self):
        """Initialize OpenAI and Pinecone clients"""
        try:
            # Initialize OpenAI client
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            # Initialize Pinecone client
            self.pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Get or create the index
            self.index_name = settings.PINECONE_INDEX_NAME
            self.embedding_model = settings.EMBEDDING_MODEL
            self.embedding_dimension = settings.EMBEDDING_DIMENSION
            
            # Initialize index connection
            self._initialize_index()
            
            logger.info("EmbeddingService initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize EmbeddingService: {str(e)}")
            raise
    
    def _initialize_index(self):
        """Initialize Pinecone index, create if doesn't exist"""
        try:
            # Check if index exists
            existing_indexes = [index.name for index in self.pinecone_client.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating Pinecone index: {self.index_name}")
                
                self.pinecone_client.create_index(
                    name=self.index_name,
                    dimension=self.embedding_dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                
                # Wait for index to be ready
                import time
                time.sleep(10)
            
            # Connect to index
            self.index = self.pinecone_client.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone index: {str(e)}")
            raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            # Clean and prepare text
            clean_text = self._clean_text_for_embedding(text)
            
            # Generate embedding
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=clean_text
            )
            
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with dimension: {len(embedding)}")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise
    
    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            # Clean texts
            clean_texts = [self._clean_text_for_embedding(text) for text in texts]
            
            # Generate embeddings in batch (more efficient)
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=clean_texts
            )
            
            embeddings = [data.embedding for data in response.data]
            logger.debug(f"Generated {len(embeddings)} embeddings")
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {str(e)}")
            raise
    
    def _clean_text_for_embedding(self, text: str) -> str:
        """Clean and prepare text for embedding generation"""
        # Remove excessive whitespace and normalize
        clean_text = " ".join(text.split())
        
        # Truncate if too long (OpenAI embedding models have token limits)
        max_chars = 8000  # Conservative limit
        if len(clean_text) > max_chars:
            clean_text = clean_text[:max_chars] + "..."
            logger.warning(f"Text truncated to {max_chars} characters for embedding")
        
        return clean_text
    
    def _generate_scan_id(self, job_title: str, job_description: str, company_domain: str) -> str:
        """Generate unique ID for a market scan"""
        content = f"{job_title}|{job_description}|{company_domain}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    async def upsert_market_scan(
        self, 
        scan_id: str,
        job_title: str, 
        job_description: str, 
        job_analysis: Dict[str, Any],
        company_domain: str,
        client_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Upsert a market scan to Pinecone"""
        try:
            # Create embedding text from job posting
            embedding_text = f"Job Title: {job_title}\n\nJob Description: {job_description}"
            
            # Generate embedding
            embedding = await self.generate_embedding(embedding_text)
            
            # Prepare metadata
            vector_metadata = {
                "scan_id": scan_id,
                "job_title": job_title,
                "company_domain": company_domain,
                "client_name": client_name,
                "role_category": job_analysis.get("role_category", ""),
                "experience_level": job_analysis.get("experience_level", ""),
                "complexity_score": job_analysis.get("complexity_score", 5),
                "remote_work_suitability": job_analysis.get("remote_work_suitability", ""),
                "must_have_skills": json.dumps(job_analysis.get("must_have_skills", [])),
                "recommended_regions": json.dumps(job_analysis.get("recommended_regions", [])),
                "created_at": metadata.get("created_at", "") if metadata else "",
                "embedding_text_preview": embedding_text[:200] + "..." if len(embedding_text) > 200 else embedding_text
            }
            
            # Add any additional metadata
            if metadata:
                vector_metadata.update(metadata)
            
            # Upsert to Pinecone
            self.index.upsert(
                vectors=[
                    {
                        "id": scan_id,
                        "values": embedding,
                        "metadata": vector_metadata
                    }
                ]
            )
            
            logger.info(f"Successfully upserted market scan to Pinecone: {scan_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upsert market scan to Pinecone: {str(e)}")
            return False
    
    async def find_similar_scans(
        self, 
        job_title: str, 
        job_description: str, 
        top_k: int = 5,
        similarity_threshold: float = 0.7,
        exclude_scan_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Find similar market scans based on job content"""
        try:
            # Create embedding text
            embedding_text = f"Job Title: {job_title}\n\nJob Description: {job_description}"
            
            # Generate embedding for the query
            query_embedding = await self.generate_embedding(embedding_text)
            
            # Prepare filter to exclude current scan if provided
            filter_dict = {}
            if exclude_scan_id:
                filter_dict = {"scan_id": {"$ne": exclude_scan_id}}
            
            # Query Pinecone
            query_response = self.index.query(
                vector=query_embedding,
                top_k=top_k + (1 if exclude_scan_id else 0),  # Get extra in case we need to exclude
                include_metadata=True,
                filter=filter_dict if filter_dict else None
            )
            
            # Process results
            similar_scans = []
            for match in query_response.matches:
                # Skip if below similarity threshold
                if match.score < similarity_threshold:
                    continue
                
                # Skip if this is the excluded scan (double-check)
                if exclude_scan_id and match.id == exclude_scan_id:
                    continue
                
                similar_scan = {
                    "scan_id": match.id,
                    "similarity_score": match.score,
                    "job_title": match.metadata.get("job_title", ""),
                    "company_domain": match.metadata.get("company_domain", ""),
                    "client_name": match.metadata.get("client_name", ""),
                    "role_category": match.metadata.get("role_category", ""),
                    "experience_level": match.metadata.get("experience_level", ""),
                    "complexity_score": match.metadata.get("complexity_score", 5),
                    "must_have_skills": json.loads(match.metadata.get("must_have_skills", "[]")),
                    "recommended_regions": json.loads(match.metadata.get("recommended_regions", "[]")),
                    "created_at": match.metadata.get("created_at", ""),
                    "embedding_preview": match.metadata.get("embedding_text_preview", "")
                }
                
                similar_scans.append(similar_scan)
            
            # Limit to requested number
            similar_scans = similar_scans[:top_k]
            
            logger.info(f"Found {len(similar_scans)} similar scans above threshold {similarity_threshold}")
            return similar_scans
            
        except Exception as e:
            logger.error(f"Failed to find similar scans: {str(e)}")
            return []
    
    async def get_scan_by_id(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific scan from Pinecone by ID"""
        try:
            # Fetch by ID
            response = self.index.fetch(ids=[scan_id])
            
            if scan_id not in response.vectors:
                return None
            
            vector = response.vectors[scan_id]
            
            return {
                "scan_id": scan_id,
                "job_title": vector.metadata.get("job_title", ""),
                "company_domain": vector.metadata.get("company_domain", ""),
                "client_name": vector.metadata.get("client_name", ""),
                "role_category": vector.metadata.get("role_category", ""),
                "experience_level": vector.metadata.get("experience_level", ""),
                "complexity_score": vector.metadata.get("complexity_score", 5),
                "must_have_skills": json.loads(vector.metadata.get("must_have_skills", "[]")),
                "recommended_regions": json.loads(vector.metadata.get("recommended_regions", "[]")),
                "created_at": vector.metadata.get("created_at", ""),
                "embedding_preview": vector.metadata.get("embedding_text_preview", "")
            }
            
        except Exception as e:
            logger.error(f"Failed to get scan by ID {scan_id}: {str(e)}")
            return None
    
    def delete_scan(self, scan_id: str) -> bool:
        """Delete a scan from Pinecone"""
        try:
            self.index.delete(ids=[scan_id])
            logger.info(f"Deleted scan from Pinecone: {scan_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete scan {scan_id}: {str(e)}")
            return False
    
    async def get_index_stats(self) -> Dict[str, Any]:
        """Get Pinecone index statistics"""
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vector_count": stats.total_vector_count,
                "index_fullness": stats.index_fullness,
                "dimension": stats.dimension
            }
            
        except Exception as e:
            logger.error(f"Failed to get index stats: {str(e)}")
            return {}


# Create global instance
embedding_service = EmbeddingService()