# 🔧 Canva Developer Setup Guide

## 🎯 Prerequisites & Account Setup

### 1. Canva Developer Account
**URL**: [https://canva.com/developers](https://canva.com/developers)

**Steps**:
1. Sign up with your business email
2. Complete developer verification (may take 24-48 hours)
3. Accept Terms of Service for Canva Developer Platform

### 2. Create Your App
**In Canva Developer Console**:
1. Click "Create an App"
2. **App Type**: Choose "Public App" (for broader access)
3. **App Name**: "Tidal Market Scan Reports"
4. **Description**: "Automated market scan report generation for recruitment analytics"
5. **Scopes Needed**:
   - `design:read` - Read design templates
   - `design:write` - Create/modify designs
   - `brand:read` - Access brand assets (if using branded templates)

### 3. Get API Credentials
**You'll receive**:
- **Client ID**: `ABC123...` (public, can be in frontend)
- **Client Secret**: `XYZ789...` (private, backend only)
- **Redirect URI**: `http://localhost:8008/api/v1/auth/canva/callback`

---

## 🔑 Authentication Methods

### Option A: OAuth Flow (Recommended for Production)
**Best for**: Multi-user access, secure token management

```python
# Backend endpoint for OAuth initiation
@app.get("/api/v1/auth/canva/login")
async def canva_oauth_login():
    auth_url = f"https://www.canva.com/api/oauth/authorize"
    params = {
        "client_id": CANVA_CLIENT_ID,
        "response_type": "code", 
        "redirect_uri": CANVA_REDIRECT_URI,
        "scope": "design:read design:write"
    }
    return {"auth_url": f"{auth_url}?{urlencode(params)}"}

# Handle the callback
@app.get("/api/v1/auth/canva/callback")
async def canva_oauth_callback(code: str):
    # Exchange code for access token
    token_response = requests.post("https://api.canva.com/rest/v1/oauth/token", {
        "grant_type": "authorization_code",
        "client_id": CANVA_CLIENT_ID,
        "client_secret": CANVA_CLIENT_SECRET,
        "code": code,
        "redirect_uri": CANVA_REDIRECT_URI
    })
    # Store token securely
    access_token = token_response.json()["access_token"]
    return {"status": "authenticated"}
```

### Option B: API Key (Simpler for Testing)
**Best for**: Development, single-user access

```python
# Simpler approach using API key
headers = {
    "Authorization": f"Bearer {CANVA_API_KEY}",
    "Content-Type": "application/json"
}
```

---

## 🏗️ Template Preparation

### 1. Convert Static Text to Variables
**In Canva Editor**:
1. Select text element
2. Click "Make dynamic" (if available) OR
3. Replace text with `{{variable_name}}`

**Example Transformations**:
```
Before: "Shopify Store Manager"
After:  "{{job_title}}"

Before: "$75,000 - $120,000"
After:  "{{united_states_salary_range}}"

Before: "71% savings vs US rates"
After:  "{{philippines_savings_vs_us}} savings vs US rates"
```

### 2. Template Variable Mapping
**Create mapping document**:
```json
{
  "template_variables": {
    "job_title": "{{job_title}}",
    "company_name": "{{company_domain}}",
    "us_salary": "{{united_states_mid_salary}}",
    "ph_salary": "{{philippines_mid_salary}}",
    "ph_savings": "{{philippines_savings_vs_us}}",
    "must_have_skills": "{{must_have_skills}}",
    "experience_level": "{{experience_level}}"
  }
}
```

### 3. Get Template ID
**After creating template**:
1. In Canva, click "Share" on your template
2. Copy the template URL: `https://canva.com/design/ABC123.../`
3. Extract template ID: `ABC123...`

---

## 🔗 API Integration Implementation

### 1. Install Required Packages
```bash
# Backend dependencies
pip install canva-api-python  # If available
# OR use direct HTTP requests with:
pip install httpx requests
```

### 2. Basic API Service
```python
# app/services/canva_service.py
import httpx
from app.core.config import settings

class CanvaService:
    def __init__(self):
        self.base_url = "https://api.canva.com/rest/v1"
        self.headers = {
            "Authorization": f"Bearer {settings.CANVA_API_KEY}",
            "Content-Type": "application/json"
        }
    
    async def create_design_from_template(self, template_id: str, data: dict):
        """Create new design from template with data"""
        endpoint = f"{self.base_url}/designs"
        
        payload = {
            "design_type": "presentation",  # or document, social-media-post
            "template_id": template_id,
            "title": f"Market Scan - {data.get('job_title', 'Role')}",
            "variables": data
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, json=payload, headers=self.headers)
            return response.json()
    
    async def get_design_export_urls(self, design_id: str):
        """Get downloadable URLs for the design"""
        endpoint = f"{self.base_url}/designs/{design_id}/export"
        
        payload = {
            "format": "pdf",  # or png, jpg
            "quality": "high"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, json=payload, headers=self.headers)
            return response.json()
```

### 3. New API Endpoint
```python
# app/api/v1/endpoints/reports.py
from app.services.canva_service import CanvaService

@router.post("/generate-canva-report/{scan_id}")
async def generate_canva_report(scan_id: str):
    # Get scan data
    scan = await get_market_scan(scan_id)
    if not scan:
        raise HTTPException(404, "Scan not found")
    
    # Format data for Canva template
    template_data = format_scan_for_canva(scan)
    
    # Create design
    canva_service = CanvaService()
    design = await canva_service.create_design_from_template(
        template_id=settings.CANVA_TEMPLATE_ID,
        data=template_data
    )
    
    # Get export URLs
    export_urls = await canva_service.get_design_export_urls(design["id"])
    
    return {
        "design_id": design["id"],
        "edit_url": design["edit_url"],
        "preview_url": design["preview_url"], 
        "download_urls": export_urls
    }

def format_scan_for_canva(scan: MarketScanResponse) -> dict:
    """Format scan data for Canva template variables"""
    return {
        "job_title": scan.job_title,
        "company_domain": scan.company_domain.replace('.com', '').upper(),
        "analysis_date": datetime.now().strftime("%B %d, %Y"),
        
        # Salary data
        "us_salary_range": f"${scan.salary_recommendations.salary_recommendations['United States']['low']:,} - ${scan.salary_recommendations.salary_recommendations['United States']['high']:,}",
        "ph_salary_range": f"${scan.salary_recommendations.salary_recommendations['Philippines']['low']:,} - ${scan.salary_recommendations.salary_recommendations['Philippines']['high']:,}",
        "ph_savings": f"{scan.salary_recommendations.salary_recommendations['Philippines']['savings_vs_us']}%",
        
        # Skills
        "must_have_skills": ", ".join(scan.skills_recommendations.must_have_skills[:5]),  # Limit for space
        "nice_to_have_skills": ", ".join(scan.skills_recommendations.nice_to_have_skills[:5]),
        
        # Analysis
        "complexity_score": f"{scan.job_analysis.complexity_score}/10",
        "experience_level": scan.job_analysis.experience_level.title(),
        "recommended_regions": ", ".join(scan.job_analysis.recommended_regions),
        
        # Metadata
        "confidence_score": f"{int(scan.confidence_score * 100)}%",
        "similar_scans_count": str(scan.similar_scans_count)
    }
```

---

## 🧪 Testing Strategy

### 1. Manual Testing
```bash
# Test authentication
curl -X GET "https://api.canva.com/rest/v1/me" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Expected response: User info
```

### 2. Template Testing
```python
# Test data formatting
test_data = {
    "job_title": "Test Role",
    "company_domain": "testcompany",
    "us_salary_range": "$75,000 - $120,000"
}

# Verify all required variables are included
```

### 3. End-to-End Testing
1. Create test market scan
2. Generate Canva report
3. Verify all fields populate correctly
4. Test download functionality

---

## 🚨 Error Handling & Edge Cases

### Common Issues
1. **API Rate Limits**: Canva typically allows 100 requests/minute
2. **Template Not Found**: Handle invalid template IDs
3. **Missing Variables**: Provide default values
4. **Large Data**: Truncate long strings to fit template space

### Error Handling
```python
try:
    design = await canva_service.create_design_from_template(template_id, data)
except CanvaAPIError as e:
    if e.status_code == 429:  # Rate limit
        await asyncio.sleep(60)  # Wait and retry
    elif e.status_code == 404:  # Template not found
        raise HTTPException(404, "Template configuration error")
    else:
        logger.error(f"Canva API error: {e}")
        raise HTTPException(500, "Report generation failed")
```

---

## 📊 Environment Variables

```env
# Add to backend/.env
CANVA_CLIENT_ID=your_canva_client_id
CANVA_CLIENT_SECRET=your_canva_client_secret  
CANVA_API_KEY=your_canva_api_key
CANVA_TEMPLATE_ID=your_template_id
CANVA_REDIRECT_URI=http://localhost:8008/api/v1/auth/canva/callback
```

---

## 🎯 Implementation Priority

### Phase 1: Setup & Authentication (Week 1)
- [ ] Create Canva developer account
- [ ] Set up authentication flow
- [ ] Test basic API connectivity

### Phase 2: Template Preparation (Week 1-2)  
- [ ] Analyze your current template
- [ ] Convert to dynamic variables
- [ ] Map our data fields to template variables

### Phase 3: Integration (Week 2)
- [ ] Build Canva service class
- [ ] Create API endpoint
- [ ] Add to frontend UI

### Phase 4: Testing & Production (Week 3)
- [ ] End-to-end testing
- [ ] Error handling
- [ ] Production deployment

**Ready to start? Share your template details and we'll begin mapping!** 🚀