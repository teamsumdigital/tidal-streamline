#!/usr/bin/env python3
"""
Populate ALL 23 candidate profiles with data from Regional Talent Comparison Master PDF
Run after database migration to add template-ready candidate data
"""

import os
import sys
import json
from datetime import date
from supabase import create_client

# Set Supabase credentials
os.environ['SUPABASE_URL'] = 'https://fhaiolgezcghbiwyayrp.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZoYWlvbGdlemNnaGJpd3lheXJwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTIxNDQ5OSwiZXhwIjoyMDcwNzkwNDk5fQ.uWSsz2y6hdNrzZ8iMQeLKfMrZ24QdRPAQPzyO7RSkqg'

def populate_all_candidates():
    """Populate candidate profiles with template-ready data for all 23 candidates"""
    
    # Load complete candidate data
    try:
        with open('complete_candidates.json', 'r', encoding='utf-8') as f:
            candidate_data = json.load(f)
    except FileNotFoundError:
        print("❌ complete_candidates.json not found. Please run extract_all_candidates.py first.")
        sys.exit(1)
    
    # Initialize Supabase client
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables required")
        sys.exit(1)
    
    supabase = create_client(supabase_url, supabase_key)
    
    print(f"Populating {len(candidate_data)} candidate profiles with template data...")
    
    success_count = 0
    error_count = 0
    
    for candidate in candidate_data:
        try:
            # Check if candidate exists
            existing = supabase.table('candidate_profiles').select('id').eq('name', candidate['name']).execute()
            
            if existing.data:
                # Update existing candidate
                result = supabase.table('candidate_profiles').update(candidate).eq('name', candidate['name']).execute()
                print(f"✅ Updated candidate: {candidate['name']} ({candidate['role_category']}) - {candidate['region']}")
                success_count += 1
            else:
                # Insert new candidate
                result = supabase.table('candidate_profiles').insert(candidate).execute()
                print(f"✅ Inserted candidate: {candidate['name']} ({candidate['role_category']}) - {candidate['region']}")
                success_count += 1
                
        except Exception as e:
            print(f"❌ Error processing {candidate['name']}: {str(e)}")
            error_count += 1
    
    print(f"\n🎉 Candidate data population complete!")
    print(f"✅ Successfully processed: {success_count} candidates")
    if error_count > 0:
        print(f"❌ Errors encountered: {error_count} candidates")
    
    print(f"\n📊 Summary by region:")
    regions = {}
    for candidate in candidate_data:
        region = candidate['region']
        if region not in regions:
            regions[region] = 0
        regions[region] += 1
    
    for region, count in regions.items():
        print(f"  {region}: {count} candidates")
    
    print(f"\n📊 Summary by role category:")
    roles = {}
    for candidate in candidate_data:
        role = candidate['role_category']
        if role not in roles:
            roles[role] = 0
        roles[role] += 1
    
    for role, count in sorted(roles.items()):
        print(f"  {role}: {count} candidates")
    
    print("\nNext steps:")
    print("1. ✅ Database populated with all 23 candidates")
    print("2. 🔄 Create backend CSV export endpoint (/api/v1/market-scans/{scanId}/export)")
    print("3. 🧪 Test template variable generation with candidate data")
    print("4. 🎨 Verify Canva template integration with all 134 variables")

if __name__ == "__main__":
    populate_all_candidates()