"""
Tidal Report Generation Service
Generates professional market scan reports using Canva API integration
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

class TidalReportGenerator:
    """
    Generates professional Tidal-branded market scan reports
    Integrates with Canva API for template-based report creation
    """
    
    def __init__(self):
        self.canva_api_key = os.getenv("CANVA_API_KEY")
        self.canva_base_url = "https://api.canva.com/rest/v1"
        self.template_mapping = {
            "cover_page": "BAEAGv1XZkg",  # Tidal cover page template ID
            "regional_overview": "BAEAGv1XZkh", # Regional comparison template
            "role_details": "BAEAGv1XZki", # Detailed role breakdown
            "candidate_profiles": "BAEAGv1XZkj" # Candidate showcase template
        }
    
    async def generate_market_scan_report(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete market scan report from scan data
        
        Args:
            scan_data: Complete market scan results from database
            
        Returns:
            Dict with report URLs and metadata
        """
        try:
            logger.info(f"Generating report for scan ID: {scan_data.get('id')}")
            
            # Prepare template data mappings
            template_data = self._prepare_template_data(scan_data)
            
            # Generate individual report pages
            report_pages = []
            
            # 1. Cover Page
            cover_page = await self._generate_cover_page(template_data)
            report_pages.append(cover_page)
            
            # 2. Regional Overview
            regional_overview = await self._generate_regional_overview(template_data)
            report_pages.append(regional_overview)
            
            # 3. Detailed Role Analysis (per region)
            for region in template_data['regions']:
                role_detail = await self._generate_role_detail_page(template_data, region)
                report_pages.append(role_detail)
            
            # 4. Role Insights Page
            insights_page = await self._generate_insights_page(template_data)
            report_pages.append(insights_page)
            
            # 5. Candidate Profiles
            candidate_page = await self._generate_candidate_profiles(template_data)
            report_pages.append(candidate_page)
            
            # Combine pages into final report
            final_report = await self._combine_report_pages(report_pages, template_data)
            
            logger.info(f"Report generated successfully: {final_report['download_url']}")
            
            return {
                "success": True,
                "report_url": final_report['download_url'],
                "preview_url": final_report['preview_url'],
                "pages": len(report_pages),
                "generated_at": datetime.utcnow().isoformat(),
                "client_name": template_data['client_name'],
                "role_title": template_data['role_title']
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat()
            }
    
    def _prepare_template_data(self, scan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map market scan data to template placeholders
        """
        job_analysis = scan_data.get('job_analysis', {})
        salary_recommendations = scan_data.get('salary_recommendations', {})
        skills_recommendations = scan_data.get('skills_recommendations', {})
        
        # Extract regional data
        regions_data = []
        region_names = ["Philippines", "Argentina", "South Africa"]  # Based on template
        
        for region in region_names:
            region_salary = salary_recommendations.get('regional_rates', {}).get(region, {})
            
            regions_data.append({
                "name": region,
                "country_code": self._get_country_code(region),
                "salary_range": self._format_salary_range(region_salary),
                "recommendation": self._get_recommendation_level(region_salary),
                "availability_percentage": self._calculate_availability(region),
                "detailed_breakdown": self._get_detailed_salary_breakdown(region_salary)
            })
        
        return {
            "client_name": scan_data.get('client_info', {}).get('client_name', 'UNDERCLUB'),
            "role_title": job_analysis.get('role_title', 'Operations Manager'),
            "prepared_date": datetime.now().strftime("%m/%d/%Y"),
            "regions": regions_data,
            "role_insights": {
                "similar_roles": skills_recommendations.get('similar_roles', []),
                "unique_challenges": job_analysis.get('key_challenges', []),
                "required_tools": skills_recommendations.get('must_have_skills', []),
                "recommended_pay_band": salary_recommendations.get('recommended_range', '$2,500 - $3,000')
            },
            "candidate_profiles": self._get_sample_candidates(job_analysis.get('role_category')),
            "global_regions_sourced": self._get_global_regions(),
            "branding": {
                "logo_url": "https://your-domain.com/tidal-logo.png",
                "website": "HIRETIDAL.COM",
                "email": "CONNECT@HIRETIDAL.COM",
                "tagline": "Connecting brands to the best global talent."
            }
        }
    
    async def _generate_cover_page(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cover page with client branding"""
        
        cover_elements = {
            "client_name": template_data['client_name'],
            "prepared_date": template_data['prepared_date'],
            "tidal_logo": template_data['branding']['logo_url'],
            "website": template_data['branding']['website'],
            "email": template_data['branding']['email'],
            "tagline": template_data['branding']['tagline']
        }
        
        return await self._create_canva_design(
            template_id=self.template_mapping['cover_page'],
            elements=cover_elements
        )
    
    async def _generate_regional_overview(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate regional comparison overview page"""
        
        overview_elements = {
            "role_title": "Great talent can be found anywhere.",
            "subtitle": "Our goal is to optimize for a successful outcome — finding the right balance between labor pool and budget.",
            "monthly_pay_band_button": "Monthly Pay Band",
            "recommendation_button": "Recommendation"
        }
        
        # Add regional data
        for i, region in enumerate(template_data['regions']):
            overview_elements.update({
                f"region_{i+1}_name": region['name'],
                f"region_{i+1}_flag": region['country_code'],
                f"region_{i+1}_salary": region['salary_range'],
                f"region_{i+1}_recommendation": region['recommendation']
            })
        
        return await self._create_canva_design(
            template_id=self.template_mapping['regional_overview'],
            elements=overview_elements
        )
    
    async def _generate_role_detail_page(self, template_data: Dict[str, Any], region: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed role analysis page for specific region"""
        
        detail_elements = {
            "role_title": f"{template_data['role_title']} - {region['name'][:3].upper()}",
            "country_flag": region['country_code'],
            "availability_percentage": f"{region['availability_percentage']}%",
            "recommended_pay_band": region['salary_range']
        }
        
        # Add salary breakdown table
        breakdown = region['detailed_breakdown']
        for exp_level, rates in breakdown.items():
            detail_elements.update({
                f"{exp_level}_low": f"${rates['low']:,.2f}",
                f"{exp_level}_mid": f"${rates['mid']:,.2f}",
                f"{exp_level}_high": f"${rates['high']:,.2f}"
            })
        
        return await self._create_canva_design(
            template_id=self.template_mapping['role_details'],
            elements=detail_elements
        )
    
    async def _generate_insights_page(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate role insights and similar roles page"""
        
        insights = template_data['role_insights']
        
        insights_elements = {
            "role_title": template_data['role_title'],
            "recommended_pay_band": insights['recommended_pay_band'],
            "unique_challenges_text": self._format_challenges_text(insights['unique_challenges']),
            "required_tools_list": "\n".join([f"• {tool}" for tool in insights['required_tools'][:5]])
        }
        
        # Add similar roles with percentages
        for i, role in enumerate(insights['similar_roles'][:3]):
            insights_elements.update({
                f"similar_role_{i+1}": role['title'],
                f"similar_role_{i+1}_percentage": f"{role['similarity']}%"
            })
        
        # Add global regions flags
        for i, region in enumerate(template_data['global_regions_sourced']):
            insights_elements[f"global_region_{i+1}_flag"] = region['flag']
            insights_elements[f"global_region_{i+1}_name"] = region['name']
        
        return await self._create_canva_design(
            template_id=self.template_mapping['role_details'], # Reuse template with different data
            elements=insights_elements
        )
    
    async def _generate_candidate_profiles(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate candidate profile showcase page"""
        
        candidate = template_data['candidate_profiles'][0]  # Use first candidate as example
        
        profile_elements = {
            "candidate_name": f"Meet {candidate['name']}",
            "candidate_video_thumbnail": candidate['video_thumbnail'],
            "experience_years": f"{candidate['experience']}+ Yrs",
            "specialization": candidate['specialization'],
            "capabilities_text": candidate['capabilities'],
            "tech_stack_list": "\n".join(candidate['tech_stack']),
            "region_flag": candidate['region_flag'],
            "region_name": candidate['region_name'],
            "working_hours": candidate['working_hours'],
            "role_category": candidate['role_category']
        }
        
        return await self._create_canva_design(
            template_id=self.template_mapping['candidate_profiles'],
            elements=profile_elements
        )
    
    async def _create_canva_design(self, template_id: str, elements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Canva design from template with dynamic data
        """
        if not self.canva_api_key:
            # Fallback: Return mock data for development
            return {
                "design_id": f"mock_design_{template_id}",
                "preview_url": f"https://mock-canva.com/preview/{template_id}",
                "download_url": f"https://mock-canva.com/download/{template_id}",
                "elements": elements
            }
        
        headers = {
            "Authorization": f"Bearer {self.canva_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "design": {
                "type": "presentation",
                "template_id": template_id,
                "elements": elements
            }
        }
        
        try:
            response = requests.post(
                f"{self.canva_base_url}/designs",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            design_data = response.json()
            return {
                "design_id": design_data['id'],
                "preview_url": design_data['urls']['view_url'],
                "download_url": design_data['urls']['download_url']
            }
            
        except requests.RequestException as e:
            logger.error(f"Canva API error: {str(e)}")
            raise Exception(f"Failed to create Canva design: {str(e)}")
    
    async def _combine_report_pages(self, pages: List[Dict], template_data: Dict) -> Dict[str, Any]:
        """
        Combine individual pages into final report
        """
        # For now, return the first page as the main report
        # In production, this would combine all pages into a PDF
        
        return {
            "download_url": pages[0]["download_url"],
            "preview_url": pages[0]["preview_url"],
            "total_pages": len(pages),
            "client_name": template_data['client_name']
        }
    
    # Helper methods for data formatting
    
    def _get_country_code(self, region: str) -> str:
        """Get country code for flag display"""
        mapping = {
            "Philippines": "PH",
            "Argentina": "AR", 
            "South Africa": "ZA",
            "Colombia": "CO",
            "Mexico": "MX",
            "Brazil": "BR",
            "Peru": "PE"
        }
        return mapping.get(region, "US")
    
    def _format_salary_range(self, salary_data: Dict) -> str:
        """Format salary range for display"""
        if not salary_data:
            return "N/A"
        
        low = salary_data.get('range_low', 0)
        high = salary_data.get('range_high', 0)
        
        if low and high:
            return f"${low:,.0f}-${high:,.0f}"
        return "Contact for pricing"
    
    def _get_recommendation_level(self, salary_data: Dict) -> str:
        """Determine recommendation level"""
        if not salary_data:
            return "N/A"
        
        savings = salary_data.get('savings_vs_us', 0)
        
        if savings >= 60:
            return "1st option"
        elif savings >= 40:
            return "2nd option"
        else:
            return "Other option"
    
    def _calculate_availability(self, region: str) -> int:
        """Calculate availability percentage for region"""
        # Mock data - in production, calculate from actual candidate pool
        availability_map = {
            "Philippines": 40,
            "Argentina": 30,
            "South Africa": 35,
            "Colombia": 25,
            "Mexico": 20,
            "Brazil": 15
        }
        return availability_map.get(region, 20)
    
    def _get_detailed_salary_breakdown(self, salary_data: Dict) -> Dict[str, Dict]:
        """Get detailed salary breakdown by experience level"""
        base_rate = salary_data.get('range_mid', 2000)
        
        return {
            "associate": {
                "low": base_rate * 0.45,
                "mid": base_rate * 0.64,
                "high": base_rate * 0.86
            },
            "junior": {
                "low": base_rate * 0.64,
                "mid": base_rate * 0.90,
                "high": base_rate * 1.15
            },
            "senior": {
                "low": base_rate * 0.90,
                "mid": base_rate * 1.23,
                "high": base_rate * 1.50
            },
            "expert": {
                "low": base_rate * 1.23,
                "mid": base_rate * 1.58,
                "high": base_rate * 1.90
            }
        }
    
    def _format_challenges_text(self, challenges: List[str]) -> str:
        """Format unique challenges text"""
        if not challenges:
            return "Finding the right candidate with the specific tools you need starts with understanding what you're aiming to achieve for your business."
        
        return f"Finding the right candidate with the specific tools you need starts with understanding what you're aiming to achieve for your business.\n\nWith that in mind, here's a list of tools we think will be great to focus on for your candidates."
    
    def _get_sample_candidates(self, role_category: str) -> List[Dict]:
        """Get sample candidate profiles for role category"""
        # Mock candidate data - in production, query from candidate database
        return [{
            "name": "Solanyi",
            "video_thumbnail": "https://example.com/candidate-video-thumbnail.jpg",
            "experience": "10",
            "specialization": "Freelancing",
            "secondary_experience": "8+ Yrs EDI/ERP Coordinator, 2.5+ Yrs e-Commerce",
            "capabilities": "13 years of supply chain and logistics experience and 8 years working with ERP and EDI systems. Exceptional strength in order management and process optimization, and use of systems like NetSuite, SAP, Oracle, and Power BI",
            "tech_stack": ["Shopify", "ERP Systems", "3PL Management", "Supply Chain Management", "Logistics Management"],
            "region_flag": "DO",
            "region_name": "Dominican Republic", 
            "working_hours": "9am - 5pm EST",
            "role_category": "EDI SYSTEMS / EDI PLATFORMS"
        }]
    
    def _get_global_regions(self) -> List[Dict]:
        """Get global regions with flags for sourcing display"""
        return [
            {"name": "USA", "flag": "US"},
            {"name": "Philippines", "flag": "PH"},
            {"name": "Colombia", "flag": "CO"},
            {"name": "Argentina", "flag": "AR"},
            {"name": "Brazil", "flag": "BR"},
            {"name": "Mexico", "flag": "MX"},
            {"name": "Peru", "flag": "PE"},
            {"name": "South Africa", "flag": "ZA"},
            {"name": "Ukraine", "flag": "UA"},
            {"name": "Poland", "flag": "PL"}
        ]