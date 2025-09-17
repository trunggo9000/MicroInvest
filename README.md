# MicroInvest - AI-Powered Investment Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20%2B-FF6F00?logo=tensorflow&logoColor=white)](https://tensorflow.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

**AI-powered** investment platform that helps students and beginners make informed decisions through personalized portfolio recommendations, risk assessment, and goal tracking using **advanced machine learning models.**

https://github.com/user-attachments/assets/a852c334-35a3-4d74-b04a-8ec7bf45c11d

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

### Streamlit App (Enhanced AI Features)
**Requirements:**
- Python 3.10+
- pip
- TensorFlow 2.20+
- scikit-learn

**Setup:**
```bash
# Install all ML dependencies for maximum functionality
pip install -r requirements.txt
pip install tensorflow scikit-learn xgboost lightgbm matplotlib seaborn

# Start enhanced Streamlit app
streamlit run src/streamlit_app/app.py

# Open in browser - Full AI features enabled
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
- **AI/ML:** TensorFlow, scikit-learn, XGBoost, LightGBM, NumPy/Pandas
- **Data Science:** Matplotlib, Seaborn, Plotly for advanced visualizations
- **Machine Learning:** Neural Networks, Random Forest, Gradient Boosting
- **Technical Analysis:** RSI, MACD, Moving Averages, Volatility Analysis
- **Infra:** Docker, GitHub Actions
- **Real-time Features:** Live ML model training, Auto-refresh predictions

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

### Quick Deployment (Streamlit Only)
```bash
# Clone repository
git clone https://github.com/trunggo9000/MicroInvest.git
cd MicroInvest

# Install ML dependencies
pip install -r requirements.txt
pip install tensorflow scikit-learn xgboost lightgbm matplotlib seaborn

# Run with full AI features
streamlit run src/streamlit_app/app.py
```

### Docker Deployment
```bash
# Production build with ML support
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale backend=3
```

### Cloud Deployment Options
**Streamlit Cloud:**
```bash
# Deploy directly from GitHub
# Connect repository: https://github.com/trunggo9000/MicroInvest
# Main file: src/streamlit_app/app.py
# Python version: 3.10+
```

**Heroku/Railway:**
```bash
# Deploy to staging
npm run deploy:staging

# Deploy to production  
npm run deploy:production
```

### Performance Notes
- **ML Models**: TensorFlow training may take 30-60 seconds on first load
- **Memory**: Recommend 2GB+ RAM for full ML functionality
- **Dependencies**: All ML libraries auto-fallback if unavailable

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
