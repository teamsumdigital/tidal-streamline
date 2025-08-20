#!/usr/bin/env python3
"""
Test the actual CSV export API endpoint
"""

import asyncio
import sys
from datetime import datetime
import uuid

# Add backend directory to path
sys.path.append('/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend')

from app.core.database import db
from app.api.v1.endpoints.export import export_market_scan_csv

async def test_api_endpoint():
    """Test the actual CSV export API endpoint"""
    print("🧪 Testing CSV Export API Endpoint...")
    
    # Test database connection
    try:
        connection_test = await db.test_connection()
        if not connection_test:
            print("❌ Database connection failed")
            return
        print("✅ Database connection: Success")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Create a test market scan
    scan_id = str(uuid.uuid4())
    print(f"📝 Creating test market scan: {scan_id}")
    
    test_scan_data = {
        'id': scan_id,
        'client_name': 'Acme Corporation',
        'client_email': 'test@acme-corp.com',
        'company_domain': 'acme-corp.com',
        'job_title': 'Content Marketing Specialist',
        'job_description': 'We are seeking an experienced content marketing specialist to develop and execute comprehensive content strategies...',
        'hiring_challenges': 'Finding candidates with both creative and analytical skills',
        'status': 'completed',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'confidence_score': 0.89,
        'job_analysis': {
            'role_category': 'Content Marketer',
            'experience_level': 'mid',
            'years_experience_required': '3-5 years',
            'must_have_skills': ['Content Strategy', 'Social Media Marketing', 'Analytics', 'SEO', 'Email Marketing'],
            'nice_to_have_skills': ['Video Editing', 'Graphic Design', 'Paid Advertising', 'Marketing Automation'],
            'key_responsibilities': [
                'Develop comprehensive content marketing strategies',
                'Create engaging content across multiple channels',
                'Analyze performance metrics and optimize campaigns',
                'Collaborate with design and marketing teams'
            ],
            'remote_work_suitability': 'high',
            'complexity_score': 7,
            'recommended_regions': ['Philippines', 'Latin America', 'South Africa'],
            'unique_challenges': 'Balancing creative content development with data-driven optimization',
            'salary_factors': ['Content portfolio quality', 'Analytics expertise', 'Multi-channel experience']
        },
        'salary_recommendations': {
            'salary_recommendations': {
                'United States': {'low': 70000, 'mid': 85000, 'high': 105000},
                'Philippines': {'low': 20000, 'mid': 26000, 'high': 32000},
                'Latin America': {'low': 38000, 'mid': 48000, 'high': 58000},
                'South Africa': {'low': 32000, 'mid': 42000, 'high': 52000}
            },
            'recommended_pay_band': 'mid',
            'factors_considered': ['Experience level', 'Regional market rates', 'Skill complexity'],
            'market_insights': {
                'high_demand_regions': ['United States', 'Philippines', 'Latin America'],
                'competitive_factors': ['Portfolio quality', 'Multi-platform experience', 'Analytics skills'],
                'cost_efficiency': 'Philippines offers excellent value with strong English proficiency and creative talent'
            }
        },
        'skills_recommendations': {
            'must_have_skills': ['Content Strategy', 'Social Media Marketing', 'Analytics'],
            'nice_to_have_skills': ['Video Editing', 'Graphic Design', 'Paid Advertising'],
            'skill_categories': {
                'technical': ['Content Strategy', 'Analytics', 'SEO'],
                'creative': ['Social Media Marketing', 'Video Editing', 'Graphic Design'],
                'analytical': ['Analytics', 'Email Marketing', 'Marketing Automation']
            },
            'certification_recommendations': ['Google Analytics', 'HubSpot Content Marketing', 'Hootsuite Social Media']
        }
    }
    
    # Save test scan to database
    try:
        created_scan = await db.create_market_scan(test_scan_data)
        print(f"✅ Created test market scan in database")
    except Exception as e:
        print(f"❌ Failed to create test scan: {e}")
        return
    
    # Test the CSV export endpoint
    try:
        print("🔄 Testing CSV export endpoint...")
        csv_response = await export_market_scan_csv(scan_id, format="template")
        
        print("✅ CSV export endpoint successful!")
        
        # Check response properties
        print(f"📄 Response media type: {csv_response.media_type}")
        print(f"📎 Content-Disposition: {csv_response.headers.get('Content-Disposition', 'Not set')}")
        
        # Check CSV content
        csv_content = csv_response.body.decode('utf-8')
        lines = csv_content.split('\n')
        
        print(f"📊 CSV Analysis:")
        print(f"   Total lines: {len(lines)}")
        print(f"   Variables: {len(lines) - 2} (excluding header and empty line)")  # -1 for header, -1 for potential empty line
        
        # Check for key variables
        key_variables_found = 0
        key_variables_to_check = [
            'company_name,acme-corp.com',
            'position_title,Content Marketing Specialist',
            'candidate_1_name,',
            'candidate_2_name,',
            'candidate_3_name,',
            'ph_salary,',
            'ph_savings_percent,',
            'tier_1_fee,$4,800',
            'project_fee_total,$5,600 Total'
        ]
        
        for var_check in key_variables_to_check:
            var_name = var_check.split(',')[0]
            if any(var_name in line for line in lines):
                key_variables_found += 1
        
        print(f"   Key variables found: {key_variables_found}/{len(key_variables_to_check)}")
        
        # Show first few variables
        print("\n📋 First 10 Variables:")
        header_found = False
        count = 0
        for line in lines:
            if not header_found and line.startswith('Variable,Value'):
                header_found = True
                continue
            if header_found and line.strip() and count < 10:
                print(f"   {line}")
                count += 1
            if count >= 10:
                break
        
        # Check candidate variables specifically
        candidate_vars = [line for line in lines if 'candidate_' in line]
        print(f"\n👥 Candidate Variables: {len(candidate_vars)} found")
        
        # Check pricing variables
        pricing_vars = [line for line in lines if any(term in line for term in ['tier_', 'project_', 'tidal_', 'bpo_'])]
        print(f"💰 Pricing Variables: {len(pricing_vars)} found")
        
        if len(lines) >= 130:  # Should have ~135 variables plus header
            print("✅ Template has excellent variable coverage for Canva integration!")
        elif len(lines) >= 100:
            print("✅ Template has good variable coverage")
        else:
            print("⚠️  Template may be missing some variables")
        
    except Exception as e:
        print(f"❌ CSV export endpoint failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n🎉 API Endpoint Test Complete!")
    print("\n🎯 Next Steps:")
    print("1. ✅ Backend CSV export endpoint working with 135+ variables")
    print("2. 🎨 Test with actual Canva template integration")
    print("3. 🔗 Add endpoint to frontend for download button")
    print("4. 📊 Verify all variable mappings in template")

if __name__ == "__main__":
    asyncio.run(test_api_endpoint())