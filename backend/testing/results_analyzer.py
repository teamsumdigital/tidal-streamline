"""
AI-powered results analyzer for scoring test results
"""

import json
import openai
from typing import Dict, List, Any, Optional
from datetime import datetime, UTC
from test_config import SCORING_CRITERIA, OPENAI_CONFIG
import os

class ResultsAnalyzer:
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.scoring_criteria = SCORING_CRITERIA
        self.analysis_results = []
        
    async def analyze_test_results(self, test_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze all test results using AI"""
        print(f"🤖 Starting AI analysis of {len(test_results)} test results")
        
        completed_tests = [r for r in test_results if r['status'] == 'completed']
        print(f"📊 Analyzing {len(completed_tests)} completed tests")
        
        for i, test_result in enumerate(completed_tests, 1):
            print(f"\n🔍 Analyzing test {i}/{len(completed_tests)}: {test_result['test_id']}")
            
            analysis = await self._analyze_single_result(test_result)
            self.analysis_results.append(analysis)
        
        print(f"\n✅ Completed analysis of {len(self.analysis_results)} tests")
        return self.analysis_results
    
    async def _analyze_single_result(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single test result using AI"""
        analysis = {
            'test_id': test_result['test_id'],
            'scan_id': test_result['scan_id'],
            'overall_score': 0,
            'category_scores': {},
            'feedback': {},
            'strengths': [],
            'improvements': [],
            'data_quality_issues': [],
            'analysis_timestamp': datetime.now(UTC).isoformat()
        }
        
        try:
            # Prepare data for AI analysis
            analysis_prompt = self._create_analysis_prompt(test_result)
            
            # Get AI analysis
            ai_response = await self._get_ai_analysis(analysis_prompt)
            
            # Parse AI response
            parsed_analysis = self._parse_ai_response(ai_response)
            analysis.update(parsed_analysis)
            
            print(f"  📋 Overall Score: {analysis['overall_score']}/100")
            
        except Exception as e:
            print(f"  ❌ Analysis failed: {e}")
            analysis['error'] = str(e)
            analysis['overall_score'] = 0
        
        return analysis
    
    def _create_analysis_prompt(self, test_result: Dict[str, Any]) -> str:
        """Create a detailed prompt for AI analysis"""
        test_case = test_result['test_case']
        scan_data = test_result['scan_data']
        
        # Extract key data points
        job_title = test_case['market_scan_request']['job_title']
        role_category = test_case['role_data']['core_role']
        role_description = test_case['role_data']['description']
        job_description = test_case['market_scan_request']['job_description']
        
        # Format scan results
        salary_data = scan_data.get('salary_recommendations', {})
        skills_data = scan_data.get('skills_recommendations', {})
        job_analysis = scan_data.get('job_analysis', {})
        
        prompt = f"""
Please analyze the following job market scan results and provide a detailed score from 0-100 based on the criteria below.

TEST CASE INFORMATION:
- Job Title: {job_title}
- Role Category: {role_category}  
- Role Description: {role_description}
- Test Variation: {test_case.get('variation_type', 'unknown')}

JOB DESCRIPTION PROVIDED:
{job_description}

SCAN RESULTS TO EVALUATE:

1. SALARY RECOMMENDATIONS:
{json.dumps(salary_data, indent=2)}

2. SKILLS RECOMMENDATIONS:
{json.dumps(skills_data, indent=2)}

3. JOB ANALYSIS:
{json.dumps(job_analysis, indent=2)}

SCORING CRITERIA (Total: 100 points):
1. Salary Accuracy (25 points): Are the salary ranges reasonable for this role and regions?
2. Skills Relevance (25 points): Do the must-have and nice-to-have skills match the role requirements?
3. Regional Recommendations (15 points): Are the recommended regions appropriate for this type of role?
4. Experience Level (15 points): Does the experience level assessment match the role requirements?
5. Data Completeness (10 points): Are all expected fields populated with valid data?
6. Logical Consistency (10 points): Is there any contradictory information across sections?

Please provide your analysis in the following JSON format:
{{
  "overall_score": <0-100>,
  "category_scores": {{
    "salary_accuracy": <0-25>,
    "skills_relevance": <0-25>, 
    "regional_recommendations": <0-15>,
    "experience_level": <0-15>,
    "data_completeness": <0-10>,
    "logical_consistency": <0-10>
  }},
  "feedback": {{
    "salary_accuracy": "<detailed feedback>",
    "skills_relevance": "<detailed feedback>",
    "regional_recommendations": "<detailed feedback>",
    "experience_level": "<detailed feedback>",
    "data_completeness": "<detailed feedback>",
    "logical_consistency": "<detailed feedback>"
  }},
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "improvements": ["<improvement 1>", "<improvement 2>", ...],
  "data_quality_issues": ["<issue 1>", "<issue 2>", ...]
}}

Provide specific, actionable feedback and be thorough in your analysis.
        """.strip()
        
        return prompt
    
    async def _get_ai_analysis(self, prompt: str) -> str:
        """Get analysis from OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_CONFIG['model'],
                messages=[
                    {"role": "system", "content": OPENAI_CONFIG['system_prompt']},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_CONFIG['temperature'],
                max_tokens=OPENAI_CONFIG['max_tokens']
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
    
    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse the AI response JSON"""
        try:
            # Extract JSON from response (handle cases where AI adds extra text)
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise Exception("No JSON found in AI response")
            
            json_str = ai_response[start_idx:end_idx]
            parsed = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['overall_score', 'category_scores', 'feedback', 'strengths', 'improvements']
            for field in required_fields:
                if field not in parsed:
                    parsed[field] = {} if field in ['category_scores', 'feedback'] else []
            
            return parsed
            
        except Exception as e:
            print(f"    ⚠️ Failed to parse AI response: {e}")
            return {
                'overall_score': 0,
                'category_scores': {},
                'feedback': {},
                'strengths': [],
                'improvements': ['Failed to parse AI analysis'],
                'data_quality_issues': ['AI analysis parsing error']
            }
    
    def generate_summary_report(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive summary report"""
        if not self.analysis_results:
            return {'error': 'No analysis results available'}
        
        # Calculate overall statistics
        scores = [r['overall_score'] for r in self.analysis_results if 'overall_score' in r]
        
        if not scores:
            return {'error': 'No valid scores found'}
        
        # Aggregate category scores
        category_stats = {}
        for category in SCORING_CRITERIA.keys():
            category_scores = []
            for result in self.analysis_results:
                if category in result.get('category_scores', {}):
                    category_scores.append(result['category_scores'][category])
            
            if category_scores:
                category_stats[category] = {
                    'average': sum(category_scores) / len(category_scores),
                    'min': min(category_scores),
                    'max': max(category_scores),
                    'total_possible': SCORING_CRITERIA[category]['weight']
                }
        
        # Find common issues and strengths
        all_improvements = []
        all_strengths = []
        for result in self.analysis_results:
            all_improvements.extend(result.get('improvements', []))
            all_strengths.extend(result.get('strengths', []))
        
        # Count frequency of issues/strengths
        improvement_counts = {}
        strength_counts = {}
        
        for item in all_improvements:
            improvement_counts[item] = improvement_counts.get(item, 0) + 1
        
        for item in all_strengths:
            strength_counts[item] = strength_counts.get(item, 0) + 1
        
        # Role category performance
        role_performance = {}
        for result in self.analysis_results:
            # Find corresponding test result to get role info
            test_result = next((tr for tr in test_results if tr['test_id'] == result['test_id']), None)
            if test_result:
                role_category = test_result['test_case']['role_data']['core_role']
                if role_category not in role_performance:
                    role_performance[role_category] = []
                role_performance[role_category].append(result['overall_score'])
        
        # Average by role
        for role in role_performance:
            scores_list = role_performance[role]
            role_performance[role] = {
                'average_score': sum(scores_list) / len(scores_list),
                'test_count': len(scores_list),
                'scores': scores_list
            }
        
        return {
            'summary_statistics': {
                'total_tests_analyzed': len(self.analysis_results),
                'overall_average_score': sum(scores) / len(scores),
                'highest_score': max(scores),
                'lowest_score': min(scores),
                'tests_above_80': len([s for s in scores if s >= 80]),
                'tests_below_60': len([s for s in scores if s < 60])
            },
            'category_performance': category_stats,
            'role_category_performance': role_performance,
            'common_improvements_needed': sorted(improvement_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            'common_strengths': sorted(strength_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            'detailed_results': self.analysis_results,
            'report_timestamp': datetime.now(UTC).isoformat()
        }
    
    def save_analysis_results(self, summary_report: Dict[str, Any], filename: str = None) -> str:
        """Save analysis results and summary report"""
        if not filename:
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            filename = f"ai_analysis_report_{timestamp}.json"
        
        try:
            filepath = f"/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend/testing/{filename}"
            
            with open(filepath, 'w') as f:
                json.dump(summary_report, f, indent=2)
            
            print(f"💾 Saved analysis report to {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Failed to save analysis results: {e}")
            return ""

if __name__ == "__main__":
    # Test the analyzer (requires test results)
    print("🤖 AI Results Analyzer")
    print("This module requires test execution results to analyze.")
    print("Run the full test suite with run_comprehensive_test.py")