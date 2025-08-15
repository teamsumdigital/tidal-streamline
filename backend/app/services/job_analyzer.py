"""
Job Analyzer Service - AI-powered job analysis using OpenAI with semantic matching
"""

import openai
import os
import json
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from app.models.market_scan import JobAnalysis, RoleCategory, ExperienceLevel, Region
from app.services.vector_search import vector_search_service
from loguru import logger

class JobAnalyzer:
    """AI-powered job analysis service"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    async def analyze_job(self, job_title: str, job_description: str, hiring_challenges: str = None) -> JobAnalysis:
        """Analyze job posting and extract structured data"""
        
        prompt = self._create_analysis_prompt(job_title, job_description, hiring_challenges)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000
            )
            
            analysis_text = response.choices[0].message.content
            return self._parse_analysis_response(analysis_text)
            
        except Exception as e:
            logger.error(f"AI job analysis failed: {str(e)}")
            # Fallback to rule-based analysis if AI fails
            return self._fallback_analysis(job_title, job_description)
    
    async def analyze_job_with_similar_scans(
        self, 
        job_title: str, 
        job_description: str, 
        hiring_challenges: str = None,
        scan_id: Optional[str] = None
    ) -> Tuple[JobAnalysis, List[Dict[str, Any]], float]:
        """
        Analyze job and find similar historical scans using semantic matching
        
        Returns:
            Tuple of (job_analysis, similar_scans, confidence_score)
        """
        try:
            logger.info(f"Analyzing job with semantic matching: {job_title[:50]}...")
            
            # Perform standard job analysis
            job_analysis = await self.analyze_job(job_title, job_description, hiring_challenges)
            
            # Find similar scans using vector search
            similar_scans, confidence_score = await vector_search_service.find_similar_market_scans(
                job_title=job_title,
                job_description=job_description,
                current_scan_id=scan_id,
                similarity_threshold=0.70,  # Adjust threshold as needed
                max_results=5
            )
            
            # Enhance job analysis with insights from similar scans
            enhanced_analysis = await self._enhance_analysis_with_similar_scans(
                job_analysis, similar_scans
            )
            
            logger.info(f"Job analysis completed. Found {len(similar_scans)} similar scans with confidence: {confidence_score:.2f}")
            
            return enhanced_analysis, similar_scans, confidence_score
            
        except Exception as e:
            logger.error(f"Error in analyze_job_with_similar_scans: {str(e)}")
            # Fallback to basic analysis
            job_analysis = await self.analyze_job(job_title, job_description, hiring_challenges)
            return job_analysis, [], 0.0
    
    async def _enhance_analysis_with_similar_scans(
        self, 
        job_analysis: JobAnalysis, 
        similar_scans: List[Dict[str, Any]]
    ) -> JobAnalysis:
        """Enhance job analysis using insights from similar scans"""
        try:
            if not similar_scans:
                return job_analysis
            
            # Extract insights from similar scans
            similar_skills = set()
            similar_regions = set()
            complexity_scores = []
            
            for scan in similar_scans:
                # Collect skills from similar scans
                scan_skills = scan.get("must_have_skills", [])
                similar_skills.update(scan_skills)
                
                # Collect regions
                scan_regions = scan.get("recommended_regions", [])
                similar_regions.update(scan_regions)
                
                # Collect complexity scores
                complexity = scan.get("complexity_score", 5)
                complexity_scores.append(complexity)
            
            # Create enhanced job analysis
            enhanced_analysis = JobAnalysis(
                role_category=job_analysis.role_category,
                experience_level=job_analysis.experience_level,
                years_experience_required=job_analysis.years_experience_required,
                must_have_skills=job_analysis.must_have_skills,
                nice_to_have_skills=job_analysis.nice_to_have_skills,
                key_responsibilities=job_analysis.key_responsibilities,
                remote_work_suitability=job_analysis.remote_work_suitability,
                complexity_score=job_analysis.complexity_score,
                recommended_regions=job_analysis.recommended_regions,
                unique_challenges=job_analysis.unique_challenges,
                salary_factors=job_analysis.salary_factors
            )
            
            # Enhance with similar scan insights if they provide valuable additions
            if len(similar_scans) >= 2:  # Only enhance if we have good similar data
                # Add skills that appear in multiple similar scans but not in current analysis
                current_skills = set(job_analysis.must_have_skills + job_analysis.nice_to_have_skills)
                frequent_similar_skills = [skill for skill in similar_skills 
                                         if skill not in current_skills and 
                                         sum(1 for scan in similar_scans if skill in scan.get("must_have_skills", [])) >= 2]
                
                # Add up to 2 additional skills to nice_to_have
                enhanced_analysis.nice_to_have_skills.extend(frequent_similar_skills[:2])
                
                # Adjust complexity score based on similar scans (weighted average)
                if complexity_scores:
                    similar_avg_complexity = sum(complexity_scores) / len(complexity_scores)
                    # Blend original score (70%) with similar scans average (30%)
                    adjusted_complexity = int(job_analysis.complexity_score * 0.7 + similar_avg_complexity * 0.3)
                    enhanced_analysis.complexity_score = max(1, min(10, adjusted_complexity))
            
            return enhanced_analysis
            
        except Exception as e:
            logger.error(f"Error enhancing analysis with similar scans: {str(e)}")
            return job_analysis
    
    async def store_analysis_vector(
        self,
        scan_id: str,
        job_title: str,
        job_description: str,
        job_analysis: JobAnalysis,
        company_domain: str,
        client_name: str
    ) -> bool:
        """Store the job analysis in vector database for future semantic matching"""
        try:
            success = await vector_search_service.store_market_scan_vector(
                scan_id=scan_id,
                job_title=job_title,
                job_description=job_description,
                job_analysis=job_analysis,
                company_domain=company_domain,
                client_name=client_name,
                created_at=datetime.now()
            )
            
            if success:
                logger.info(f"Stored analysis vector for scan: {scan_id}")
            else:
                logger.warning(f"Failed to store analysis vector for scan: {scan_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error storing analysis vector: {str(e)}")
            return False
    
    def _create_analysis_prompt(self, job_title: str, job_description: str, hiring_challenges: str = None) -> str:
        """Create structured prompt for job analysis"""
        
        challenges_text = f"\nHiring Challenges: {hiring_challenges}" if hiring_challenges else ""
        
        return f"""
Analyze this job posting and return a JSON response with the following structure:

Job Title: {job_title}
Job Description: {job_description}{challenges_text}

Return JSON with these exact fields:
{{
    "role_category": "one of: Brand Marketing Manager, Community Manager, Content Marketer, Retention Manager, Ecommerce Manager, Sales Operations Manager, Data Analyst, Logistics Manager, Operations Manager",
    "experience_level": "one of: junior, mid, senior, expert",
    "years_experience_required": "e.g. 2-4 years, 5-8 years, 9+ years",
    "must_have_skills": ["list of 4-6 essential skills"],
    "nice_to_have_skills": ["list of 3-4 bonus skills"],
    "key_responsibilities": ["list of 4-5 main responsibilities"],
    "remote_work_suitability": "high, medium, or low",
    "complexity_score": "1-10 integer based on role complexity",
    "recommended_regions": ["list of 1-3 regions: United States, Philippines, Latin America, South Africa"],
    "unique_challenges": "brief description of unique aspects",
    "salary_factors": ["list of 3-4 factors affecting compensation"]
}}

Focus on practical analysis based on the specific requirements mentioned."""
    
    def _parse_analysis_response(self, response_text: str) -> JobAnalysis:
        """Parse AI response into JobAnalysis model"""
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_text = response_text[json_start:json_end]
            
            data = json.loads(json_text)
            
            return JobAnalysis(
                role_category=RoleCategory(data['role_category']),
                experience_level=ExperienceLevel(data['experience_level']),
                years_experience_required=data['years_experience_required'],
                must_have_skills=data['must_have_skills'],
                nice_to_have_skills=data['nice_to_have_skills'],
                key_responsibilities=data['key_responsibilities'],
                remote_work_suitability=data['remote_work_suitability'],
                complexity_score=data['complexity_score'],
                recommended_regions=[Region(r) for r in data['recommended_regions']],
                unique_challenges=data['unique_challenges'],
                salary_factors=data['salary_factors']
            )
        except Exception as e:
            # If parsing fails, return fallback
            return self._fallback_analysis("Unknown", "Unknown")
    
    def _fallback_analysis(self, job_title: str, job_description: str) -> JobAnalysis:
        """Fallback rule-based analysis when AI fails"""
        
        # Simple keyword-based role detection
        title_lower = job_title.lower()
        desc_lower = job_description.lower()
        
        if any(word in title_lower for word in ['brand', 'marketing', 'creative']):
            role_category = RoleCategory.BRAND_MARKETING_MANAGER
        elif any(word in title_lower for word in ['ecommerce', 'shopify', 'e-commerce']):
            role_category = RoleCategory.ECOMMERCE_MANAGER
        elif any(word in title_lower for word in ['data', 'analyst', 'analytics']):
            role_category = RoleCategory.DATA_ANALYST
        elif any(word in title_lower for word in ['content', 'social']):
            role_category = RoleCategory.CONTENT_MARKETER
        else:
            role_category = RoleCategory.OPERATIONS_MANAGER
        
        # Simple experience level detection
        if any(word in desc_lower for word in ['senior', '5+', '7+', 'lead']):
            experience_level = ExperienceLevel.SENIOR
        elif any(word in desc_lower for word in ['junior', 'entry', '1-2']):
            experience_level = ExperienceLevel.JUNIOR
        else:
            experience_level = ExperienceLevel.MID
        
        return JobAnalysis(
            role_category=role_category,
            experience_level=experience_level,
            years_experience_required="3-5 years",
            must_have_skills=["Communication", "Project Management", "Analytical Thinking"],
            nice_to_have_skills=["Remote Work Experience", "Industry Knowledge"],
            key_responsibilities=["Manage daily operations", "Coordinate with teams", "Analyze performance"],
            remote_work_suitability="high",
            complexity_score=5,
            recommended_regions=[Region.PHILIPPINES, Region.LATIN_AMERICA],
            unique_challenges="Standard remote role requirements",
            salary_factors=["Experience level", "Technical skills", "Industry knowledge"]
        )