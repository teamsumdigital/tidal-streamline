# 🎨 Canva Template Integration - Complete Data Audit

## 📊 Available Data Fields Summary

**Total Available Fields**: 50+ data points across 5 categories
**Export Page**: `/scan/{scanId}/export` - Ready for Canva integration
**API Endpoint**: `GET /api/v1/market-scans/{scanId}` - Full data structure

---

## 🏗️ Data Structure Breakdown

### 1. Basic Information (7 fields)
| Field Name | Description | Example Value |
|------------|-------------|---------------|
| `company_domain` | Client company domain | "yourcompany.com" |
| `job_title` | Position title being analyzed | "Shopify Store Manager" |
| `client_name` | Contact person name | "Sean Agatep" |
| `client_email` | Contact email | "sean@company.com" |
| `status` | Analysis completion status | "completed" |
| `created_at` | Analysis creation date | "March 15, 2025" |
| `confidence_score` | AI confidence in recommendations | "87%" |

### 2. Salary Data by Region (28+ fields)
**Format**: `{region_name}_field` (e.g., `united_states_low_salary`)

#### United States
- `united_states_region` → "United States"
- `united_states_currency` → "USD"
- `united_states_low_salary` → "$75,000"
- `united_states_mid_salary` → "$95,000"
- `united_states_high_salary` → "$120,000"
- `united_states_period` → "annual"
- `united_states_savings_vs_us` → "0%" (baseline)

#### Philippines  
- `philippines_region` → "Philippines"
- `philippines_currency` → "USD"
- `philippines_low_salary` → "$22,000"
- `philippines_mid_salary` → "$28,000"
- `philippines_high_salary` → "$35,000"
- `philippines_period` → "annual"
- `philippines_savings_vs_us` → "71%"

#### Latin America
- `latin_america_region` → "Latin America"
- `latin_america_currency` → "USD"
- `latin_america_low_salary` → "$40,000"
- `latin_america_mid_salary` → "$52,000"
- `latin_america_high_salary` → "$65,000"
- `latin_america_period` → "annual"
- `latin_america_savings_vs_us` → "45%"

#### South Africa
- `south_africa_region` → "South Africa"
- `south_africa_currency` → "USD"
- `south_africa_low_salary` → "$35,000"
- `south_africa_mid_salary` → "$45,000"
- `south_africa_high_salary` → "$58,000"
- `south_africa_period` → "annual"
- `south_africa_savings_vs_us` → "52%"

#### Salary Insights
- `recommended_pay_band` → "mid" (low/mid/high)
- `factors_considered` → "Role complexity, Experience level, Regional market"
- `high_demand_regions` → "United States, Philippines"
- `competitive_factors` → "Ecommerce expertise, Shopify experience"
- `cost_efficiency` → "Philippines offers best value for this role"

### 3. Skills & Requirements (8+ fields)
| Field Name | Description | Example Value |
|------------|-------------|---------------|
| `must_have_skills` | Essential required skills | "Shopify, Email Marketing, Analytics" |
| `nice_to_have_skills` | Preferred additional skills | "Klaviyo, Facebook Ads, Photoshop" |
| `certification_recommendations` | Relevant certifications | "Shopify Partner, Google Analytics" |
| `technical_skills` | Technical skill breakdown | "Shopify Admin, HTML/CSS, Excel" |
| `marketing_skills` | Marketing skill breakdown | "Email Marketing, Social Media, SEO" |
| `analytical_skills` | Analytics skill breakdown | "Google Analytics, Data Analysis, Reporting" |

### 4. Job Analysis (12+ fields)
| Field Name | Description | Example Value |
|------------|-------------|---------------|
| `complexity_score` | Role complexity rating (1-10) | "7" |
| `role_category` | Primary job category | "Ecommerce Manager" |
| `experience_level` | Required experience level | "mid" |
| `years_experience_required` | Years of experience required | "3-5 years" |
| `remote_work_suitability` | Remote work suitability | "High" |
| `key_responsibilities` | Main job responsibilities | "Manage store; Optimize conversions; Analyze performance" |
| `unique_challenges` | Unique challenges for this role | "Peak season management and inventory coordination" |
| `recommended_regions` | Best region recommendations | "Philippines, Latin America" |
| `salary_factors` | Factors affecting salary | "Shopify expertise, Analytics skills, Ecommerce experience" |

### 5. Metadata (3 fields)
| Field Name | Description | Example Value |
|------------|-------------|---------------|
| `processing_time` | Time taken to complete analysis | "45s" |
| `similar_scans_count` | Number of similar roles analyzed | "127" |
| `analysis_confidence` | Overall analysis confidence | "High" |

---

## 🎯 Canva Template Mapping Strategy

### Phase 1: Essential Fields (Start Here)
**Recommendation**: Focus on these 15 most impactful fields first

```
Company & Role:
- {{company_domain}}
- {{job_title}} 
- {{client_name}}

Salary Comparison (Top 3 Regions):
- {{united_states_mid_salary}}
- {{philippines_mid_salary}} + {{philippines_savings_vs_us}}
- {{latin_america_mid_salary}} + {{latin_america_savings_vs_us}}

Key Skills:
- {{must_have_skills}}
- {{nice_to_have_skills}}

Role Insights:
- {{complexity_score}}/10
- {{experience_level}}
- {{recommended_regions}}
```

### Phase 2: Advanced Fields
**For detailed templates with more data visualization**

```
Complete Salary Ranges:
- All regions with low/mid/high ranges
- Savings percentages
- Market insights

Detailed Skills:
- Skill categories (technical, marketing, analytical)
- Certification recommendations

Job Analysis:
- Key responsibilities breakdown
- Unique challenges
- Remote work suitability
```

---

## 🔧 Current Export Capabilities

### ✅ What Works Now
1. **Data Export Page**: `/scan/{scanId}/export`
   - Displays all 50+ fields in organized tables
   - Copy-to-clipboard functionality for each field
   - Categorized by Basic Info, Salary Data, Skills, Job Analysis, Metadata

2. **Field Naming Convention**: 
   - Clean, Canva-friendly variable names
   - No spaces or special characters
   - Descriptive and intuitive

3. **Data Formatting**:
   - Currency formatted with $ symbols
   - Percentages formatted with % symbols
   - Arrays converted to comma-separated strings
   - Proper capitalization

### 🔄 What Needs Enhancement
1. **CSV Export**: Not yet implemented
2. **Bulk Data Copy**: One-click copy all fields
3. **Template Variables**: Pre-formatted for Canva API
4. **Dynamic Region Selection**: Choose which regions to include

---

## 📋 Next Steps & Recommendations

### Option A: Quick Start (CSV Method) - **Recommended First**
1. **Add CSV Export Button** to existing export page
2. **Format data** for Canva's bulk import feature
3. **Test with your template** - No developer account needed initially
4. **Iterate on field selection** based on your template needs

### Option B: Full API Integration
1. **Canva Developer Setup**:
   - Register at [canva.com/developers](https://canva.com/developers)
   - Create new app
   - Get API credentials
   
2. **Template Preparation**:
   - Convert static text to dynamic variables
   - Map our field names to your template variables
   
3. **API Integration**:
   - Build `/api/v1/reports/canva-generate` endpoint
   - Connect to Canva API
   - Auto-generate reports

---

## 🎨 Template Analysis Questions

**To optimize integration, please share**:

1. **Template Structure**:
   - How many pages/sections?
   - What data points are you showing?
   - Screenshots would be incredibly helpful

2. **Priority Fields**:
   - Which of our 50+ fields are most important?
   - Any custom calculations needed?
   - Specific formatting requirements?

3. **Visual Elements**:
   - Charts/graphs that need data?
   - Regional comparison layouts?
   - Brand-specific styling needs?

4. **Output Requirements**:
   - Format (PDF, PNG, editable design)?
   - Distribution method (email, download, share link)?
   - Multiple versions per scan?

---

## 💡 Implementation Strategy

### Week 1: Template Audit & CSV
- Map your template fields to our data
- Add CSV export functionality  
- Test bulk import to Canva

### Week 2: API Integration Setup
- Canva developer account setup
- Template variable configuration
- Initial API integration

### Week 3: Full Automation
- Complete API integration
- Error handling & edge cases
- Production deployment

**Ready to see your template and start the mapping process!** 🚀