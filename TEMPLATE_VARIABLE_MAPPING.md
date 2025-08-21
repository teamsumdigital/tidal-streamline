# 🎨 Template Variable Mapping - Market Scan PDF Integration

## 📋 Complete Variable Reference

**Template CSV Export**: Available at `/scan/{scanId}/export` → **📄 Template CSV** button

### 🏢 Company & Role Information
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `company_name` | Client company domain | "acme-corp.com" |
| `position_title` | Role being analyzed | "Shopify Store Manager" |
| `scan_date` | When analysis was performed | "March 15, 2025" |
| `analysis_confidence` | AI confidence percentage | "87%" |

### 💰 Salary Data - All Regions

#### United States (Baseline)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `us_salary` | Average US salary | "$95,000" |
| `us_salary_min` | Minimum US range | "$75,000" |
| `us_salary_max` | Maximum US range | "$120,000" |

#### Philippines (High Savings)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `ph_salary` | Average Philippines salary | "$28,000" |
| `ph_salary_min` | Minimum Philippines range | "$22,000" |
| `ph_salary_max` | Maximum Philippines range | "$35,000" |
| `ph_savings_percent` | Cost savings vs US | "71%" |

#### Latin America
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `latam_salary` | Average Latin America salary | "$52,000" |
| `latam_salary_min` | Minimum LATAM range | "$40,000" |
| `latam_salary_max` | Maximum LATAM range | "$65,000" |
| `latam_savings_percent` | Cost savings vs US | "45%" |

#### South Africa
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `sa_salary` | Average South Africa salary | "$45,000" |
| `sa_salary_min` | Minimum SA range | "$35,000" |
| `sa_salary_max` | Maximum SA range | "$58,000" |
| `sa_savings_percent` | Cost savings vs US | "52%" |

### 🛠️ Skills & Requirements
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `required_skills` | Must-have skills | "Shopify, Email Marketing, Analytics" |
| `preferred_skills` | Nice-to-have skills | "Klaviyo, Facebook Ads, Photoshop" |
| `certifications` | Recommended certifications | "Shopify Partner, Google Analytics" |
| `tech_skills` | Technical skills breakdown | "Shopify Admin, HTML/CSS, Excel" |
| `marketing_skills` | Marketing skills breakdown | "Email Marketing, Social Media, SEO" |
| `analytics_skills` | Analytics skills breakdown | "Google Analytics, Data Analysis, Reporting" |

### 📊 Job Analysis
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `role_complexity` | Complexity score (1-10) | "7" |
| `seniority_level` | Experience level required | "mid" |
| `experience_years` | Years of experience needed | "3-5 years" |
| `remote_suitability` | Remote work compatibility | "High" |
| `best_regions` | Recommended hiring regions | "Philippines, Latin America" |
| `main_duties` | Key responsibilities | "Manage store; Optimize conversions; Analyze performance" |
| `role_challenges` | Unique role challenges | "Peak season management and inventory coordination" |

### 💡 Market Insights
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `high_demand_regions` | Regions with high demand | "United States, Philippines" |
| `competitive_factors` | What makes candidates competitive | "Ecommerce expertise, Shopify experience" |
| `cost_efficiency` | Best value analysis | "Philippines offers best value for this role" |
| `salary_factors` | What affects salary ranges | "Shopify expertise, Analytics skills, Ecommerce experience" |

### 🆕 New Variables Needed for Template

#### Similar Roles Data (Slide 2)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `similar_role_1` | Most similar role title | "E-commerce Analyst" |
| `similar_role_1_percent` | Similarity percentage | "45" |
| `similar_role_2` | Second similar role | "Marketing Data Analyst" |
| `similar_role_2_percent` | Similarity percentage | "25" |
| `similar_role_3` | Third similar role | "Business Intelligence Analyst" |
| `similar_role_3_percent` | Similarity percentage | "20" |

#### Experience Level Breakdowns (Slide 5)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `junior_salary_min` | 0-2 years minimum | "$1,200" |
| `junior_salary_max` | 0-2 years maximum | "$1,800" |
| `mid_salary_min` | 3-6 years minimum | "$1,800" |
| `mid_salary_max` | 3-6 years maximum | "$2,300" |
| `senior_salary_min` | 6-8 years minimum | "$2,300" |
| `senior_salary_max` | 6-8 years maximum | "$2,800" |
| `expert_salary_min` | 9+ years minimum | "$2,800" |
| `expert_salary_max` | 9+ years maximum | "$3,500" |

#### Europe Region Data (Slide 4)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `europe_salary_min` | Minimum Europe salary | "$3,200" |
| `europe_salary_max` | Maximum Europe salary | "$4,800" |
| `europe_savings_percent` | Cost savings vs US | "32%" |

#### Regional Recommendations (Slide 4)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `asia_recommendation` | Asia hiring insight | "High skill availability, excellent English proficiency" |
| `latam_recommendation` | Latin America insight | "Strong technical skills, overlapping US timezone" |
| `africa_recommendation` | Africa hiring insight | "Growing tech talent pool, cost-effective rates" |
| `europe_recommendation` | Europe hiring insight | "Premium talent, higher costs but excellent quality" |

#### Additional Variables
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `client_logo_url` | Client logo URL | "https://client.com/logo.png" |
| `recommended_salary_min` | Final recommended minimum | "$1,800" |
| `recommended_salary_max` | Final recommended maximum | "$2,300" |

#### Candidate Profile 1 (Philippines) - Slides 6
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `candidate_1_name` | Candidate first name | "Ana" |
| `candidate_1_photo_url` | Profile photo URL | "https://example.com/ana.jpg" |
| `candidate_1_bio` | Brief candidate description | "A dynamic Content Marketer based in the Philippines with 6+ years of experience..." |
| `candidate_1_responsibilities` | Key responsibilities bullets | "• Develop and implement content strategies\n• Create written and visual content\n• Analyze performance to refine content" |
| `candidate_1_region` | Candidate region | "Philippines" |
| `candidate_1_salary_range` | Monthly salary range | "$1,500-$2,000" |
| `candidate_1_onboarded_date` | When candidate joined | "2/4/2025" |
| `candidate_1_experience_1` | First experience line | "6+ Yrs Freelance" |
| `candidate_1_experience_2` | Second experience line | "6+ Yrs Content Marketing" |
| `candidate_1_experience_3` | Third experience line | "10+ Yrs Adobe Suite" |
| `candidate_1_tech_stack` | Technical skills | "Meta Ads Manager\nShopify\nLanding Page Creation\nInfluencer Marketing" |

#### Candidate Profile 2 (Latin America) - Slides 7
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `candidate_2_name` | Candidate first name | "Natália" |
| `candidate_2_photo_url` | Profile photo URL | "https://example.com/natalia.jpg" |
| `candidate_2_bio` | Brief candidate description | "Has 8+ years of experience creating multifaceted content for brands..." |
| `candidate_2_responsibilities` | Key responsibilities bullets | "• Create visual content that aligns with brand guidelines\n• Design assets for various mediums\n• Collaborate with teams" |
| `candidate_2_region` | Candidate region | "Brazil" |
| `candidate_2_salary_range` | Monthly salary range | "$2,000-$2,500" |
| `candidate_2_onboarded_date` | When candidate joined | "NA" |
| `candidate_2_experience_1` | First experience line | "5+ Yrs Freelancing" |
| `candidate_2_experience_2` | Second experience line | "8+ Yrs Content Marketing" |
| `candidate_2_experience_3` | Third experience line | "10+ Yrs Adobe Suite" |
| `candidate_2_tech_stack` | Technical skills | "Adobe Creative Suite\nFigma\nVideo Editing\nCopywriting" |

#### Candidate Profile 3 (South Africa) - Slides 8
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `candidate_3_name` | Candidate first name | "Sarah" |
| `candidate_3_photo_url` | Profile photo URL | "https://example.com/sarah.jpg" |
| `candidate_3_bio` | Brief candidate description | "Experienced marketing professional based in South Africa..." |
| `candidate_3_responsibilities` | Key responsibilities bullets | "• Develop comprehensive marketing strategies\n• Execute cross-channel campaigns\n• Optimize performance metrics" |
| `candidate_3_region` | Candidate region | "South Africa" |
| `candidate_3_salary_range` | Monthly salary range | "$1,800-$2,200" |
| `candidate_3_experience_1` | First experience line | "5+ Yrs Marketing" |
| `candidate_3_experience_2` | Second experience line | "3+ Yrs Digital Strategy" |
| `candidate_3_experience_3` | Third experience line | "7+ Yrs Analytics" |
| `candidate_3_tech_stack` | Technical skills | "Google Analytics\nHubSpot\nSocial Media Management\nEmail Marketing" |

#### Featured Candidate Profile (Slide 11 - Corinna)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `featured_candidate_name` | Featured candidate name | "Corinna" |
| `featured_candidate_photo_url` | Profile photo URL | "https://example.com/corinna.jpg" |
| `featured_candidate_title` | Role title | "Content Marketer" |
| `featured_candidate_bio` | Detailed biography | "Has a strong passion for advertising and art, with hands-on experience in marketing coordination and brand identity for events. She is currently pursuing an MBA in advertising, further refining her strategic and creative expertise." |
| `featured_candidate_region` | Candidate region | "Brazil" |
| `featured_candidate_salary_range` | Monthly salary range | "$2,000-$2,500" |
| `featured_candidate_onboarded` | Onboarding status | "NA" |
| `featured_candidate_experience_freelance` | Freelancing experience | "7+ Yrs Freelancing" |
| `featured_candidate_experience_content` | Content marketing experience | "2+ Yrs Content Marketing" |
| `featured_candidate_experience_adobe` | Adobe Suite experience | "5+ Yrs Adobe Suite" |
| `featured_candidate_tech_1` | First tech skill | "Adobe Creative Suite" |
| `featured_candidate_tech_2` | Second tech skill | "Figma" |
| `featured_candidate_tech_3` | Third tech skill | "Video Editing" |
| `featured_candidate_tech_4` | Fourth tech skill | "Copywriting" |
| `featured_candidate_responsibilities` | Key responsibilities | "• Create visual content that aligns with brand guidelines.\n• Design assets for various mediums (social media, print, web).\n• Collaborate with teams to ensure design meets marketing objectives." |

#### Pricing & Service Structure (Slide 13)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `tier_1_salary_range` | Tier 1 monthly pay band | "$1,500 - $2,000" |
| `tier_1_regions` | Tier 1 recommended markets | "Philippines" |
| `tier_1_fee` | Tier 1 placement fee | "$4,800" |
| `tier_2_salary_range` | Tier 2 monthly pay band | "$2,500 - $4,000" |
| `tier_2_regions` | Tier 2 recommended markets | "Philippines + Latin America" |
| `tier_2_fee` | Tier 2 placement fee | "$5,600" |
| `tier_3_salary_range` | Tier 3 monthly pay band | "$4,000+" |
| `tier_3_regions` | Tier 3 recommended markets | "PI + LatAm + Africa + EU" |
| `tier_3_fee` | Tier 3 placement fee | "$6,400 - $8,000" |

#### Project Summary (Slide 14)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `project_role` | Role for this project | "Content Marketer" |
| `project_salary_range` | Monthly pay band for project | "$1,350 - $1,600" |
| `project_fee_total` | Total Tidal fee | "$5,600 Total" |
| `project_fee_deposit` | Deposit amount | "$1,500 deposit due now" |
| `project_fee_balance` | Balance due after placement | "Balance Due after successful placement" |
| `project_guarantee` | Replacement guarantee terms | "Culture fit, performance, life events- we'll replace them free of charge" |

#### Service Comparison (Slide 17)
| Variable Name | Description | Example Value |
|---------------|-------------|---------------|
| `bpo_agency_cost` | BPO agency monthly cost | "$3K / month" |
| `bpo_agency_annual` | BPO agency annual cost | "$36K / year" |
| `bpo_hire_gets` | What hire actually receives | "$2K/month → $24K / Year" |
| `bpo_results` | BPO service results | "Less quality talent.\nBPO is squeezing recurring revenue monthly\nAdded layer of middle-management & stakeholders" |
| `tidal_fee` | Tidal one-time fee | "$5,600 one-time fee" |
| `tidal_monthly_cost` | Tidal monthly cost | "$3K / month" |
| `tidal_annual_cost` | Tidal annual cost | "$36K / year" |
| `tidal_hire_gets` | What hire receives with Tidal | "$3K/month → $36K / Year" |
| `tidal_results` | Tidal service results | "Attract better candidates.\nPay people the most & retain talent longer\nTidal only gets paid when we perform" |
| `fixed_budget_example` | Example fixed budget | "$36K/year" |
| `tidal_salary_option_1` | Tidal salary option 1 | "Hire @ $2,500 / month → $30K / year" |
| `tidal_salary_option_2` | Tidal salary option 2 | "Deel COR @ $500 / month → $6K / year" |

---

## 🎯 Slide-by-Slide Variable Mapping

### **Slide 1: Cover Page**
```
PREPARED FOR: {{company_name}}
Date: {{scan_date}}
[LOGO HERE]: Upload client logo manually or use {{client_logo_url}}
```

### **Slide 2: Role Overview**
```
ROLE TITLE: {{position_title}}
RECOMMENDED PAY BAND: {{ph_salary_min}} - {{ph_salary_max}}

SIMILAR ROLES BY JOB TITLE:
{{similar_role_1}} ({{similar_role_1_percent}}%)
{{similar_role_2}} ({{similar_role_2_percent}}%)  
{{similar_role_3}} ({{similar_role_3_percent}}%)

UNIQUE CHALLENGES: {{role_challenges}}
```

### **Slide 3: Role Analysis with Availability**
```
ROLE TITLE: {{position_title}}
RECOMMENDED PAY BAND: {{ph_salary_min}} - {{ph_salary_max}}
ROLE AVAILABILITY: {{seniority_level}}

UNIQUE CHALLENGES: {{role_challenges}}
```

### **Slide 4: Regional Salary Comparison**
```
Asia/Philippines: {{ph_salary_min}} - {{ph_salary_max}}
LatAm: {{latam_salary_min}} - {{latam_salary_max}}  
Africa: {{sa_salary_min}} - {{sa_salary_max}}
Europe: {{europe_salary_min}} - {{europe_salary_max}}

Regional Recommendations:
Asia: {{asia_recommendation}}
LatAm: {{latam_recommendation}}
Africa: {{africa_recommendation}}  
Europe: {{europe_recommendation}}
```

### **Slide 5: Experience Level Matrix**
```
ROLE TITLE: {{position_title}}
ROLE AVAILABILITY: {{seniority_level}}

Experience Matrix:
0-2 years: {{junior_salary_min}} - {{junior_salary_max}}
3-6 years: {{mid_salary_min}} - {{mid_salary_max}}
6-8 years: {{senior_salary_min}} - {{senior_salary_max}}
9+ years: {{expert_salary_min}} - {{expert_salary_max}}

RECOMMENDED PAY BAND: {{recommended_salary_min}} - {{recommended_salary_max}}
```

### **Slide 6: Candidate Profile 1 (Philippines)**
```
ROLE TITLE: {{position_title}}
[PHOTO]: {{candidate_1_photo_url}}

Meet {{candidate_1_name}}
{{candidate_1_bio}}

RESPONSIBILITIES:
{{candidate_1_responsibilities}}

REGION: {{candidate_1_region}} (with flag icon)
MONTHLY PAY BAND: {{candidate_1_salary_range}}
ONBOARDED IN: {{candidate_1_onboarded_date}}

EXPERIENCE:
{{candidate_1_experience_1}}
{{candidate_1_experience_2}}
{{candidate_1_experience_3}}

TECH STACK:
{{candidate_1_tech_stack}}
```

### **Slide 7: Candidate Profile 2 (Latin America)**
```
ROLE TITLE: {{position_title}}
[PHOTO]: {{candidate_2_photo_url}}

Meet {{candidate_2_name}}
{{candidate_2_bio}}

RESPONSIBILITIES:
{{candidate_2_responsibilities}}

REGION: {{candidate_2_region}} (with flag icon)
EXPECTED SALARY: {{candidate_2_salary_range}}
ONBOARDED IN: {{candidate_2_onboarded_date}}

EXPERIENCE:
{{candidate_2_experience_1}}
{{candidate_2_experience_2}}
{{candidate_2_experience_3}}

TECH STACK:
{{candidate_2_tech_stack}}
```

### **Slide 8: Candidate Profile 3 (South Africa)**
```
ROLE TITLE: {{position_title}}
[PHOTO]: {{candidate_3_photo_url}}

Meet {{candidate_3_name}}
{{candidate_3_bio}}

RESPONSIBILITIES:
{{candidate_3_responsibilities}}

REGION: {{candidate_3_region}} (with flag icon)
MONTHLY PAY BENCHMARK: {{candidate_3_salary_range}}

EXPERIENCE:
{{candidate_3_experience_1}}
{{candidate_3_experience_2}}
{{candidate_3_experience_3}}

TECH STACK:
{{candidate_3_tech_stack}}
```

### **Slides 9-10: Additional Candidate Profiles (Optional)**
```
Note: The template supports 3 standard candidate profiles (slides 6-8).
If additional candidate profiles are needed for slides 9-10, the same
variable pattern can be extended with candidate_4_* and candidate_5_*
variables following the same structure as above.

This allows for flexible candidate comparison presentations based on
the specific market scan requirements and available talent pool.
```

### **Slide 11: Featured Candidate Profile (Corinna)**
```
ROLE TITLE: {{featured_candidate_title}}
[PHOTO]: {{featured_candidate_photo_url}}

Meet {{featured_candidate_name}}
{{featured_candidate_bio}}

RESPONSIBILITIES:
{{featured_candidate_responsibilities}}

REGION: {{featured_candidate_region}} (with flag icon)
EXPECTED SALARY: {{featured_candidate_salary_range}}
ONBOARDED IN: {{featured_candidate_onboarded}}

EXPERIENCE:
{{featured_candidate_experience_freelance}}
{{featured_candidate_experience_content}}
{{featured_candidate_experience_adobe}}

TECH STACK:
{{featured_candidate_tech_1}}
{{featured_candidate_tech_2}}
{{featured_candidate_tech_3}}
{{featured_candidate_tech_4}}
```

### **Slide 12: Our Process Timeline**
```
Static content - no variables needed for process flow diagram
Timeline shows: Intake → Recruiting & Screening → Finalist Selection → Handoff
```

### **Slide 13: Precision Placement Pricing Table**
```
TIER 1: {{tier_1_salary_range}}
RECOMMENDED MARKETS: {{tier_1_regions}}
OUR FEE: {{tier_1_fee}}

TIER 2: {{tier_2_salary_range}}
RECOMMENDED MARKETS: {{tier_2_regions}}
OUR FEE: {{tier_2_fee}}

TIER 3: {{tier_3_salary_range}}
RECOMMENDED MARKETS: {{tier_3_regions}}
OUR FEE: {{tier_3_fee}}
```

### **Slide 14: Summary of Work**
```
ROLE: {{project_role}}
MONTHLY PAY BAND: {{project_salary_range}}
TIDAL FEE: {{project_fee_total}}

NOTE:
{{project_fee_deposit}}
{{project_fee_balance}}

FOUNDER GUARANTEE (6 months):
{{project_guarantee}}
```

### **Slide 17: Managed Services BPO vs. Direct Placement (Tidal)**
```
BPO SCENARIO:
Agency Says: "We'll cover payroll & paperwork for one flat fee"
You Pay: {{bpo_agency_cost}} → {{bpo_agency_annual}}
Your Hire Gets: {{bpo_hire_gets}}
End Result: {{bpo_results}}

TIDAL SCENARIO:
Tidal Says: "We'll maximize your budget for one flat fee"
You Pay: {{tidal_fee}} + {{tidal_monthly_cost}} → {{tidal_annual_cost}}
Your Hire Gets: {{tidal_hire_gets}}
End Result: {{tidal_results}}

MY BUDGET IS FIXED AT: {{fixed_budget_example}}
Option 1: {{tidal_salary_option_1}}
Option 2: {{tidal_salary_option_2}}
```

---

## 🎯 Canva Template Setup Guide

### Step 1: Prepare Your Template
1. **Open your Market Scan PDF template in Canva**
2. **Convert static text to variables** using `{{variable_name}}` format
3. **Use the exact variable names** from the table above

### Step 2: Common Template Sections

#### **Header Section**
```
Company: {{company_name}}
Position: {{position_title}}
Analysis Date: {{scan_date}}
Confidence: {{analysis_confidence}}
```

#### **Salary Comparison Chart**
```
US Average: {{us_salary}}
Philippines: {{ph_salary}} (Save {{ph_savings_percent}})
Latin America: {{latam_salary}} (Save {{latam_savings_percent}})
South Africa: {{sa_salary}} (Save {{sa_savings_percent}})
```

#### **Skills Requirements**
```
Required Skills: {{required_skills}}
Preferred Skills: {{preferred_skills}}
Certifications: {{certifications}}
```

#### **Role Analysis**
```
Complexity: {{role_complexity}}/10
Experience Level: {{seniority_level}}
Years Required: {{experience_years}}
Remote Work: {{remote_suitability}}
```

### Step 3: Bulk Import Process
1. **Create market scan** in Tidal Streamline
2. **Go to export page**: `/scan/{scanId}/export`
3. **Click "📄 Template CSV"** button
4. **In Canva**: Design → Bulk Create → Upload CSV
5. **Map columns** to your template variables
6. **Generate** multiple variations if needed

---

## 🔧 Customization Options

### Option 1: Standard Template (Current)
**Uses all 70+ variables** for comprehensive reports including candidate profiles

### Option 2: Essential Template
**Use only these 15 key variables for simpler templates:**
- company_name, position_title, scan_date
- us_salary, ph_salary, ph_savings_percent
- latam_salary, latam_savings_percent
- required_skills, preferred_skills
- role_complexity, seniority_level
- experience_years, best_regions
- analysis_confidence

### Option 3: Custom Variable Names
**Tell us your preferred variable names and we'll create a custom CSV export**

Example: If your template uses `{{client_company}}` instead of `{{company_name}}`, we can modify the export accordingly.

---

## 📈 Charts & Visualizations

### Salary Comparison Bar Chart
**Data points available:**
- All regions: min, average, max salaries
- Savings percentages vs US baseline
- Currency formatting included

### Skills Assessment Radar/Bar Chart
**Categories available:**
- Technical Skills
- Marketing Skills  
- Analytics Skills
- Certifications

### Regional Recommendations
**Visual elements:**
- Best regions ranking
- Cost efficiency analysis
- Demand level indicators

---

## 🚀 Advanced Integration

### Future API Integration
Once your template is working with CSV, we can build:
- **Direct Canva API connection**
- **Automated report generation**
- **Multi-template support**
- **Branded template variations**

### Template Optimization
**Share screenshots of your template and we can:**
- Optimize variable mapping
- Add missing data points
- Create template-specific calculations
- Build custom formatting

---

## 📞 Next Steps

### Immediate Actions
1. **Test the current Template CSV** with your Canva template
2. **Share template screenshots** or variable names for optimization
3. **Report any missing data points** your template needs

### Template Mapping Help
**Contact with:**
- Screenshots of key template sections
- List of variable names currently used
- Any specific formatting requirements
- Charts or visualizations that need data

### Questions to Consider
- Which regions are most important for your templates?
- Do you need multiple template variations?
- Any custom calculations or formatting needed?
- Integration with other systems required?

**Ready to create beautiful, data-driven market scan reports!** 🎨📊

---

## 🚨 Implementation Status & Critical To-Dos

### Current Implementation Coverage
**Variables Implemented**: 44 out of 134 (33% coverage)  
**Variables Missing**: 90+ (67% gap)

### 🔴 Critical Missing Categories

#### **1. Candidate Profiles (45+ fields) - COMPLETELY MISSING**
- All candidate profile data exists in database but not exported
- Missing: photos, bios, experience details, tech stacks, regions, salary ranges
- **Impact**: Slides 6-8, 11 cannot be templated

#### **2. Similar Roles Analysis (6 fields) - CRITICAL MISSING**
- `similar_role_1`, `similar_role_1_percent`
- `similar_role_2`, `similar_role_2_percent`  
- `similar_role_3`, `similar_role_3_percent`
- **Impact**: Slide 2 role overview incomplete

#### **3. Experience Level Breakdowns (8 fields) - CRITICAL MISSING**
- `junior_salary_min/max`, `mid_salary_min/max`
- `senior_salary_min/max`, `expert_salary_min/max`
- **Impact**: Slide 5 experience matrix missing

#### **4. Pricing & Service Structure (27 fields) - MISSING**
- Tier pricing (9 fields), project summary (6 fields)
- Service comparison BPO vs Tidal (12 fields)
- **Impact**: Slides 13, 14, 17 cannot be templated

### 🎯 Implementation Priority

#### **Phase 1: Backend CSV Endpoint (HIGH PRIORITY)**
**Timeline**: 1-2 days  
**Current Issue**: CSV export is frontend-only, can't access full database

**Tasks**:
1. **Create Backend Endpoint**
   ```
   GET /api/v1/market-scans/{scanId}/export?format=template
   ```
2. **Move CSV Logic to Backend**
   - From: `/frontend/src/pages/DataExport.tsx`
   - To: `/backend/app/api/v1/endpoints/export.py`

3. **Integrate Candidate Profiles**
   - Query candidates table for profile data
   - Map to candidate_1_*, candidate_2_*, candidate_3_* variables
   - Add featured_candidate_* variables

4. **Add Similar Roles Analysis**
   - Use existing vector search to find similar job titles
   - Calculate similarity percentages
   - Export similar_role_* variables

**Expected Outcome**: 70+ additional variables (85% coverage)

#### **Phase 2: Database Enhancements (MEDIUM PRIORITY)**
**Timeline**: 2-3 days  

**Tasks**:
1. **Experience-Level Salary Breakdown**
   ```sql
   ALTER TABLE market_scans ADD COLUMN experience_breakdown JSONB;
   ```
   - Calculate salary ranges by experience level (0-2, 3-6, 6-8, 9+ years)
   - Export junior_*, mid_*, senior_*, expert_* variables

2. **Regional Recommendations**
   ```sql
   ALTER TABLE market_scans ADD COLUMN regional_recommendations JSONB;
   ```
   - Add descriptive text for each region's hiring benefits
   - Export asia_recommendation, latam_recommendation, etc.

3. **Europe Region Data**
   - Add Europe to salary calculations
   - Export europe_salary_min/max, europe_savings_percent

4. **Pricing Tiers Configuration**
   ```sql
   CREATE TABLE pricing_tiers (
     tier_level INTEGER PRIMARY KEY,
     salary_range_min INTEGER,
     salary_range_max INTEGER,
     regions TEXT[],
     fee INTEGER
   );
   ```

**Expected Outcome**: 95% coverage

#### **Phase 3: Advanced Features (LOW PRIORITY)**
**Timeline**: 1-2 days  

**Tasks**:
1. **Service Comparison Calculations**
   - Generate BPO vs Tidal comparison data
   - Calculate cost savings scenarios

2. **Project Summary Auto-Generation**
   - Auto-calculate project costs and timelines
   - Generate guarantee terms

3. **Template Customization**
   - Support multiple template formats
   - Custom variable mapping

**Expected Outcome**: 100% coverage + enhanced features

### 🛠️ Technical Implementation Notes

#### **Current Export Location**
- **Frontend**: `/frontend/src/pages/DataExport.tsx` (lines 40-165)
- **Route**: `/scan/{scanId}/export` (frontend only)
- **Method**: Client-side CSV generation

#### **Required Backend Implementation**
- **Endpoint**: `/backend/app/api/v1/endpoints/export.py`
- **Route**: `GET /api/v1/market-scans/{scanId}/export`
- **Method**: Server-side with full database access

#### **Database Tables Needed**
- ✅ `market_scans` - Role and salary data (exists)
- ✅ `candidates` - Profile data (exists, not used in export)
- ❌ `pricing_tiers` - Service pricing (needs creation)
- ❌ Experience breakdown (needs column addition)

### 🚀 Immediate Next Steps

1. **Backend Endpoint Creation** (Day 1)
   - Create export endpoint with database access
   - Integrate candidate profile queries
   - Add similar roles vector search

2. **CSV Generation Enhancement** (Day 1)
   - Move logic from frontend to backend
   - Add missing candidate variables
   - Implement similar roles analysis

3. **Testing & Validation** (Day 2)
   - Test all 134 variables in CSV output
   - Validate Canva template integration
   - Verify data accuracy

4. **Experience Level Implementation** (Day 3)
   - Add experience breakdown calculations
   - Regional recommendations text
   - Europe region data

### 📊 Success Metrics

- **Phase 1 Success**: 85% variable coverage (110+ of 134 variables)
- **Phase 2 Success**: 95% variable coverage (125+ of 134 variables)  
- **Phase 3 Success**: 100% variable coverage + template customization

### ⚠️ Blockers & Dependencies

1. **Database Access**: Backend endpoint needed for candidate data
2. **Vector Search**: Similar roles requires existing similarity calculation
3. **Pricing Data**: Static pricing tiers need database storage
4. **Regional Text**: Recommendation descriptions need content creation

---

**Status**: 🔴 **CRITICAL IMPLEMENTATION NEEDED**  
**Next Action**: Create backend CSV export endpoint  
**Owner**: Development Team  
**Timeline**: Phase 1 completion within 2 days