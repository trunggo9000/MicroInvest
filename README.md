# Micro Invest Wise

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-1.x-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

## Project Structure

This project is organized into separate frontend and backend components:

```
Micro/
├── frontend/          # React + Vite frontend application
│   ├── src/          # React source code
│   ├── public/       # Static assets
│   ├── package.json  # Frontend dependencies
│   └── ...           # Frontend config files
├── backend/          # Python Streamlit backend
│   ├── streamlit_app.py
│   └── requirements.txt
├── shared/           # Shared resources
│   ├── supabase/     # Database configuration
│   └── .env          # Environment variables
└── package.json      # Root workspace configuration
```

## Local Development

### Frontend (React app)

Requirements:
- Node.js 18+ and npm 9+

Setup:
```sh
# 1) Install dependencies (from root directory)
npm install

# 2) Start the dev server
npm run dev

# 3) Open the app
# Visit the URL printed in the terminal (typically http://localhost:8080)
```

### Backend (Python Streamlit App)

Requirements:
- Python 3.10+

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
