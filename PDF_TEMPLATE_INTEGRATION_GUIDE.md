# 📄 PDF Template Integration Guide - Tidal Market Scan

## 🎯 Overview

This guide details the integration of your "Market Scan - Masterfile.pdf" template with the Tidal Streamline data export system. The system already generates 50+ structured data fields that can be mapped to your template variables.

---

## 📋 Template Analysis Checklist

### Step 1: Template Structure Analysis
**Please help identify the following from your PDF template:**

#### **Page Layout**
- [ ] How many pages does the template have?
- [ ] What are the main sections on each page?
- [ ] Are there charts, graphs, or data visualization elements?

#### **Data Fields Required**
- [ ] Company/Client information fields
- [ ] Job title and role description areas
- [ ] Salary comparison sections
- [ ] Regional salary breakdowns
- [ ] Skills and requirements lists
- [ ] Charts or graphs that need data
- [ ] Summary/insights sections

#### **Variable Naming Convention**
- [ ] How are variables currently named in the template?
- [ ] Are they using Canva's {{variable_name}} format?
- [ ] Any specific formatting requirements (currency, percentages, etc.)?

---

## 🔄 Available Data Mapping

### Current Tidal Export Fields → Template Variables

#### **Company & Role Information**
```
Available Data:
- company_domain → {{company_name}}
- job_title → {{position_title}}
- created_at → {{scan_date}}
- confidence_score → {{analysis_confidence}}
- status → {{scan_status}}
```

#### **Salary Data (All Regions)**
```
United States:
- united_states_mid_salary → {{us_salary}}
- united_states_low_salary → {{us_salary_min}}
- united_states_high_salary → {{us_salary_max}}

Philippines:
- philippines_mid_salary → {{ph_salary}}
- philippines_savings_vs_us → {{ph_savings_percent}}

Latin America:
- latin_america_mid_salary → {{latam_salary}}
- latin_america_savings_vs_us → {{latam_savings_percent}}

South Africa:
- south_africa_mid_salary → {{sa_salary}}
- south_africa_savings_vs_us → {{sa_savings_percent}}
```

#### **Skills & Requirements**
```
Available Data:
- must_have_skills → {{required_skills}}
- nice_to_have_skills → {{preferred_skills}}
- certification_recommendations → {{certifications}}
- technical_skills → {{tech_skills}}
- marketing_skills → {{marketing_skills}}
- analytical_skills → {{analytics_skills}}
```

#### **Job Analysis**
```
Available Data:
- complexity_score → {{role_complexity}}
- experience_level → {{seniority_level}}
- years_experience_required → {{experience_years}}
- remote_work_suitability → {{remote_suitability}}
- recommended_regions → {{best_regions}}
- key_responsibilities → {{main_duties}}
- unique_challenges → {{role_challenges}}
```

---

## 🛠️ Implementation Options

### Option 1: Enhanced CSV Export (Recommended First Step)
**Quick to implement, works with Canva bulk import**

1. **Template-Specific CSV Format**
   - Create CSV with your exact variable names as headers
   - Format data to match your template requirements
   - Include only fields your template actually uses

2. **Benefits**:
   - No Canva developer account needed initially
   - Works with existing Canva bulk create feature
   - Easy to test and iterate

### Option 2: Canva API Integration (Full Automation)
**Complete automation for high-volume use**

1. **Direct API Integration**
   - Connect to Canva API
   - Auto-generate completed templates
   - Return shareable links or PDFs

2. **Benefits**:
   - Fully automated workflow
   - Professional presentation
   - Scalable for multiple clients

### Option 3: JSON Export for Custom Integration
**Flexible data format for any automation needs**

1. **Structured JSON Output**
   - All data in clean JSON format
   - Easy to integrate with any system
   - Supports custom post-processing

---

## 📊 Template Field Mapping Worksheet

**Please fill in the following to complete the mapping:**

### Template Variable Names
```
Company Information:
Your template uses: [ ? ]
Maps to: company_domain

Job Title:
Your template uses: [ ? ]
Maps to: job_title

Main Salary (US):
Your template uses: [ ? ]
Maps to: united_states_mid_salary

Philippines Salary:
Your template uses: [ ? ]
Maps to: philippines_mid_salary

Savings Percentage:
Your template uses: [ ? ]
Maps to: philippines_savings_vs_us

Required Skills:
Your template uses: [ ? ]
Maps to: must_have_skills

Role Complexity:
Your template uses: [ ? ]
Maps to: complexity_score
```

### Charts & Visualizations
```
Salary Comparison Chart:
- Needs: [ List required data points ]
- Format: [ Bar chart / Table / Other ]

Regional Breakdown:
- Regions shown: [ US, PH, LATAM, SA, Other? ]
- Data points: [ Salary ranges, savings %, Other ]

Skills Assessment:
- Format: [ List / Chart / Rating system ]
- Categories: [ Technical, Marketing, Analytics, Other ]
```

---

## 🚀 Next Steps

### Immediate Actions
1. **Share Template Details**:
   - Screenshot key pages from your PDF
   - List the main variable names used
   - Describe any charts or special formatting

2. **Test Current Export**:
   - Create a test market scan in Tidal Streamline
   - Visit the `/scan/{scanId}/export` page
   - Download the CSV and review available fields

3. **Map Template Variables**:
   - Match your template's variable names to our export fields
   - Identify any missing data points your template needs
   - Note any special formatting requirements

### Implementation Plan
**Week 1**: Template analysis and field mapping
**Week 2**: Enhanced export functionality development
**Week 3**: Canva integration testing and deployment

---

## 🔧 Technical Implementation

### Enhanced CSV Export Structure
```csv
Template_Variable,Value,Description
company_name,acme-corp.com,Client company domain
position_title,Shopify Store Manager,Role being analyzed
us_salary,$95000,United States average salary
ph_salary,$28000,Philippines average salary
ph_savings,71%,Cost savings vs US rates
required_skills,"Shopify, Email Marketing, Analytics",Essential skills
role_complexity,7,Complexity score (1-10)
```

### Canva API Integration Endpoint
```
POST /api/v1/reports/canva-generate
{
  "scan_id": "uuid",
  "template_id": "your_canva_template_id",
  "output_format": "pdf|png|editable"
}
```

---

## 📞 Support & Questions

**Ready to help with:**
- Template variable mapping
- Custom export formats
- Canva API integration
- Data formatting requirements
- Chart and visualization data
- Template optimization

**Please provide:**
1. Screenshots or descriptions of your template layout
2. List of variable names currently used
3. Any specific formatting or calculation requirements
4. Preferred integration method (CSV, API, or JSON)

Let's get your template integrated and generating beautiful market scan reports! 🎨