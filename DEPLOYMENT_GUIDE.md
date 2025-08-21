# Tidal Streamline - Production Deployment Guide

**Date**: August 20, 2025  
**Target**: Render (Backend) + Netlify (Frontend)  
**Repository**: https://github.com/teamsumdigital/tidal-streamline

---

## 🎯 Deployment Architecture

```
Frontend (Netlify)  →  Backend API (Render)  →  Supabase Database
     ↓                        ↓                      ↓
React + Vite          FastAPI + Python        PostgreSQL + Vector
Static Site           Web Service             Cloud Database
```

---

## 🚀 Phase 1: Backend Deployment (Render)

### **Step 1: Prepare Backend for Production**

#### **1.1 Create Production Environment File**
Create `backend/.env.production`:
```env
# Database
SUPABASE_URL=https://fhaiolgezcghbiwyayrp.supabase.co
SUPABASE_SERVICE_KEY=[YOUR_SUPABASE_SERVICE_KEY]

# AI Services
OPENAI_API_KEY=[YOUR_OPENAI_API_KEY]

# Vector Database (if using Pinecone)
PINECONE_API_KEY=[YOUR_PINECONE_KEY]
PINECONE_ENVIRONMENT=[YOUR_PINECONE_ENV]

# App Configuration
DEBUG_MODE=false
PORT=8000
CORS_ORIGINS=https://tidal-streamline.netlify.app

# Optional: Monitoring
SENTRY_DSN=[YOUR_SENTRY_DSN]
```

#### **1.2 Update Requirements for Production**
Add to `backend/requirements.txt`:
```txt
# Current dependencies (already there)
fastapi==0.104.1
uvicorn[standard]==0.24.0
supabase==2.3.4
python-multipart==0.0.6
loguru==0.7.2

# Production additions
gunicorn==21.2.0
python-dotenv==1.0.0
sentry-sdk[fastapi]==1.38.0
```

#### **1.3 Create Production Startup Script**
Create `backend/start.py`:
```python
"""
Production startup script for Render deployment
"""
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable in production
        access_log=True,
        log_level="info"
    )
```

### **Step 2: Deploy to Render**

#### **2.1 Connect Repository**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select repository: `teamsumdigital/tidal-streamline`

#### **2.2 Configure Build Settings**
```yaml
# Render will auto-detect these, but verify:
Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && python start.py
```

#### **2.3 Environment Variables in Render**
Add these in Render Dashboard → Environment:
```
SUPABASE_URL=https://fhaiolgezcghbiwyayrp.supabase.co
SUPABASE_SERVICE_KEY=[PASTE_YOUR_REAL_KEY]
OPENAI_API_KEY=[PASTE_YOUR_REAL_KEY]
DEBUG_MODE=false
PORT=8000
CORS_ORIGINS=https://tidal-streamline.netlify.app
```

#### **2.4 Configure Build Settings**
- **Runtime**: Python 3.11
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && python start.py`
- **Root Directory**: Leave blank (will cd into backend)

---

## 🎨 Phase 2: Frontend Deployment (Netlify)

### **Step 1: Prepare Frontend for Production**

#### **1.1 Update API Base URL**
Edit `frontend/src/services/api.ts`:
```typescript
// Update API_BASE_URL for production
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://tidal-streamline-api.onrender.com';
```

#### **1.2 Create Environment Files**
Create `frontend/.env.production`:
```env
VITE_API_BASE_URL=https://tidal-streamline-api.onrender.com
VITE_APP_ENV=production
```

Create `frontend/.env.local` (for local dev pointing to production):
```env
VITE_API_BASE_URL=https://tidal-streamline-api.onrender.com
VITE_APP_ENV=development
```

#### **1.3 Update Build Configuration**
Verify `frontend/package.json` has correct build script:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "build:ssg": "vite-ssg build"
  }
}
```

### **Step 2: Deploy to Netlify**

#### **2.1 Connect Repository**
1. Go to [Netlify Dashboard](https://app.netlify.com/)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect to GitHub
4. Select repository: `teamsumdigital/tidal-streamline`

#### **2.2 Configure Build Settings**
```yaml
Base directory: frontend
Build command: npm run build
Publish directory: frontend/dist
```

#### **2.3 Environment Variables in Netlify**
Add in Netlify Dashboard → Environment variables:
```
VITE_API_BASE_URL=https://tidal-streamline-api.onrender.com
VITE_APP_ENV=production
```

#### **2.4 Configure Redirects**
Create `frontend/public/_redirects`:
```
# SPA routing - redirect all to index.html
/*    /index.html   200
```

---

## ⚙️ Phase 3: Production Configuration

### **Step 1: Update CORS Settings**
Update `backend/app/core/config.py`:
```python
class Settings(BaseSettings):
    # ... existing settings
    
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # Development
        "https://tidal-streamline.netlify.app",  # Production
        "https://main--tidal-streamline.netlify.app"  # Branch deploys
    ]
```

### **Step 2: Database Migrations**
Ensure all database tables exist in production Supabase:

1. **Verify Tables**: 
   - `market_scans`
   - `candidate_profiles`
   - `roles`
   - `salary_benchmarks`

2. **Run Migrations** (if needed):
```sql
-- Check if all tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- If missing, run your table creation scripts
```

### **Step 3: Health Check Endpoint**
Verify `backend/app/api/v1/endpoints/health.py` exists:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "tidal-streamline-api",
        "version": "1.0.0"
    }
```

---

## 🔧 Phase 4: Domain Configuration (Optional)

### **Step 1: Custom Domains**
If you want custom domains:

**Frontend (Netlify)**:
- Domain: `app.hiretidal.com`
- Set up in Netlify → Domain settings

**Backend (Render)**:
- Domain: `api.hiretidal.com` 
- Set up in Render → Settings → Custom domains

### **Step 2: Update Environment Variables**
Update all API_BASE_URL references to use your custom domain.

---

## 📋 Pre-Deployment Checklist

### **Backend (Render)**:
- [ ] Environment variables set
- [ ] Database connection tested
- [ ] OpenAI API key working
- [ ] Health endpoint responding
- [ ] CORS origins updated

### **Frontend (Netlify)**:
- [ ] API_BASE_URL pointing to Render service
- [ ] Build completing successfully
- [ ] Redirects configured for SPA routing
- [ ] Environment variables set

### **Integration**:
- [ ] Frontend can call backend API
- [ ] Database operations working
- [ ] File uploads/exports working
- [ ] Authentication working (if applicable)

---

## 🚀 Deployment Steps

### **Step-by-Step Execution:**

1. **Deploy Backend First**:
   ```bash
   # Commit any final changes
   git add .
   git commit -m "Prepare for production deployment"
   git push origin main
   
   # Deploy to Render (will auto-deploy from main branch)
   ```

2. **Test Backend**:
   ```bash
   # Test health endpoint
   curl https://tidal-streamline-api.onrender.com/health
   
   # Test API endpoint
   curl https://tidal-streamline-api.onrender.com/api/v1/candidates/
   ```

3. **Deploy Frontend**:
   ```bash
   # Update API URL in frontend code
   # Commit and push
   git add .
   git commit -m "Update API URL for production"
   git push origin main
   
   # Deploy to Netlify (will auto-deploy)
   ```

4. **Test Full Integration**:
   - Visit your Netlify URL
   - Create a test payroll calculation
   - Verify data exports work
   - Test all key functionality

---

## 🐛 Troubleshooting

### **Common Issues**:

1. **CORS Errors**:
   - Check CORS_ORIGINS includes your Netlify domain
   - Verify API URL is correct in frontend

2. **Database Connection Issues**:
   - Verify Supabase credentials
   - Check network/firewall settings

3. **Build Failures**:
   - Check dependency versions
   - Verify environment variables
   - Review build logs

4. **API Not Responding**:
   - Check Render logs
   - Verify start command
   - Check health endpoint

---

## 📞 Next Steps After Reading

1. **Review this plan** - any questions or concerns?
2. **Gather credentials** - Supabase keys, OpenAI key, etc.
3. **Set up Render account** if you don't have one
4. **Set up Netlify account** if you don't have one
5. **Execute deployment** following the steps above

**Ready to start the deployment process?** Let me know if you need clarification on any steps or want to begin with Phase 1!

---

*This guide assumes your current repository structure and dependencies. Adjust paths and commands as needed for your specific setup.*