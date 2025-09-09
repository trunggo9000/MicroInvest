# MicroInvest - AI-Powered Investment Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
MicroInvest is a smart investment platform designed to help students and beginners make informed investment decisions. The platform provides personalized portfolio recommendations, risk assessment, and investment goal tracking using advanced algorithms and rule-based intelligence.

## ✨ Features

- **Smart Recommendations**: Get personalized investment portfolio suggestions based on your risk tolerance and financial goals.
- **Risk Assessment**: Complete a detailed questionnaire to determine your risk profile.
- **Portfolio Analysis**: Visualize your portfolio allocation and performance metrics.
- **Goal Tracking**: Set and track your investment goals with progress visualization.
- **Monte Carlo Simulations**: Project potential portfolio growth with sophisticated simulation models.
- **Educational Resources**: Learn about investing with AI-generated explanations and tips.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/trunggo9000/MicroInvest.git
   cd MicroInvest
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   - The application works without external API keys
   - Database configuration is handled automatically

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run frontend/app.py
   ```

2. **Access the application**
   - Open your browser and navigate to `http://localhost:8501`

## 🏗️ Project Structure

```
MicroInvest/
├── backend/                  # Backend services and logic
│   ├── ai/                  # AI and machine learning components
│   │   └── advisor.py       # AI advisor with GPT integration
│   │
│   ├── database/            # Database models and connections
│   │   └── models.py        # SQLAlchemy models
│   │
│   └── services/            # Business logic services
│       └── investment_engine.py  # Portfolio optimization and simulations
│
├── frontend/                # Streamlit frontend application
│   ├── components/          # Reusable UI components
│   │   ├── header.py        # Application header
│   │   └── sidebar.py       # Navigation sidebar
│   │
│   └── pages/               # Application pages
│       ├── __init__.py      # Page exports
│       ├── welcome.py       # Landing page
│       ├── questionnaire.py # Risk assessment questionnaire
│       ├── portfolio.py     # Portfolio dashboard
│       ├── analysis.py      # Portfolio analysis
│       └── goals.py         # Investment goals tracking
│
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🧠 Smart Advisory System

The application uses rule-based intelligence to provide:
- Personalized investment explanations
- Natural language Q&A about investments
- Scenario analysis and what-if simulations
- Educational content and recommendations

No external API keys required - everything runs locally.

## 📊 Database

The application uses SQLite by default (for development) but can be configured to use PostgreSQL or other databases supported by SQLAlchemy.

To initialize the database:
```bash
python -c "from backend.database.models import init_db; init_db()"
```

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)
- Data visualization with [Plotly](https://plotly.com/python/)

Setup:
```sh
# 1) Create a virtual environment (recommended)
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

# 2) Install Python dependencies
pip install -r backend/requirements.txt

# 3) Run Streamlit backend
npm run backend
# OR directly: cd backend && streamlit run streamlit_app.py
```

The Streamlit app includes:
- DCA Simulator (upload CSV with `date,price` or generate synthetic series)
- Simple ML demo (linear regression on synthetic data)

## Build for Production (React app)
```sh
# Create an optimized build in dist/
npm run build

# (optional) Preview the production build locally
npm run preview
```

## Project Stack
- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS
- Python / Streamlit / Pandas / scikit-learn

## Testing (if applicable)
If you add tests, document how to run them here, e.g.:
```sh
npm test
```

## Deploying (React app)
This project builds to a static bundle in `dist/`. You can deploy it to any static hosting provider or container platform. Typical options:
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront

General steps:
1) Run `npm run build`
2) Upload the contents of `dist/` to your hosting provider

## Environment Variables
If you introduce environment variables (e.g., API keys), create a `.env` file and reference variables via `import.meta.env` in Vite. Do not commit secrets.

## Contributing
- Create a new branch for your change
- Commit with clear, descriptive messages
- Open a pull request
