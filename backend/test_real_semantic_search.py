#!/usr/bin/env python3
"""
Test semantic search with real data in Pinecone
"""

import asyncio
from app.services.embedding_service import embedding_service

async def test_semantic_search():
    """Test semantic search with real embeddings and data"""
    
    print("🎯 Testing Real Semantic Search with Pinecone")
    print("=" * 50)
    
    # Test job descriptions to search for
    test_queries = [
        "Looking for an E-commerce Marketing Manager to handle our Shopify store and run Facebook ads",
        "Need a Data Analyst to work with SQL and create reports from our customer data",
        "Hiring a Social Media Manager to manage our Instagram and TikTok accounts",
        "Seeking an Operations Manager to handle our customer service and logistics"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test Query #{i}:")
        print(f"📝 \"{query}\"")
        
        try:
            # Generate embedding for the query
            query_embedding = await embedding_service.generate_embedding(query)
            print(f"✅ Generated embedding ({len(query_embedding)} dimensions)")
            
            # Search for similar jobs
            results = await embedding_service.search_similar(
                query_vector=query_embedding,
                top_k=5,
                include_metadata=True
            )
            
            print(f"\n🎯 Found {len(results)} similar jobs:")
            
            for j, result in enumerate(results, 1):
                metadata = result.get('metadata', {})
                similarity_score = result.get('score', 0) * 100
                
                job_title = metadata.get('job_title', 'Unknown Job')
                role_category = metadata.get('role_category', 'Unknown Category')
                complexity = metadata.get('complexity_score', 0)
                
                # Determine similarity level
                if similarity_score >= 80:
                    level = "🟢 Excellent Match"
                elif similarity_score >= 60:
                    level = "🟡 Good Match"
                elif similarity_score >= 40:
                    level = "🟠 Fair Match"
                else:
                    level = "🔴 Weak Match"
                
                print(f"  {j}. {job_title}")
                print(f"     Category: {role_category} | Complexity: {complexity}/10")
                print(f"     Similarity: {similarity_score:.1f}% - {level}")
                
                # Show skills if available
                skills = metadata.get('must_have_skills', '[]')
                try:
                    import json
                    skills_list = json.loads(skills) if skills else []
                    if skills_list:
                        print(f"     Skills: {', '.join(skills_list[:4])}")
                except:
                    pass
                print()
        
        except Exception as e:
            print(f"❌ Error testing query: {str(e)}")
        
        print("-" * 50)
    
    # Test index statistics
    try:
        stats = await embedding_service.get_index_stats()
        print(f"\n📊 Pinecone Index Statistics:")
        print(f"   Total Vectors: {stats.get('total_vector_count', 0)}")
        print(f"   Dimension: {stats.get('dimension', 0)}")
        print(f"   Index Fullness: {stats.get('index_fullness', 0) * 100:.2f}%")
        
    except Exception as e:
        print(f"❌ Error getting stats: {str(e)}")
    
    print("\n✨ Semantic Search Test Complete!")
    print("The system can now find similar jobs based on semantic meaning,")
    print("not just keyword matching. This will greatly improve the quality")
    print("of salary recommendations and skills suggestions!")

if __name__ == "__main__":
    asyncio.run(test_semantic_search())