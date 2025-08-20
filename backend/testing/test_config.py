"""
Configuration settings for the automated testing system
"""

import os
from typing import Dict, List

# API Configuration
API_BASE_URL = "http://localhost:8008"
API_ENDPOINTS = {
    'MARKET_SCANS': '/api/v1/market-scans',
    'ANALYSIS': '/api/v1/analysis',
    'EXPORT': '/api/v1/market-scans'
}

# Test User Information
TEST_USER = {
    'client_name': 'Joey Muller',
    'client_email': 'joey@sumdigital.com',
    'company_domain': 'www.sumdigital.com'
}

# Standard Hiring Challenge
STANDARD_CHALLENGE = "It's hard to find someone good and cheap and reliable"

# Test Configuration
TEST_CONFIG = {
    'max_wait_time': 300,  # 5 minutes max wait per test
    'poll_interval': 5,    # Check status every 5 seconds
    'retry_attempts': 3,   # Retry failed requests 3 times
    'use_common_titles_probability': 0.4  # 40% chance to use common_title instead of core_role
}

# Job Description Templates by Category
JOB_DESCRIPTION_TEMPLATES = {
    'Marketing': """
We are looking for a {role_title} to join our growing e-commerce team. 

Key Responsibilities:
- {description}
- Develop and execute marketing campaigns across multiple channels
- Collaborate with cross-functional teams to drive brand awareness
- Analyze campaign performance and optimize for better ROI
- Manage marketing budgets and vendor relationships

Requirements:
- 3-5 years of experience in digital marketing
- Strong analytical and project management skills
- Experience with marketing automation tools
- Excellent communication and creative thinking abilities
- Ability to work independently in a remote environment

This is a full-time remote position with competitive compensation.
    """.strip(),
    
    'Operations': """
We are seeking an experienced {role_title} to streamline our operations.

Key Responsibilities:
- {description}
- Optimize operational processes and workflows
- Coordinate with multiple departments to ensure efficiency
- Implement and maintain operational systems and tools
- Monitor KPIs and create performance reports
- Lead process improvement initiatives

Requirements:
- 4-6 years of operations experience
- Strong analytical and problem-solving skills
- Experience with operational software and systems
- Excellent organizational and communication skills
- Ability to manage multiple projects simultaneously
- Remote work experience preferred

Join our team and help scale our operations efficiently.
    """.strip(),
    
    'Analytics': """
We need a detail-oriented {role_title} to drive data-driven decision making.

Key Responsibilities:
- {description}
- Collect, analyze, and interpret complex datasets
- Create dashboards and automated reporting systems
- Provide actionable insights to stakeholders
- Collaborate with teams to implement data solutions
- Ensure data quality and accuracy across systems

Requirements:
- 3-5 years of data analysis experience
- Proficiency in SQL, Excel, and analytics tools
- Experience with business intelligence platforms
- Strong statistical analysis and visualization skills
- Excellent communication of technical concepts
- Remote collaboration experience required

Help us turn data into strategic advantages.
    """.strip(),
    
    'Product': """
We are looking for a strategic {role_title} to lead our product initiatives.

Key Responsibilities:
- {description}
- Manage product roadmap and feature development
- Coordinate with engineering and design teams
- Conduct market research and competitive analysis
- Define product requirements and user stories
- Monitor product performance and user feedback

Requirements:
- 4-7 years of product management experience
- Strong project management and leadership skills
- Experience with product development methodologies
- Excellent analytical and strategic thinking abilities
- Strong communication and stakeholder management skills
- Experience working with remote teams

Drive innovation and product excellence with us.
    """.strip(),
    
    'Customer Success': """
We are seeking a customer-focused {role_title} to enhance our customer experience.

Key Responsibilities:
- {description}
- Develop and implement customer success strategies
- Monitor customer satisfaction and engagement metrics
- Handle customer inquiries and resolve issues promptly
- Create customer onboarding and retention programs
- Collaborate with sales and product teams on customer feedback

Requirements:
- 3-5 years of customer success or CX experience
- Strong interpersonal and communication skills
- Experience with CRM and customer success tools
- Analytical mindset with focus on metrics
- Problem-solving and conflict resolution abilities
- Comfortable with remote customer interactions

Help us deliver exceptional customer experiences.
    """.strip(),
    
    'Administrative': """
We need an organized {role_title} to support our executive team and operations.

Key Responsibilities:
- {description}
- Provide administrative and executive support
- Manage schedules, meetings, and travel arrangements
- Coordinate projects and cross-functional initiatives
- Maintain filing systems and documentation
- Handle communications and correspondence

Requirements:
- 3-5 years of administrative or EA experience
- Excellent organizational and time management skills
- Proficiency in office software and productivity tools
- Strong written and verbal communication abilities
- Discretion and ability to handle confidential information
- Experience supporting remote executives preferred

Join our team and keep our operations running smoothly.
    """.strip(),
    
    'Default': """
We are looking for a talented {role_title} to join our dynamic team.

Key Responsibilities:
- {description}
- Execute key projects and initiatives in your area of expertise
- Collaborate with cross-functional teams to achieve business goals
- Monitor performance metrics and optimize processes
- Provide insights and recommendations to leadership
- Support the growth and development of team capabilities

Requirements:
- 3-6 years of relevant professional experience
- Strong analytical and problem-solving skills
- Excellent communication and collaboration abilities
- Self-motivated with ability to work independently
- Experience in fast-paced, remote work environment
- Proficiency with relevant tools and technologies

This is an exciting opportunity to make a significant impact.
    """.strip()
}

# AI Scoring Criteria
SCORING_CRITERIA = {
    'salary_accuracy': {
        'weight': 25,
        'description': 'Salary ranges are reasonable for the role and regions'
    },
    'skills_relevance': {
        'weight': 25, 
        'description': 'Must-have and nice-to-have skills match role requirements'
    },
    'regional_recommendations': {
        'weight': 15,
        'description': 'Recommended regions are appropriate for the role'
    },
    'experience_level': {
        'weight': 15,
        'description': 'Experience level assessment matches role requirements'
    },
    'data_completeness': {
        'weight': 10,
        'description': 'All expected fields are populated with valid data'
    },
    'logical_consistency': {
        'weight': 10,
        'description': 'No contradictory information across different sections'
    }
}

# OpenAI Configuration
OPENAI_CONFIG = {
    'model': 'gpt-4o',
    'temperature': 0.3,  # Lower temperature for more consistent scoring
    'max_tokens': 1500,
    'system_prompt': '''You are an expert HR and compensation analyst evaluating the accuracy and quality of job market analysis results. You will score each analysis on a scale of 0-100 based on specific criteria and provide detailed feedback on strengths and areas for improvement.'''
}