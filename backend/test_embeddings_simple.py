#!/usr/bin/env python3
"""
Simple embedding test for Tidal Streamline
"""

import os
from pinecone import Pinecone

def test_embeddings():
    """Test embedding generation and storage"""
    print("🧪 Testing Embeddings (Mock)...")
    
    # Mock embedding for testing (1536 dimensions)
    mock_embedding = [0.1] * 1536
    
    # Initialize Pinecone
    api_key = "pcsk_2asZaU_4JFVKA6KRDqh2i37Vn8bcWRx5cPhhGDhYcDmcemg3GGpG2m44TPouFMVkEzQqBe"
    index_name = "tidal-streamline"
    
    try:
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)
        
        # Test vector upsert
        test_vector = {
            "id": "test-scan-001",
            "values": mock_embedding,
            "metadata": {
                "job_title": "E-commerce Marketing Manager",
                "role_category": "Brand Marketing Manager",
                "experience_level": "mid",
                "complexity_score": 7,
                "skills": ["Excel", "Shopify", "Facebook Ads"],
                "regions": ["Philippines", "Latin America"],
                "created_at": "2025-01-15T21:00:00Z"
            }
        }
        
        print("📤 Upserting test vector...")
        index.upsert(vectors=[test_vector])
        print("✅ Test vector upserted successfully")
        
        # Test vector query
        print("🔍 Testing vector search...")
        results = index.query(
            vector=mock_embedding,
            top_k=5,
            include_metadata=True
        )
        
        print(f"📊 Query results: {len(results.matches)} matches found")
        if results.matches:
            match = results.matches[0]
            print(f"🎯 Top match: {match.metadata.get('job_title')} (score: {match.score:.4f})")
        
        # Get index stats
        stats = index.describe_index_stats()
        print(f"📈 Index stats: {stats['total_vector_count']} vectors")
        
        print("\n🎉 Embeddings test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Embeddings test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_embeddings()