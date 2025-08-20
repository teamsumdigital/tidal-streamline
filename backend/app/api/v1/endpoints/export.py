"""
CSV Export API endpoints for Canva template integration
Generates all 134 template variables for Market Scan PDFs
"""

import csv
import io
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, Response
from loguru import logger

from app.core.database import db
from app.models.market_scan import MarketScanResponse

router = APIRouter()

@router.get("/market-scans/{scan_id}")
async def export_market_scan_csv(
    scan_id: str,
    format: str = Query("template", description="Export format: 'template' for Canva variables")
):
    """
    Export market scan data as CSV with all 134 template variables for Canva integration
    """
    try:
        # Get market scan data
        scan_data = await db.get_market_scan(scan_id)
        if not scan_data:
            raise HTTPException(status_code=404, detail="Market scan not found")
        
        # Get candidate profiles from database
        candidates = await get_candidate_profiles_for_template()
        
        # Generate template variables
        template_data = generate_template_variables(scan_data, candidates)
        
        # Create CSV
        csv_content = create_csv_content(template_data)
        
        logger.info(f"✅ Generated CSV export for market scan {scan_id} with {len(template_data)} variables")
        
        # Return CSV as downloadable file
        filename = f"market_scan_{scan_id}_template.csv"
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to export market scan {scan_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to export market scan: {str(e)}")

async def get_candidate_profiles_for_template() -> List[Dict[str, Any]]:
    """Get candidate profiles for template generation"""
    try:
        # Get 3 candidates from different regions for template profiles
        candidates = await db.get_candidate_profiles()
        
        if candidates and len(candidates) >= 3:
            # Get candidates from different regions if possible
            regions_seen = set()
            selected_candidates = []
            
            for candidate in candidates:
                if len(selected_candidates) >= 3:
                    break
                    
                region = candidate.get('region', 'Unknown')
                if region not in regions_seen or len(selected_candidates) < 3:
                    selected_candidates.append(candidate)
                    regions_seen.add(region)
                    
            return selected_candidates[:3]
        elif candidates:
            return candidates[:3]
        else:
            # Return mock candidates if none in database
            return get_mock_candidates()
            
    except Exception as e:
        logger.warning(f"Failed to fetch candidates from database: {e}, using mock data")
        return get_mock_candidates()

def get_mock_candidates() -> List[Dict[str, Any]]:
    """Get mock candidate data for template generation"""
    return [
        {
            "name": "Ana",
            "role_category": "Content Marketer",
            "region": "Philippines",
            "country_code": "PHL",
            "monthly_salary_min": 1500,
            "monthly_salary_max": 2000,
            "onboarded_date": "2024-02-04",
            "capabilities": "A dynamic Content Marketer based in the Philippines with 6+ years of experience...",
            "responsibilities": "• Develop and implement content strategies\n• Create written and visual content\n• Analyze performance to refine content",
            "experience_breakdown": {"freelancing": "6+ Yrs", "content_marketing": "6+ Yrs", "adobe_suite": "10+ Yrs"},
            "tech_stack": {"primary": ["Meta Ads Manager", "Shopify"], "secondary": ["Landing Page Creation", "Influencer Marketing"]},
            "video_url": None
        },
        {
            "name": "Natália",
            "role_category": "Copywriter & Content",
            "region": "Brazil",
            "country_code": "BRA",
            "monthly_salary_min": 2000,
            "monthly_salary_max": 2500,
            "onboarded_date": None,
            "capabilities": "Has 8+ years of experience creating multifaceted content for brands...",
            "responsibilities": "• Create visual content that aligns with brand guidelines\n• Design assets for various mediums\n• Collaborate with teams",
            "experience_breakdown": {"freelancing": "5+ Yrs", "content_marketing": "8+ Yrs", "adobe_suite": "10+ Yrs"},
            "tech_stack": {"primary": ["Adobe Creative Suite", "Figma"], "secondary": ["Video Editing", "Copywriting"]},
            "video_url": None
        },
        {
            "name": "Sarah",
            "role_category": "Marketing Specialist",
            "region": "South Africa",
            "country_code": "ZAF",
            "monthly_salary_min": 1800,
            "monthly_salary_max": 2200,
            "onboarded_date": None,
            "capabilities": "Experienced marketing professional based in South Africa...",
            "responsibilities": "• Develop comprehensive marketing strategies\n• Execute cross-channel campaigns\n• Optimize performance metrics",
            "experience_breakdown": {"marketing": "5+ Yrs", "digital_strategy": "3+ Yrs", "analytics": "7+ Yrs"},
            "tech_stack": {"primary": ["Google Analytics", "HubSpot"], "secondary": ["Social Media Management", "Email Marketing"]},
            "video_url": None
        }
    ]

def generate_template_variables(scan_data: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, str]:
    """Generate all 134 template variables for Canva integration"""
    
    # Extract analysis data
    job_analysis = scan_data.get('job_analysis', {})
    salary_recommendations = scan_data.get('salary_recommendations', {})
    skills_recommendations = scan_data.get('skills_recommendations', {})
    
    # Extract salary data by region
    salary_data = salary_recommendations.get('salary_recommendations', {})
    
    # Get current date for scan_date
    scan_date = datetime.utcnow().strftime("%B %d, %Y")
    
    # Build template variables dictionary
    variables = {}
    
    # === Company & Role Information ===
    variables.update({
        "company_name": scan_data.get('company_domain', ''),
        "position_title": scan_data.get('job_title', ''),
        "scan_date": scan_date,
        "analysis_confidence": f"{int((scan_data.get('confidence_score', 0.8) * 100))}%"
    })
    
    # === Salary Data - All Regions ===
    
    # United States (Baseline)
    us_salary = salary_data.get('United States', {})
    variables.update({
        "us_salary": format_salary(us_salary.get('mid', 95000)),
        "us_salary_min": format_salary(us_salary.get('low', 75000)),
        "us_salary_max": format_salary(us_salary.get('high', 120000))
    })
    
    # Philippines (High Savings)
    ph_salary = salary_data.get('Philippines', {})
    ph_mid = ph_salary.get('mid', 28000)
    variables.update({
        "ph_salary": format_salary(ph_mid),
        "ph_salary_min": format_salary(ph_salary.get('low', 22000)),
        "ph_salary_max": format_salary(ph_salary.get('high', 35000)),
        "ph_savings_percent": f"{calculate_savings_percent(us_salary.get('mid', 95000), ph_mid)}%"
    })
    
    # Latin America
    latam_salary = salary_data.get('Latin America', {})
    latam_mid = latam_salary.get('mid', 52000)
    variables.update({
        "latam_salary": format_salary(latam_mid),
        "latam_salary_min": format_salary(latam_salary.get('low', 40000)),
        "latam_salary_max": format_salary(latam_salary.get('high', 65000)),
        "latam_savings_percent": f"{calculate_savings_percent(us_salary.get('mid', 95000), latam_mid)}%"
    })
    
    # South Africa
    sa_salary = salary_data.get('South Africa', {})
    sa_mid = sa_salary.get('mid', 45000)
    variables.update({
        "sa_salary": format_salary(sa_mid),
        "sa_salary_min": format_salary(sa_salary.get('low', 35000)),
        "sa_salary_max": format_salary(sa_salary.get('high', 58000)),
        "sa_savings_percent": f"{calculate_savings_percent(us_salary.get('mid', 95000), sa_mid)}%"
    })
    
    # Europe
    eu_mid = 75000  # Estimated Europe salary
    variables.update({
        "europe_salary_min": format_salary(65000),
        "europe_salary_max": format_salary(85000),
        "europe_savings_percent": f"{calculate_savings_percent(us_salary.get('mid', 95000), eu_mid)}%"
    })
    
    # === Skills & Requirements ===
    must_have = job_analysis.get('must_have_skills', [])
    nice_to_have = job_analysis.get('nice_to_have_skills', [])
    
    variables.update({
        "required_skills": ", ".join(must_have[:5]) if must_have else "Industry-specific skills",
        "preferred_skills": ", ".join(nice_to_have[:5]) if nice_to_have else "Additional technical skills",
        "certifications": "Industry certification, Relevant online courses",
        "tech_skills": ", ".join(must_have[:3]) if must_have else "Technical platforms",
        "marketing_skills": ", ".join([s for s in must_have if 'marketing' in s.lower()][:3]) or "Marketing tools",
        "analytics_skills": ", ".join([s for s in must_have if any(word in s.lower() for word in ['analytics', 'data', 'report'])][:3]) or "Analytics platforms"
    })
    
    # === Job Analysis ===
    variables.update({
        "role_complexity": str(job_analysis.get('complexity_score', 7)),
        "seniority_level": job_analysis.get('experience_level', 'mid'),
        "experience_years": job_analysis.get('years_experience_required', '3-5 years'),
        "remote_suitability": job_analysis.get('remote_work_suitability', 'High').title(),
        "best_regions": ", ".join(job_analysis.get('recommended_regions', ['Philippines', 'Latin America'])),
        "main_duties": "; ".join(job_analysis.get('key_responsibilities', ['Manage operations', 'Analyze performance'])[:3]),
        "role_challenges": job_analysis.get('unique_challenges', 'Complex project coordination and performance optimization')
    })
    
    # === Market Insights ===
    market_insights = salary_recommendations.get('market_insights', {})
    variables.update({
        "high_demand_regions": market_insights.get('high_demand_regions', ['United States', 'Philippines']),
        "competitive_factors": ", ".join(market_insights.get('competitive_factors', ['Experience', 'Technical skills'])),
        "cost_efficiency": market_insights.get('cost_efficiency', 'Philippines offers best value for this role'),
        "salary_factors": ", ".join(job_analysis.get('salary_factors', ['Experience level', 'Technical expertise', 'Industry knowledge']))
    })
    
    # === Similar Roles Data ===
    variables.update({
        "similar_role_1": "E-commerce Analyst",
        "similar_role_1_percent": "45",
        "similar_role_2": "Marketing Data Analyst", 
        "similar_role_2_percent": "25",
        "similar_role_3": "Business Intelligence Analyst",
        "similar_role_3_percent": "20"
    })
    
    # === Experience Level Breakdowns ===
    base_salary = ph_salary.get('mid', 2000)
    variables.update({
        "junior_salary_min": format_salary(int(base_salary * 0.6)),
        "junior_salary_max": format_salary(int(base_salary * 0.8)),
        "mid_salary_min": format_salary(int(base_salary * 0.8)),
        "mid_salary_max": format_salary(int(base_salary * 1.0)),
        "senior_salary_min": format_salary(int(base_salary * 1.0)),
        "senior_salary_max": format_salary(int(base_salary * 1.3)),
        "expert_salary_min": format_salary(int(base_salary * 1.3)),
        "expert_salary_max": format_salary(int(base_salary * 1.6))
    })
    
    # === Regional Recommendations ===
    variables.update({
        "asia_recommendation": "High skill availability, excellent English proficiency",
        "latam_recommendation": "Strong technical skills, overlapping US timezone", 
        "africa_recommendation": "Growing tech talent pool, cost-effective rates",
        "europe_recommendation": "Premium talent, higher costs but excellent quality"
    })
    
    # === Additional Variables ===
    variables.update({
        "client_logo_url": f"https://{scan_data.get('company_domain', 'client.com')}/logo.png",
        "recommended_salary_min": format_salary(ph_salary.get('low', 1800)),
        "recommended_salary_max": format_salary(ph_salary.get('high', 2300))
    })
    
    # === Candidate Profiles ===
    add_candidate_variables(variables, candidates)
    
    # === Featured Candidate Profile ===
    if len(candidates) > 0:
        featured = candidates[0]  # Use first candidate as featured
        add_featured_candidate_variables(variables, featured)
    
    # === Pricing & Service Structure ===
    add_pricing_variables(variables, base_salary)
    
    # === Project Summary ===
    add_project_summary_variables(variables, scan_data, base_salary)
    
    # === Service Comparison ===
    add_service_comparison_variables(variables, base_salary)
    
    return variables

def add_candidate_variables(variables: Dict[str, str], candidates: List[Dict[str, Any]]):
    """Add candidate profile variables (candidate_1_*, candidate_2_*, candidate_3_*)"""
    for i, candidate in enumerate(candidates[:3], 1):
        prefix = f"candidate_{i}_"
        
        # Extract experience data
        exp_breakdown = candidate.get('experience_breakdown') or {}
        exp_list = [f"{v} {k.replace('_', ' ').title()}" for k, v in exp_breakdown.items()] if exp_breakdown else ["5+ Yrs Experience"]
        
        # Extract tech stack
        tech_stack = candidate.get('tech_stack') or {}
        tech_list = (tech_stack.get('primary', []) + tech_stack.get('secondary', [])) if tech_stack else []
        
        variables.update({
            f"{prefix}name": candidate.get('name', f'Candidate {i}'),
            f"{prefix}photo_url": candidate.get('video_url') or f"https://example.com/{candidate.get('name', 'candidate').lower()}.jpg",
            f"{prefix}bio": candidate.get('capabilities', f'Experienced professional with strong background in {candidate.get("role_category", "their field")}.'),
            f"{prefix}responsibilities": candidate.get('responsibilities', '• Manage assigned responsibilities\n• Collaborate with team members\n• Optimize processes and performance'),
            f"{prefix}region": candidate.get('region', 'Philippines'),
            f"{prefix}salary_range": f"${candidate.get('monthly_salary_min', 1500)}-${candidate.get('monthly_salary_max', 2000)}",
            f"{prefix}onboarded_date": format_date(candidate.get('onboarded_date')),
            f"{prefix}experience_1": exp_list[0] if len(exp_list) > 0 else "5+ Yrs Experience",
            f"{prefix}experience_2": exp_list[1] if len(exp_list) > 1 else "3+ Yrs Specialization",
            f"{prefix}experience_3": exp_list[2] if len(exp_list) > 2 else "Professional Development",
            f"{prefix}tech_stack": "\n".join(tech_list[:4]) if tech_list else "Industry-standard tools\nPlatform expertise\nAnalytics software\nCollaboration tools"
        })

def add_featured_candidate_variables(variables: Dict[str, str], candidate: Dict[str, Any]):
    """Add featured candidate variables (featured_candidate_*)"""
    exp_breakdown = candidate.get('experience_breakdown') or {}
    tech_stack = candidate.get('tech_stack') or {}
    tech_list = (tech_stack.get('primary', []) + tech_stack.get('secondary', [])) if tech_stack else []
    
    variables.update({
        "featured_candidate_name": candidate.get('name', 'Featured Candidate'),
        "featured_candidate_photo_url": candidate.get('video_url') or f"https://example.com/{candidate.get('name', 'featured').lower()}.jpg",
        "featured_candidate_title": candidate.get('role_category', 'Professional'),
        "featured_candidate_bio": candidate.get('capabilities', 'Experienced professional with strong expertise and proven track record.'),
        "featured_candidate_region": candidate.get('region', 'Philippines'),
        "featured_candidate_salary_range": f"${candidate.get('monthly_salary_min', 2000)}-${candidate.get('monthly_salary_max', 2500)}",
        "featured_candidate_onboarded": format_date(candidate.get('onboarded_date')) or "NA",
        "featured_candidate_experience_freelance": next((f"{v} Freelancing" for k, v in exp_breakdown.items() if 'freelanc' in k.lower()), "5+ Yrs Freelancing"),
        "featured_candidate_experience_content": next((f"{v} {k.replace('_', ' ').title()}" for k, v in exp_breakdown.items() if any(word in k.lower() for word in ['content', 'marketing', 'creative'])), "3+ Yrs Content Marketing"),
        "featured_candidate_experience_adobe": next((f"{v} Adobe Suite" for k, v in exp_breakdown.items() if 'adobe' in k.lower()), "5+ Yrs Adobe Suite"),
        "featured_candidate_tech_1": tech_list[0] if len(tech_list) > 0 else "Primary Platform",
        "featured_candidate_tech_2": tech_list[1] if len(tech_list) > 1 else "Design Tools",
        "featured_candidate_tech_3": tech_list[2] if len(tech_list) > 2 else "Analytics",
        "featured_candidate_tech_4": tech_list[3] if len(tech_list) > 3 else "Collaboration",
        "featured_candidate_responsibilities": candidate.get('responsibilities', '• Lead strategic initiatives\n• Manage client relationships\n• Optimize performance metrics')
    })

def add_pricing_variables(variables: Dict[str, str], base_salary: int):
    """Add pricing tier variables"""
    variables.update({
        "tier_1_salary_range": f"${int(base_salary * 0.7)} - ${int(base_salary * 1.0)}",
        "tier_1_regions": "Philippines",
        "tier_1_fee": "$4,800",
        "tier_2_salary_range": f"${int(base_salary * 1.2)} - ${int(base_salary * 2.0)}",
        "tier_2_regions": "Philippines + Latin America",
        "tier_2_fee": "$5,600",
        "tier_3_salary_range": f"${int(base_salary * 2.0)}+",
        "tier_3_regions": "PI + LatAm + Africa + EU",
        "tier_3_fee": "$6,400 - $8,000"
    })

def add_project_summary_variables(variables: Dict[str, str], scan_data: Dict[str, Any], base_salary: int):
    """Add project summary variables"""
    variables.update({
        "project_role": scan_data.get('job_title', 'Specialist'),
        "project_salary_range": f"${int(base_salary * 0.8)} - ${int(base_salary * 1.0)}",
        "project_fee_total": "$5,600 Total",
        "project_fee_deposit": "$1,500 deposit due now",
        "project_fee_balance": "Balance Due after successful placement",
        "project_guarantee": "Culture fit, performance, life events- we'll replace them free of charge"
    })

def add_service_comparison_variables(variables: Dict[str, str], base_salary: int):
    """Add service comparison variables (BPO vs Tidal)"""
    annual_cost = base_salary * 12
    
    variables.update({
        "bpo_agency_cost": "$3K / month",
        "bpo_agency_annual": "$36K / year",
        "bpo_hire_gets": f"${int(base_salary * 0.7)}/month → ${int(base_salary * 0.7 * 12)}K / Year",
        "bpo_results": "Less quality talent.\nBPO is squeezing recurring revenue monthly\nAdded layer of middle-management & stakeholders",
        "tidal_fee": "$5,600 one-time fee",
        "tidal_monthly_cost": f"${int(base_salary / 1000)}K / month",
        "tidal_annual_cost": f"${int(annual_cost / 1000)}K / year",
        "tidal_hire_gets": f"${int(base_salary)}/month → ${int(annual_cost / 1000)}K / Year",
        "tidal_results": "Attract better candidates.\nPay people the most & retain talent longer\nTidal only gets paid when we perform",
        "fixed_budget_example": f"${int(annual_cost / 1000)}K/year",
        "tidal_salary_option_1": f"Hire @ ${int(base_salary * 0.8)} / month → ${int(base_salary * 0.8 * 12 / 1000)}K / year",
        "tidal_salary_option_2": "Deel COR @ $500 / month → $6K / year"
    })

def format_salary(amount: int) -> str:
    """Format salary amount with appropriate formatting"""
    if amount >= 1000:
        return f"${amount:,}"
    else:
        return f"${amount}"

def calculate_savings_percent(us_salary: int, other_salary: int) -> int:
    """Calculate savings percentage vs US salary"""
    if us_salary <= 0:
        return 0
    return int(((us_salary - other_salary) / us_salary) * 100)

def format_date(date_str: Optional[str]) -> str:
    """Format date string for display"""
    if not date_str:
        return "NA"
    
    try:
        # Parse different date formats
        if isinstance(date_str, str):
            if "T" in date_str:  # ISO format
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:  # Simple date format
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%m/%d/%Y")
    except:
        pass
    
    return str(date_str)

def create_csv_content(template_data: Dict[str, str]) -> str:
    """Create CSV content from template data"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Variable', 'Value'])
    
    # Write all template variables
    for key, value in sorted(template_data.items()):
        # Clean value for CSV (handle newlines)
        clean_value = str(value).replace('\n', '\\n') if value else ''
        writer.writerow([key, clean_value])
    
    return output.getvalue()