# Tidal Streamline Comprehensive Testing System

A comprehensive automated testing framework that evaluates the accuracy and integrity of the Tidal Streamline job market analysis application.

## Overview

This testing system cycles through all role categories in the database, generates realistic market scan requests, executes them via the API, and uses AI to analyze and score the results on a 0-100 scale.

## Components

### 1. Test Data Generator (`test_data_generator.py`)
- Fetches all role categories from the database
- Generates realistic job descriptions using role-specific templates
- Creates test cases with mix of core roles and common titles
- Uses consistent test user: Joey Muller, joey@sumdigital.com, www.sumdigital.com

### 2. Test Executor (`test_executor.py`)
- Submits market scan requests via API
- Waits for completion and collects results
- Exports full CSV data for each test
- Tracks performance metrics and errors

### 3. AI Results Analyzer (`results_analyzer.py`)
- Uses OpenAI GPT-4o to evaluate test results
- Scores based on 6 criteria (0-100 total):
  - **Salary Accuracy** (25 points)
  - **Skills Relevance** (25 points)
  - **Regional Recommendations** (15 points)
  - **Experience Level** (15 points)
  - **Data Completeness** (10 points)
  - **Logical Consistency** (10 points)

### 4. Test Orchestrator (`run_comprehensive_test.py`)
- Coordinates the entire testing process
- Generates comprehensive reports
- Provides recommendations for improvements

### 5. Configuration (`test_config.py`)
- Test parameters and settings
- Job description templates
- Scoring criteria definitions

## Quick Start

### Prerequisites
1. **API Server**: Ensure Tidal Streamline backend is running on `localhost:8008`
2. **OpenAI API Key**: Set `OPENAI_API_KEY` environment variable for AI analysis
3. **Python Packages**: `requests`, `openai`

### Run Tests

#### Option 1: Automated Setup and Run
```bash
cd /Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend/testing
python setup_and_run.py
```

#### Option 2: Manual Run
```bash
# Set OpenAI API key
export OPENAI_API_KEY=your_key_here

# Run comprehensive test suite
python run_comprehensive_test.py
```

#### Option 3: Individual Components
```bash
# Generate test cases only
python test_data_generator.py

# Execute tests only
python test_executor.py

# Analyze results only (requires existing results)
python results_analyzer.py
```

## Test Coverage

The system tests all role categories in the database:

1. **Brand Marketing Manager** (Marketing)
2. **Community Manager** (Marketing)
3. **Content Marketer** (Marketing)
4. **Retention Manager** (Marketing)
5. **Ecommerce Manager** (Operations)
6. **Sales Operations Manager** (Operations)
7. **Data Analyst** (Analytics)
8. **Logistics Manager** (Operations)
9. **Demand Planner** (Operations)
10. **Product Development Manager** (Product)
11. **Customer Experience Manager** (Customer Success)
12. **Admin & EA** (Administrative)

## Test Variations

- **Core Role Tests**: Use the primary role name (e.g., "Data Analyst")
- **Common Title Tests**: Use alternative titles (e.g., "Data Engineer", "Business Intelligence Analyst")
- **Realistic Job Descriptions**: Generated using category-specific templates
- **Consistent Challenge**: "It's hard to find someone good and cheap and reliable"

## Output Files

The system generates several output files with timestamps:

- `test_cases_{timestamp}.json` - Generated test cases
- `execution_results_{timestamp}.json` - Test execution results
- `ai_analysis_report_{timestamp}.json` - AI analysis and scoring
- `comprehensive_test_report_{timestamp}.json` - Final comprehensive report

## Scoring Criteria

### Salary Accuracy (25 points)
- Salary ranges are reasonable for the role and regions
- Regional cost differences make sense
- Currency and period information is correct

### Skills Relevance (25 points)
- Must-have skills match core role requirements
- Nice-to-have skills are relevant and appropriate
- Skill categories align with job description

### Regional Recommendations (15 points)
- Recommended regions are suitable for the role type
- Regional preferences align with common practices
- High-demand regions make business sense

### Experience Level (15 points)
- Experience level matches role complexity
- Years of experience required is reasonable
- Seniority assessment is appropriate

### Data Completeness (10 points)
- All expected fields are populated
- No missing critical information
- Data export contains full template variables

### Logical Consistency (10 points)
- No contradictory information across sections
- Salary ranges align with experience requirements
- Skills match complexity and experience level

## Sample Output

```
🏁 COMPREHENSIVE TEST RESULTS SUMMARY
============================================================

📊 Execution Results:
  • Tests Generated: 12
  • Tests Executed: 12
  • Successful: 11
  • Failed: 1
  • Success Rate: 91.7%

⚡ Performance Metrics:
  • Average Execution Time: 45.3s
  • Fastest Test: 28.1s
  • Slowest Test: 67.2s

🤖 AI Analysis Results:
  • Overall Average Score: 82.4/100
  • Highest Score: 95/100
  • Lowest Score: 67/100
  • Tests Above 80: 8
  • Tests Below 60: 0

💡 Recommendations:
  🎯 Focus on regional recommendations - scoring 11.2/15
  📈 Improve salary accuracy for junior roles
  ⚡ Optimize processing speed for complex roles
```

## Troubleshooting

### Common Issues

1. **API Server Not Running**
   ```bash
   cd /Users/joeymuller/Documents/coding-projects/active-projects/tidal-streamline/backend
   uvicorn main:app --reload --port 8008
   ```

2. **Missing OpenAI API Key**
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

3. **Missing Python Packages**
   ```bash
   pip install requests openai
   ```

4. **Permission Issues**
   ```bash
   chmod +x setup_and_run.py
   ```

### Environment Variables

- `OPENAI_API_KEY` - Required for AI analysis
- `API_BASE_URL` - Override default API URL (default: http://localhost:8008)

## Customization

### Adding New Test Criteria
1. Update `SCORING_CRITERIA` in `test_config.py`
2. Modify the analysis prompt in `results_analyzer.py`
3. Update scoring logic in AI analysis

### Custom Job Description Templates
1. Edit `JOB_DESCRIPTION_TEMPLATES` in `test_config.py`
2. Add category-specific templates
3. Include role-specific requirements

### Performance Tuning
1. Adjust `TEST_CONFIG` timeouts in `test_config.py`
2. Modify polling intervals for faster/slower systems
3. Change retry logic for unreliable environments

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Test Data      │    │  Test Executor  │    │  Results        │
│  Generator      │────▶│                 │────▶│  Analyzer       │
│                 │    │                 │    │  (AI-powered)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Test Cases     │    │  API Responses  │    │  Scored Results │
│  (JSON)         │    │  + CSV Exports  │    │  + Feedback     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Comprehensive  │
                       │  Report         │
                       └─────────────────┘
```

This testing system provides comprehensive validation of the Tidal Streamline application's accuracy and helps identify areas for improvement across all supported role categories.