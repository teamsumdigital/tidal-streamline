"""
Quick test runner - runs a subset of tests for demonstration
"""

import asyncio
import os
import sys
from datetime import datetime, UTC

# Set OpenAI API key from environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_data_generator import generate_all_test_cases
from test_executor import TestExecutor
from results_analyzer import ResultsAnalyzer

async def run_quick_test(num_tests: int = 3):
    """Run a quick test with a subset of role categories"""
    print(f"🚀 Running Quick Test ({num_tests} test cases)")
    print("=" * 50)
    
    start_time = datetime.now(UTC)
    
    try:
        # Generate test cases
        print("\\n📝 Generating test cases...")
        all_test_cases = generate_all_test_cases()
        
        if not all_test_cases:
            print("❌ No test cases generated")
            return
        
        # Take subset for quick test
        test_cases = all_test_cases[:num_tests]
        print(f"✅ Selected {len(test_cases)} test cases for quick test:")
        
        for i, case in enumerate(test_cases, 1):
            job_title = case['market_scan_request']['job_title']
            variation = case['variation_type']
            print(f"  {i}. {job_title} ({variation})")
        
        # Execute tests
        print("\\n🔧 Executing tests...")
        executor = TestExecutor()
        results = await executor.execute_test_suite(test_cases)
        
        # Show execution summary
        summary = executor.get_execution_summary()
        print(f"\\n📊 Execution Summary:")
        print(f"  • Completed: {summary['completed_tests']}/{summary['total_tests']}")
        print(f"  • Success Rate: {summary['success_rate']:.1f}%")
        print(f"  • Average Time: {summary['average_execution_time']:.2f}s")
        
        if summary['failed_tests'] > 0:
            print(f"\\n⚠️ Failed tests:")
            for error in summary['error_summary']:
                print(f"  • {error['test_id']}: {error['error']}")
        
        # AI Analysis (if OpenAI key available)
        if os.getenv('OPENAI_API_KEY') and summary['completed_tests'] > 0:
            print("\\n🤖 Running AI analysis...")
            
            analyzer = ResultsAnalyzer()
            analysis_results = await analyzer.analyze_test_results(results)
            
            if analysis_results:
                scores = [r.get('overall_score', 0) for r in analysis_results]
                avg_score = sum(scores) / len(scores)
                
                print(f"\\n🎯 AI Analysis Results:")
                print(f"  • Average Score: {avg_score:.1f}/100")
                print(f"  • Highest Score: {max(scores)}/100")
                print(f"  • Lowest Score: {min(scores)}/100")
                
                # Show individual scores
                print(f"\\n📋 Individual Test Scores:")
                for result in analysis_results:
                    test_id = result['test_id']
                    score = result.get('overall_score', 0)
                    print(f"  • {test_id}: {score}/100")
                    
                    # Show top improvements if available
                    improvements = result.get('improvements', [])
                    if improvements:
                        print(f"    Top improvement: {improvements[0]}")
        else:
            if not os.getenv('OPENAI_API_KEY'):
                print("\\n⚠️ Skipping AI analysis - OPENAI_API_KEY not set")
            else:
                print("\\n⚠️ Skipping AI analysis - no completed tests")
        
        # Summary
        end_time = datetime.now(UTC)
        total_duration = (end_time - start_time).total_seconds()
        
        print(f"\\n✅ Quick test completed in {total_duration:.2f} seconds")
        
        if summary['completed_tests'] == len(test_cases):
            print("🎉 All tests passed! The system is working correctly.")
        else:
            print("⚠️ Some tests failed. Check the logs above for details.")
        
        return results
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return None

def main():
    """Main entry point for quick test"""
    print("🧪 Tidal Streamline Quick Test")
    print("This runs a subset of tests to verify the system is working")
    print("")
    
    # Check if API is running
    try:
        import requests
        response = requests.get("http://localhost:8008/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server is not responding correctly")
            print("   Make sure the backend is running: uvicorn main:app --reload --port 8008")
            return
        print("✅ API server is running")
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        print("   Make sure the backend is running: uvicorn main:app --reload --port 8008")
        return
    
    # Ask for number of tests
    while True:
        try:
            num_tests = input("\\nHow many tests to run? (1-12, default 3): ").strip()
            if not num_tests:
                num_tests = 3
            else:
                num_tests = int(num_tests)
            
            if 1 <= num_tests <= 12:
                break
            else:
                print("Please enter a number between 1 and 12")
        except ValueError:
            print("Please enter a valid number")
    
    # Check for OpenAI key
    if not os.getenv('OPENAI_API_KEY'):
        key = input("\\nEnter OpenAI API key for AI scoring (or press Enter to skip): ").strip()
        if key:
            os.environ['OPENAI_API_KEY'] = key
    
    # Run the test
    print(f"\\n🚀 Starting quick test with {num_tests} test cases...")
    asyncio.run(run_quick_test(num_tests))

if __name__ == "__main__":
    main()