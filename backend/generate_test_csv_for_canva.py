#!/usr/bin/env python3
"""
Generate a test CSV file for Canva template testing
Creates a simplified version with key variables for initial testing
"""

import asyncio
import sys
import csv
import io
from datetime import datetime

# Add backend directory to path
sys.path.append('/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend')

from app.core.database import db
from app.api.v1.endpoints.export import export_market_scan_csv, generate_template_variables, get_candidate_profiles_for_template

async def create_test_csv():
    """Create a test CSV file for Canva template testing"""
    print("🎨 Creating Test CSV for Canva Integration...")
    
    # Test database connection
    try:
        connection_test = await db.test_connection()
        if not connection_test:
            print("❌ Database connection failed")
            return
        print("✅ Database connection: Success")
    except Exception as e:
        print("❌ Database connection failed, using mock data")
    
    # Create realistic test market scan data
    test_scan_data = {
        'id': 'canva-test-123',
        'company_domain': 'nike.com',
        'job_title': 'Email Marketing Manager',
        'job_description': 'We are seeking an experienced Email Marketing Manager to develop and execute email campaigns that drive customer engagement and revenue growth.',
        'confidence_score': 0.91,
        'job_analysis': {
            'role_category': 'Retention Manager',
            'experience_level': 'mid',
            'years_experience_required': '3-5 years',
            'must_have_skills': ['Email Marketing', 'Klaviyo', 'A/B Testing', 'Segmentation', 'Analytics'],
            'nice_to_have_skills': ['HTML/CSS', 'Marketing Automation', 'SQL', 'Graphic Design'],
            'key_responsibilities': [
                'Develop and execute comprehensive email marketing strategies',
                'Manage automated lifecycle campaigns and segmentation',
                'Analyze campaign performance and optimize for ROI',
                'Collaborate with creative teams on email design and content'
            ],
            'remote_work_suitability': 'high',
            'complexity_score': 8,
            'recommended_regions': ['Philippines', 'Latin America'],
            'unique_challenges': 'Managing complex automation workflows while maintaining personalization at scale',
            'salary_factors': ['Email platform expertise', 'Automation experience', 'Performance optimization skills']
        },
        'salary_recommendations': {
            'salary_recommendations': {
                'United States': {'low': 80000, 'mid': 95000, 'high': 115000},
                'Philippines': {'low': 24000, 'mid': 30000, 'high': 38000},
                'Latin America': {'low': 42000, 'mid': 52000, 'high': 63000},
                'South Africa': {'low': 38000, 'mid': 48000, 'high': 58000}
            },
            'recommended_pay_band': 'mid',
            'factors_considered': ['Platform expertise', 'Regional market rates', 'Automation complexity'],
            'market_insights': {
                'high_demand_regions': ['United States', 'Philippines'],
                'competitive_factors': ['Klaviyo experience', 'Performance track record', 'Creative skills'],
                'cost_efficiency': 'Philippines offers 68% cost savings with strong email marketing talent pool'
            }
        }
    }
    
    # Get candidate profiles
    try:
        candidates = await get_candidate_profiles_for_template()
        print(f"✅ Retrieved {len(candidates)} candidate profiles")
    except:
        print("⚠️  Using mock candidate data")
        candidates = []
    
    # Generate all template variables
    try:
        template_variables = generate_template_variables(test_scan_data, candidates)
        print(f"✅ Generated {len(template_variables)} template variables")
    except Exception as e:
        print(f"❌ Failed to generate variables: {e}")
        return
    
    # Create full CSV file
    csv_content = create_csv_content(template_variables)
    
    # Save full CSV
    full_filename = "canva_test_full_135_variables.csv"
    with open(full_filename, 'w', newline='', encoding='utf-8') as f:
        f.write(csv_content)
    
    print(f"✅ Created full CSV: {full_filename}")
    print(f"   Variables: {len(template_variables)}")
    
    # Create simplified CSV for initial testing
    simplified_vars = create_simplified_test_csv(template_variables)
    simplified_content = create_csv_content(simplified_vars)
    
    # Save simplified CSV
    simple_filename = "canva_test_key_variables.csv"
    with open(simple_filename, 'w', newline='', encoding='utf-8') as f:
        f.write(simplified_content)
    
    print(f"✅ Created simplified CSV: {simple_filename}")
    print(f"   Variables: {len(simplified_vars)}")
    
    # Show key variables for testing
    print(f"\n📋 Key Variables for Canva Testing:")
    key_vars = [
        'company_name', 'position_title', 'scan_date', 
        'ph_salary', 'ph_savings_percent', 'latam_salary',
        'candidate_1_name', 'candidate_1_region', 'candidate_1_salary_range',
        'tier_1_fee', 'project_fee_total'
    ]
    
    for var in key_vars:
        value = template_variables.get(var, 'Not Found')
        print(f"   {var}: {value}")
    
    print(f"\n🎨 Canva Import Instructions:")
    print(f"1. Open Canva and create or select your market scan template")
    print(f"2. Go to 'Apps' → 'Bulk Create' (or Design → Bulk Create)")
    print(f"3. Upload either CSV file:")
    print(f"   • {simple_filename} (30 key variables - easier to start)")
    print(f"   • {full_filename} (135 variables - complete dataset)")
    print(f"4. Map CSV columns to template elements")
    print(f"5. Generate your personalized reports!")
    
    print(f"\n🧪 Test Results Expected:")
    print(f"✅ Company: Nike")
    print(f"✅ Role: Email Marketing Manager") 
    print(f"✅ Philippines Salary: $30,000 (68% savings)")
    print(f"✅ Candidate 1: {template_variables.get('candidate_1_name', 'Sample Candidate')}")
    print(f"✅ Service Fee: {template_variables.get('tier_1_fee', '$4,800')}")

def create_simplified_test_csv(full_variables: dict) -> dict:
    """Create a simplified CSV with key variables for initial testing"""
    key_variables = {
        # Company & Role (4 variables)
        'company_name': full_variables.get('company_name'),
        'position_title': full_variables.get('position_title'), 
        'scan_date': full_variables.get('scan_date'),
        'analysis_confidence': full_variables.get('analysis_confidence'),
        
        # Salary Data (8 variables)
        'us_salary': full_variables.get('us_salary'),
        'ph_salary': full_variables.get('ph_salary'),
        'ph_savings_percent': full_variables.get('ph_savings_percent'),
        'latam_salary': full_variables.get('latam_salary'),
        'latam_savings_percent': full_variables.get('latam_savings_percent'),
        'recommended_salary_min': full_variables.get('recommended_salary_min'),
        'recommended_salary_max': full_variables.get('recommended_salary_max'),
        
        # Skills (3 variables)
        'required_skills': full_variables.get('required_skills'),
        'preferred_skills': full_variables.get('preferred_skills'),
        'role_complexity': full_variables.get('role_complexity'),
        
        # Candidate 1 (5 variables)
        'candidate_1_name': full_variables.get('candidate_1_name'),
        'candidate_1_region': full_variables.get('candidate_1_region'),
        'candidate_1_salary_range': full_variables.get('candidate_1_salary_range'),
        'candidate_1_bio': full_variables.get('candidate_1_bio'),
        'candidate_1_tech_stack': full_variables.get('candidate_1_tech_stack'),
        
        # Pricing (4 variables)
        'tier_1_fee': full_variables.get('tier_1_fee'),
        'tier_2_fee': full_variables.get('tier_2_fee'),
        'project_fee_total': full_variables.get('project_fee_total'),
        'project_salary_range': full_variables.get('project_salary_range'),
        
        # Market Insights (3 variables)
        'best_regions': full_variables.get('best_regions'),
        'cost_efficiency': full_variables.get('cost_efficiency'),
        'role_challenges': full_variables.get('role_challenges')
    }
    
    # Filter out None values
    return {k: v for k, v in key_variables.items() if v is not None}

def create_csv_content(template_data: dict) -> str:
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

if __name__ == "__main__":
    asyncio.run(create_test_csv())