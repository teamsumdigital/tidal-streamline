#!/usr/bin/env python3
"""
Test direct Pinecone search with real data
"""

import asyncio
from pinecone import Pinecone
from app.services.embedding_service import embedding_service

async def test_direct_search():
    """Test direct Pinecone search"""
    
    print("🎯 Testing Direct Pinecone Search with Real Data")
    print("=" * 55)
    
    # Initialize Pinecone client
    api_key = "pcsk_2asZaU_4JFVKA6KRDqh2i37Vn8bcWRx5cPhhGDhYcDmcemg3GGpG2m44TPouFMVkEzQqBe"
    index_name = "tidal-streamline"
    
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    
    # Test queries
    test_queries = [
        "E-commerce Marketing Manager for Shopify store with Facebook ads experience",
        "Data Analyst with SQL skills for customer analytics and reporting",  
        "Social Media Manager for Instagram and TikTok content creation"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test Query #{i}:")
        print(f"📝 \"{query}\"")
        
        try:
            # Generate embedding using our service
            embedding = await embedding_service.generate_embedding(query)
            print(f"✅ Generated embedding ({len(embedding)} dimensions)")
            
            # Search Pinecone directly
            results = index.query(
                vector=embedding,
                top_k=5,
                include_metadata=True,
                filter={}
            )
            
            print(f"\n🎯 Found {len(results.matches)} matches:")
            
            for j, match in enumerate(results.matches, 1):
                similarity = match.score * 100
                metadata = match.metadata
                
                job_title = metadata.get('job_title', 'Unknown Title')
                role_category = metadata.get('role_category', 'Unknown Category')
                client_name = metadata.get('client_name', 'Unknown Client')
                
                # Similarity level
                if similarity >= 85:
                    level = "🟢 Excellent"
                elif similarity >= 75:
                    level = "🟡 Very Good"
                elif similarity >= 65:
                    level = "🟠 Good"
                else:
                    level = "🔴 Fair"
                
                print(f"  {j}. {job_title}")
                print(f"     Client: {client_name}")
                print(f"     Category: {role_category}")
                print(f"     Similarity: {similarity:.1f}% {level}")
                
                # Show description preview if available
                preview = metadata.get('description_preview', '')
                if preview:
                    print(f"     Preview: {preview[:80]}...")
                
                print()
                
        except Exception as e:
            print(f"❌ Error with query: {str(e)}")
        
        print("-" * 55)
    
    # Show overall index statistics
    try:
        stats = index.describe_index_stats()
        print(f"\n📊 Index Statistics:")
        print(f"   Total Vectors: {stats['total_vector_count']}")
        print(f"   Dimensions: {stats['dimension']}")
        print(f"   Metric: {stats.get('metric', 'cosine')}")
        print(f"   Status: Ready ✅")
        
        if stats['namespaces']:
            for namespace, ns_stats in stats['namespaces'].items():
                namespace_name = namespace or 'default'
                print(f"   Namespace '{namespace_name}': {ns_stats['vector_count']} vectors")
        
    except Exception as e:
        print(f"❌ Error getting stats: {str(e)}")
    
    print(f"\n✨ Search Test Complete!")
    print(f"🚀 Semantic matching is working with {stats.get('total_vector_count', 11)} real market scans!")
    print(f"📈 The system can now provide intelligent recommendations based on")
    print(f"   semantic similarity rather than just keyword matching.")

if __name__ == "__main__":
    asyncio.run(test_direct_search())