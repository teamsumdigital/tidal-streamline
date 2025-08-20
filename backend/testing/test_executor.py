"""
Test executor for running market scan tests and collecting results
"""

import asyncio
import time
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, UTC
from test_config import API_BASE_URL, API_ENDPOINTS, TEST_CONFIG

class TestExecutor:
    def __init__(self):
        self.api_base = API_BASE_URL
        self.results = []
        self.execution_log = []
        
    async def execute_test_suite(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute all test cases and collect results"""
        print(f"🚀 Starting execution of {len(test_cases)} test cases")
        start_time = datetime.now(UTC)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Executing test {i}/{len(test_cases)}: {test_case['test_id']}")
            
            test_result = await self._execute_single_test(test_case)
            self.results.append(test_result)
            
            # Add small delay between tests to avoid overwhelming the API
            await asyncio.sleep(2)
        
        end_time = datetime.now(UTC)
        execution_duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Completed {len(test_cases)} tests in {execution_duration:.2f} seconds")
        return self.results
    
    async def _execute_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single test case"""
        test_start = time.time()
        test_result = {
            'test_id': test_case['test_id'],
            'test_case': test_case,
            'status': 'pending',
            'scan_id': None,
            'scan_data': None,
            'csv_export': None,
            'execution_time': 0,
            'error_message': None,
            'timestamps': {
                'start': datetime.now(UTC).isoformat(),
                'submitted': None,
                'completed': None,
                'exported': None
            }
        }
        
        try:
            # Step 1: Submit market scan request
            scan_id = await self._submit_market_scan(test_case['market_scan_request'])
            if not scan_id:
                raise Exception("Failed to submit market scan")
            
            test_result['scan_id'] = scan_id
            test_result['timestamps']['submitted'] = datetime.now(UTC).isoformat()
            print(f"  📤 Submitted scan: {scan_id}")
            
            # Step 2: Wait for completion
            scan_data = await self._wait_for_completion(scan_id)
            if not scan_data:
                raise Exception("Scan did not complete successfully")
            
            test_result['scan_data'] = scan_data
            test_result['timestamps']['completed'] = datetime.now(UTC).isoformat()
            print(f"  ✅ Scan completed: {scan_data.get('status', 'unknown')}")
            
            # Step 3: Export CSV data
            csv_data = await self._export_csv_data(scan_id)
            test_result['csv_export'] = csv_data
            test_result['timestamps']['exported'] = datetime.now(UTC).isoformat()
            print(f"  💾 Exported CSV data: {len(csv_data.split(',')) if csv_data else 0} columns")
            
            test_result['status'] = 'completed'
            
        except Exception as e:
            test_result['status'] = 'failed'
            test_result['error_message'] = str(e)
            print(f"  ❌ Test failed: {e}")
        
        test_result['execution_time'] = time.time() - test_start
        return test_result
    
    async def _submit_market_scan(self, request_data: Dict[str, Any]) -> Optional[str]:
        """Submit a market scan request"""
        try:
            url = f"{self.api_base}{API_ENDPOINTS['MARKET_SCANS']}/analyze"
            
            response = requests.post(
                url,
                json=request_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('id')
            
        except Exception as e:
            print(f"    ❌ Submit failed: {e}")
            return None
    
    async def _wait_for_completion(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Wait for market scan to complete"""
        max_wait = TEST_CONFIG['max_wait_time']
        poll_interval = TEST_CONFIG['poll_interval']
        elapsed = 0
        
        while elapsed < max_wait:
            try:
                url = f"{self.api_base}{API_ENDPOINTS['MARKET_SCANS']}/{scan_id}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                status = data.get('status', 'unknown')
                
                if status == 'completed':
                    return data
                elif status == 'failed':
                    raise Exception(f"Scan failed with status: {status}")
                
                # Still processing, wait and check again
                await asyncio.sleep(poll_interval)
                elapsed += poll_interval
                
                if elapsed % 30 == 0:  # Progress update every 30 seconds
                    print(f"    ⏳ Still processing... ({elapsed}s elapsed)")
                
            except Exception as e:
                print(f"    ⚠️ Error checking status: {e}")
                await asyncio.sleep(poll_interval)
                elapsed += poll_interval
        
        raise Exception(f"Scan timed out after {max_wait} seconds")
    
    async def _export_csv_data(self, scan_id: str) -> Optional[str]:
        """Export CSV data for the completed scan"""
        try:
            url = f"{self.api_base}{API_ENDPOINTS['EXPORT']}/{scan_id}/export?format=template"
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            return response.text
            
        except Exception as e:
            print(f"    ❌ CSV export failed: {e}")
            return None
    
    def save_results(self, filename: str = None) -> str:
        """Save test execution results"""
        if not filename:
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            filename = f"test_execution_results_{timestamp}.json"
        
        try:
            filepath = f"/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend/testing/{filename}"
            
            # Prepare summary data
            summary = {
                'execution_summary': {
                    'total_tests': len(self.results),
                    'completed_tests': len([r for r in self.results if r['status'] == 'completed']),
                    'failed_tests': len([r for r in self.results if r['status'] == 'failed']),
                    'average_execution_time': sum(r['execution_time'] for r in self.results) / len(self.results) if self.results else 0,
                    'timestamp': datetime.now(UTC).isoformat()
                },
                'test_results': self.results
            }
            
            with open(filepath, 'w') as f:
                json.dump(summary, f, indent=2)
            
            print(f"💾 Saved execution results to {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            return ""
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of test execution"""
        if not self.results:
            return {'message': 'No test results available'}
        
        completed = [r for r in self.results if r['status'] == 'completed']
        failed = [r for r in self.results if r['status'] == 'failed']
        
        return {
            'total_tests': len(self.results),
            'completed_tests': len(completed),
            'failed_tests': len(failed),
            'success_rate': len(completed) / len(self.results) * 100,
            'average_execution_time': sum(r['execution_time'] for r in self.results) / len(self.results),
            'completed_scan_ids': [r['scan_id'] for r in completed],
            'failed_test_ids': [r['test_id'] for r in failed],
            'error_summary': [{'test_id': r['test_id'], 'error': r['error_message']} for r in failed]
        }

if __name__ == "__main__":
    # Test the executor with sample data
    async def main():
        from test_data_generator import generate_all_test_cases
        
        # Generate test cases
        test_cases = generate_all_test_cases()
        if not test_cases:
            print("❌ No test cases generated")
            return
        
        # Execute tests (limit to first 3 for testing)
        executor = TestExecutor()
        results = await executor.execute_test_suite(test_cases[:3])
        
        # Save results and show summary
        executor.save_results()
        summary = executor.get_execution_summary()
        
        print(f"\n📊 Execution Summary:")
        print(f"  - Total tests: {summary['total_tests']}")
        print(f"  - Completed: {summary['completed_tests']}")
        print(f"  - Failed: {summary['failed_tests']}")
        print(f"  - Success rate: {summary['success_rate']:.1f}%")
        print(f"  - Average time: {summary['average_execution_time']:.2f}s")
    
    asyncio.run(main())