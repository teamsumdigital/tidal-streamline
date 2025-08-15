#!/usr/bin/env python3
"""
Demo of Tidal Streamline Semantic Matching with Mock Data
"""

import asyncio
import json
from pinecone import Pinecone

# Mock embedding function (in real system this would call OpenAI)
def mock_embedding(text: str) -> list:
    """Generate a mock embedding based on text content"""
    # This is a simplified mock - real system uses OpenAI embeddings
    words = text.lower().split()
    base_embedding = [0.0] * 1536
    
    # Simple keyword-based mock embedding
    keyword_weights = {
        "marketing": ([100, 200, 300], 0.8),
        "manager": ([150, 250, 350], 0.7),
        "ecommerce": ([400, 500, 600], 0.9),
        "shopify": ([700, 800, 900], 0.6),
        "facebook": ([1000, 1100, 1200], 0.5),
        "ads": ([1300, 1400, 1500], 0.5),
        "social": ([50, 150, 250], 0.4),
        "content": ([350, 450, 550], 0.4),
    }
    
    for word in words:
        if word in keyword_weights:
            positions, weight = keyword_weights[word]
            for pos in positions:
                if pos < 1536:
                    base_embedding[pos] = weight
    
    # Add some randomness based on text length
    text_factor = min(len(text) / 1000.0, 1.0)
    for i in range(0, min(50, 1536), 5):
        base_embedding[i] += text_factor * 0.3
    
    return base_embedding

async def demo_semantic_matching():
    """Demonstrate semantic matching with mock job descriptions"""
    print("🎯 Tidal Streamline - Semantic Matching Demo")
    print("=" * 50)
    
    # Initialize Pinecone
    api_key = "pcsk_2asZaU_4JFVKA6KRDqh2i37Vn8bcWRx5cPhhGDhYcDmcemg3GGpG2m44TPouFMVkEzQqBe"
    index_name = "tidal-streamline"
    
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    
    # Sample historical job descriptions
    historical_jobs = [
        {
            "id": "job-001",
            "title": "E-commerce Marketing Manager",
            "description": "We need an experienced marketing manager to handle our Shopify store, manage Facebook ads, and coordinate with our creative team. Must have 3+ years of e-commerce experience.",
            "role_category": "Brand Marketing Manager",
            "experience_level": "mid",
            "complexity_score": 7,
            "skills": ["Shopify", "Facebook Ads", "Email Marketing", "Analytics"],
            "regions": ["Philippines", "Latin America"]
        },
        {
            "id": "job-002", 
            "title": "Digital Marketing Specialist",
            "description": "Looking for a digital marketing specialist to manage social media campaigns, create content, and analyze performance metrics. Experience with Google Ads preferred.",
            "role_category": "Brand Marketing Manager",
            "experience_level": "junior",
            "complexity_score": 5,
            "skills": ["Social Media", "Content Creation", "Google Ads", "Analytics"],
            "regions": ["Philippines"]
        },
        {
            "id": "job-003",
            "title": "Online Store Manager", 
            "description": "Seeking an online store manager to oversee our e-commerce operations, manage product listings, and optimize conversion rates. Shopify experience required.",
            "role_category": "Ecommerce Manager",
            "experience_level": "mid",
            "complexity_score": 6,
            "skills": ["Shopify", "Product Management", "Conversion Optimization", "Inventory Management"],
            "regions": ["Latin America", "Philippines"]
        },
        {
            "id": "job-004",
            "title": "Data Analyst",
            "description": "We're looking for a data analyst to help us make sense of our customer data, create reports, and identify growth opportunities. SQL and Excel skills required.",
            "role_category": "Data Analyst", 
            "experience_level": "mid",
            "complexity_score": 8,
            "skills": ["SQL", "Excel", "Data Visualization", "Python"],
            "regions": ["Philippines", "Latin America"]
        }
    ]
    
    # Add historical jobs to vector index
    print("📤 Adding historical job descriptions to vector index...")
    vectors_to_upsert = []
    
    for job in historical_jobs:
        text_for_embedding = f"{job['title']} {job['description']}"
        embedding = mock_embedding(text_for_embedding)
        
        vectors_to_upsert.append({
            "id": job["id"],
            "values": embedding,
            "metadata": {
                "job_title": job["title"],
                "role_category": job["role_category"],
                "experience_level": job["experience_level"],
                "complexity_score": job["complexity_score"],
                "skills": job["skills"],
                "regions": job["regions"],
                "description_preview": job["description"][:200] + "..."
            }
        })
    
    # Upsert vectors
    index.upsert(vectors=vectors_to_upsert)
    print(f"✅ Added {len(vectors_to_upsert)} historical jobs to index")
    
    # Wait a moment for indexing
    await asyncio.sleep(2)
    
    # Test semantic matching with new job descriptions
    test_jobs = [
        {
            "title": "Marketing Manager for Online Store",
            "description": "We need someone to handle marketing for our e-commerce business. You'll manage our Shopify store, run Facebook advertising campaigns, and work with our design team on creative assets."
        },
        {
            "title": "Social Media Marketing Specialist", 
            "description": "Looking for a social media expert to create engaging content, manage our Instagram and Facebook pages, and run targeted advertising campaigns."
        },
        {
            "title": "Business Intelligence Analyst",
            "description": "Seeking a data-driven professional to analyze our sales data, create dashboards, and provide insights to help grow our business. Need strong Excel and SQL skills."
        }
    ]
    
    print("\n🔍 Testing Semantic Matching...")
    print("=" * 50)
    
    for i, test_job in enumerate(test_jobs, 1):
        print(f"\n🆕 Test Job #{i}: {test_job['title']}")
        print(f"📄 Description: {test_job['description'][:100]}...")
        
        # Generate embedding for test job
        test_text = f"{test_job['title']} {test_job['description']}"
        test_embedding = mock_embedding(test_text)
        
        # Search for similar jobs
        results = index.query(
            vector=test_embedding,
            top_k=3,
            include_metadata=True,
            filter={}  # No filtering for demo
        )
        
        print(f"\n🎯 Top {len(results.matches)} Similar Jobs Found:")
        
        for j, match in enumerate(results.matches, 1):
            similarity_score = match.score
            metadata = match.metadata
            
            # Convert similarity score to confidence percentage
            confidence = min(similarity_score * 100, 99)
            
            print(f"  {j}. {metadata.get('job_title')} (Confidence: {confidence:.1f}%)")
            print(f"     Role: {metadata.get('role_category')} | Level: {metadata.get('experience_level')}")
            print(f"     Skills: {', '.join(metadata.get('skills', [])[:4])}")
            print(f"     Regions: {', '.join(metadata.get('regions', []))}")
            
            if similarity_score > 0.7:
                print(f"     🟢 High similarity - Strong match for analysis enhancement")
            elif similarity_score > 0.5:
                print(f"     🟡 Medium similarity - Good for insights")
            else:
                print(f"     🔴 Low similarity - Basic match")
            print()
    
    # Show index statistics
    stats = index.describe_index_stats()
    print(f"\n📊 Index Statistics:")
    print(f"   Total Vectors: {stats['total_vector_count']}")
    print(f"   Dimension: {stats['dimension']}")
    print(f"   Metric: {stats['metric']}")
    
    print("\n✨ Semantic Matching Demo Complete!")
    print("\nIn the full system:")
    print("• Job descriptions are converted to 1536-dimensional OpenAI embeddings")
    print("• Similar jobs are found using cosine similarity in vector space") 
    print("• Analysis is enhanced using insights from semantically similar roles")
    print("• Confidence scores guide recommendation quality")

if __name__ == "__main__":
    asyncio.run(demo_semantic_matching())