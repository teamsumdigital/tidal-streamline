"""
Test data generator for comprehensive app testing
"""

import random
import requests
import json
from typing import Dict, List, Any
from test_config import API_BASE_URL, API_ENDPOINTS, TEST_USER, STANDARD_CHALLENGE, JOB_DESCRIPTION_TEMPLATES, TEST_CONFIG

class TestDataGenerator:
    def __init__(self):
        self.api_base = API_BASE_URL
        self.role_categories = []
        
    async def fetch_role_categories(self) -> List[Dict[str, Any]]:
        """Fetch all role categories from the API"""
        try:
            url = f"{self.api_base}{API_ENDPOINTS['ANALYSIS']}/role-categories"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            self.role_categories = data.get('categories', [])
            print(f"✅ Fetched {len(self.role_categories)} role categories")
            return self.role_categories
        except Exception as e:
            print(f"❌ Failed to fetch role categories: {e}")
            return []
    
    def generate_test_cases(self) -> List[Dict[str, Any]]:
        """Generate test cases for all role categories"""
        if not self.role_categories:
            print("❌ No role categories available. Run fetch_role_categories() first.")
            return []
        
        test_cases = []
        
        for i, role in enumerate(self.role_categories):
            # Decide whether to use core_role or common_title
            use_common_title = random.random() < TEST_CONFIG['use_common_titles_probability']
            
            if use_common_title and role.get('common_titles'):
                job_title = random.choice(role['common_titles'])
                variation_type = "common_title"
            else:
                job_title = role['core_role']
                variation_type = "core_role"
            
            # Generate job description using appropriate template
            job_description = self._generate_job_description(
                role_title=job_title,
                role_category=role.get('category', 'Default'),
                role_description=role.get('description', '')
            )
            
            # Create test case
            test_case = {
                'test_id': f"test_{i+1:02d}_{role['core_role'].lower().replace(' ', '_')}",
                'role_data': role,
                'variation_type': variation_type,
                'market_scan_request': {
                    'client_name': TEST_USER['client_name'],
                    'client_email': TEST_USER['client_email'], 
                    'company_domain': TEST_USER['company_domain'],
                    'job_title': job_title,
                    'job_description': job_description,
                    'hiring_challenges': STANDARD_CHALLENGE
                },
                'expected_outcomes': self._generate_expected_outcomes(role)
            }
            
            test_cases.append(test_case)
            print(f"📝 Generated test case: {test_case['test_id']} ({variation_type})")
        
        print(f"✅ Generated {len(test_cases)} test cases")
        return test_cases
    
    def _generate_job_description(self, role_title: str, role_category: str, role_description: str) -> str:
        """Generate a realistic job description based on role information"""
        template = JOB_DESCRIPTION_TEMPLATES.get(role_category, JOB_DESCRIPTION_TEMPLATES['Default'])
        
        return template.format(
            role_title=role_title,
            description=role_description
        )
    
    def _generate_expected_outcomes(self, role: Dict[str, Any]) -> Dict[str, Any]:
        """Generate expected outcomes for validation"""
        return {
            'role_category': role['core_role'],
            'category_type': role.get('category', 'Unknown'),
            'should_have_salary_data': True,
            'should_have_skills_data': True,
            'should_have_regional_data': True,
            'expected_regions': ['Philippines', 'Latin America', 'South Africa'],  # Common regions
            'expected_experience_levels': ['junior', 'mid', 'senior'],
            'min_confidence_score': 0.7  # Expect at least 70% confidence
        }
    
    def save_test_cases(self, test_cases: List[Dict[str, Any]], filename: str = 'generated_test_cases.json') -> str:
        """Save generated test cases to file"""
        try:
            filepath = f"/Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend/testing/{filename}"
            with open(filepath, 'w') as f:
                json.dump(test_cases, f, indent=2)
            print(f"💾 Saved {len(test_cases)} test cases to {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Failed to save test cases: {e}")
            return ""

# Standalone function for easy import
def generate_all_test_cases() -> List[Dict[str, Any]]:
    """Generate test cases for all roles - can be imported by other modules"""
    generator = TestDataGenerator()
    
    # Fetch role categories synchronously
    try:
        url = f"{API_BASE_URL}{API_ENDPOINTS['ANALYSIS']}/role-categories"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        generator.role_categories = data.get('categories', [])
    except Exception as e:
        print(f"❌ Failed to fetch role categories: {e}")
        return []
    
    return generator.generate_test_cases()

if __name__ == "__main__":
    # Test the generator
    import asyncio
    
    async def main():
        generator = TestDataGenerator()
        await generator.fetch_role_categories()
        test_cases = generator.generate_test_cases()
        generator.save_test_cases(test_cases)
        
        print(f"\n📊 Test Case Summary:")
        for case in test_cases:
            print(f"  - {case['test_id']}: {case['market_scan_request']['job_title']} ({case['variation_type']})")
    
    asyncio.run(main())