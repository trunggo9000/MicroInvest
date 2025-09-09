# MicroInvest - AI-Powered Investment Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
MicroInvest is a smart investment platform designed to help students and beginners make informed investment decisions. The platform provides personalized portfolio recommendations, risk assessment, and investment goal tracking using advanced algorithms and rule-based intelligence.

## Project Structure
```
MicroInvest/
├── src/
│   ├── streamlit_app/     # Streamlit web application
│   ├── backend/           # Python backend services
│   ├── frontend/          # React frontend (optional)
│   └── shared/            # Shared utilities
├── config/                # Configuration files
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── pytest.ini
└── tests/                 # Test suites
```

## Local Development

### Streamlit App
**Requirements:**
- Python 3.9+
- pip

**Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start Streamlit app
cd src/streamlit_app
streamlit run app.py

# Open in browser
# http://localhost:8501
```

### Backend Services
**Requirements:**
- Python 3.9+
- PostgreSQL (optional)
- Redis (optional)

**Setup:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start backend services
cd src/backend
python -m uvicorn main:app --reload
```

### Docker Development
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Production Build
```bash
# Build frontend
cd src/frontend && npm run build

# Start production stack
docker-compose -f docker-compose.prod.yml up -d
```

## Tech Stack
- **Frontend:** Streamlit, React, TypeScript, Tailwind CSS
- **Backend:** Python (FastAPI), SQLAlchemy, PostgreSQL
- **AI:** OpenAI GPT-4, scikit-learn, NumPy/Pandas
- **Infra:** Docker, GitHub Actions
- **Visualization:** Plotly, Chart.js

## Environment Variables
Create a `.env` file in the project root:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/microinvest
REDIS_URL=redis://localhost:6379

# API Keys
OPENAI_API_KEY=your-openai-api-key
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key

# Security
JWT_SECRET_KEY=your-jwt-secret
```

## Testing
```bash
# Run all tests
pytest

# Backend tests with coverage
pytest --cov=src/backend --cov-report=html

# Integration tests
pytest tests/test_integration.py -v
```

## API Documentation

### Authentication
```bash
# Register new user
POST /api/auth/register
{
  "email": "investor@example.com",
  "password": "securepassword",
  "name": "John Investor"
}

# Login
POST /api/auth/login
{
  "email": "investor@example.com",
  "password": "securepassword"
}
```

### Portfolio Management
```bash
# Create portfolio
POST /api/portfolio/create
Authorization: Bearer <jwt_token>
{
  "name": "Retirement Portfolio",
  "riskTolerance": "moderate",
  "timeHorizon": 20,
  "monthlyContribution": 1000
}

# Get portfolio analysis
GET /api/portfolio/{portfolio_id}/analysis
Authorization: Bearer <jwt_token>
```

### AI Advisor
```bash
# Get investment advice
POST /api/advisor/recommend
Authorization: Bearer <jwt_token>
{
  "question": "Should I invest in tech stocks?",
  "portfolioContext": { ... },
  "riskProfile": "moderate"
}
```

## Deployment

### Docker Deployment
```bash
# Production build
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale backend=3
```

### Cloud Deployment
```bash
# Deploy to staging
npm run deploy:staging

# Deploy to production
npm run deploy:production
```

## Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Maintain 90%+ test coverage
- Use conventional commits
- Update documentation for new features
