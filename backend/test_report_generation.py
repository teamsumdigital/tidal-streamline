#!/usr/bin/env python3
"""
Test Report Generation Workflow
Tests the complete report generation system with mock data
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add the backend directory to Python path for proper imports
sys.path.insert(0, os.path.dirname(__file__))

# Mock the dependencies to test the core logic
class MockConfig:
    def __init__(self):
        pass

class MockLogger:
    def info(self, msg): print(f"INFO: {msg}")
    def error(self, msg): print(f"ERROR: {msg}")
    def warning(self, msg): print(f"WARNING: {msg}")

def get_logger(name=None):
    return MockLogger()

def get_settings():
    return MockConfig()

# Create mock modules
config_module = type('module', (), {})()
config_module.get_settings = get_settings

logger_module = type('module', (), {})()
logger_module.get_logger = get_logger

# Patch the imports
sys.modules['app.core.config'] = config_module
sys.modules['app.core.logger'] = logger_module

from app.services.report_generator import TidalReportGenerator

def create_mock_scan_data() -> Dict[str, Any]:
    """Create mock market scan data for testing"""
    return {
        "id": "test-scan-001",
        "client_info": {
            "client_name": "UNDERCLUB",
            "client_email": "hiring@underclub.com",
            "company_domain": "underclub.com"
        },
        "job_title": "Operations Manager",
        "job_description": "We are looking for an experienced Operations Manager to oversee our e-commerce operations, manage supply chain logistics, and optimize our business processes. The ideal candidate will have experience with Shopify, inventory management, and team leadership.",
        "job_analysis": {
            "role_title": "Operations Manager",
            "role_category": "Operations Manager",
            "experience_level": "5-8 years",
            "complexity_score": 7,
            "key_responsibilities": [
                "Manage daily e-commerce operations",
                "Oversee supply chain and logistics",
                "Lead and develop operations team",
                "Optimize business processes",
                "Analyze performance metrics"
            ],
            "key_challenges": [
                "Managing complex inventory systems",
                "Coordinating multiple suppliers and vendors",
                "Scaling operations efficiently",
                "Maintaining quality while reducing costs"
            ],
            "remote_work_suitability": "Excellent",
            "recommended_regions": ["Philippines", "Latin America", "South Africa"]
        },
        "salary_recommendations": {
            "salary_recommendations": {
                "Philippines": {
                    "range_low": 1800,
                    "range_mid": 2050,
                    "range_high": 2300,
                    "currency": "USD",
                    "period": "monthly",
                    "savings_vs_us": 71
                },
                "Latin America": {
                    "range_low": 2200,
                    "range_mid": 2575,
                    "range_high": 2950,
                    "currency": "USD", 
                    "period": "monthly",
                    "savings_vs_us": 58
                },
                "South Africa": {
                    "range_low": 2300,
                    "range_mid": 2650,
                    "range_high": 3000,
                    "currency": "USD",
                    "period": "monthly", 
                    "savings_vs_us": 48
                },
                "United States": {
                    "range_low": 5000,
                    "range_mid": 6000,
                    "range_high": 7000,
                    "currency": "USD",
                    "period": "monthly",
                    "savings_vs_us": 0
                }
            },
            "recommended_pay_band": "$2,500 - $3,000",
            "factors_considered": [
                "Role complexity and responsibilities",
                "Required experience level",
                "Regional market rates",
                "Skills requirements"
            ]
        },
        "skills_recommendations": {
            "must_have_skills": [
                "Shopify Admin Experience",
                "Supply Chain Management", 
                "Project Management",
                "Team Leadership",
                "Data Analysis"
            ],
            "nice_to_have_skills": [
                "ERP Systems (NetSuite, SAP)",
                "Power BI / Tableau",
                "Amazon Seller Central",
                "3PL Management",
                "Process Optimization"
            ],
            "similar_roles": [
                {
                    "title": "Business Operations Manager",
                    "similarity": 35
                },
                {
                    "title": "E-commerce Operations Manager", 
                    "similarity": 30
                },
                {
                    "title": "Shopify Operations Manager",
                    "similarity": 20
                }
            ]
        },
        "status": "completed",
        "confidence_score": 0.89,
        "created_at": datetime.utcnow().isoformat(),
        "processing_time_seconds": 45
    }

async def test_report_generation():
    """Test the complete report generation workflow"""
    print("🧪 Testing Tidal Report Generation System")
    print("=" * 50)
    
    # Create mock scan data
    print("📝 Creating mock market scan data...")
    scan_data = create_mock_scan_data()
    
    # Print scan summary
    print(f"   Client: {scan_data['client_info']['client_name']}")
    print(f"   Role: {scan_data['job_title']}")
    print(f"   Regions: {len(scan_data['salary_recommendations']['salary_recommendations'])} regions")
    print(f"   Skills: {len(scan_data['skills_recommendations']['must_have_skills'])} must-have skills")
    print()
    
    # Initialize report generator
    print("🔧 Initializing TidalReportGenerator...")
    report_generator = TidalReportGenerator()
    print("   ✅ Report generator initialized")
    print()
    
    # Test template data preparation
    print("📋 Testing template data mapping...")
    try:
        template_data = report_generator._prepare_template_data(scan_data)
        
        print("   ✅ Template data mapping successful!")
        print(f"   📊 Data fields mapped:")
        print(f"      - Client: {template_data['client_name']}")
        print(f"      - Role: {template_data['role_title']}")
        print(f"      - Regions: {len(template_data['regions'])} regions")
        print(f"      - Candidate profiles: {len(template_data['candidate_profiles'])}")
        print(f"      - Similar roles: {len(template_data['role_insights']['similar_roles'])}")
        print(f"      - Required tools: {len(template_data['role_insights']['required_tools'])}")
        print()
        
        # Display regional data details
        print("   🌍 Regional Analysis:")
        for region in template_data['regions']:
            print(f"      - {region['name']}: {region['salary_range']} ({region['recommendation']})")
        print()
        
        # Display role insights
        print("   🎯 Role Insights:")
        print(f"      - Similar roles: {', '.join([r['title'] for r in template_data['role_insights']['similar_roles'][:3]])}")
        print(f"      - Required tools: {', '.join(template_data['role_insights']['required_tools'][:5])}")
        print()
        
    except Exception as e:
        print(f"   ❌ Template data mapping failed: {str(e)}")
        return False
    
    # Test report generation (mock mode)
    print("📄 Testing report generation...")
    try:
        report_result = await report_generator.generate_market_scan_report(scan_data)
        
        if report_result['success']:
            print("   ✅ Report generation successful!")
            print(f"   📊 Report details:")
            print(f"      - Report URL: {report_result['report_url']}")
            print(f"      - Preview URL: {report_result.get('preview_url', 'N/A')}")
            print(f"      - Pages: {report_result['pages']}")
            print(f"      - Client: {report_result['client_name']}")
            print(f"      - Role: {report_result['role_title']}")
            print(f"      - Generated: {report_result['generated_at']}")
            print()
        else:
            print(f"   ❌ Report generation failed: {report_result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Report generation error: {str(e)}")
        return False
    
    # Test individual page generation
    print("📑 Testing individual page generation...")
    try:
        # Test cover page
        cover_page = await report_generator._generate_cover_page(template_data)
        print(f"   ✅ Cover page: {cover_page['design_id']}")
        
        # Test regional overview
        regional_overview = await report_generator._generate_regional_overview(template_data)
        print(f"   ✅ Regional overview: {regional_overview['design_id']}")
        
        # Test role detail page
        role_detail = await report_generator._generate_role_detail_page(template_data, template_data['regions'][0])
        print(f"   ✅ Role detail ({template_data['regions'][0]['name']}): {role_detail['design_id']}")
        
        # Test insights page
        insights_page = await report_generator._generate_insights_page(template_data)
        print(f"   ✅ Insights page: {insights_page['design_id']}")
        
        # Test candidate profiles
        candidate_page = await report_generator._generate_candidate_profiles(template_data)
        print(f"   ✅ Candidate profiles: {candidate_page['design_id']}")
        print()
        
    except Exception as e:
        print(f"   ❌ Individual page generation error: {str(e)}")
        return False
    
    print("🎉 All tests passed! Report generation system is working correctly.")
    print()
    print("💡 Next Steps:")
    print("   1. Set up Canva API integration (add CANVA_API_KEY to .env)")
    print("   2. Create actual Canva templates with proper IDs")
    print("   3. Test with real market scan data")
    print("   4. Deploy and integrate with frontend")
    
    return True

async def main():
    """Main test function"""
    try:
        success = await test_report_generation()
        if success:
            print("\n✅ Report generation test completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Report generation test failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())