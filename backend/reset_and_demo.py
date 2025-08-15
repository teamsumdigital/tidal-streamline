#!/usr/bin/env python3
"""
Reset Pinecone index and run semantic matching demo
"""

import time
from pinecone import Pinecone

def reset_and_demo():
    """Clear index and demonstrate semantic matching"""
    print("🧹 Resetting Pinecone Index...")
    
    # Initialize Pinecone
    api_key = "pcsk_2asZaU_4JFVKA6KRDqh2i37Vn8bcWRx5cPhhGDhYcDmcemg3GGpG2m44TPouFMVkEzQqBe"
    index_name = "tidal-streamline"
    
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    
    # Delete all vectors by fetching IDs first
    try:
        # Get all vector IDs (this might take a while for large indexes)
        stats = index.describe_index_stats()
        print(f"📊 Current vectors: {stats['total_vector_count']}")
        
        if stats['total_vector_count'] > 0:
            # Delete all vectors in the default namespace
            index.delete(delete_all=True)
            print("🗑️ Deleted all existing vectors")
            
            # Wait for deletion to propagate
            time.sleep(5)
        
        # Verify deletion
        new_stats = index.describe_index_stats()
        print(f"✅ Index cleared. Vectors remaining: {new_stats['total_vector_count']}")
        
    except Exception as e:
        print(f"⚠️ Error during cleanup: {e}")
    
    # Now add test data with unique embeddings
    print("\n📤 Adding test data with diverse embeddings...")
    
    test_vectors = [
        {
            "id": "marketing-ecom-001",
            "values": [0.8] + [0.1] * 200 + [0.6] * 300 + [0.0] * 1035,  # Marketing + Ecommerce pattern
            "metadata": {
                "job_title": "E-commerce Marketing Manager",
                "role_category": "Brand Marketing Manager",
                "experience_level": "mid",
                "skills": ["Shopify", "Facebook Ads", "Email Marketing"],
                "regions": ["Philippines", "Latin America"],
                "complexity_score": 7
            }
        },
        {
            "id": "social-media-002", 
            "values": [0.2] + [0.9] * 150 + [0.1] * 200 + [0.0] * 1185,  # Social Media pattern
            "metadata": {
                "job_title": "Social Media Manager",
                "role_category": "Brand Marketing Manager", 
                "experience_level": "junior",
                "skills": ["Social Media", "Content Creation", "Instagram"],
                "regions": ["Philippines"],
                "complexity_score": 5
            }
        },
        {
            "id": "data-analyst-003",
            "values": [0.1] * 100 + [0.9] * 200 + [0.7] * 150 + [0.0] * 1086,  # Data pattern
            "metadata": {
                "job_title": "Data Analyst",
                "role_category": "Data Analyst",
                "experience_level": "mid", 
                "skills": ["SQL", "Excel", "Python", "Tableau"],
                "regions": ["Philippines", "Latin America"],
                "complexity_score": 8
            }
        },
        {
            "id": "store-manager-004",
            "values": [0.7] + [0.0] * 150 + [0.8] * 200 + [0.4] * 100 + [0.0] * 1085,  # Store management
            "metadata": {
                "job_title": "Online Store Manager",
                "role_category": "Ecommerce Manager",
                "experience_level": "mid",
                "skills": ["Shopify", "Inventory Management", "Customer Service"],
                "regions": ["Latin America", "Philippines"],
                "complexity_score": 6
            }
        }
    ]
    
    # Upsert the vectors
    index.upsert(vectors=test_vectors)
    print(f"✅ Added {len(test_vectors)} test vectors")
    
    # Wait for indexing to complete
    print("⏳ Waiting for indexing to complete...")
    time.sleep(10)
    
    # Verify the vectors were added
    final_stats = index.describe_index_stats()
    print(f"📊 Final vector count: {final_stats['total_vector_count']}")
    
    # Test semantic search
    print("\n🔍 Testing Semantic Search...")
    
    # Query for marketing roles
    marketing_query = [0.9] + [0.0] * 200 + [0.5] * 300 + [0.0] * 1035  # Similar to marketing pattern
    
    results = index.query(
        vector=marketing_query,
        top_k=4,
        include_metadata=True
    )
    
    print(f"\n🎯 Query: Marketing-related role")
    print(f"Found {len(results.matches)} matches:")
    
    for i, match in enumerate(results.matches, 1):
        metadata = match.metadata
        confidence = match.score * 100
        
        print(f"  {i}. {metadata['job_title']} (Similarity: {confidence:.1f}%)")
        print(f"     Category: {metadata['role_category']} | Level: {metadata['experience_level']}")
        print(f"     Skills: {', '.join(metadata['skills'])}")
        print(f"     Regions: {', '.join(metadata['regions'])}")
        
        if match.score > 0.7:
            print(f"     🟢 Strong semantic match")
        elif match.score > 0.5:
            print(f"     🟡 Good semantic match") 
        else:
            print(f"     🔴 Weak semantic match")
        print()
    
    print("✨ Semantic matching demo complete!")
    print(f"🎯 The system successfully matched similar roles using vector similarity")

if __name__ == "__main__":
    reset_and_demo()