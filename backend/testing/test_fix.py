"""
Simple test to verify the comprehensive testing system fix
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

from run_comprehensive_test import ComprehensiveTestRunner

async def test_final_report_generation():
    """Test just the final report generation without full test execution"""
    print("🧪 Testing Final Report Generation Fix")
    print("=" * 50)
    
    try:
        # Create test runner
        runner = ComprehensiveTestRunner()
        
        # Mock some basic data to test report generation
        runner.start_time = datetime.now(UTC)
        runner.test_cases = [
            {'test_id': 'test_1', 'role_data': {'core_role': 'Software Engineer'}, 'variation_type': 'core_role'},
            {'test_id': 'test_2', 'role_data': {'core_role': 'Data Scientist'}, 'variation_type': 'common_title'}
        ]
        runner.execution_results = [
            {'test_id': 'test_1', 'status': 'completed', 'execution_time': 45.2},
            {'test_id': 'test_2', 'status': 'completed', 'execution_time': 52.8}
        ]
        runner.analysis_results = [
            {'test_id': 'test_1', 'overall_score': 85, 'category_scores': {}, 'feedback': {}},
            {'test_id': 'test_2', 'overall_score': 78, 'category_scores': {}, 'feedback': {}}
        ]
        
        # Test final report generation
        print("🔄 Testing final report generation...")
        await runner._generate_final_report()
        
        # Check if report was generated successfully
        if runner.final_report and 'execution_summary' in runner.final_report:
            print("✅ Final report generated successfully!")
            print(f"📊 Report contains {len(runner.final_report)} sections")
            
            # Display key sections
            exec_summary = runner.final_report['execution_summary']
            print(f"\n📋 Execution Summary:")
            print(f"  • Tests Generated: {exec_summary['total_tests_generated']}")
            print(f"  • Tests Executed: {exec_summary['total_tests_executed']}")
            print(f"  • Success Rate: {exec_summary['execution_success_rate']:.1f}%")
            
            if 'recommendations' in runner.final_report:
                print(f"\n💡 Recommendations:")
                for rec in runner.final_report['recommendations'][:3]:
                    print(f"  • {rec}")
            
            if 'ai_analysis_summary' in runner.final_report and not runner.final_report['ai_analysis_summary'].get('error'):
                ai_summary = runner.final_report['ai_analysis_summary']
                if 'summary_statistics' in ai_summary:
                    stats = ai_summary['summary_statistics']
                    print(f"\n🤖 AI Analysis Summary:")
                    print(f"  • Average Score: {stats['overall_average_score']:.1f}/100")
                    print(f"  • Tests Analyzed: {stats['total_tests_analyzed']}")
            
            print("\n🎉 Final report generation is now working correctly!")
            return True
            
        else:
            print("❌ Final report generation failed")
            if runner.final_report and 'error' in runner.final_report:
                print(f"Error: {runner.final_report['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the test"""
    success = await test_final_report_generation()
    
    if success:
        print("\n✅ Comprehensive testing system fix is working!")
        print("You can now run the full test suite with: python3 testing/run_comprehensive_test.py")
    else:
        print("\n❌ Fix still has issues. Check the error logs above.")

if __name__ == "__main__":
    asyncio.run(main())