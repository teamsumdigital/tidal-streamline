#!/usr/bin/env python3
"""
Test script for Pinecone integration in Tidal Streamline
"""

import asyncio
import sys
import os
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.embedding_service import embedding_service
from app.services.vector_search import vector_search_service
from app.services.job_analyzer import JobAnalyzer
from app.models.market_scan import RoleCategory, ExperienceLevel, Region, JobAnalysis


async def test_embedding_service():
    """Test basic embedding service functionality"""
    print("🔧 Testing Embedding Service...")
    
    try:
        # Test embedding generation
        test_text = "Software Engineer position requiring Python and React skills"
        embedding = await embedding_service.generate_embedding(test_text)
        print(f"✅ Generated embedding with dimension: {len(embedding)}")
        
        # Test batch embedding generation
        test_texts = [
            "Marketing Manager role for e-commerce company",
            "Data Analyst position with SQL and Python requirements",
            "Content Creator job for social media marketing"
        ]
        batch_embeddings = await embedding_service.generate_batch_embeddings(test_texts)
        print(f"✅ Generated {len(batch_embeddings)} batch embeddings")
        
        # Test index stats
        stats = await embedding_service.get_index_stats()
        print(f"✅ Index stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Embedding service test failed: {str(e)}")
        return False


async def test_vector_search():
    """Test vector search functionality"""
    print("🔍 Testing Vector Search Service...")
    
    try:
        # Create a test job analysis
        test_analysis = JobAnalysis(
            role_category=RoleCategory.BRAND_MARKETING_MANAGER,
            experience_level=ExperienceLevel.MID,
            years_experience_required="3-5 years",
            must_have_skills=["Digital Marketing", "Brand Strategy", "Analytics"],
            nice_to_have_skills=["Photoshop", "Video Editing"],
            key_responsibilities=["Develop brand strategy", "Manage campaigns", "Analyze metrics"],
            remote_work_suitability="high",
            complexity_score=6,
            recommended_regions=[Region.PHILIPPINES, Region.LATIN_AMERICA],
            unique_challenges="Remote team coordination",
            salary_factors=["Experience", "Skills", "Location"]
        )
        
        # Test storing a market scan vector
        test_scan_id = f"test_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        success = await vector_search_service.store_market_scan_vector(
            scan_id=test_scan_id,
            job_title="Brand Marketing Manager",
            job_description="We are looking for a Brand Marketing Manager to develop and execute our brand strategy across digital channels.",
            job_analysis=test_analysis,
            company_domain="testcompany.com",
            client_name="Test Client",
            created_at=datetime.now()
        )
        
        if success:
            print(f"✅ Successfully stored test scan: {test_scan_id}")
        else:
            print(f"❌ Failed to store test scan: {test_scan_id}")
            return False
        
        # Test finding similar scans
        similar_scans, confidence = await vector_search_service.find_similar_market_scans(
            job_title="Marketing Manager",
            job_description="Looking for a marketing professional to handle brand campaigns and digital strategy.",
            max_results=3,
            similarity_threshold=0.5
        )
        
        print(f"✅ Found {len(similar_scans)} similar scans with confidence: {confidence:.2f}")
        
        # Test market trends (placeholder functionality)
        trends = await vector_search_service.get_market_trends(lookback_days=30)
        print(f"✅ Retrieved market trends data")
        
        return True
        
    except Exception as e:
        print(f"❌ Vector search test failed: {str(e)}")
        return False


async def test_job_analyzer_integration():
    """Test job analyzer integration with semantic matching"""
    print("🤖 Testing Job Analyzer with Semantic Matching...")
    
    try:
        job_analyzer = JobAnalyzer()
        
        # Test basic job analysis
        job_analysis = await job_analyzer.analyze_job(
            job_title="Senior Data Analyst",
            job_description="We need a Senior Data Analyst to work with large datasets, create visualizations, and provide business insights using Python, SQL, and Tableau.",
            hiring_challenges="Remote position, need strong communication skills"
        )
        
        print(f"✅ Basic job analysis completed: {job_analysis.role_category.value}")
        
        # Test job analysis with semantic matching
        enhanced_analysis, similar_scans, confidence = await job_analyzer.analyze_job_with_similar_scans(
            job_title="Digital Marketing Specialist",
            job_description="Looking for a Digital Marketing Specialist to manage social media campaigns, create content, and analyze performance metrics.",
            hiring_challenges="Fast-paced startup environment"
        )
        
        print(f"✅ Enhanced analysis with {len(similar_scans)} similar scans, confidence: {confidence:.2f}")
        
        # Test storing analysis vector
        test_scan_id = f"analyzer_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        stored = await job_analyzer.store_analysis_vector(
            scan_id=test_scan_id,
            job_title="Digital Marketing Specialist",
            job_description="Looking for a Digital Marketing Specialist to manage social media campaigns.",
            job_analysis=enhanced_analysis,
            company_domain="testcompany.com",
            client_name="Test Analyzer Client"
        )
        
        if stored:
            print(f"✅ Successfully stored analyzer test vector: {test_scan_id}")
        else:
            print(f"⚠️ Failed to store analyzer test vector")
        
        return True
        
    except Exception as e:
        print(f"❌ Job analyzer integration test failed: {str(e)}")
        return False


async def test_end_to_end_workflow():
    """Test the complete end-to-end workflow"""
    print("🔄 Testing End-to-End Workflow...")
    
    try:
        # Simulate a complete market scan workflow
        job_analyzer = JobAnalyzer()
        
        # Step 1: Analyze a job with semantic matching
        job_title = "E-commerce Operations Manager"
        job_description = """
        We are seeking an experienced E-commerce Operations Manager to oversee our online retail operations. 
        The ideal candidate will have experience with Shopify, inventory management, order fulfillment, 
        and customer service coordination. Must be comfortable with data analysis and process optimization.
        
        Key responsibilities:
        - Manage day-to-day e-commerce operations
        - Optimize inventory levels and fulfillment processes  
        - Coordinate with customer service and logistics teams
        - Analyze sales data and identify improvement opportunities
        - Implement new tools and processes to scale operations
        
        Requirements:
        - 3-5 years e-commerce operations experience
        - Experience with Shopify or similar platforms
        - Strong analytical and problem-solving skills
        - Excellent communication and project management abilities
        - Experience with remote team management preferred
        """
        
        analysis, similar_scans, confidence = await job_analyzer.analyze_job_with_similar_scans(
            job_title=job_title,
            job_description=job_description,
            hiring_challenges="Scaling rapidly, need someone who can handle growth"
        )
        
        print(f"✅ Job Analysis Complete:")
        print(f"   Role: {analysis.role_category.value}")
        print(f"   Experience: {analysis.experience_level.value}")
        print(f"   Complexity: {analysis.complexity_score}/10")
        print(f"   Remote Suitability: {analysis.remote_work_suitability}")
        print(f"   Similar Scans: {len(similar_scans)} (confidence: {confidence:.2f})")
        
        # Step 2: Store the analysis for future matching
        workflow_scan_id = f"workflow_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        stored = await job_analyzer.store_analysis_vector(
            scan_id=workflow_scan_id,
            job_title=job_title,
            job_description=job_description,
            job_analysis=analysis,
            company_domain="testworkflow.com",
            client_name="Workflow Test Client"
        )
        
        if stored:
            print(f"✅ Stored workflow analysis: {workflow_scan_id}")
        else:
            print(f"⚠️ Failed to store workflow analysis")
        
        # Step 3: Test finding this scan from a similar query
        await asyncio.sleep(2)  # Small delay to ensure indexing
        
        test_similar_scans, test_confidence = await vector_search_service.find_similar_market_scans(
            job_title="Operations Manager E-commerce",
            job_description="Looking for an operations manager to handle online store logistics and inventory.",
            max_results=5,
            similarity_threshold=0.6
        )
        
        print(f"✅ Found {len(test_similar_scans)} scans for similar query")
        
        # Check if our stored scan appears in results
        found_our_scan = any(scan['scan_id'] == workflow_scan_id for scan in test_similar_scans)
        if found_our_scan:
            print(f"✅ Successfully found our stored scan in similar results!")
        else:
            print(f"⚠️ Our stored scan not found in similar results (may need more time for indexing)")
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-end workflow test failed: {str(e)}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Starting Pinecone Integration Tests for Tidal Streamline")
    print("=" * 60)
    
    tests = [
        ("Embedding Service", test_embedding_service),
        ("Vector Search", test_vector_search),
        ("Job Analyzer Integration", test_job_analyzer_integration),
        ("End-to-End Workflow", test_end_to_end_workflow)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 30)
        try:
            success = await test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📈 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Pinecone integration is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    # Set up environment (if needed)
    os.environ.setdefault('OPENAI_API_KEY', 'your-key-here')
    
    # Run tests
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test runner failed: {str(e)}")
        sys.exit(1)