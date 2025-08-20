"""
Main test orchestrator - runs the complete testing system
"""

import asyncio
import json
import os
import sys
from datetime import datetime, UTC
from typing import Dict, Any, List

# Set your OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Ensure the key is available for the testing modules
if OPENAI_API_KEY:
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_data_generator import TestDataGenerator, generate_all_test_cases
from test_executor import TestExecutor
from results_analyzer import ResultsAnalyzer

class ComprehensiveTestRunner:
    def __init__(self):
        self.start_time = None
        self.test_cases = []
        self.execution_results = []
        self.analysis_results = []
        self.final_report = {}
        
    async def run_full_test_suite(self, save_intermediate_results: bool = True) -> Dict[str, Any]:
        """Run the complete test suite from start to finish"""
        print("🚀 Starting Comprehensive Tidal Streamline Testing System")
        print("=" * 60)
        
        self.start_time = datetime.now(UTC)
        
        try:
            # Phase 1: Generate Test Cases
            print("\n📝 PHASE 1: Generating Test Cases")
            print("-" * 40)
            await self._generate_test_cases()
            
            if save_intermediate_results:
                self._save_test_cases()
            
            # Phase 2: Execute Tests
            print("\n🔧 PHASE 2: Executing Market Scan Tests")
            print("-" * 40)
            await self._execute_tests()
            
            if save_intermediate_results:
                self._save_execution_results()
            
            # Phase 3: AI Analysis
            print("\n🤖 PHASE 3: AI-Powered Results Analysis")
            print("-" * 40)
            await self._analyze_results()
            
            # Phase 4: Generate Final Report
            print("\n📊 PHASE 4: Generating Final Report")
            print("-" * 40)
            await self._generate_final_report()
            
            # Save and display results
            if self.final_report:
                self._save_final_report()
                self._display_summary()
            else:
                print("❌ Failed to generate final report")
            
            return self.final_report
            
        except Exception as e:
            print(f"❌ Test suite failed: {e}")
            return {'error': str(e), 'partial_results': self.final_report}
    
    async def _generate_test_cases(self):
        """Generate test cases for all role categories"""
        generator = TestDataGenerator()
        await generator.fetch_role_categories()
        self.test_cases = generator.generate_test_cases()
        
        print(f"✅ Generated {len(self.test_cases)} test cases")
        
        # Show test case summary
        print("\\n📋 Test Cases Summary:")
        for case in self.test_cases:
            variation = case['variation_type']
            job_title = case['market_scan_request']['job_title']
            print(f"  • {case['test_id']}: {job_title} ({variation})")
    
    def _save_test_cases(self):
        """Save generated test cases"""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"test_cases_{timestamp}.json"
        filepath = f"/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend/testing/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.test_cases, f, indent=2)
        print(f"💾 Saved test cases to {filename}")
    
    async def _execute_tests(self):
        """Execute all test cases"""
        executor = TestExecutor()
        self.execution_results = await executor.execute_test_suite(self.test_cases)
        
        # Get execution summary
        summary = executor.get_execution_summary()
        print(f"\\n📊 Execution Summary:")
        print(f"  • Total tests: {summary['total_tests']}")
        print(f"  • Completed: {summary['completed_tests']}")
        print(f"  • Failed: {summary['failed_tests']}")
        print(f"  • Success rate: {summary['success_rate']:.1f}%")
        print(f"  • Average execution time: {summary['average_execution_time']:.2f}s")
        
        if summary['failed_tests'] > 0:
            print(f"\\n⚠️ Failed Tests:")
            for error in summary['error_summary']:
                print(f"  • {error['test_id']}: {error['error']}")
    
    def _save_execution_results(self):
        """Save test execution results"""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"execution_results_{timestamp}.json"
        filepath = f"/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend/testing/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.execution_results, f, indent=2)
        print(f"💾 Saved execution results to {filename}")
    
    async def _analyze_results(self):
        """Analyze results using AI"""
        # Check if we have OpenAI API key
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️ OPENAI_API_KEY not found. Skipping AI analysis.")
            print("   Set OPENAI_API_KEY environment variable to enable AI scoring.")
            self.analysis_results = []
            return
        
        analyzer = ResultsAnalyzer()
        self.analysis_results = await analyzer.analyze_test_results(self.execution_results)
        
        print(f"✅ Completed AI analysis of {len(self.analysis_results)} test results")
    
    async def _generate_final_report(self):
        """Generate comprehensive final report"""
        try:
            print("🔄 Generating final report...")
            end_time = datetime.now(UTC)
            total_duration = (end_time - self.start_time).total_seconds()
            
            # Basic execution statistics
            completed_tests = [r for r in self.execution_results if r['status'] == 'completed']
            failed_tests = [r for r in self.execution_results if r['status'] == 'failed']
            
            print(f"📊 Report data: {len(self.test_cases)} test cases, {len(self.execution_results)} results, {len(completed_tests)} completed")
            
            # Calculate all data components first
            execution_summary = {
                'total_tests_generated': len(self.test_cases),
                'total_tests_executed': len(self.execution_results),
                'successful_executions': len(completed_tests),
                'failed_executions': len(failed_tests),
                'execution_success_rate': len(completed_tests) / len(self.execution_results) * 100 if self.execution_results else 0
            }
            
            performance_metrics = self._calculate_performance_metrics()
            test_coverage = self._calculate_test_coverage()
            
            # Generate recommendations with calculated data
            recommendations = self._generate_recommendations(execution_summary, performance_metrics)
            
            # Generate AI analysis summary if available
            ai_analysis_summary = {}
            if self.analysis_results:
                print(f"🤖 Generating AI analysis summary for {len(self.analysis_results)} results")
                try:
                    analyzer = ResultsAnalyzer()
                    analyzer.analysis_results = self.analysis_results
                    ai_analysis_summary = analyzer.generate_summary_report(self.execution_results)
                    print("✅ AI analysis summary generated")
                except Exception as e:
                    print(f"⚠️ Failed to generate AI summary: {e}")
                    ai_analysis_summary = {'error': f'Failed to generate AI summary: {str(e)}'}
            
            # Build final report with all components
            self.final_report = {
                'test_run_info': {
                    'start_time': self.start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'total_duration_seconds': total_duration,
                    'test_framework_version': '1.0.0',
                    'environment': 'localhost:8008'
                },
                'execution_summary': execution_summary,
                'test_coverage': test_coverage,
                'performance_metrics': performance_metrics,
                'ai_analysis_summary': ai_analysis_summary,
                'recommendations': recommendations,
                'detailed_results': {
                    'test_cases': self.test_cases,
                    'execution_results': self.execution_results,
                    'analysis_results': self.analysis_results
                }
            }
            
            print("✅ Final report generated successfully")
            
        except Exception as e:
            print(f"❌ Error generating final report: {e}")
            import traceback
            traceback.print_exc()
            # Create minimal report on error
            self.final_report = {
                'error': str(e),
                'execution_summary': {
                    'total_tests_generated': len(self.test_cases) if hasattr(self, 'test_cases') else 0,
                    'total_tests_executed': len(self.execution_results) if hasattr(self, 'execution_results') else 0,
                    'successful_executions': 0,
                    'failed_executions': 0,
                    'execution_success_rate': 0
                }
            }
    
    def _calculate_test_coverage(self) -> Dict[str, Any]:
        """Calculate test coverage statistics"""
        role_categories = set()
        variation_types = {'core_role': 0, 'common_title': 0}
        
        for case in self.test_cases:
            role_categories.add(case['role_data']['core_role'])
            variation_types[case['variation_type']] += 1
        
        return {
            'unique_role_categories_tested': len(role_categories),
            'role_categories': list(role_categories),
            'variation_distribution': variation_types,
            'total_variations_tested': len(self.test_cases)
        }
    
    def _calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics"""
        completed_tests = [r for r in self.execution_results if r['status'] == 'completed']
        
        if not completed_tests:
            return {'message': 'No completed tests to analyze'}
        
        execution_times = [r['execution_time'] for r in completed_tests]
        
        return {
            'average_execution_time': sum(execution_times) / len(execution_times),
            'fastest_execution': min(execution_times),
            'slowest_execution': max(execution_times),
            'total_execution_time': sum(execution_times),
            'tests_under_60s': len([t for t in execution_times if t < 60]),
            'tests_over_120s': len([t for t in execution_times if t > 120])
        }
    
    def _generate_recommendations(self, execution_summary: Dict[str, Any], performance_metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check execution success rate
        success_rate = execution_summary.get('execution_success_rate', 0)
        if success_rate < 90:
            recommendations.append(f"🔧 Improve system reliability - only {success_rate:.1f}% of tests completed successfully")
        
        # Check performance
        if performance_metrics and 'average_execution_time' in performance_metrics:
            avg_time = performance_metrics['average_execution_time']
            if avg_time > 120:
                recommendations.append(f"⚡ Optimize processing speed - average test took {avg_time:.1f}s")
        
        # Basic AI analysis recommendations (detailed ones added later)
        if self.analysis_results:
            scores = [r.get('overall_score', 0) for r in self.analysis_results]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            if avg_score < 80:
                recommendations.append(f"📈 Improve overall accuracy - average AI score is {avg_score:.1f}/100")
        
        if not recommendations:
            recommendations.append("🎉 Excellent performance! All metrics look good.")
        
        return recommendations
    
    def _save_final_report(self):
        """Save the final comprehensive report"""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_test_report_{timestamp}.json"
        filepath = f"/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend/testing/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.final_report, f, indent=2)
        
        print(f"💾 Saved comprehensive report to {filename}")
        return filepath
    
    def _display_summary(self):
        """Display final summary to console"""
        print("\\n" + "=" * 60)
        print("🏁 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 60)
        
        # Check if final_report exists and has execution_summary
        if not self.final_report:
            print("❌ No final report generated")
            return
            
        if 'execution_summary' not in self.final_report:
            print("❌ Execution summary missing from final report")
            print(f"Available keys: {list(self.final_report.keys())}")
            return
        
        # Execution Summary
        exec_summary = self.final_report['execution_summary']
        print(f"\\n📊 Execution Results:")
        print(f"  • Tests Generated: {exec_summary['total_tests_generated']}")
        print(f"  • Tests Executed: {exec_summary['total_tests_executed']}")
        print(f"  • Successful: {exec_summary['successful_executions']}")
        print(f"  • Failed: {exec_summary['failed_executions']}")
        print(f"  • Success Rate: {exec_summary['execution_success_rate']:.1f}%")
        
        # Performance
        if 'performance_metrics' in self.final_report:
            perf = self.final_report['performance_metrics']
            print(f"\\n⚡ Performance Metrics:")
            print(f"  • Average Execution Time: {perf.get('average_execution_time', 0):.2f}s")
            print(f"  • Fastest Test: {perf.get('fastest_execution', 0):.2f}s")
            print(f"  • Slowest Test: {perf.get('slowest_execution', 0):.2f}s")
        
        # AI Analysis (if available)
        if 'ai_analysis_summary' in self.final_report and 'summary_statistics' in self.final_report['ai_analysis_summary']:
            ai_stats = self.final_report['ai_analysis_summary']['summary_statistics']
            print(f"\\n🤖 AI Analysis Results:")
            print(f"  • Overall Average Score: {ai_stats['overall_average_score']:.1f}/100")
            print(f"  • Highest Score: {ai_stats['highest_score']}/100")
            print(f"  • Lowest Score: {ai_stats['lowest_score']}/100")
            print(f"  • Tests Above 80: {ai_stats['tests_above_80']}")
            print(f"  • Tests Below 60: {ai_stats['tests_below_60']}")
        
        # Recommendations
        print(f"\\n💡 Recommendations:")
        for rec in self.final_report['recommendations']:
            print(f"  {rec}")
        
        # Test Coverage
        coverage = self.final_report['test_coverage']
        print(f"\\n🎯 Test Coverage:")
        print(f"  • Role Categories Tested: {coverage['unique_role_categories_tested']}")
        print(f"  • Core Role Tests: {coverage['variation_distribution']['core_role']}")
        print(f"  • Common Title Tests: {coverage['variation_distribution']['common_title']}")
        
        print("\\n" + "=" * 60)

async def main():
    """Main entry point"""
    # Check environment
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️ Warning: OPENAI_API_KEY not set. AI analysis will be skipped.")
        print("   To enable AI scoring, set: export OPENAI_API_KEY=your_key_here")
        print("")
    
    # Run comprehensive test
    runner = ComprehensiveTestRunner()
    report = await runner.run_full_test_suite()
    
    return report

if __name__ == "__main__":
    asyncio.run(main())