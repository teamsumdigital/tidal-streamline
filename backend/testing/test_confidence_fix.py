"""
Test the confidence score and candidate matching fixes
"""

import asyncio
import requests
import json

async def test_fixes():
    """Test that confidence score and candidate matching are working"""
    
    print("🧪 Testing Confidence Score and Candidate Matching Fixes")
    print("=" * 60)
    
    # Test data - Data Engineer job
    test_data = {
        "client_name": "Test User",
        "client_email": "test@example.com", 
        "company_domain": "test.com",
        "job_title": "Data Engineer",
        "job_description": "We are looking for a skilled Data Engineer to join our team. Responsibilities include building and maintaining data pipelines, ensuring data quality, and working with cloud platforms.",
        "hiring_challenges": "Finding candidates with both technical skills and cloud experience"
    }
    
    try:
        print("📤 Submitting test market scan...")
        
        # Submit scan
        response = requests.post(
            "http://localhost:8008/api/v1/market-scans/analyze",
            json=test_data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to submit scan: {response.status_code}")
            print(response.text)
            return
            
        scan_data = response.json()
        scan_id = scan_data['id']
        print(f"✅ Scan submitted: {scan_id}")
        
        # Wait for completion
        print("⏳ Waiting for analysis to complete...")
        await asyncio.sleep(15)
        
        # Get completed scan
        response = requests.get(f"http://localhost:8008/api/v1/market-scans/{scan_id}")
        if response.status_code == 200:
            completed_scan = response.json()
            
            # Check confidence score
            confidence = completed_scan.get('confidence_score', 0)
            print(f"📊 Confidence Score: {confidence}")
            
            if confidence > 0:
                print("✅ Fix #1 SUCCESS: Confidence score is no longer 0")
            else:
                print("❌ Fix #1 FAILED: Confidence score is still 0")
            
            # Export CSV to check candidates
            print("\n📁 Testing CSV export...")
            response = requests.get(f"http://localhost:8008/api/v1/market-scans/{scan_id}/export?format=template")
            
            if response.status_code == 200:
                csv_content = response.text
                lines = csv_content.strip().split('\n')
                
                if len(lines) >= 2:  # Header + data
                    headers = lines[0].split(',')
                    data = lines[1].split(',')
                    
                    # Find candidate role columns
                    candidate_roles = []
                    for i, header in enumerate(headers):
                        if 'candidate_' in header and '_role' in header:
                            if i < len(data):
                                candidate_roles.append(data[i])
                    
                    print(f"🎯 Candidate Roles Found: {candidate_roles}")
                    
                    # Check if any candidates match "Data Analyst" (the correct role category)
                    data_related_roles = [role for role in candidate_roles if any(word in role.lower() for word in ['data', 'analyst', 'engineer'])]
                    
                    if data_related_roles:
                        print("✅ Fix #2 SUCCESS: Found data-related candidates")
                        for role in data_related_roles:
                            print(f"   • {role}")
                    else:
                        print("❌ Fix #2 NEEDS WORK: No data-related candidates found")
                        print(f"   Found roles: {candidate_roles}")
                else:
                    print("❌ CSV export failed - not enough lines")
            else:
                print(f"❌ CSV export failed: {response.status_code}")
        else:
            print(f"❌ Failed to get completed scan: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_fixes())