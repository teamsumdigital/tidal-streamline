#!/usr/bin/env python3
"""
Test the CSV export endpoint with template variable generation
"""

import asyncio
import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.append('/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend')

from app.core.database import db
from app.api.v1.endpoints.export import generate_template_variables, get_candidate_profiles_for_template

async def test_csv_export():
    """Test CSV export functionality"""
    print("🧪 Testing CSV Export Endpoint...")
    
    # Test database connection
    try:
        connection_test = await db.test_connection()
        print(f"✅ Database connection: {'Success' if connection_test else 'Failed'}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Get candidate profiles
    try:
        candidates = await get_candidate_profiles_for_template()
        print(f"✅ Retrieved {len(candidates)} candidate profiles")
        
        for i, candidate in enumerate(candidates, 1):
            print(f"   {i}. {candidate.get('name', 'Unknown')} - {candidate.get('role_category', 'Unknown')} ({candidate.get('region', 'Unknown')})")
    except Exception as e:
        print(f"❌ Failed to get candidates: {e}")
        return
    
    # Create mock scan data
    mock_scan_data = {
        'id': 'test-scan-123',
        'company_domain': 'acme-corp.com',
        'job_title': 'Content Marketing Manager',
        'job_description': 'We are looking for an experienced content marketing manager...',
        'confidence_score': 0.87,
        'job_analysis': {
            'role_category': 'Content Marketer',
            'experience_level': 'mid',
            'years_experience_required': '3-5 years',
            'must_have_skills': ['Content Strategy', 'Social Media', 'Analytics', 'Copywriting', 'Email Marketing'],
            'nice_to_have_skills': ['SEO', 'Paid Advertising', 'Video Editing', 'Graphic Design'],
            'key_responsibilities': ['Develop content strategies', 'Create engaging content', 'Analyze performance metrics'],
            'remote_work_suitability': 'high',
            'complexity_score': 7,
            'recommended_regions': ['Philippines', 'Latin America'],
            'unique_challenges': 'Managing content across multiple channels and measuring ROI',
            'salary_factors': ['Content expertise', 'Analytics skills', 'Experience level']
        },
        'salary_recommendations': {
            'salary_recommendations': {
                'United States': {'low': 75000, 'mid': 95000, 'high': 120000},
                'Philippines': {'low': 22000, 'mid': 28000, 'high': 35000},
                'Latin America': {'low': 40000, 'mid': 52000, 'high': 65000},
                'South Africa': {'low': 35000, 'mid': 45000, 'high': 58000}
            },
            'market_insights': {
                'high_demand_regions': ['United States', 'Philippines'],
                'competitive_factors': ['Experience', 'Portfolio quality', 'Technical skills'],
                'cost_efficiency': 'Philippines offers the best value for content marketing roles'
            }
        }
    }
    
    # Generate template variables
    try:
        template_variables = generate_template_variables(mock_scan_data, candidates)
        print(f"✅ Generated {len(template_variables)} template variables")
        
        # Show some key variables
        print("\n📊 Key Template Variables Generated:")
        key_vars = [
            'company_name', 'position_title', 'ph_salary', 'ph_savings_percent',
            'candidate_1_name', 'candidate_1_region', 'candidate_2_name', 'candidate_3_name',
            'tier_1_fee', 'project_fee_total', 'tidal_results'
        ]
        
        for var in key_vars:
            value = template_variables.get(var, 'Not Found')
            print(f"   {var}: {value}")
            
        # Count variables by category
        candidate_vars = len([v for v in template_variables.keys() if v.startswith('candidate_')])
        pricing_vars = len([v for v in template_variables.keys() if 'tier_' in v or 'project_' in v])
        salary_vars = len([v for v in template_variables.keys() if 'salary' in v])
        
        print(f"\n📈 Variable Categories:")
        print(f"   Candidate Variables: {candidate_vars}")
        print(f"   Pricing Variables: {pricing_vars}")
        print(f"   Salary Variables: {salary_vars}")
        print(f"   Total Variables: {len(template_variables)}")
        
        # Check for missing variables from the 134 target
        target_variables = 134
        coverage_percent = (len(template_variables) / target_variables) * 100
        print(f"\n🎯 Template Coverage: {len(template_variables)}/{target_variables} ({coverage_percent:.1f}%)")
        
        if len(template_variables) >= 120:
            print("✅ Excellent coverage! Ready for Canva integration")
        elif len(template_variables) >= 100:
            print("✅ Good coverage! Minor variables may be missing")
        else:
            print("⚠️  Coverage below target. Additional variables needed")
            
    except Exception as e:
        print(f"❌ Failed to generate template variables: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n🎉 CSV Export Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_csv_export())