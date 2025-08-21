"""
Test Fix #2 - Candidate Role Matching with fresh request
"""

import asyncio
import requests
import json

async def test_candidate_fix():
    """Test that candidates now match the role category"""
    
    print("🔧 Testing Fix #2: Candidate Role Matching")
    print("=" * 50)
    
    # Test data - Data Engineer job (should map to Data Analyst candidates)
    test_data = {
        "client_name": "Fix Test",
        "client_email": "test@fix.com", 
        "company_domain": "fix.com",
        "job_title": "Data Engineer",
        "job_description": "Build data pipelines and work with databases.",
        "hiring_challenges": "Finding technical talent"
    }
    
    try:
        print("📤 Submitting fresh test scan...")
        
        # Submit new scan to test the fix
        response = requests.post(
            "http://localhost:8008/api/v1/market-scans/analyze",
            json=test_data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to submit scan: {response.status_code}")
            return
            
        scan_data = response.json()
        scan_id = scan_data['id']
        print(f"✅ New scan submitted: {scan_id}")
        
        # Wait for completion
        print("⏳ Waiting for analysis...")
        await asyncio.sleep(15)
        
        # Get completed scan to verify role_category
        response = requests.get(f"http://localhost:8008/api/v1/market-scans/{scan_id}")
        if response.status_code == 200:
            completed_scan = response.json()
            detected_role = completed_scan.get('job_analysis', {}).get('role_category', 'Unknown')
            print(f"🎯 Detected Role Category: {detected_role}")
            
            # Export CSV
            print("📁 Testing CSV export with fix...")
            response = requests.get(f"http://localhost:8008/api/v1/market-scans/{scan_id}/export?format=template")
            
            if response.status_code == 200:
                csv_content = response.text
                lines = csv_content.strip().split('\n')
                
                if len(lines) >= 2:
                    headers = lines[0].split(',')
                    data_row = lines[1]
                    
                    # Parse CSV more carefully
                    import csv
                    import io
                    
                    csv_reader = csv.DictReader(io.StringIO(csv_content))
                    row = next(csv_reader)
                    
                    # Extract candidate information
                    candidates_info = []
                    for i in range(1, 4):  # candidates 1-3
                        candidate = {
                            'name': row.get(f'candidate_{i}_name', ''),
                            'role': row.get(f'candidate_{i}_role', ''),
                            'experience': row.get(f'candidate_{i}_experience', ''),
                            'region': row.get(f'candidate_{i}_region', '')
                        }
                        if candidate['name']:  # Only include if name exists
                            candidates_info.append(candidate)
                    
                    print(f"\n👥 Exported Candidates:")
                    for i, candidate in enumerate(candidates_info, 1):
                        print(f"  {i}. {candidate['name']}")
                        print(f"     Role: {candidate['role']}")
                        print(f"     Experience: {candidate['experience']}")
                        print(f"     Region: {candidate['region']}")
                        print()
                    
                    # Check if candidates match the expected role
                    data_related_candidates = [
                        c for c in candidates_info 
                        if any(keyword in c['role'].lower() for keyword in ['data', 'analyst', 'engineer'])
                    ]
                    
                    if data_related_candidates:
                        print("✅ SUCCESS: Found data-related candidates!")
                        print(f"   Expected role: {detected_role}")
                        print(f"   Matching candidates: {len(data_related_candidates)}")
                    else:
                        print("❌ ISSUE: No data-related candidates found")
                        print(f"   Expected role: {detected_role}")
                        print(f"   Actual roles: {[c['role'] for c in candidates_info]}")
                
                else:
                    print("❌ CSV export malformed")
                    
            else:
                print(f"❌ CSV export failed: {response.status_code}")
        else:
            print(f"❌ Failed to get scan: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_candidate_fix())