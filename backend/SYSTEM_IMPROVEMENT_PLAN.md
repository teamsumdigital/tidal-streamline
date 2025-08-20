# Tidal Streamline System Improvement Plan

**Generated**: August 20, 2025  
**Current Overall Score**: 87.8/100  
**Target Score**: 90+/100  
**Primary Issue**: Logical Consistency (35.8% - Critical)

---

## 🚨 Critical Issues Identified

### **Issue #1: Regional Logic Alignment (HIGH PRIORITY)**
**Impact**: Logical Consistency score 35.8% → Target 80%+  
**Root Cause**: Contradictory information between Market Insights and Regional Recommendations

#### **Specific Problems**:
1. Market Insights always says "High demand in Philippines & Latin America"
2. Regional Recommendations always includes "US, Philippines, Latin America"  
3. AI asks: "Why recommend US if it's not high demand?"

#### **Examples from Test Results**:
- **Ecommerce Manager**: High demand = Philippines & South Africa, Recommended = US, Philippines, Latin America
- **Retention Manager**: High demand = Philippines & Latin America, Recommended = US, Philippines, Latin America
- **Executive Assistant**: High demand regions don't align with salary recommendations

---

### **Issue #2: Role Category Mapping Errors (MEDIUM PRIORITY)**
**Impact**: Data completeness and logical consistency  
**Root Cause**: Job titles incorrectly mapped to role categories

#### **Specific Problems**:
1. AI service returns wrong role_category for job titles
2. Different sections use different role category names
3. No validation between job title and assigned role category

#### **Examples from Test Results**:
- **Executive Assistant** → labeled as `Operations Manager`
- **Brand Marketing Manager** → labeled as `Ecommerce Manager`  
- **Customer Experience Manager** → labeled as `Retention Manager`
- **Product Development Manager** → labeled as `Operations Manager`

---

### **Issue #3: Skills Redundancy (LOW PRIORITY)**
**Impact**: Data quality and logical consistency  
**Root Cause**: No deduplication logic for skills across categories

#### **Specific Problems**:
1. Same skill appears in both "Must Have" and "Nice to Have"
2. Skills duplicated within same category
3. No priority logic (must-have should override nice-to-have)

#### **Examples from Test Results**:
- `Marketing automation tools` → both must-have AND nice-to-have
- `Statistical analysis` → both must-have AND nice-to-have
- `Process optimization` → listed twice in nice-to-have

---

## 🔧 Technical Implementation Plan

### **Fix #1: Regional Logic Alignment**

#### **Files to Modify**:

**1. `app/services/salary_calculator.py`**
```python
# Current Issue: Hardcoded logic
def _generate_market_insights(self, job_analysis: JobAnalysis, salary_recommendations: Dict[str, SalaryRange]):
    # Line ~186: Always returns ["Philippines", "Latin America"]
    high_demand = ["Philippines", "Latin America"]  # ❌ HARDCODED
```

**Proposed Fix**:
```python
def _generate_market_insights(self, job_analysis: JobAnalysis, salary_recommendations: Dict[str, SalaryRange]):
    # ✅ NEW: Align high demand with recommended regions
    recommended_regions = [r.value for r in job_analysis.recommended_regions]
    
    # High demand should match recommended regions
    high_demand = recommended_regions.copy()
    
    # Remove US if it's only there for completeness but not actually high demand
    if "United States" in high_demand and len(high_demand) > 1:
        # Only keep US if complexity score is high (8+) indicating need for premium talent
        if job_analysis.complexity_score < 8:
            high_demand.remove("United States")
    
    return MarketInsights(
        high_demand_regions=high_demand,  # ✅ NOW ALIGNED
        competitive_factors=competitive_factors,
        cost_efficiency=cost_efficiency
    )
```

**2. `app/services/job_analyzer.py`**
```python
# Current Issue: Always includes US in recommendations
# Line ~XXX in recommended_regions logic
recommended_regions = [Region.UNITED_STATES, Region.PHILIPPINES, Region.LATIN_AMERICA]  # ❌ ALWAYS US
```

**Proposed Fix**:
```python
def _determine_recommended_regions(self, role_category: RoleCategory, complexity_score: int, remote_suitability: str) -> List[Region]:
    """Determine recommended regions based on role complexity and requirements"""
    regions = []
    
    # Always include cost-effective regions for remote work
    if remote_suitability in ["high", "medium"]:
        regions.extend([Region.PHILIPPINES, Region.LATIN_AMERICA])
    
    # Only include US for high complexity roles or when local presence needed
    include_us = (
        complexity_score >= 8 or  # High complexity needs premium talent
        remote_suitability == "low" or  # Needs local presence
        role_category in [RoleCategory.SALES_OPERATIONS_MANAGER]  # Strategic roles
    )
    
    if include_us:
        regions.insert(0, Region.UNITED_STATES)  # US first if included
    
    return regions[:3]  # Max 3 regions
```

#### **Database Changes Required**:
**None** - This is purely logic changes in service layer

#### **Testing Strategy**:
1. Run comprehensive test suite
2. Verify logical consistency scores improve to 70%+
3. Check that high_demand_regions == recommended_regions for each test

---

### **Fix #2: Role Category Mapping**

#### **Files to Modify**:

**1. `app/models/enums.py`**
Add validation mapping:
```python
# Add after existing RoleCategory enum
ROLE_TITLE_MAPPINGS = {
    # Exact matches
    "Brand Marketing Manager": RoleCategory.BRAND_MARKETING_MANAGER,
    "Community Manager": RoleCategory.COMMUNITY_MANAGER,
    "Content Marketer": RoleCategory.CONTENT_MARKETER,
    "Executive Assistant": RoleCategory.ADMIN_EA,
    "Customer Experience Manager": RoleCategory.CUSTOMER_EXPERIENCE_MANAGER,
    "Product Development Manager": RoleCategory.PRODUCT_DEVELOPMENT_MANAGER,
    
    # Common title variations
    "Creative Project Manager": RoleCategory.BRAND_MARKETING_MANAGER,
    "Social Media Manager": RoleCategory.COMMUNITY_MANAGER,
    "E-commerce Manager": RoleCategory.ECOMMERCE_MANAGER,
    "Product Lifecycle Manager": RoleCategory.PRODUCT_DEVELOPMENT_MANAGER,
}

def validate_role_category_mapping(job_title: str, assigned_category: RoleCategory) -> bool:
    """Validate that assigned role category matches job title"""
    expected = ROLE_TITLE_MAPPINGS.get(job_title)
    if expected and expected != assigned_category:
        return False
    return True
```

**2. `app/services/job_analyzer.py`**
Add validation logic:
```python
async def analyze_job_with_similar_scans(self, job_title: str, job_description: str, ...):
    # Existing analysis logic...
    job_analysis = await self._analyze_job_with_ai(...)
    
    # ✅ NEW: Validate role category mapping
    from app.models.enums import validate_role_category_mapping
    
    if not validate_role_category_mapping(job_title, job_analysis.role_category):
        # Log warning and attempt correction
        logger.warning(f"Role category mismatch: '{job_title}' assigned to '{job_analysis.role_category}'")
        
        # Try to correct from mapping
        correct_category = ROLE_TITLE_MAPPINGS.get(job_title)
        if correct_category:
            job_analysis.role_category = correct_category
            logger.info(f"Corrected role category to: {correct_category}")
    
    return job_analysis, similar_scans, confidence_score
```

**3. Update AI Prompt in `app/core/ai_service.py`**
```python
# Current prompt needs better role category examples
ANALYSIS_PROMPT = f"""
...
"role_category": "Choose from: Brand Marketing Manager, Community Manager, Content Marketer, Retention Manager, 
Ecommerce Manager, Sales Operations Manager, Data Analyst, Logistics Manager, Demand Planner, 
Product Development Manager, Customer Experience Manager, Admin & EA",

IMPORTANT: The role_category MUST match the job title closely. Examples:
- "Executive Assistant" → "Admin & EA"
- "Brand Marketing Manager" → "Brand Marketing Manager" 
- "Customer Experience Manager" → "Customer Experience Manager"
- "Creative Project Manager" → "Brand Marketing Manager"
"""
```

#### **Database Changes Required**:
**New Table**: `role_mappings`
```sql
CREATE TABLE role_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_title TEXT NOT NULL,
    role_category TEXT NOT NULL,
    is_exact_match BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(job_title, role_category)
);

-- Insert standard mappings
INSERT INTO role_mappings (job_title, role_category, is_exact_match) VALUES
('Executive Assistant', 'Admin & EA', true),
('Brand Marketing Manager', 'Brand Marketing Manager', true),
('Customer Experience Manager', 'Customer Experience Manager', true),
('Product Development Manager', 'Product Development Manager', true),
('Creative Project Manager', 'Brand Marketing Manager', false),
('Social Media Manager', 'Community Manager', false),
('E-commerce Manager', 'Ecommerce Manager', false);
```

#### **Testing Strategy**:
1. Add unit tests for role mapping validation
2. Test with known problematic job titles
3. Verify role categories are consistent across all sections

---

### **Fix #3: Skills Deduplication**

#### **Files to Modify**:

**1. `app/services/job_analyzer.py`**
Add deduplication logic:
```python
def _deduplicate_skills(self, must_have: List[str], nice_to_have: List[str]) -> tuple[List[str], List[str]]:
    """Remove duplicates and prioritize must-have skills"""
    
    # Convert to lowercase for comparison but preserve original case
    must_have_lower = [skill.lower() for skill in must_have]
    
    # Remove must-have skills from nice-to-have
    deduplicated_nice_to_have = []
    for skill in nice_to_have:
        if skill.lower() not in must_have_lower:
            deduplicated_nice_to_have.append(skill)
    
    # Remove internal duplicates
    must_have_unique = list(dict.fromkeys(must_have))  # Preserves order
    nice_to_have_unique = list(dict.fromkeys(deduplicated_nice_to_have))
    
    return must_have_unique, nice_to_have_unique

async def _analyze_job_with_ai(self, ...):
    # Existing AI analysis...
    
    # ✅ NEW: Deduplicate skills before returning
    must_have_clean, nice_to_have_clean = self._deduplicate_skills(
        parsed_analysis['must_have_skills'],
        parsed_analysis['nice_to_have_skills']
    )
    
    return JobAnalysis(
        must_have_skills=must_have_clean,
        nice_to_have_skills=nice_to_have_clean,
        # ... other fields
    )
```

**2. `app/api/v1/endpoints/market_scans.py`**
Update skills recommendations generation:
```python
def process_market_scan_analysis(...):
    # After generating job analysis...
    
    # ✅ NEW: Clean up skills recommendations too
    skills_recommendations = SkillsRecommendation(
        must_have_skills=job_analysis.must_have_skills,  # Already cleaned
        nice_to_have_skills=job_analysis.nice_to_have_skills,  # Already cleaned
        skill_categories={
            "technical": [s for s in job_analysis.must_have_skills[:3] if any(tech in s.lower() for tech in ['software', 'tool', 'platform', 'system'])],
            "soft": [s for s in job_analysis.nice_to_have_skills[:2] if not any(tech in s.lower() for tech in ['software', 'tool', 'platform', 'system'])]
        },
        certification_recommendations=_generate_specific_certifications(job_analysis.role_category)
    )
```

#### **Database Changes Required**:
**None** - Pure logic improvement

#### **Testing Strategy**:
1. Test with roles known to have duplicate skills
2. Verify no skill appears in both must-have and nice-to-have
3. Check that skill categories don't overlap

---

## 🎯 Implementation Priority

### **Phase 1: Regional Logic (Week 1)**
- **Expected Impact**: Logical consistency 35.8% → 75%+
- **Files**: `salary_calculator.py`, `job_analyzer.py`
- **Risk**: Low (logic changes only)

### **Phase 2: Role Category Mapping (Week 2)** 
- **Expected Impact**: Data completeness 93.3% → 95%+, Logical consistency +5%
- **Files**: `enums.py`, `job_analyzer.py`, `ai_service.py`
- **Database**: Add `role_mappings` table
- **Risk**: Medium (database changes, AI prompt changes)

### **Phase 3: Skills Deduplication (Week 3)**
- **Expected Impact**: Data quality improvement, Logical consistency +3%  
- **Files**: `job_analyzer.py`, `market_scans.py`
- **Risk**: Low (logic improvements only)

---

## 📊 Expected Results

**Before Fixes**:
- Overall Score: 87.8/100
- Logical Consistency: 35.8% (3.6/10)
- Tests Above 80: 12/12

**After All Fixes**:
- **Overall Score**: 92+/100 (**Target Achieved**)
- **Logical Consistency**: 80%+ (8+/10)
- **Tests Above 90**: 8+/12

---

## ✅ Success Metrics

1. **Logical Consistency Score** > 75% (vs current 35.8%)
2. **Overall Average Score** > 90/100 (vs current 87.8)
3. **Zero contradictory information** in AI feedback
4. **Role category accuracy** = 100% (all titles match categories)
5. **Skills deduplication** = 100% (no overlapping skills)

---

## 🔄 Testing & Validation

### **After Each Fix**:
1. Run comprehensive test suite (12 role categories)
2. Compare before/after logical consistency scores  
3. Review AI feedback for remaining contradictions
4. Update this document with actual results

### **Final Validation**:
1. All 12 tests score 85+ points
2. No "contradictory information" mentioned in AI feedback
3. Regional recommendations align with market insights
4. Role categories match job titles exactly
5. No duplicate skills across categories

---

*This document will be updated as fixes are implemented and tested.*