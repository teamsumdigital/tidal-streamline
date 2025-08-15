"""
Vector Search Service - Semantic matching and search functionality
"""

from typing import List, Dict, Any, Optional, Tuple
from app.services.embedding_service import embedding_service
from app.models.market_scan import MarketScanResponse, JobAnalysis, RoleCategory, ExperienceLevel, Region
from loguru import logger
import asyncio
from datetime import datetime, timedelta


class VectorSearchService:
    """Service for semantic search and matching of market scans"""
    
    def __init__(self):
        """Initialize the vector search service"""
        self.embedding_service = embedding_service
        
    async def find_similar_market_scans(
        self, 
        job_title: str,
        job_description: str,
        current_scan_id: Optional[str] = None,
        similarity_threshold: float = 0.75,
        max_results: int = 5
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Find similar market scans using semantic matching
        
        Returns:
            Tuple of (similar_scans, confidence_score)
        """
        try:
            logger.info(f"Searching for similar scans to: {job_title[:50]}...")
            
            # Find similar scans using embeddings
            similar_scans = await self.embedding_service.find_similar_scans(
                job_title=job_title,
                job_description=job_description,
                top_k=max_results,
                similarity_threshold=similarity_threshold,
                exclude_scan_id=current_scan_id
            )
            
            # Calculate confidence score based on similarity scores
            confidence_score = self._calculate_confidence_score(similar_scans)
            
            # Enrich similar scans with additional insights
            enriched_scans = await self._enrich_similar_scans(similar_scans)
            
            logger.info(f"Found {len(enriched_scans)} similar scans with confidence: {confidence_score:.2f}")
            
            return enriched_scans, confidence_score
            
        except Exception as e:
            logger.error(f"Error finding similar market scans: {str(e)}")
            return [], 0.0
    
    def _calculate_confidence_score(self, similar_scans: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on similarity results"""
        if not similar_scans:
            return 0.0
        
        # Use weighted average of top similarities
        total_weight = 0
        weighted_sum = 0
        
        for i, scan in enumerate(similar_scans[:3]):  # Focus on top 3
            weight = 1.0 / (i + 1)  # Decreasing weight
            weighted_sum += scan["similarity_score"] * weight
            total_weight += weight
        
        confidence = weighted_sum / total_weight if total_weight > 0 else 0.0
        return min(confidence, 1.0)  # Cap at 1.0
    
    async def _enrich_similar_scans(self, similar_scans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich similar scans with additional insights and analysis"""
        enriched_scans = []
        
        for scan in similar_scans:
            try:
                enriched_scan = {
                    **scan,
                    "match_reasons": self._analyze_match_reasons(scan),
                    "key_similarities": self._extract_key_similarities(scan),
                    "relevance_factors": self._calculate_relevance_factors(scan)
                }
                
                enriched_scans.append(enriched_scan)
                
            except Exception as e:
                logger.warning(f"Failed to enrich scan {scan.get('scan_id', 'unknown')}: {str(e)}")
                # Include original scan without enrichment
                enriched_scans.append(scan)
        
        return enriched_scans
    
    def _analyze_match_reasons(self, scan: Dict[str, Any]) -> List[str]:
        """Analyze why this scan is similar"""
        reasons = []
        
        # Role category match
        if scan.get("role_category"):
            reasons.append(f"Similar role: {scan['role_category']}")
        
        # Experience level match
        if scan.get("experience_level"):
            reasons.append(f"Same experience level: {scan['experience_level']}")
        
        # Complexity score similarity
        complexity = scan.get("complexity_score", 5)
        if complexity >= 7:
            reasons.append("High complexity role")
        elif complexity <= 3:
            reasons.append("Low complexity role")
        
        # Skills overlap
        skills = scan.get("must_have_skills", [])
        if len(skills) >= 4:
            reasons.append(f"Rich skill requirements ({len(skills)} skills)")
        
        # Remote work suitability
        remote_suitability = scan.get("remote_work_suitability", "")
        if remote_suitability:
            reasons.append(f"Remote work: {remote_suitability}")
        
        return reasons[:4]  # Limit to top 4 reasons
    
    def _extract_key_similarities(self, scan: Dict[str, Any]) -> List[str]:
        """Extract key similarity factors"""
        similarities = []
        
        # Company domain insights
        domain = scan.get("company_domain", "")
        if domain:
            similarities.append(f"Company: {domain}")
        
        # Recent scan indicator
        created_at = scan.get("created_at", "")
        if created_at:
            try:
                # Parse date and check if recent (within last 6 months)
                scan_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                if datetime.now().astimezone() - scan_date < timedelta(days=180):
                    similarities.append("Recent market scan")
            except:
                pass
        
        # Regional alignment
        regions = scan.get("recommended_regions", [])
        if regions:
            similarities.append(f"Regions: {', '.join(regions[:2])}")
        
        return similarities
    
    def _calculate_relevance_factors(self, scan: Dict[str, Any]) -> Dict[str, float]:
        """Calculate various relevance factors"""
        factors = {
            "similarity_score": scan.get("similarity_score", 0.0),
            "role_alignment": 0.0,
            "complexity_match": 0.0,
            "recency_score": 0.0
        }
        
        # Role alignment (based on role category match)
        if scan.get("role_category"):
            factors["role_alignment"] = 0.8  # High if we have role category
        
        # Complexity match (how well complexity scores align)
        complexity = scan.get("complexity_score", 5)
        # Normalize complexity to 0-1 scale
        factors["complexity_match"] = min(complexity / 10.0, 1.0)
        
        # Recency score (newer scans are more relevant)
        created_at = scan.get("created_at", "")
        if created_at:
            try:
                scan_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                days_old = (datetime.now().astimezone() - scan_date).days
                # Score decreases with age, max 1.0 for scans < 30 days old
                factors["recency_score"] = max(0.0, 1.0 - (days_old / 365.0))
            except:
                factors["recency_score"] = 0.5  # Default for unparseable dates
        
        return factors
    
    async def search_scans_by_criteria(
        self,
        role_category: Optional[str] = None,
        experience_level: Optional[str] = None,
        complexity_range: Optional[Tuple[int, int]] = None,
        regions: Optional[List[str]] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for scans matching specific criteria
        Note: This is a basic implementation. In production, you'd use Pinecone filtering.
        """
        try:
            # For now, we'll do a broad search and filter results
            # In production, this would use Pinecone's metadata filtering
            
            logger.info(f"Searching scans by criteria: role={role_category}, exp={experience_level}")
            
            # This is a placeholder implementation
            # In a real scenario, you'd use Pinecone's filter parameter in the query
            
            # Get index stats to understand available data
            stats = await self.embedding_service.get_index_stats()
            
            return {
                "message": "Criteria-based search not fully implemented",
                "available_vectors": stats.get("total_vector_count", 0),
                "criteria": {
                    "role_category": role_category,
                    "experience_level": experience_level,
                    "complexity_range": complexity_range,
                    "regions": regions
                }
            }
            
        except Exception as e:
            logger.error(f"Error in criteria-based search: {str(e)}")
            return []
    
    async def get_market_trends(self, lookback_days: int = 90) -> Dict[str, Any]:
        """
        Analyze market trends from vector data
        Note: This is a placeholder for trend analysis functionality
        """
        try:
            logger.info(f"Analyzing market trends for last {lookback_days} days")
            
            # Get index statistics
            stats = await self.embedding_service.get_index_stats()
            
            # In production, this would analyze the vector metadata
            # to identify trends in role categories, complexity, regions, etc.
            
            return {
                "total_scans": stats.get("total_vector_count", 0),
                "analysis_period": f"{lookback_days} days",
                "trends": {
                    "most_common_roles": ["Brand Marketing Manager", "Content Marketer", "Data Analyst"],
                    "popular_regions": ["Philippines", "Latin America", "United States"],
                    "average_complexity": 5.2,
                    "remote_suitability": "high"
                },
                "note": "This is sample trend data - full implementation would analyze actual vector metadata"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {str(e)}")
            return {}
    
    async def store_market_scan_vector(
        self,
        scan_id: str,
        job_title: str,
        job_description: str,
        job_analysis: JobAnalysis,
        company_domain: str,
        client_name: str,
        created_at: datetime
    ) -> bool:
        """Store a market scan in the vector database"""
        try:
            # Convert JobAnalysis to dict for storage
            analysis_dict = {
                "role_category": job_analysis.role_category.value,
                "experience_level": job_analysis.experience_level.value,
                "complexity_score": job_analysis.complexity_score,
                "remote_work_suitability": job_analysis.remote_work_suitability,
                "must_have_skills": job_analysis.must_have_skills,
                "recommended_regions": [region.value for region in job_analysis.recommended_regions],
                "years_experience_required": job_analysis.years_experience_required,
                "key_responsibilities": job_analysis.key_responsibilities,
                "unique_challenges": job_analysis.unique_challenges,
                "salary_factors": job_analysis.salary_factors
            }
            
            # Additional metadata
            metadata = {
                "created_at": created_at.isoformat()
            }
            
            # Store in Pinecone
            success = await self.embedding_service.upsert_market_scan(
                scan_id=scan_id,
                job_title=job_title,
                job_description=job_description,
                job_analysis=analysis_dict,
                company_domain=company_domain,
                client_name=client_name,
                metadata=metadata
            )
            
            if success:
                logger.info(f"Successfully stored market scan vector: {scan_id}")
            else:
                logger.error(f"Failed to store market scan vector: {scan_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error storing market scan vector: {str(e)}")
            return False


# Create global instance
vector_search_service = VectorSearchService()