#!/usr/bin/env python3
"""
Fix and retry failed scans with null metadata values
"""

import asyncio
import json
from typing import Dict, Any
from app.services.embedding_service import embedding_service
from app.core.database import DatabaseManager

async def fix_and_retry_failed_scans():
    """Fix failed scans and retry upload to Pinecone"""
    
    # List of failed scan IDs from the previous run
    failed_scan_ids = [
        'c3eacf1e-24d8-45f3-8665-a677c45a580d',
        '13ddd96d-9257-4b28-8869-a38db230aca9', 
        '80a0aadb-488b-48b3-906c-18e8822b82c2',
        'fc7b4178-2a88-4ab0-aaec-18da2a5bd030',
        'fe1a66c5-ec2d-4391-a04e-fd3e339cc36a'
    ]
    
    print(f"🔧 Fixing and retrying {len(failed_scan_ids)} failed scans...")
    
    # Initialize services
    db_manager = DatabaseManager()
    
    successful_fixes = 0
    
    for scan_id in failed_scan_ids:
        try:
            print(f"\n🔍 Processing scan: {scan_id}")
            
            # Fetch the scan from database
            query = "SELECT * FROM market_scans WHERE id = %s"
            result = db_manager.execute_query(query, (scan_id,))
            
            if not result:
                print(f"❌ Scan not found in database: {scan_id}")
                continue
                
            scan = result[0]
            
            # Create text for embedding
            job_title = scan.get('job_title', '') or ''
            job_description = scan.get('job_description', '') or ''
            text_content = f"{job_title} {job_description}".strip()
            
            if not text_content:
                print(f"❌ No content to embed for scan: {scan_id}")
                continue
            
            print(f"📝 Content: {text_content[:100]}...")
            
            # Generate embedding
            embedding = await embedding_service.generate_embedding(text_content)
            
            # Parse job analysis
            job_analysis = {}
            if scan.get('job_analysis'):
                try:
                    if isinstance(scan['job_analysis'], str):
                        job_analysis = json.loads(scan['job_analysis'])
                    else:
                        job_analysis = scan['job_analysis']
                except:
                    job_analysis = {}
            
            # Clean metadata - ensure no null values
            def clean_value(value, default=''):
                if value is None:
                    return default
                return value
            
            def clean_numeric(value, default=0):
                if value is None:
                    return default
                try:
                    return int(value) if isinstance(value, (int, float)) else default
                except:
                    return default
            
            metadata = {
                "job_title": clean_value(scan.get('job_title'), ''),
                "company_domain": clean_value(scan.get('company_domain'), ''),
                "client_name": clean_value(scan.get('client_name'), ''),
                "role_category": clean_value(scan.get('role_category') or job_analysis.get('role_category'), ''),
                "experience_level": clean_value(job_analysis.get('experience_level'), ''),
                "complexity_score": clean_numeric(job_analysis.get('complexity_score'), 0),
                "status": clean_value(scan.get('status'), ''),
                "created_at": clean_value(scan.get('created_at'), ''),
                "updated_at": clean_value(scan.get('updated_at'), ''),
                "processing_time_seconds": clean_numeric(scan.get('processing_time_seconds'), 0),
                "confidence_score": clean_numeric(scan.get('confidence_score'), 0),
                "similar_scans_count": clean_numeric(scan.get('similar_scans_count'), 0),
                "must_have_skills": json.dumps(job_analysis.get('must_have_skills', [])),
                "recommended_regions": json.dumps(scan.get('recommended_regions', []) or job_analysis.get('recommended_regions', [])),
                "remote_work_suitability": clean_value(job_analysis.get('remote_work_suitability'), ''),
                "hiring_challenges": clean_value(scan.get('hiring_challenges'), '')[:500],
                "description_preview": text_content[:200] + "..." if len(text_content) > 200 else text_content
            }
            
            # Verify no null values
            for key, value in metadata.items():
                if value is None:
                    print(f"⚠️ Found null value for {key}, fixing...")
                    metadata[key] = '' if key.endswith(('_at', 'name', 'title', 'category', 'level', 'status')) else 0
            
            print(f"📤 Uploading to Pinecone...")
            
            # Upload to Pinecone
            vector = {
                "id": scan_id,
                "values": embedding,
                "metadata": metadata
            }
            
            success = await embedding_service.upsert_vectors([vector])
            
            if success:
                print(f"✅ Successfully uploaded scan: {scan_id}")
                successful_fixes += 1
            else:
                print(f"❌ Failed to upload scan: {scan_id}")
                
        except Exception as e:
            print(f"❌ Error processing scan {scan_id}: {str(e)}")
            continue
    
    print(f"\n📊 Fix Results:")
    print(f"   Total attempted: {len(failed_scan_ids)}")
    print(f"   Successfully fixed: {successful_fixes}")
    print(f"   Still failing: {len(failed_scan_ids) - successful_fixes}")
    
    # Check final index stats
    try:
        stats = embedding_service.get_index_stats()
        print(f"   Pinecone index now has: {stats['total_vector_count']} vectors")
    except:
        pass
    
    print("✨ Fix operation completed!")

if __name__ == "__main__":
    asyncio.run(fix_and_retry_failed_scans())