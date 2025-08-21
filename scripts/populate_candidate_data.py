#!/usr/bin/env python3
"""
Populate candidate profiles with data from Regional Talent Comparison Master PDF
Run after database migration to add template-ready candidate data
"""

import os
import sys
import json
from datetime import date
from supabase import create_client

def load_complete_candidate_data():
    """Load all 23 candidates from the extracted JSON file"""
    try:
        with open('complete_candidates.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ complete_candidates.json not found. Please run extract_all_candidates.py first.")
        sys.exit(1)

# Load all candidates from the comprehensive extraction
CANDIDATE_DATA = load_complete_candidate_data() if __name__ == "__main__" else [
    {
        "name": "Agustina",
        "role_category": "Creative Strategy",
        "experience_years": "5+ years",
        "region": "Argentina",
        "country_code": "ARG",
        "skills": ["Creative Strategy", "Multi-channels platforms", "Canva/Adobe Creative Suite", "Notion", "Social Media Tools"],
        "video_url": None,
        "capabilities": "Grows TikTok with scroll-stopping content; worked with agencies in Canada, Hungary, and the U.S. Leads creative direction and strategy; blends systems with storytelling to create authentic, standout content.",
        "monthly_salary_min": 2475,
        "monthly_salary_max": 3025,
        "working_hours": "9am - 5pm EST",
        "timezone": "EST",
        "availability_type": "Full-Time",
        "experience_breakdown": {
            "freelancing": "5+ Yrs",
            "creative_strategy": "3+ Yrs",
            "product_design": "3+ Yrs"
        },
        "tech_stack": {
            "primary": ["Creative Strategy", "Multi-channels platforms"],
            "secondary": ["Canva/Adobe Creative Suite", "Notion", "Social Media Tools"]
        },
        "responsibilities": "• Develop creative strategies for multi-channel campaigns\n• Create scroll-stopping content for TikTok and social platforms\n• Lead creative direction across international agency projects",
        "onboarded_date": "2024-12-01",
        "english_proficiency": "Fluent",
        "is_active": True
    },
    {
        "name": "Aria",
        "role_category": "Content Creation & Marketing",
        "experience_years": "10+ years",
        "region": "Argentina",
        "country_code": "ARG",
        "skills": ["Klaviyo", "Figma", "ChatGPT", "Creative Copywriting"],
        "video_url": None,
        "capabilities": "10 years of experience in content marketing, creative strategy, and growth marketing. 9.5 years of experience in managing and analyzing ad campaigns across platforms like Google Ads and Meta Ads.",
        "monthly_salary_min": 2250,
        "monthly_salary_max": 2750,
        "working_hours": "9am - 5pm EST",
        "timezone": "EST",
        "availability_type": "Full-Time",
        "experience_breakdown": {
            "freelancing": "9+ Yrs",
            "content_creation_marketing": "10+ Yrs"
        },
        "tech_stack": {
            "primary": ["Klaviyo", "Figma"],
            "secondary": ["ChatGPT", "Creative Copywriting"]
        },
        "responsibilities": "• Create and execute content marketing strategies\n• Manage ad campaigns across Google and Meta platforms\n• Analyze campaign performance and optimize ROI",
        "onboarded_date": "2024-11-15",
        "english_proficiency": "Fluent",
        "is_active": True
    },
    {
        "name": "Thuli",
        "role_category": "Graphic Design & Influencer",
        "experience_years": "3+ years",
        "region": "South Africa",
        "country_code": "ZAF",
        "skills": ["Adobe Creative Suite", "Canva", "Google Analytics", "Social Media Management"],
        "video_url": None,
        "capabilities": "Create visual content that aligns with brand guidelines. Design assets for various mediums (social media, print, web). Collaborate with teams to ensure design meets marketing objectives.",
        "monthly_salary_min": 2700,
        "monthly_salary_max": 3300,
        "working_hours": "9am - 5pm EST",
        "timezone": "EST",
        "availability_type": "Full-Time",
        "experience_breakdown": {
            "freelancing": "3+ Yrs",
            "community_manager": "2+ Yrs",
            "adobe_suite": "2+ Yrs"
        },
        "tech_stack": {
            "primary": ["Adobe Creative Suite", "Canva"],
            "secondary": ["Google Analytics", "Social Media Management"]
        },
        "responsibilities": "• Create visual content that aligns with brand guidelines\n• Design assets for various mediums (social media, print, web)\n• Collaborate with teams to ensure design meets marketing objectives",
        "onboarded_date": "2024-10-15",
        "english_proficiency": "Fluent",
        "is_active": True
    },
    {
        "name": "Karl",
        "role_category": "Retention Manager",
        "experience_years": "5+ years",
        "region": "Philippines",
        "country_code": "PHL",
        "skills": ["Email Marketing", "Klaviyo", "A/B Testing", "Segmentation Strategies", "Google Analytics"],
        "video_url": None,
        "capabilities": "5 years of focused experience in retention marketing and a solid 8 years in the e-commerce industry. Robust hands-on experience in email and SMS marketing tools, A/B testing, and segmentation strategies.",
        "monthly_salary_min": 1665,
        "monthly_salary_max": 2035,
        "working_hours": "9am - 5pm EST",
        "timezone": "EST",
        "availability_type": "Full-Time",
        "experience_breakdown": {
            "freelancing": "5+ Yrs",
            "ecomm_management": "6+ Yrs",
            "beauty_industry": "3+ Yrs"
        },
        "tech_stack": {
            "primary": ["Email Marketing", "Klaviyo"],
            "secondary": ["A/B Testing", "Segmentation Strategies", "Google Analytics"]
        },
        "responsibilities": "• Develop and execute retention marketing strategies\n• Manage email and SMS marketing campaigns\n• Perform A/B testing and segmentation analysis",
        "onboarded_date": "2024-09-20",
        "english_proficiency": "Fluent",
        "is_active": True
    },
    {
        "name": "John",
        "role_category": "Brand and Advertising",
        "experience_years": "12+ years",
        "region": "Philippines",
        "country_code": "PHL",
        "skills": ["HubSpot", "Meta Ads Manager", "Canva", "Google Analytics"],
        "video_url": None,
        "capabilities": "12 years specializing in digital marketing, including content creation, lead generation, and campaign management. 6 years of experience in e-commerce, Amazon and NetSuite, combined with 10 years in brand management.",
        "monthly_salary_min": 1665,
        "monthly_salary_max": 2035,
        "working_hours": "9am - 5pm EST",
        "timezone": "EST",
        "availability_type": "Full-Time",
        "experience_breakdown": {
            "freelancing": "8+ Yrs",
            "brand_marketing_management": "10+ Yrs",
            "ecommerce": "6+ Yrs"
        },
        "tech_stack": {
            "primary": ["HubSpot", "Meta Ads Manager"],
            "secondary": ["Canva", "Google Analytics"]
        },
        "responsibilities": "• Manage digital marketing campaigns\n• Oversee brand management and advertising\n• Handle e-commerce platform optimization",
        "onboarded_date": "2024-08-10",
        "english_proficiency": "Fluent",
        "is_active": True
    },
    {
        "name": "Shasnei",
        "role_category": "Graphic Design and Brand Direction",
        "experience_years": "5+ years",
        "region": "Philippines",
        "country_code": "PHL",
        "skills": ["Figma", "Canva", "Shopify", "Google Suite", "Klaviyo"],
        "video_url": None,
        "capabilities": "Designed Shopify and WordPress sites for brands like The Oodie—boosting conversions with UX-first, story-driven design. Delivered end-to-end creative for BFCM, product launches, and email campaigns across AU-based eCom brands and agencies.",
        "monthly_salary_min": 1665,
        "monthly_salary_max": 2035,
        "working_hours": "9am - 5pm EST",
        "timezone": "EST",
        "availability_type": "Full-Time",
        "experience_breakdown": {
            "freelancing": "3+ Yrs",
            "graphic_design": "5+ Yrs",
            "ecommerce": "4+ Yrs"
        },
        "tech_stack": {
            "primary": ["Figma", "Canva"],
            "secondary": ["Shopify", "Google Suite", "Klaviyo"]
        },
        "responsibilities": "• Design e-commerce websites and landing pages\n• Create brand identity and visual assets\n• Develop email marketing creative campaigns",
        "onboarded_date": "2024-07-25",
        "english_proficiency": "Fluent",
        "is_active": True
    }
]

def populate_candidates():
    """Populate candidate profiles with template-ready data"""
    
    # Initialize Supabase client
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables required")
        sys.exit(1)
    
    supabase = create_client(supabase_url, supabase_key)
    
    print("Populating candidate profiles with template data...")
    
    for candidate in CANDIDATE_DATA:
        try:
            # Check if candidate exists
            existing = supabase.table('candidate_profiles').select('id').eq('name', candidate['name']).execute()
            
            if existing.data:
                # Update existing candidate
                result = supabase.table('candidate_profiles').update(candidate).eq('name', candidate['name']).execute()
                print(f"✅ Updated candidate: {candidate['name']}")
            else:
                # Insert new candidate
                result = supabase.table('candidate_profiles').insert(candidate).execute()
                print(f"✅ Inserted candidate: {candidate['name']}")
                
        except Exception as e:
            print(f"❌ Error processing {candidate['name']}: {str(e)}")
    
    print("\n✅ Candidate data population complete!")
    print("\nNext steps:")
    print("1. Run database migration: add_candidate_template_fields.sql")
    print("2. Upload candidate videos to CDN and update video_url fields")
    print("3. Test CSV export with new template variables")

if __name__ == "__main__":
    populate_candidates()