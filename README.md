# Tidal Streamline - Payroll Calculator

Precision Placement for E-Commerce Teams. Increase Output. Save on Payroll. Scale Confidently.

## 🌊 Overview

Tidal Streamline is a powerful payroll calculator for global recruiting, transforming Tidal's manual 2-day analysis into AI-powered salary recommendations delivered in minutes. The system analyzes roles and generates professional market scan reports with accurate salary benchmarks, skills recommendations, and candidate matching across four global regions.

## 🏗️ Architecture

```
tidal-streamline/
├── backend/           # FastAPI + Python (Port 8008)
├── frontend/          # React + Vite + TypeScript (Port 3008)  
├── database/          # Supabase PostgreSQL schema
└── data/             # Historical market scans & benchmarks
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+ and pip
- **Supabase** account and project
- **OpenAI** API key
- **Pinecone** account (optional, for enhanced similarity search)

### 1. Clone & Setup

```bash
cd /path/to/tidal-streamline
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials:
# - SUPABASE_URL=https://your-project.supabase.co
# - SUPABASE_SERVICE_KEY=your_service_key
# - OPENAI_API_KEY=sk-your_openai_key

# Setup database
python scripts/setup_database.py
```

### 3. Database Schema

In your Supabase dashboard, execute the SQL from:
```
database/schema.sql
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Start Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8008
```

### 6. Access Application

- **Frontend**: http://localhost:3008
- **Backend API**: http://localhost:8008
- **API Docs**: http://localhost:8008/docs

## ⚙️ Configuration

### Environment Variables

**Backend (.env)**:
```env
# Server
PORT=8008
DEBUG_MODE=true

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_key

# AI Services  
OPENAI_API_KEY=sk-your_openai_key
OPENAI_MODEL=gpt-4

# Vector Store (Optional)
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_environment
```

**Frontend (.env)**:
```env
VITE_API_BASE_URL=http://localhost:8008
```

## 🎯 Core Features

### 1. AI-Powered Market Scans
- **Job Description Analysis**: OpenAI GPT-4 extracts role requirements, complexity, and regional fit
- **Historical Matching**: Vector similarity search against 200+ previous market scans  
- **Instant Results**: 30-60 second analysis vs 2-day manual process

### 2. Regional Salary Benchmarks
- **Four Global Regions**: United States, Philippines, Latin America, South Africa
- **Experience-Based Ranges**: Junior (2-4yr), Mid (5-8yr), Senior (9+yr) 
- **Cost Savings Analysis**: Up to 71% savings vs US rates
- **Real-Time Recommendations**: Dynamic pricing based on role complexity

### 3. Skills & Tools Mapping
- **Must-Have vs Nice-to-Have**: AI categorization of required vs preferred skills
- **Historical Frequency**: Skills ranked by appearance in similar roles
- **Certification Recommendations**: Relevant certifications for role enhancement

### 4. Candidate Matching
- **50+ Vetted Profiles**: Pre-screened candidates with video introductions
- **Regional Filtering**: Filter by location, timezone, and availability
- **Skills Alignment**: Match candidates to specific role requirements
- **Experience Highlights**: Key strengths and portfolio examples

### 5. Admin Coaching System
- **Performance Analytics**: Track recommendation accuracy and processing times
- **Historical Data Management**: Review and refine past market scans  
- **Quality Metrics**: Confidence scores and success rate monitoring
- **Continuous Improvement**: Retrain recommendation algorithms

## 📊 Data Models

### Market Scans
```sql
market_scans (
  id, client_info, job_details,
  job_analysis (JSONB),
  salary_recommendations (JSONB), 
  skills_recommendations (JSONB),
  status, processing_time, confidence_score
)
```

### Salary Benchmarks
```sql
salary_benchmarks (
  role_category, region, experience_level,
  salary_low, salary_mid, salary_high,
  savings_vs_us, data_source
)
```

### Candidate Profiles
```sql
candidate_profiles (
  name, role_category, region, skills[],
  bio, video_url, hourly_rate, timezone
)
```

## 🔄 API Endpoints

### Market Scans
- `POST /api/v1/market-scans/analyze` - Create new market scan
- `GET /api/v1/market-scans/{id}` - Get scan results
- `GET /api/v1/market-scans/` - List scans with filtering

### Analysis
- `POST /api/v1/analysis/quick` - Quick job analysis  
- `POST /api/v1/analysis/compare` - Compare to historical data
- `GET /api/v1/analysis/role-categories` - Available role categories

### Recommendations  
- `POST /api/v1/recommendations/salary` - Get salary recommendations
- `GET /api/v1/recommendations/skills/{role}` - Skills for role
- `GET /api/v1/recommendations/market-insights/{role}` - Market trends

### Candidates
- `GET /api/v1/candidates` - List candidate profiles
- `GET /api/v1/candidates/for-role/{role}` - Candidates for specific role
- `GET /api/v1/candidates/regions/{region}` - Regional candidate insights

### Admin
- `GET /api/v1/admin/stats` - System statistics
- `GET /api/v1/admin/quality-metrics` - Quality analysis
- `POST /api/v1/admin/retrain-recommendations` - Trigger retraining

## 🎨 Frontend Components

### Client Portal
- **MarketScanForm**: Job details input with validation
- **SalaryAnalysis**: Regional salary comparison display
- **SkillsRecommendations**: Must-have vs nice-to-have matrix
- **CandidateProfiles**: Example candidate showcase

### Admin Dashboard  
- **SystemStats**: Performance metrics and usage analytics
- **DataManagement**: Historical scan review and editing
- **QualityMetrics**: Confidence scores and accuracy tracking

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend  
npm run test
```

### API Testing
```bash
# Health check
curl http://localhost:8008/health

# Create market scan
curl -X POST http://localhost:8008/api/v1/market-scans/analyze \
  -H "Content-Type: application/json" \
  -d '{"client_name":"Test","client_email":"test@example.com",...}'
```

## 📈 Performance Metrics

### Target Performance
- **Analysis Time**: 30-60 seconds per market scan
- **Accuracy Rate**: 85%+ confidence score on recommendations  
- **Cost Savings**: 48-71% vs US salary rates
- **Processing Capacity**: 100+ concurrent scans

### Monitoring
- **Processing Time**: Real-time analysis duration tracking
- **Confidence Scores**: AI recommendation quality metrics
- **Error Rates**: Failed analysis tracking and debugging
- **Usage Analytics**: Client engagement and feature adoption

## 🚢 Deployment

### Production Environment Variables
```env
# Backend
DEBUG_MODE=false
PORT=8008
SUPABASE_URL=https://prod-project.supabase.co
OPENAI_MODEL=gpt-4

# Frontend  
VITE_API_BASE_URL=https://api.tidalstreamline.com
```

### Docker Support (Optional)
```bash
# Build and run with Docker
docker-compose up --build
```

## 🔧 Development

### Code Structure
```
backend/app/
├── api/v1/endpoints/     # FastAPI route handlers
├── core/                 # Configuration, database, AI services
├── models/              # Pydantic data models  
├── services/            # Business logic services
└── scripts/             # Database setup and utilities

frontend/src/
├── components/          # Reusable UI components
├── pages/              # Route-level page components
├── services/           # API client and utilities
└── types/              # TypeScript type definitions
```

### Adding New Features
1. **Backend**: Add endpoint in `api/v1/endpoints/`
2. **Frontend**: Add component and integrate API call
3. **Database**: Update schema.sql if needed
4. **Documentation**: Update README and API docs

## 🐛 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check environment variables
echo $SUPABASE_URL
python scripts/setup_database.py
```

**OpenAI API Errors**  
```bash
# Verify API key and quota
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Frontend Build Issues**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Port Conflicts**
```bash
# Kill conflicting processes
lsof -ti:3008 | xargs kill -9  # Frontend
lsof -ti:8008 | xargs kill -9  # Backend
```

## 📄 License

This project is proprietary to Tidal and Sum Digital Inc.

## 🤝 Support

- **Website**: [hiretidal.com](https://hiretidal.com)
- **Email**: connect@hiretidal.com
- **Documentation**: `/docs` endpoint when running locally

---

**Built with ❤️ by Sum Digital for Tidal's Global Recruiting Excellence**