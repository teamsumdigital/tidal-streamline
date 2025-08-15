"""
Job Analyzer Service - AI-powered job analysis using OpenAI
"""

import openai
import os
import json
from typing import Dict, Any, List
from app.models.market_scan import JobAnalysis, RoleCategory, ExperienceLevel, Region

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
            # Fallback to rule-based analysis if AI fails
            return self._fallback_analysis(job_title, job_description)
    
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