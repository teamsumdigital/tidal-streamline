"""
AI Service integration for job analysis and recommendations
"""

import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
from loguru import logger
from app.core.config import settings

class AIService:
    """OpenAI integration for job description analysis and recommendations"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def analyze_job_description(self, job_title: str, job_description: str, hiring_challenges: str = "") -> Dict[str, Any]:
        """
        Analyze job description and extract key information for market scan
        """
        try:
            prompt = self._build_job_analysis_prompt(job_title, job_description, hiring_challenges)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert recruiter analyzing job requirements for global talent sourcing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"✅ Successfully analyzed job: {job_title}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze job description: {e}")
            raise
    
    def _build_job_analysis_prompt(self, job_title: str, job_description: str, hiring_challenges: str) -> str:
        """Build the prompt for job description analysis"""
        return f"""
        Analyze this job posting and provide a structured response in JSON format:

        **Job Title:** {job_title}
        **Job Description:** {job_description}
        **Hiring Challenges:** {hiring_challenges}

        Please provide your analysis in this exact JSON structure:

        {{
            "role_category": "One of: Brand Marketing Manager, Community Manager, Content Marketer, Retention Manager, Ecommerce Manager, Sales Operations Manager, Data Analyst, Logistics Manager, Operations Manager",
            "experience_level": "junior|mid|senior|expert",
            "years_experience_required": "2-4|5-8|9+",
            "must_have_skills": [
                "List of 3-5 essential skills/tools required"
            ],
            "nice_to_have_skills": [
                "List of 3-5 preferred skills/tools"
            ],
            "key_responsibilities": [
                "List of 3-5 main job responsibilities"
            ],
            "remote_work_suitability": "high|medium|low",
            "complexity_score": 1-10,
            "recommended_regions": [
                "List of 2-3 recommended regions from: United States, Philippines, Latin America, South Africa"
            ],
            "unique_challenges": "Brief description of specific hiring challenges for this role",
            "salary_factors": [
                "List of factors that might affect salary expectations"
            ]
        }}

        Base your analysis on:
        1. The specific requirements mentioned in the job description
        2. Industry standards for similar roles
        3. The complexity and seniority level required
        4. Regional availability of talent for these skills
        5. Any specific challenges mentioned by the hiring manager

        Respond only with valid JSON, no additional text.
        """
    
    async def generate_salary_recommendations(self, job_analysis: Dict[str, Any], similar_scans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate salary recommendations based on job analysis and historical data
        """
        try:
            prompt = self._build_salary_prompt(job_analysis, similar_scans)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a compensation expert specializing in global talent markets."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("✅ Generated salary recommendations")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to generate salary recommendations: {e}")
            raise
    
    def _build_salary_prompt(self, job_analysis: Dict[str, Any], similar_scans: List[Dict[str, Any]]) -> str:
        """Build prompt for salary recommendations"""
        similar_data = "\n".join([
            f"- {scan.get('job_title', 'N/A')}: {scan.get('salary_range', 'N/A')} in {scan.get('region', 'N/A')}"
            for scan in similar_scans[:5]
        ])
        
        return f"""
        Generate salary recommendations based on this job analysis and historical market data:

        **Job Analysis:**
        Role: {job_analysis.get('role_category')}
        Experience: {job_analysis.get('experience_level')} ({job_analysis.get('years_experience_required')})
        Complexity: {job_analysis.get('complexity_score')}/10
        Key Skills: {', '.join(job_analysis.get('must_have_skills', []))}

        **Similar Historical Roles:**
        {similar_data or 'No similar roles found'}

        **Target Regions:** Philippines, Latin America, South Africa, United States

        Provide salary recommendations in this JSON format:

        {{
            "salary_recommendations": {{
                "United States": {{
                    "low": 5000,
                    "mid": 6000,
                    "high": 7000,
                    "currency": "USD",
                    "period": "monthly"
                }},
                "Philippines": {{
                    "low": 1750,
                    "mid": 2000,
                    "high": 2250,
                    "currency": "USD",
                    "period": "monthly",
                    "savings_vs_us": 71
                }},
                "Latin America": {{
                    "low": 2500,
                    "mid": 2650,
                    "high": 2800,
                    "currency": "USD", 
                    "period": "monthly",
                    "savings_vs_us": 58
                }},
                "South Africa": {{
                    "low": 3000,
                    "mid": 3125,
                    "high": 3250,
                    "currency": "USD",
                    "period": "monthly", 
                    "savings_vs_us": 48
                }}
            }},
            "recommended_pay_band": "mid",
            "factors_considered": [
                "List of factors that influenced these salary ranges"
            ],
            "market_insights": {{
                "high_demand_regions": ["Regions with strong talent availability"],
                "competitive_factors": ["Factors that might affect hiring competition"],
                "cost_efficiency": "Brief analysis of cost vs quality trade-offs"
            }}
        }}

        Base recommendations on:
        1. Role complexity and required experience
        2. Market rates in each region
        3. Demand for specific skills
        4. Cost of living adjustments
        5. Historical data from similar roles

        Respond only with valid JSON.
        """
    
    async def enhance_skills_recommendations(self, job_analysis: Dict[str, Any], role_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enhance and categorize skills recommendations
        """
        try:
            prompt = f"""
            Enhance the skills recommendations for this role:

            **Role:** {job_analysis.get('role_category')}
            **Current Must-Have:** {', '.join(job_analysis.get('must_have_skills', []))}
            **Current Nice-to-Have:** {', '.join(job_analysis.get('nice_to_have_skills', []))}

            Provide enhanced recommendations in JSON format:

            {{
                "must_have_skills": [
                    "Excel/Google Sheets (Advanced)",
                    "Inventory Management Systems", 
                    "Data Analysis & Reporting"
                ],
                "nice_to_have_skills": [
                    "Shopify Admin Experience",
                    "SQL/Database Knowledge",
                    "Project Management Tools"
                ],
                "skill_categories": {{
                    "technical": ["Technical skills required"],
                    "software": ["Specific software/tools"],
                    "analytical": ["Analysis and reporting skills"],
                    "communication": ["Communication requirements"]
                }},
                "certification_recommendations": [
                    "Relevant certifications that would be valuable"
                ]
            }}

            Respond only with valid JSON.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert in skill assessment and job requirements analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("✅ Enhanced skills recommendations")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to enhance skills recommendations: {e}")
            raise

# Global AI service instance
ai_service = AIService()