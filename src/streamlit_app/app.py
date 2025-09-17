import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import sys
import os

# Add backend services to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from services.investment_engine import InvestmentEngine
    from services.market_data_service import MarketDataService
    REAL_DATA_AVAILABLE = True
except ImportError:
    REAL_DATA_AVAILABLE = False
    print("Warning: Real market data services not available, using mock data")

# Import ML components
try:
    from ai.ml_investment_advisor import MLInvestmentAdvisor
    from ai.transaction_analyzer import TransactionAnalyzer
    ML_FEATURES_AVAILABLE = True
    ml_advisor = MLInvestmentAdvisor()
    transaction_analyzer = TransactionAnalyzer()
except ImportError:
    ML_FEATURES_AVAILABLE = False
    print("Warning: ML features not available, using standard recommendations")

# React-style investment options and portfolio generation
INVESTMENT_OPTIONS = [
    {
        "symbol": "VOO",
        "name": "Vanguard S&P 500 ETF",
        "allocation": 0,
        "expectedReturn": 10.5,
        "riskLevel": "low",
        "description": "Tracks the S&P 500 index, providing broad market exposure with low fees. Perfect for long-term growth with reduced volatility."
    },
    {
        "symbol": "VTI", 
        "name": "Vanguard Total Stock Market ETF",
        "allocation": 0,
        "expectedReturn": 10.8,
        "riskLevel": "medium",
        "description": "Invests in the entire U.S. stock market, including small, mid, and large-cap stocks for comprehensive market exposure."
    },
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "allocation": 0,
        "expectedReturn": 12.0,
        "riskLevel": "medium", 
        "description": "Blue-chip technology stock with strong fundamentals and consistent growth. A stable choice for growth-oriented portfolios."
    },
    {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "allocation": 0,
        "expectedReturn": 11.5,
        "riskLevel": "medium",
        "description": "Leading technology company with diversified revenue streams in cloud computing, productivity software, and gaming."
    },
    {
        "symbol": "BND",
        "name": "Vanguard Total Bond Market ETF",
        "allocation": 0,
        "expectedReturn": 4.2,
        "riskLevel": "low",
        "description": "Provides exposure to the entire U.S. investment-grade bond market. Offers stability and income generation."
    },
    {
        "symbol": "QQQ",
        "name": "Invesco QQQ ETF",
        "allocation": 0,
        "expectedReturn": 13.2,
        "riskLevel": "high",
        "description": "Tracks the Nasdaq-100 index, focusing on technology and growth companies. Higher potential returns with increased volatility."
    }
]

def generate_react_style_portfolio(monthly_budget, risk_tolerance, time_horizon, investment_goal):
    """Generate portfolio recommendation using ML or fallback to mock data."""
    
    # Try ML-powered recommendation first
    if ML_FEATURES_AVAILABLE:
        try:
            # Create user profile for ML analysis
            user_profile = {
                'monthly_investment': monthly_budget,
                'risk_tolerance': risk_tolerance,
                'time_horizon': time_horizon,
                'investment_goal': investment_goal,
                'age': st.session_state.get('user_age', 25),
                'monthly_income': st.session_state.get('user_income', monthly_budget * 10),
                'investment_experience': st.session_state.get('user_experience', 'Beginner')
            }
            
            # Generate ML-powered allocation
            allocation = ml_advisor.predict_optimal_allocation(user_profile, pd.DataFrame())
            
            # Predict returns using ML
            market_conditions = {'volatility': 0.15, 'interest_rate': 0.05, 'inflation': 0.03}
            return_prediction = ml_advisor.predict_investment_returns(allocation, market_conditions)
            
            # Convert to expected format
            return _convert_ml_to_portfolio_format(allocation, return_prediction, user_profile)
            
        except Exception as e:
            st.warning(f"ML recommendation failed: {e}. Using fallback method.")
            return _generate_mock_portfolio(monthly_budget, risk_tolerance, time_horizon, investment_goal)
    
    # Fallback to original logic
    if REAL_DATA_AVAILABLE:
        try:
            market_service = MarketDataService()
            investment_engine = InvestmentEngine(market_service)
            
            portfolio = investment_engine.generate_portfolio_recommendation(
                monthly_investment=monthly_budget,
                risk_tolerance=risk_tolerance,
                time_horizon=time_horizon,
                investment_goal=investment_goal
            )
            
            return portfolio
            
        except Exception as e:
            st.warning(f"Unable to fetch real market data: {e}. Using fallback data.")
            return _generate_mock_portfolio(monthly_budget, risk_tolerance, time_horizon, investment_goal)
    else:
        return _generate_mock_portfolio(monthly_budget, risk_tolerance, time_horizon, investment_goal)

def _convert_ml_to_portfolio_format(allocation, return_prediction, user_profile):
    """Convert ML predictions to portfolio format expected by the app."""
    # Map ML allocation to specific investments
    stocks_allocation = allocation.get('stocks', 0.6)
    bonds_allocation = allocation.get('bonds', 0.3)
    alternatives_allocation = allocation.get('alternatives', 0.1)
    
    # Create investment list based on ML allocation
    selected_investments = []
    
    if stocks_allocation > 0:
        # Split stock allocation between growth and conservative
        if "Growth" in user_profile.get('risk_tolerance', ''):
            selected_investments.extend([
                {"symbol": "QQQ", "name": "Invesco QQQ ETF", "allocation": stocks_allocation * 0.4, 
                 "expectedReturn": 13.2, "riskLevel": "high", "description": "Technology-focused growth ETF"},
                {"symbol": "VOO", "name": "Vanguard S&P 500 ETF", "allocation": stocks_allocation * 0.6, 
                 "expectedReturn": 10.5, "riskLevel": "medium", "description": "Broad market exposure"}
            ])
        else:
            selected_investments.append({
                "symbol": "VOO", "name": "Vanguard S&P 500 ETF", "allocation": stocks_allocation, 
                "expectedReturn": 10.5, "riskLevel": "medium", "description": "Broad market S&P 500 exposure"
            })
    
    if bonds_allocation > 0:
        selected_investments.append({
            "symbol": "BND", "name": "Vanguard Total Bond Market ETF", "allocation": bonds_allocation,
            "expectedReturn": 4.2, "riskLevel": "low", "description": "Broad bond market exposure"
        })
    
    if alternatives_allocation > 0:
        selected_investments.append({
            "symbol": "VNQ", "name": "Vanguard Real Estate ETF", "allocation": alternatives_allocation,
            "expectedReturn": 9.1, "riskLevel": "medium", "description": "Real estate investment exposure"
        })
    
    # Calculate time horizon in years
    time_horizon_str = user_profile.get('time_horizon', '5+ years')
    years = 5  # Default
    if "3 months" in time_horizon_str:
        years = 0.25
    elif "6 months" in time_horizon_str:
        years = 0.5
    elif "1 year" in time_horizon_str:
        years = 1
    elif "2 years" in time_horizon_str:
        years = 2
    elif "5+ years" in time_horizon_str:
        years = 5
    
    # Calculate projected value using ML-predicted returns
    monthly_budget = user_profile.get('monthly_investment', 100)
    expected_return = return_prediction.get('expected_annual_return', 0.08)
    
    monthly_return = expected_return / 12
    months = years * 12
    
    if years < 1:
        projected_value = monthly_budget * months * (1 + expected_return * years)
    elif monthly_return > 0:
        projected_value = monthly_budget * (((1 + monthly_return) ** months - 1) / monthly_return)
    else:
        projected_value = monthly_budget * months
    
    return {
        "monthlyAmount": monthly_budget,
        "investments": selected_investments,
        "totalExpectedReturn": expected_return * 100,
        "projectedValue": projected_value,
        "timeHorizon": years,
        "riskTolerance": user_profile.get('risk_tolerance', 'Balanced'),
        "investmentGoal": user_profile.get('investment_goal', 'Build Long-term Wealth'),
        "volatility": return_prediction.get('volatility', 0.12) * 100,
        "sharpeRatio": return_prediction.get('sharpe_ratio', 0.5),
        "maxDrawdown": -15.0,  # Default value
        "portfolioMetrics": {
            "annual_return": expected_return,
            "annual_volatility": return_prediction.get('volatility', 0.12),
            "sharpe_ratio": return_prediction.get('sharpe_ratio', 0.5),
            "max_drawdown": -0.15
        },
        "ml_confidence": allocation.get('confidence_score', 0.7),
        "ml_reasoning": allocation.get('reasoning', 'ML-optimized allocation based on your profile')
    }

def _generate_mock_portfolio(monthly_budget, risk_tolerance, time_horizon, investment_goal):
    """Generate mock portfolio as fallback when real data is unavailable."""
    
    # Select investments based on risk tolerance
    if "Conservative" in risk_tolerance:
        selected_investments = [
            {"symbol": "BND", "name": "Vanguard Total Bond Market ETF", "allocation": 0.4, "expectedReturn": 4.2, "riskLevel": "low", "description": "Broad bond market exposure with low volatility"},
            {"symbol": "VGIT", "name": "Vanguard Intermediate-Term Treasury ETF", "allocation": 0.3, "expectedReturn": 3.8, "riskLevel": "low", "description": "Government bonds with stable returns"},
            {"symbol": "VOO", "name": "Vanguard S&P 500 ETF", "allocation": 0.2, "expectedReturn": 10.5, "riskLevel": "medium", "description": "Large-cap US stocks for growth potential"},
            {"symbol": "VTIAX", "name": "Vanguard Total International Stock Index", "allocation": 0.1, "expectedReturn": 8.2, "riskLevel": "medium", "description": "International diversification"}
        ]
        total_expected_return = 7.8
        volatility = 8.5
        sharpe_ratio = 0.65
        max_drawdown = -12.3
    elif "Balanced" in risk_tolerance:
        selected_investments = [
            {"symbol": "VOO", "name": "Vanguard S&P 500 ETF", "allocation": 0.4, "expectedReturn": 10.5, "riskLevel": "medium", "description": "Large-cap US stocks for growth potential"},
            {"symbol": "VTIAX", "name": "Vanguard Total International Stock Index", "allocation": 0.2, "expectedReturn": 8.2, "riskLevel": "medium", "description": "International diversification"},
            {"symbol": "BND", "name": "Vanguard Total Bond Market ETF", "allocation": 0.3, "expectedReturn": 4.2, "riskLevel": "low", "description": "Broad bond market exposure with low volatility"},
            {"symbol": "VNQ", "name": "Vanguard Real Estate ETF", "allocation": 0.1, "expectedReturn": 9.1, "riskLevel": "high", "description": "Real estate investment exposure"}
        ]
        total_expected_return = 9.8
        volatility = 12.4
        sharpe_ratio = 0.75
        max_drawdown = -18.7
    else:  # Growth-Focused
        selected_investments = [
            {"symbol": "VOO", "name": "Vanguard S&P 500 ETF", "allocation": 0.4, "expectedReturn": 10.5, "riskLevel": "medium", "description": "Large-cap US stocks for growth potential"},
            {"symbol": "VGT", "name": "Vanguard Information Technology ETF", "allocation": 0.3, "expectedReturn": 15.2, "riskLevel": "high", "description": "Technology sector growth exposure"},
            {"symbol": "VWO", "name": "Vanguard Emerging Markets ETF", "allocation": 0.2, "expectedReturn": 11.8, "riskLevel": "high", "description": "Emerging markets growth potential"},
            {"symbol": "VNQ", "name": "Vanguard Real Estate ETF", "allocation": 0.1, "expectedReturn": 9.1, "riskLevel": "high", "description": "Real estate investment exposure"}
        ]
        total_expected_return = 12.1
        volatility = 16.8
        sharpe_ratio = 0.68
        max_drawdown = -25.4
    
    # Calculate time horizon in years
    years = 10  # Default
    if "3 months" in time_horizon:
        years = 0.25  # 3 months
    elif "6 months" in time_horizon:
        years = 0.5  # 6 months
    elif "1 year" in time_horizon:
        years = 1  # 1 year
    elif "2 years" in time_horizon:
        years = 2  # 2 years
    elif "5+ years" in time_horizon:
        years = 5  # 5+ years
    elif "1-2 years" in time_horizon:
        years = 1.5
    elif "3-5 years" in time_horizon:
        years = 4
    elif "5-10 years" in time_horizon:
        years = 7
    elif "10+ years" in time_horizon:
        years = 15
    
    # Calculate projected value using compound interest with monthly contributions
    monthly_return = total_expected_return / 100 / 12
    months = years * 12
    
    # For very short time horizons (less than 1 year), use simple calculation
    if years < 1:
        # For short-term, minimal compound growth - mostly just contributions
        projected_value = monthly_budget * months * (1 + (total_expected_return / 100) * years)
    elif monthly_return > 0:
        # Future value of annuity formula for longer terms
        projected_value = monthly_budget * (((1 + monthly_return) ** months - 1) / monthly_return)
    else:
        projected_value = monthly_budget * months
    
    return {
        "monthlyAmount": monthly_budget,
        "investments": selected_investments,
        "totalExpectedReturn": total_expected_return,
        "projectedValue": projected_value,
        "timeHorizon": years,
        "riskTolerance": risk_tolerance,
        "investmentGoal": investment_goal,
        "volatility": volatility,
        "sharpeRatio": sharpe_ratio,
        "maxDrawdown": max_drawdown,
        "portfolioMetrics": {
            "annual_return": total_expected_return / 100,
            "annual_volatility": volatility / 100,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown / 100
        }
    }

# Page configuration
st.set_page_config(
    page_title="MicroInvest - AI Investment Planner",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'

# Main app navigation
def main():
    """Main application with navigation."""
    # Sidebar navigation
    st.sidebar.title("🤖 MicroInvest AI")
    st.sidebar.markdown("---")
    
    # Navigation buttons
    if st.sidebar.button("🏠 Welcome", use_container_width=True):
        st.session_state.current_page = 'welcome'
        st.rerun()
    
    if st.sidebar.button("📋 Investment Profile", use_container_width=True):
        st.session_state.current_page = 'questionnaire'
        st.rerun()
    
    if st.sidebar.button("📊 Portfolio", use_container_width=True):
        st.session_state.current_page = 'portfolio'
        st.rerun()
    
    if st.sidebar.button("🔮 AI Predictor", use_container_width=True):
        st.session_state.current_page = 'predictor'
        st.rerun()
    
    if st.sidebar.button("📈 Analysis", use_container_width=True):
        st.session_state.current_page = 'analysis'
        st.rerun()
    
    if st.sidebar.button("🎯 Goals", use_container_width=True):
        st.session_state.current_page = 'goals'
        st.rerun()
    
    if st.sidebar.button("📈 Stocks", use_container_width=True):
        st.session_state.current_page = 'stocks'
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Show current portfolio summary if available
    portfolio_data = st.session_state.get('portfolio_data', {})
    if portfolio_data:
        st.sidebar.markdown("### 📈 Current Portfolio")
        st.sidebar.metric("Monthly Investment", f"${portfolio_data.get('monthlyAmount', 0)}")
        st.sidebar.metric("Expected Return", f"{portfolio_data.get('totalExpectedReturn', 0):.1f}%")
        st.sidebar.metric("Projected Value", f"${portfolio_data.get('projectedValue', 0):,.2f}")
    
    # Display current page
    if st.session_state.current_page == 'welcome':
        show_welcome_page()
    elif st.session_state.current_page == 'questionnaire':
        show_questionnaire_page()
    elif st.session_state.current_page == 'portfolio':
        show_portfolio_page()
    elif st.session_state.current_page == 'predictor':
        show_predictor_page()
    elif st.session_state.current_page == 'analysis':
        show_analysis_page()
    elif st.session_state.current_page == 'goals':
        show_goals_page()
    elif st.session_state.current_page == 'stocks':
        show_stocks_page()

def show_welcome_page():
    """Display the welcome page with investment features."""
    # Hero section with enhanced styling and prominent CTA button
    st.markdown("""
    <div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
        <div style='background: rgba(255,255,255,0.15); display: inline-block; padding: 0.75rem 1.5rem; border-radius: 25px; margin-bottom: 1.5rem; backdrop-filter: blur(10px);'>
            🤖 AI-Powered Investment Advisor
        </div>
        <h1 style='font-size: 3.5rem; margin: 1.5rem 0; color: white; font-weight: 700; line-height: 1.2;'>Start Investing with <span style='color: #4CAF50; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>Just $10</span></h1>
        <p style='font-size: 1.3rem; margin: 1.5rem 0; opacity: 0.95; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.6;'>Get personalized, data-driven investment recommendations designed specifically for students. Build wealth with micro-investments that fit your budget and risk tolerance.</p>
    """, unsafe_allow_html=True)
    
    # Main CTA button - Centered
    st.markdown('<div class="main-content" style="text-align: center;">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 GET MY INVESTMENT PLAN", key="main_cta", help="Start your personalized investment journey"):
            st.session_state.current_page = "questionnaire"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Button styling - Force apply to main button
    st.markdown("""
    <style>
    /* Target the main button more specifically */
    div[data-testid="stButton"] > button[key="main_cta"],
    .main-content div[data-testid="stButton"] > button,
    div.main-content button {
        width: 100% !important;
        height: 150px !important;
        font-size: 48px !important;
        font-weight: bold !important;
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 75px !important;
        box-shadow: 0 30px 60px rgba(220, 53, 69, 0.7) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 6px !important;
        margin: 4rem auto !important;
        display: block !important;
    }
    
    div[data-testid="stButton"] > button[key="main_cta"]:hover,
    .main-content div[data-testid="stButton"] > button:hover,
    div.main-content button:hover {
        transform: translateY(-12px) !important;
        box-shadow: 0 40px 80px rgba(220, 53, 69, 0.9) !important;
        background: linear-gradient(135deg, #c82333 0%, #a71e2a 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Enhanced key benefits with icons and animations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 2.5rem 1.5rem; background: linear-gradient(145deg, #f8f9fa, #e9ecef); border-radius: 15px; margin: 1rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.8); transition: transform 0.3s ease;' onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
            <div style='background: linear-gradient(135deg, #28a745, #20c997); color: white; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; font-size: 2rem; box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);'>🛡️</div>
            <h3 style='color: #2c3e50; margin-bottom: 1rem; font-weight: 600; font-size: 1.2rem;'>Low-Risk Focus</h3>
            <p style='color: #6c757d; font-size: 0.95rem; line-height: 1.5;'>Conservative strategies prioritizing capital preservation and steady growth</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2.5rem 1.5rem; background: linear-gradient(145deg, #f8f9fa, #e9ecef); border-radius: 15px; margin: 1rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.8); transition: transform 0.3s ease;' onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
            <div style='background: linear-gradient(135deg, #007bff, #6610f2); color: white; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; font-size: 2rem; box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);'>📊</div>
            <h3 style='color: #2c3e50; margin-bottom: 1rem; font-weight: 600; font-size: 1.2rem;'>Data-Driven</h3>
            <p style='color: #6c757d; font-size: 0.95rem; line-height: 1.5;'>ML-powered recommendations based on historical market data and trends</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 2.5rem 1.5rem; background: linear-gradient(145deg, #f8f9fa, #e9ecef); border-radius: 15px; margin: 1rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.8); transition: transform 0.3s ease;' onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
            <div style='background: linear-gradient(135deg, #ffc107, #fd7e14); color: white; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; font-size: 2rem; box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);'>💰</div>
            <h3 style='color: #2c3e50; margin-bottom: 1rem; font-weight: 600; font-size: 1.2rem;'>Micro-Investing</h3>
            <p style='color: #6c757d; font-size: 0.95rem; line-height: 1.5;'>Start with small amounts and build your portfolio gradually over time</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    
    # Sample portfolio visualization
    st.markdown("## 📈 Sample Portfolio Growth")
    
    # Generate sample data
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='M')
    np.random.seed(42)
    portfolio_values = [10000]
    
    for i in range(len(dates)-1):
        monthly_return = np.random.normal(0.007, 0.04)  # ~8% annual return with volatility
        new_value = portfolio_values[-1] * (1 + monthly_return) + 100  # Add $100 monthly
        portfolio_values.append(new_value)
    
    df = pd.DataFrame({
        'Date': dates[:len(portfolio_values)],
        'Portfolio Value': portfolio_values
    })
    
    fig = px.area(df, x='Date', y='Portfolio Value', 
                  title="Sample 5-Year Investment Growth ($100/month)")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional call to action (secondary)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Your Investment Journey", type="secondary", use_container_width=True, help="Begin your personalized investment plan", key="secondary_cta"):
            st.session_state.current_page = "questionnaire"
            st.rerun()
    
    # Disclaimer with better styling
    st.markdown("""
    <div style='text-align: center; margin-top: 3rem; padding: 1.5rem; background: rgba(108, 117, 125, 0.05); border-radius: 10px; border-left: 4px solid #6c757d;'>
        <p style='font-size: 0.85rem; color: #6c757d; margin: 0; line-height: 1.5;'>
            **Disclaimer:** This tool provides educational guidance and general investment suggestions. 
            Always consult with a financial advisor for personalized advice. 
            Past performance doesn't guarantee future results.
        </p>
    </div>
    """, unsafe_allow_html=True)

def _generate_mock_transactions_from_input(food_spending, transport_spending, entertainment_spending, shopping_spending):
    """Generate mock transaction data from user spending input for ML analysis."""
    transactions = []
    
    # Generate transactions for each category
    categories = [
        ('Food and Drink', food_spending, 15),
        ('Transportation', transport_spending, 8), 
        ('Entertainment', entertainment_spending, 10),
        ('Shopping', shopping_spending, 12)
    ]
    
    for category, monthly_amount, num_transactions in categories:
        if monthly_amount > 0:
            # Distribute spending across transactions
            amounts = np.random.dirichlet(np.ones(num_transactions)) * monthly_amount
            
            for i, amount in enumerate(amounts):
                transactions.append({
                    'transaction_id': f'input_{category}_{i:03d}',
                    'account_id': 'user_input_account',
                    'amount': amount,
                    'date': datetime.now() - timedelta(days=np.random.randint(0, 30)),
                    'name': f'{category} Transaction {i+1}',
                    'merchant_name': f'{category} Merchant {i%3+1}',
                    'category': category,
                    'subcategory': 'general',
                    'account_owner': 'user'
                })
    
    # Add some income transactions
    for i in range(2):
        transactions.append({
            'transaction_id': f'income_{i:03d}',
            'account_id': 'user_input_account',
            'amount': -(food_spending + transport_spending + entertainment_spending + shopping_spending) * 0.6,  # Negative for income
            'date': datetime.now() - timedelta(days=np.random.randint(0, 30)),
            'name': f'Income Deposit {i+1}',
            'merchant_name': 'Employer',
            'category': 'Transfer',
            'subcategory': 'income',
            'account_owner': 'user'
        })
    
    return pd.DataFrame(transactions)

def show_predictor_page():
    """Dedicated AI Predictor dashboard with interactive ML predictions."""
    st.title("🔮 AI Investment Predictor")
    st.markdown("*Advanced machine learning predictions for investment optimization*")
    
    # Check if ML features are available
    if not ML_FEATURES_AVAILABLE:
        st.warning("⚠️ ML features are not fully available. Install required dependencies for full functionality.")
        st.code("pip install scikit-learn tensorflow xgboost lightgbm")
    
    # Prediction tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Portfolio Optimizer", "📈 Market Predictor", "💰 Investment Calculator", "🎯 Risk Analyzer"])
    
    with tab1:
        show_portfolio_optimizer()
    
    with tab2:
        show_market_predictor()
    
    with tab3:
        show_investment_calculator()
    
    with tab4:
        show_risk_analyzer()

def show_portfolio_optimizer():
    """Interactive portfolio optimization using ML with TensorFlow visualizations."""
    st.markdown("### 🤖 AI Portfolio Optimizer")
    st.markdown("*Get ML-powered portfolio allocation recommendations with real-time analysis*")
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Personal Profile**")
        age = st.slider("Age", 18, 65, 25)
        income = st.number_input("Monthly Income ($)", 500, 10000, 2000, step=100)
        investment_amount = st.number_input("Monthly Investment ($)", 10, 2000, 200, step=10)
        
    with col2:
        st.markdown("**Investment Preferences**")
        risk_level = st.selectbox("Risk Tolerance", ["Conservative", "Balanced", "Growth-Focused", "Aggressive"])
        time_horizon = st.selectbox("Time Horizon", ["1 year", "2-3 years", "5+ years", "10+ years"])
        goal = st.selectbox("Investment Goal", ["Emergency Fund", "Retirement", "House Down Payment", "Education", "Wealth Building"])
    
    # Real-time prediction toggle
    real_time = st.checkbox("🔄 Enable Real-time Predictions", value=False)
    
    if st.button("🧠 Generate AI Prediction", type="primary", use_container_width=True) or real_time:
        with st.spinner("🤖 AI is analyzing optimal portfolio allocation with TensorFlow..."):
            # Create user profile for ML
            user_profile = {
                'age': age,
                'monthly_income': income,
                'monthly_investment': investment_amount,
                'risk_tolerance': risk_level,
                'time_horizon': time_horizon,
                'investment_goal': goal,
                'investment_experience': 'Intermediate'
            }
            
            # Generate synthetic training data for TensorFlow model
            np.random.seed(42)
            n_samples = 1000
            
            # Create features: age, income, investment_amount, risk_score, time_score
            risk_scores = {"Conservative": 1, "Balanced": 2, "Growth-Focused": 3, "Aggressive": 4}
            time_scores = {"1 year": 1, "2-3 years": 2, "5+ years": 3, "10+ years": 4}
            
            features = np.random.rand(n_samples, 5)
            features[:, 0] = np.random.uniform(18, 65, n_samples)  # age
            features[:, 1] = np.random.uniform(500, 10000, n_samples)  # income
            features[:, 2] = np.random.uniform(10, 2000, n_samples)  # investment
            features[:, 3] = np.random.uniform(1, 4, n_samples)  # risk score
            features[:, 4] = np.random.uniform(1, 4, n_samples)  # time score
            
            # Generate target allocations (stocks, bonds, alternatives)
            targets = np.zeros((n_samples, 3))
            for i in range(n_samples):
                risk_factor = features[i, 3] / 4.0
                time_factor = features[i, 4] / 4.0
                age_factor = 1 - (features[i, 0] - 18) / 47.0
                
                stocks = 0.3 + 0.5 * risk_factor * age_factor * time_factor
                bonds = 0.5 - 0.3 * risk_factor
                alternatives = 1 - stocks - bonds
                
                targets[i] = [stocks, bonds, max(0, alternatives)]
                targets[i] = targets[i] / targets[i].sum()  # normalize
            
            # Create and train TensorFlow model (simplified for demo)
            try:
                import tensorflow as tf
                from sklearn.preprocessing import StandardScaler
                from sklearn.ensemble import RandomForestRegressor
                from sklearn.model_selection import train_test_split
                
                # Normalize features
                scaler = StandardScaler()
                features_scaled = scaler.fit_transform(features)
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(features_scaled, targets, test_size=0.2, random_state=42)
                
                # Simple TensorFlow model
                model = tf.keras.Sequential([
                    tf.keras.layers.Dense(64, activation='relu', input_shape=(5,)),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Dense(32, activation='relu'),
                    tf.keras.layers.Dense(3, activation='softmax')
                ])
                
                model.compile(optimizer='adam', loss='mse', metrics=['mae', 'accuracy'])
                
                # Train model (quick training for demo)
                history = model.fit(X_train, y_train, epochs=50, batch_size=32, 
                                  validation_split=0.2, verbose=0)
                
                # Predict for current user
                user_features = np.array([[
                    age, income, investment_amount, 
                    risk_scores[risk_level], time_scores[time_horizon]
                ]])
                user_features_scaled = scaler.transform(user_features)
                prediction = model.predict(user_features_scaled, verbose=0)[0]
                
                allocation = {
                    'stocks': prediction[0],
                    'bonds': prediction[1], 
                    'alternatives': prediction[2],
                    'confidence_score': 0.85
                }
                
                # Also use scikit-learn for comparison
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                rf_model.fit(X_train, y_train)
                rf_prediction = rf_model.predict(user_features_scaled)[0]
                
                returns = {
                    'expected_annual_return': 0.06 + 0.08 * prediction[0],
                    'volatility': 0.08 + 0.15 * prediction[0],
                    'sharpe_ratio': (0.06 + 0.08 * prediction[0]) / (0.08 + 0.15 * prediction[0])
                }
                
                ML_AVAILABLE = True
                
            except ImportError:
                # Fallback prediction
                allocation = {'stocks': 0.6, 'bonds': 0.3, 'alternatives': 0.1, 'confidence_score': 0.7}
                returns = {'expected_annual_return': 0.08, 'volatility': 0.12, 'sharpe_ratio': 0.5}
                ML_AVAILABLE = False
                history = None
                rf_prediction = None
            
            # Display results
            st.success("✅ AI Analysis Complete!")
            
            # Allocation metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Stocks Allocation", f"{allocation.get('stocks', 0.6)*100:.1f}%")
            with col2:
                st.metric("Bonds Allocation", f"{allocation.get('bonds', 0.3)*100:.1f}%")
            with col3:
                st.metric("Alternatives", f"{allocation.get('alternatives', 0.1)*100:.1f}%")
            
            # Performance metrics
            st.markdown("### 📈 Expected Performance")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Expected Return", f"{returns.get('expected_annual_return', 0.08)*100:.1f}%")
            with col2:
                st.metric("Volatility", f"{returns.get('volatility', 0.12)*100:.1f}%")
            with col3:
                st.metric("Sharpe Ratio", f"{returns.get('sharpe_ratio', 0.5):.2f}")
            
            # AI confidence
            confidence = allocation.get('confidence_score', 0.7)
            st.info(f"🤖 **AI Confidence:** {confidence:.1%} - Portfolio optimized using TensorFlow neural network")
            
            # Visualizations using matplotlib and pandas
            if ML_AVAILABLE:
                st.markdown("### 📊 AI Model Data Visualizations")
                
                # Portfolio allocation pie chart with matplotlib
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**TensorFlow Model Allocation**")
                    fig, ax = plt.subplots(figsize=(8, 6))
                    labels = ['Stocks', 'Bonds', 'Alternatives']
                    sizes = [allocation['stocks']*100, allocation['bonds']*100, allocation['alternatives']*100]
                    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
                    
                    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                                                     startangle=90, textprops={'fontsize': 10})
                    ax.set_title('AI-Optimized Portfolio Allocation', fontsize=14, fontweight='bold')
                    
                    # Add data table
                    allocation_df = pd.DataFrame({
                        'Asset Class': labels,
                        'Allocation (%)': [f"{x:.1f}%" for x in sizes],
                        'Monthly Amount ($)': [f"${investment_amount * x/100:.2f}" for x in sizes]
                    })
                    
                    st.pyplot(fig)
                    st.dataframe(allocation_df, use_container_width=True)
                
                with col2:
                    if rf_prediction is not None:
                        st.markdown("**Model Comparison Analysis**")
                        
                        # Create comparison DataFrame
                        comparison_df = pd.DataFrame({
                            'TensorFlow': [allocation['stocks']*100, allocation['bonds']*100, allocation['alternatives']*100],
                            'Random Forest': [rf_prediction[0]*100, rf_prediction[1]*100, rf_prediction[2]*100]
                        }, index=['Stocks', 'Bonds', 'Alternatives'])
                        
                        # Matplotlib bar chart
                        fig, ax = plt.subplots(figsize=(8, 6))
                        comparison_df.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
                        ax.set_title('ML Model Predictions Comparison', fontsize=14, fontweight='bold')
                        ax.set_ylabel('Allocation (%)')
                        ax.set_xlabel('Asset Classes')
                        ax.legend(title='Models')
                        ax.grid(True, alpha=0.3)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        
                        st.pyplot(fig)
                        st.dataframe(comparison_df.round(2), use_container_width=True)
                
                # Training history with matplotlib
                if history is not None:
                    st.markdown("**TensorFlow Model Training Progress**")
                    
                    # Create training history DataFrame
                    history_df = pd.DataFrame({
                        'Epoch': range(1, len(history.history['loss']) + 1),
                        'Training Loss': history.history['loss'],
                        'Validation Loss': history.history.get('val_loss', [0] * len(history.history['loss'])),
                        'Training MAE': history.history.get('mae', [0] * len(history.history['loss'])),
                        'Validation MAE': history.history.get('val_mae', [0] * len(history.history['loss']))
                    })
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Loss plot
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.plot(history_df['Epoch'], history_df['Training Loss'], 'b-', label='Training Loss', linewidth=2)
                        ax.plot(history_df['Epoch'], history_df['Validation Loss'], 'r-', label='Validation Loss', linewidth=2)
                        ax.set_title('Model Training Loss', fontsize=12, fontweight='bold')
                        ax.set_xlabel('Epoch')
                        ax.set_ylabel('Loss')
                        ax.legend()
                        ax.grid(True, alpha=0.3)
                        st.pyplot(fig)
                    
                    with col2:
                        # MAE plot
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.plot(history_df['Epoch'], history_df['Training MAE'], 'g-', label='Training MAE', linewidth=2)
                        ax.plot(history_df['Epoch'], history_df['Validation MAE'], 'orange', label='Validation MAE', linewidth=2)
                        ax.set_title('Model Training MAE', fontsize=12, fontweight='bold')
                        ax.set_xlabel('Epoch')
                        ax.set_ylabel('MAE')
                        ax.legend()
                        ax.grid(True, alpha=0.3)
                        st.pyplot(fig)
                    
                    # Show training statistics
                    st.markdown("**Training Statistics**")
                    final_stats = pd.DataFrame({
                        'Metric': ['Final Training Loss', 'Final Validation Loss', 'Final Training MAE', 'Final Validation MAE'],
                        'Value': [
                            f"{history.history['loss'][-1]:.4f}",
                            f"{history.history.get('val_loss', [0])[-1]:.4f}",
                            f"{history.history.get('mae', [0])[-1]:.4f}",
                            f"{history.history.get('val_mae', [0])[-1]:.4f}"
                        ]
                    })
                    st.dataframe(final_stats, use_container_width=True)
                
                # Risk-Return analysis with matplotlib and pandas
                st.markdown("**Risk-Return Analysis Dashboard**")
                
                # Generate risk-return data
                risk_levels = np.linspace(0.05, 0.25, 50)
                returns_sim = []
                sharpe_ratios = []
                
                for risk in risk_levels:
                    stock_alloc = min(1.0, risk * 4)
                    expected_return = 0.04 + stock_alloc * 0.08
                    sharpe = (expected_return - 0.02) / risk  # Risk-free rate = 2%
                    returns_sim.append(expected_return)
                    sharpe_ratios.append(sharpe)
                
                # Create efficient frontier DataFrame
                frontier_df = pd.DataFrame({
                    'Risk (Volatility %)': risk_levels * 100,
                    'Expected Return (%)': np.array(returns_sim) * 100,
                    'Sharpe Ratio': sharpe_ratios
                })
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Efficient frontier plot
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.plot(frontier_df['Risk (Volatility %)'], frontier_df['Expected Return (%)'], 
                           'b-', linewidth=2, label='Efficient Frontier')
                    
                    # Plot user's portfolio
                    user_risk = returns['volatility'] * 100
                    user_return = returns['expected_annual_return'] * 100
                    ax.scatter([user_risk], [user_return], color='red', s=100, zorder=5, 
                              label='Your Portfolio', marker='*')
                    
                    ax.set_title('Risk-Return Efficient Frontier', fontsize=12, fontweight='bold')
                    ax.set_xlabel('Risk (Volatility %)')
                    ax.set_ylabel('Expected Return (%)')
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                
                with col2:
                    # Sharpe ratio analysis
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.plot(frontier_df['Risk (Volatility %)'], frontier_df['Sharpe Ratio'], 
                           'g-', linewidth=2, label='Sharpe Ratio')
                    
                    # Highlight optimal Sharpe ratio
                    max_sharpe_idx = frontier_df['Sharpe Ratio'].idxmax()
                    optimal_risk = frontier_df.loc[max_sharpe_idx, 'Risk (Volatility %)']
                    optimal_sharpe = frontier_df.loc[max_sharpe_idx, 'Sharpe Ratio']
                    
                    ax.scatter([optimal_risk], [optimal_sharpe], color='red', s=100, zorder=5,
                              label=f'Optimal Sharpe: {optimal_sharpe:.2f}', marker='o')
                    
                    ax.set_title('Sharpe Ratio Analysis', fontsize=12, fontweight='bold')
                    ax.set_xlabel('Risk (Volatility %)')
                    ax.set_ylabel('Sharpe Ratio')
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                
                # Portfolio performance metrics table
                st.markdown("**Portfolio Performance Metrics**")
                metrics_df = pd.DataFrame({
                    'Metric': ['Expected Annual Return', 'Annual Volatility', 'Sharpe Ratio', 'Max Drawdown', 'AI Confidence'],
                    'Your Portfolio': [
                        f"{returns['expected_annual_return']*100:.2f}%",
                        f"{returns['volatility']*100:.2f}%", 
                        f"{returns['sharpe_ratio']:.2f}",
                        "-15.00%",  # Placeholder
                        f"{confidence:.1%}"
                    ],
                    'Benchmark (S&P 500)': ["10.50%", "16.00%", "0.53", "-20.00%", "N/A"]
                })
                st.dataframe(metrics_df, use_container_width=True)

def show_market_predictor():
    """Market trend prediction using ML with real-time data and TensorFlow models."""
    st.markdown("### 📈 AI Market Trend Predictor")
    st.markdown("*Real-time machine learning analysis with TensorFlow and scikit-learn*")
    
    # Market analysis controls
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_period = st.selectbox("Analysis Period", ["1 Month", "3 Months", "6 Months", "1 Year"])
        market_sector = st.selectbox("Market Sector", ["Overall Market", "Technology", "Healthcare", "Finance", "Energy"])
    
    with col2:
        prediction_horizon = st.selectbox("Prediction Horizon", ["1 Week", "1 Month", "3 Months", "6 Months"])
        confidence_threshold = st.slider("Confidence Threshold", 0.5, 0.95, 0.75, 0.05)
    
    # Real-time updates
    auto_refresh = st.checkbox("🔄 Auto-refresh predictions", value=False)
    
    if st.button("🔮 Predict Market Trends", type="primary", use_container_width=True) or auto_refresh:
        with st.spinner("🤖 AI is analyzing market data with TensorFlow and scikit-learn..."):
            
            # Generate synthetic market data for demonstration
            np.random.seed(int(pd.Timestamp.now().timestamp()) % 1000)
            
            # Create realistic market data
            days = 252  # Trading days in a year
            dates = pd.date_range(start='2023-01-01', periods=days, freq='D')
            
            # Generate market features
            market_data = pd.DataFrame({
                'date': dates,
                'price': 100 * np.cumprod(1 + np.random.normal(0.0005, 0.02, days)),
                'volume': np.random.lognormal(15, 0.5, days),
                'volatility': np.random.uniform(0.1, 0.4, days),
                'rsi': np.random.uniform(20, 80, days),
                'macd': np.random.normal(0, 2, days)
            })
            
            # Calculate technical indicators
            market_data['sma_20'] = market_data['price'].rolling(20).mean()
            market_data['sma_50'] = market_data['price'].rolling(50).mean()
            market_data['returns'] = market_data['price'].pct_change()
            market_data['price_change'] = market_data['returns']
            
            try:
                import tensorflow as tf
                from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
                from sklearn.preprocessing import StandardScaler
                from sklearn.model_selection import train_test_split
                
                # Prepare features for ML models
                features = ['volatility', 'rsi', 'macd', 'volume']
                X = market_data[features].fillna(0)
                
                # Create target variable (1 for bullish, 0 for bearish)
                market_data['target'] = (market_data['returns'].shift(-1) > 0).astype(int)
                y = market_data['target'].fillna(0)
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # TensorFlow model for trend prediction
                tf_model = tf.keras.Sequential([
                    tf.keras.layers.Dense(128, activation='relu', input_shape=(len(features),)),
                    tf.keras.layers.Dropout(0.3),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dropout(0.2),
                    tf.keras.layers.Dense(32, activation='relu'),
                    tf.keras.layers.Dense(1, activation='sigmoid')
                ])
                
                tf_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
                
                # Train TensorFlow model
                history = tf_model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, 
                                     validation_split=0.2, verbose=0)
                
                # Scikit-learn models for comparison
                gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                
                gb_model.fit(X_train, y_train)
                rf_model.fit(X_train, y_train)
                
                # Make predictions
                current_features = X.iloc[-1:].values
                current_features_scaled = scaler.transform(current_features)
                
                tf_prediction = tf_model.predict(current_features_scaled, verbose=0)[0][0]
                gb_prediction = gb_model.predict_proba(current_features)[0][1]
                rf_prediction = rf_model.predict(current_features)[0]
                
                # Ensemble prediction
                ensemble_prediction = (tf_prediction + gb_prediction + rf_prediction) / 3
                
                market_prediction = {
                    'bullish_probability': ensemble_prediction,
                    'tf_probability': tf_prediction,
                    'gb_probability': gb_prediction,
                    'rf_probability': rf_prediction,
                    'trend_direction': 'bullish' if ensemble_prediction > 0.5 else 'bearish',
                    'confidence': min(95, max(55, ensemble_prediction * 100)),
                    'outlook': f'Market sentiment shows {ensemble_prediction:.1%} bullish probability based on ensemble ML models.',
                    'recommended_actions': [
                        f'{"Increase" if ensemble_prediction > 0.6 else "Decrease"} equity allocation',
                        'Monitor technical indicators closely',
                        'Consider volatility-based position sizing'
                    ]
                }
                
                ML_AVAILABLE = True
                
            except ImportError:
                # Fallback prediction
                market_prediction = {
                    'bullish_probability': 0.65,
                    'trend_direction': 'bullish',
                    'confidence': 75,
                    'outlook': 'Market conditions appear favorable with positive momentum indicators.',
                    'recommended_actions': [
                        'Consider increasing equity allocation',
                        'Monitor for entry opportunities',
                        'Maintain diversified portfolio'
                    ]
                }
                ML_AVAILABLE = False
                history = None
            
            # Display prediction results
            st.success("✅ Real-time Market Analysis Complete!")
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                bullish_prob = market_prediction.get('bullish_probability', 0.65)
                st.metric("Ensemble Prediction", f"{bullish_prob:.1%}")
            with col2:
                trend = market_prediction.get('trend_direction', 'neutral')
                trend_emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}
                st.metric("Trend Direction", f"{trend_emoji.get(trend, '➡️')} {trend.title()}")
            with col3:
                confidence = market_prediction.get('confidence', 75)
                st.metric("AI Confidence", f"{confidence:.0f}%")
            with col4:
                volatility = market_data['volatility'].iloc[-1]
                st.metric("Current Volatility", f"{volatility:.1%}")
            
            # Model comparison
            if ML_AVAILABLE:
                st.markdown("### 🤖 Model Predictions Comparison")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("TensorFlow", f"{market_prediction['tf_probability']:.1%}")
                with col2:
                    st.metric("Gradient Boosting", f"{market_prediction['gb_probability']:.1%}")
                with col3:
                    st.metric("Random Forest", f"{market_prediction['rf_probability']:.1%}")
            
            # Market outlook
            st.markdown("### 🎯 Market Outlook")
            st.info(market_prediction.get('outlook', 'Market analysis complete'))
            
            # AI recommendations
            recommendations = market_prediction.get('recommended_actions', [])
            if recommendations:
                st.markdown("### 💡 AI Recommendations")
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")
            
            # Market Data Visualizations using matplotlib and pandas
            if ML_AVAILABLE:
                st.markdown("### 📊 Real-time Market Data Visualizations")
                
                # Create comprehensive market analysis DataFrame
                market_analysis_df = market_data.copy()
                market_analysis_df['price_change'] = market_analysis_df['price'].pct_change()
                market_analysis_df['volatility_ma'] = market_analysis_df['volatility'].rolling(10).mean()
                
                # Price and technical indicators
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Market Price Trend Analysis**")
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
                    
                    # Price chart with moving averages
                    ax1.plot(market_data['date'], market_data['price'], 'b-', linewidth=2, label='Price')
                    ax1.plot(market_data['date'], market_data['sma_20'], 'orange', linewidth=1.5, label='SMA 20')
                    ax1.plot(market_data['date'], market_data['sma_50'], 'red', linewidth=1.5, label='SMA 50')
                    ax1.set_title('Market Price with Moving Averages', fontweight='bold')
                    ax1.set_ylabel('Price ($)')
                    ax1.legend()
                    ax1.grid(True, alpha=0.3)
                    
                    # Volume chart
                    ax2.bar(market_data['date'], market_data['volume'], alpha=0.6, color='green')
                    ax2.set_title('Trading Volume', fontweight='bold')
                    ax2.set_ylabel('Volume')
                    ax2.set_xlabel('Date')
                    ax2.grid(True, alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Price statistics table
                    price_stats = pd.DataFrame({
                        'Metric': ['Current Price', 'Daily Change', 'Weekly High', 'Weekly Low', 'Volatility'],
                        'Value': [
                            f"${market_data['price'].iloc[-1]:.2f}",
                            f"{market_data['price_change'].iloc[-1]*100:.2f}%",
                            f"${market_data['price'].tail(7).max():.2f}",
                            f"${market_data['price'].tail(7).min():.2f}",
                            f"{market_data['volatility'].iloc[-1]*100:.1f}%"
                        ]
                    })
                    st.dataframe(price_stats, use_container_width=True)
                
                with col2:
                    st.markdown("**ML Model Predictions Comparison**")
                    
                    # Model predictions DataFrame
                    models_df = pd.DataFrame({
                        'Model': ['TensorFlow', 'Gradient Boosting', 'Random Forest', 'Ensemble'],
                        'Bullish Probability': [
                            market_prediction['tf_probability'],
                            market_prediction['gb_probability'], 
                            market_prediction['rf_probability'],
                            market_prediction['bullish_probability']
                        ]
                    })
                    
                    # Bar chart
                    fig, ax = plt.subplots(figsize=(8, 6))
                    bars = ax.bar(models_df['Model'], models_df['Bullish Probability'], 
                                 color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'], alpha=0.8)
                    ax.set_title('ML Model Predictions Comparison', fontweight='bold')
                    ax.set_ylabel('Bullish Probability')
                    ax.set_ylim(0, 1)
                    ax.grid(True, alpha=0.3, axis='y')
                    
                    # Add value labels on bars
                    for bar, prob in zip(bars, models_df['Bullish Probability']):
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                               f'{prob:.1%}', ha='center', va='bottom', fontweight='bold')
                    
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Model performance table
                    st.dataframe(models_df.round(3), use_container_width=True)
                
                # Technical indicators dashboard
                st.markdown("**Technical Indicators Dashboard**")
                col1, col2 = st.columns(2)
                
                with col1:
                    # RSI Analysis
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(market_data['date'], market_data['rsi'], 'purple', linewidth=2, label='RSI')
                    ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
                    ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
                    ax.axhline(y=50, color='gray', linestyle='-', alpha=0.5, label='Neutral (50)')
                    
                    # Fill areas
                    ax.fill_between(market_data['date'], 70, 100, alpha=0.2, color='red', label='Overbought Zone')
                    ax.fill_between(market_data['date'], 0, 30, alpha=0.2, color='green', label='Oversold Zone')
                    
                    ax.set_title('RSI (Relative Strength Index)', fontweight='bold')
                    ax.set_ylabel('RSI Value')
                    ax.set_xlabel('Date')
                    ax.set_ylim(0, 100)
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig)
                
                with col2:
                    # Volatility Analysis
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(market_data['date'], market_data['volatility']*100, 'red', linewidth=2, label='Daily Volatility')
                    ax.plot(market_data['date'], market_analysis_df['volatility_ma']*100, 'blue', linewidth=2, label='10-Day MA')
                    
                    # Add volatility bands
                    vol_mean = market_data['volatility'].mean()
                    vol_std = market_data['volatility'].std()
                    ax.axhline(y=(vol_mean + vol_std)*100, color='orange', linestyle='--', alpha=0.7, label='High Vol')
                    ax.axhline(y=(vol_mean - vol_std)*100, color='green', linestyle='--', alpha=0.7, label='Low Vol')
                    
                    ax.set_title('Market Volatility Analysis', fontweight='bold')
                    ax.set_ylabel('Volatility (%)')
                    ax.set_xlabel('Date')
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig)
                
                # MACD and correlation analysis
                st.markdown("**Advanced Technical Analysis**")
                col1, col2 = st.columns(2)
                
                with col1:
                    # MACD Analysis
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(market_data['date'], market_data['macd'], 'blue', linewidth=2, label='MACD')
                    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
                    ax.bar(market_data['date'], market_data['macd'], alpha=0.3, 
                          color=['green' if x > 0 else 'red' for x in market_data['macd']])
                    
                    ax.set_title('MACD (Moving Average Convergence Divergence)', fontweight='bold')
                    ax.set_ylabel('MACD Value')
                    ax.set_xlabel('Date')
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig)
                
                with col2:
                    # Price vs Volume correlation
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    # Create scatter plot
                    colors = ['green' if x > 0 else 'red' for x in market_data['price_change']]
                    scatter = ax.scatter(market_data['volume'], market_data['price_change']*100, 
                                       c=colors, alpha=0.6, s=30)
                    
                    # Add trend line
                    z = np.polyfit(market_data['volume'], market_data['price_change']*100, 1)
                    p = np.poly1d(z)
                    ax.plot(market_data['volume'], p(market_data['volume']), "r--", alpha=0.8, linewidth=2)
                    
                    ax.set_title('Price Change vs Trading Volume', fontweight='bold')
                    ax.set_xlabel('Trading Volume')
                    ax.set_ylabel('Price Change (%)')
                    ax.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig)
                
                # Market summary statistics
                st.markdown("**Market Analysis Summary**")
                
                # Calculate correlations and statistics
                correlation_matrix = market_data[['price', 'volume', 'volatility', 'rsi', 'macd']].corr()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Correlation Matrix**")
                    fig, ax = plt.subplots(figsize=(8, 6))
                    im = ax.imshow(correlation_matrix, cmap='RdYlBu', aspect='auto', vmin=-1, vmax=1)
                    
                    # Add correlation values
                    for i in range(len(correlation_matrix.columns)):
                        for j in range(len(correlation_matrix.columns)):
                            text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                                         ha="center", va="center", color="black", fontweight='bold')
                    
                    ax.set_xticks(range(len(correlation_matrix.columns)))
                    ax.set_yticks(range(len(correlation_matrix.columns)))
                    ax.set_xticklabels(correlation_matrix.columns, rotation=45)
                    ax.set_yticklabels(correlation_matrix.columns)
                    ax.set_title('Market Indicators Correlation', fontweight='bold')
                    
                    plt.colorbar(im, ax=ax, label='Correlation Coefficient')
                    plt.tight_layout()
                    st.pyplot(fig)
                
                with col2:
                    st.markdown("**Technical Indicators Summary**")
                    current_rsi = market_data['rsi'].iloc[-1]
                    current_macd = market_data['macd'].iloc[-1]
                    current_vol = market_data['volatility'].iloc[-1]
                    
                    # Determine signals
                    rsi_signal = "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral"
                    macd_signal = "Bullish" if current_macd > 0 else "Bearish"
                    vol_signal = "High" if current_vol > vol_mean + vol_std else "Low" if current_vol < vol_mean - vol_std else "Normal"
                    
                    indicators_summary = pd.DataFrame({
                        'Indicator': ['RSI', 'MACD', 'Volatility', 'Price Trend', 'Volume Trend'],
                        'Current Value': [
                            f"{current_rsi:.1f}",
                            f"{current_macd:.2f}",
                            f"{current_vol*100:.1f}%",
                            f"{market_data['price_change'].iloc[-1]*100:.2f}%",
                            f"{market_data['volume'].iloc[-1]:,.0f}"
                        ],
                        'Signal': [rsi_signal, macd_signal, vol_signal, 
                                 "Bullish" if market_data['price_change'].iloc[-1] > 0 else "Bearish",
                                 "High" if market_data['volume'].iloc[-1] > market_data['volume'].mean() else "Low"]
                    })
                    st.dataframe(indicators_summary, use_container_width=True)
                
                # Training progress visualization
                if history is not None:
                    st.markdown("**TensorFlow Model Training Analysis**")
                    
                    # Create training DataFrame
                    training_df = pd.DataFrame({
                        'Epoch': range(1, len(history.history['loss']) + 1),
                        'Training Loss': history.history['loss'],
                        'Validation Loss': history.history['val_loss'],
                        'Training Accuracy': history.history['accuracy'],
                        'Validation Accuracy': history.history['val_accuracy']
                    })
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Training metrics plot
                        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
                        
                        # Loss plot
                        ax1.plot(training_df['Epoch'], training_df['Training Loss'], 'b-', linewidth=2, label='Training Loss')
                        ax1.plot(training_df['Epoch'], training_df['Validation Loss'], 'r-', linewidth=2, label='Validation Loss')
                        ax1.set_title('Model Training Loss', fontweight='bold')
                        ax1.set_ylabel('Loss')
                        ax1.legend()
                        ax1.grid(True, alpha=0.3)
                        
                        # Accuracy plot
                        ax2.plot(training_df['Epoch'], training_df['Training Accuracy'], 'g-', linewidth=2, label='Training Accuracy')
                        ax2.plot(training_df['Epoch'], training_df['Validation Accuracy'], 'orange', linewidth=2, label='Validation Accuracy')
                        ax2.set_title('Model Training Accuracy', fontweight='bold')
                        ax2.set_ylabel('Accuracy')
                        ax2.set_xlabel('Epoch')
                        ax2.legend()
                        ax2.grid(True, alpha=0.3)
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    with col2:
                        # Training statistics
                        st.markdown("**Training Performance Metrics**")
                        final_metrics = pd.DataFrame({
                            'Metric': ['Final Training Loss', 'Final Validation Loss', 'Best Validation Loss', 
                                     'Final Training Accuracy', 'Final Validation Accuracy', 'Best Validation Accuracy'],
                            'Value': [
                                f"{history.history['loss'][-1]:.4f}",
                                f"{history.history['val_loss'][-1]:.4f}",
                                f"{min(history.history['val_loss']):.4f}",
                                f"{history.history['accuracy'][-1]:.4f}",
                                f"{history.history['val_accuracy'][-1]:.4f}",
                                f"{max(history.history['val_accuracy']):.4f}"
                            ]
                        })
                        st.dataframe(final_metrics, use_container_width=True)
                        
                        # Model convergence analysis
                        st.markdown("**Model Convergence Analysis**")
                        loss_improvement = (history.history['loss'][0] - history.history['loss'][-1]) / history.history['loss'][0] * 100
                        acc_improvement = (history.history['accuracy'][-1] - history.history['accuracy'][0]) * 100
                        
                        convergence_stats = pd.DataFrame({
                            'Metric': ['Loss Improvement', 'Accuracy Improvement', 'Epochs to Convergence', 'Overfitting Risk'],
                            'Value': [
                                f"{loss_improvement:.1f}%",
                                f"{acc_improvement:.1f}%",
                                f"{len(history.history['loss'])}",
                                "Low" if abs(history.history['loss'][-1] - history.history['val_loss'][-1]) < 0.1 else "Medium"
                            ]
                        })
                        st.dataframe(convergence_stats, use_container_width=True)

def show_investment_calculator():
    """AI-powered investment calculator."""
    st.markdown("### 💰 AI Investment Calculator")
    st.markdown("*Calculate optimal investment strategies with ML predictions*")
    
    # Calculator inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Investment Parameters**")
        initial_amount = st.number_input("Initial Investment ($)", 0, 50000, 1000, step=100)
        monthly_contribution = st.number_input("Monthly Contribution ($)", 0, 2000, 200, step=25)
        investment_period = st.slider("Investment Period (years)", 1, 30, 10)
        
    with col2:
        st.markdown("**Risk & Return Settings**")
        risk_preference = st.selectbox("Risk Preference", ["Low Risk", "Medium Risk", "High Risk"])
        rebalancing = st.selectbox("Rebalancing Frequency", ["Monthly", "Quarterly", "Annually", "Never"])
        tax_consideration = st.checkbox("Include Tax Considerations", value=True)
    
    if st.button("🧮 Calculate with AI", type="primary", use_container_width=True):
        with st.spinner("🤖 AI is calculating optimal investment strategy..."):
            # Risk-adjusted returns
            risk_returns = {"Low Risk": 0.06, "Medium Risk": 0.08, "High Risk": 0.11}
            
            expected_return = risk_returns[risk_preference]
            
            # Calculate future value with monthly contributions
            monthly_return = expected_return / 12
            months = investment_period * 12
            
            # Future value of initial investment
            fv_initial = initial_amount * (1 + expected_return) ** investment_period
            
            # Future value of monthly contributions
            if monthly_return > 0:
                fv_monthly = monthly_contribution * (((1 + monthly_return) ** months - 1) / monthly_return)
            else:
                fv_monthly = monthly_contribution * months
            
            total_future_value = fv_initial + fv_monthly
            total_contributions = initial_amount + (monthly_contribution * months)
            total_gains = total_future_value - total_contributions
            
            # Display results
            st.success("✅ Investment Calculation Complete!")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Future Value", f"${total_future_value:,.0f}")
            with col2:
                st.metric("Total Contributions", f"${total_contributions:,.0f}")
            with col3:
                st.metric("Total Gains", f"${total_gains:,.0f}")
            with col4:
                roi = (total_gains / total_contributions) * 100 if total_contributions > 0 else 0
                st.metric("ROI", f"{roi:.1f}%")

def show_risk_analyzer():
    """AI-powered risk analysis."""
    st.markdown("### 🎯 AI Risk Analyzer")
    st.markdown("*Comprehensive risk assessment using machine learning*")
    
    # Risk assessment inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Financial Profile**")
        net_worth = st.number_input("Net Worth ($)", 0, 1000000, 50000, step=5000)
        debt_to_income = st.slider("Debt-to-Income Ratio", 0.0, 1.0, 0.3, 0.05)
        emergency_fund_months = st.slider("Emergency Fund (months)", 0, 12, 3)
        
    with col2:
        st.markdown("**Risk Factors**")
        job_stability = st.selectbox("Job Stability", ["Very Stable", "Stable", "Moderate", "Unstable"])
        dependents = st.number_input("Number of Dependents", 0, 10, 0)
        health_insurance = st.checkbox("Health Insurance Coverage", value=True)
    
    if st.button("🎯 Analyze Risk Profile", type="primary", use_container_width=True):
        with st.spinner("🤖 AI is analyzing your risk profile..."):
            # Calculate risk scores
            financial_stability_score = min(100, (emergency_fund_months / 6) * 50 + (1 - debt_to_income) * 50)
            
            job_scores = {"Very Stable": 100, "Stable": 80, "Moderate": 60, "Unstable": 30}
            job_score = job_scores[job_stability]
            
            dependency_penalty = dependents * 10
            insurance_bonus = 10 if health_insurance else 0
            
            overall_risk_score = (financial_stability_score + job_score + insurance_bonus - dependency_penalty) / 2
            overall_risk_score = max(0, min(100, overall_risk_score))
            
            # Risk categorization
            if overall_risk_score >= 80:
                risk_category = "Low Risk"
                risk_color = "🟢"
                recommended_allocation = "70% Stocks, 25% Bonds, 5% Cash"
            elif overall_risk_score >= 60:
                risk_category = "Medium Risk"
                risk_color = "🟡"
                recommended_allocation = "50% Stocks, 40% Bonds, 10% Cash"
            else:
                risk_category = "High Risk"
                risk_color = "🔴"
                recommended_allocation = "30% Stocks, 50% Bonds, 20% Cash"
            
            # Display results
            st.success("✅ Risk Analysis Complete!")
            
            # Risk metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Risk Score", f"{overall_risk_score:.0f}/100")
            with col2:
                st.metric("Risk Category", f"{risk_color} {risk_category}")
            with col3:
                st.metric("Financial Stability", f"{financial_stability_score:.0f}/100")
            
            # Recommendations
            st.markdown("### 💡 AI Risk Recommendations")
            
            recommendations = []
            
            if emergency_fund_months < 3:
                recommendations.append("🚨 Build emergency fund to 3-6 months of expenses")
            if debt_to_income > 0.4:
                recommendations.append("💳 Reduce debt-to-income ratio below 40%")
            if not health_insurance:
                recommendations.append("🏥 Obtain health insurance coverage")
            if overall_risk_score < 60:
                recommendations.append("🛡️ Focus on conservative investments until risk factors improve")
            
            recommendations.append(f"📊 Recommended allocation: {recommended_allocation}")
            
            for rec in recommendations:
                st.write(f"• {rec}")

def show_analysis_page():
    """Display analysis and insights page."""
    st.title("📈 Investment Analysis")
    st.markdown("*Comprehensive analysis of your investment performance and trends*")
    
    # Placeholder for analysis features
    st.info("🚧 Analysis features coming soon! This will include portfolio performance tracking, trend analysis, and detailed insights.")
    
    # Sample analysis sections
    tab1, tab2, tab3 = st.tabs(["Performance", "Trends", "Insights"])
    
    with tab1:
        st.markdown("### Portfolio Performance")
        st.write("Track your investment performance over time")
    
    with tab2:
        st.markdown("### Market Trends")
        st.write("Analyze market trends affecting your investments")
    
    with tab3:
        st.markdown("### AI Insights")
        st.write("Get personalized insights from our AI advisor")

def show_goals_page():
    """Display goals tracking page."""
    st.title("🎯 Investment Goals")
    st.markdown("*Set and track your financial goals*")
    
    # Placeholder for goals features
    st.info("🚧 Goals tracking features coming soon! This will include goal setting, progress tracking, and milestone celebrations.")
    
    # Sample goals sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Goals")
        st.write("• Emergency Fund: $5,000")
        st.write("• House Down Payment: $50,000")
        st.write("• Retirement: $1,000,000")
    
    with col2:
        st.markdown("### Progress")
        st.progress(0.3, text="Emergency Fund: 30%")
        st.progress(0.1, text="House Down Payment: 10%")
        st.progress(0.05, text="Retirement: 5%")

def show_questionnaire_page():
    """Display the enhanced investment questionnaire with React-style UI."""
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back to Home"):
            st.session_state.current_page = "welcome"
            st.rerun()

    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h1 style='color: #2c3e50; margin-bottom: 0.5rem;'>📋 Investment Questionnaire</h1>
        <p style='color: #6c757d; font-size: 1.1rem;'>Help us create your personalized investment plan</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("investment_questionnaire"):
        # Monthly Investment Budget
        st.markdown("### 💰 Monthly Investment Budget")
        st.markdown("*Start with as little as $10/month*")
        
        monthly_investment = st.number_input(
            "Monthly Investment Amount ($)", 
            min_value=10, 
            max_value=2000, 
            value=25,
            step=5,
            help="How much can you invest each month?"
        )
        
        # Risk Tolerance with enhanced styling
        st.markdown("### ⚖️ Risk Tolerance")
        risk_tolerance = st.radio(
            "Choose your investment approach:",
            ["Conservative (Low Risk)", "Balanced (Medium Risk)", "Growth-Focused (High Risk)"],
            help="This determines how your portfolio will be allocated"
        )
        
        # Display risk descriptions
        risk_descriptions = {
            "Conservative (Low Risk)": "🛡️ **Conservative**: Prioritize capital preservation with steady, modest returns",
            "Balanced (Medium Risk)": "⚖️ **Balanced**: Mix of growth and stability for moderate returns", 
            "Growth-Focused (High Risk)": "📈 **Growth-Focused**: Higher potential returns with increased volatility"
        }
        
        if risk_tolerance in risk_descriptions:
            st.markdown(f"*{risk_descriptions[risk_tolerance]}*")
        
        # Investment Goal
        st.markdown("### 🎯 Investment Goal")
        investment_goal = st.selectbox(
            "What's your primary investment goal?",
            [
                "Build Emergency Fund",
                "Save for Laptop/Electronics", 
                "Build Long-term Wealth",
                "Save for Textbooks",
                "Save for Travel",
                "Graduation Goal"
            ]
        )
        
        # Time Horizon
        st.markdown("### ⏰ Time Horizon")
        time_horizon = st.selectbox(
            "When do you need the money?",
            ["3 months", "6 months", "1 year", "2 years", "5+ years"]
        )
        
        # Additional Info (optional)
        with st.expander("📊 Additional Information (Optional)"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=18, max_value=100, value=22)
                monthly_income = st.number_input("Monthly Income ($)", min_value=0, value=500)
            with col2:
                student_status = st.selectbox("Status", 
                                            ["Undergraduate", "Graduate", "Recent Graduate", "Working Professional"])
                investment_experience = st.selectbox("Investment Experience", 
                                                   ["Beginner", "Some Experience", "Experienced"])
        
        # ML-powered spending analysis section
        if ML_FEATURES_AVAILABLE:
            with st.expander("🤖 AI Spending Analysis (Optional)"):
                st.markdown("*Help us provide better recommendations by sharing your spending patterns*")
                
                # Mock spending data input for ML analysis
                col1, col2 = st.columns(2)
                with col1:
                    food_spending = st.number_input("Monthly Food & Dining ($)", min_value=0, value=200)
                    transport_spending = st.number_input("Monthly Transportation ($)", min_value=0, value=100)
                with col2:
                    entertainment_spending = st.number_input("Monthly Entertainment ($)", min_value=0, value=150)
                    shopping_spending = st.number_input("Monthly Shopping ($)", min_value=0, value=100)
                
                # Generate mock transaction data for ML analysis
                analyze_spending = st.form_submit_button("🧠 Analyze My Spending with AI")
                if analyze_spending:
                    mock_transactions = _generate_mock_transactions_from_input(
                        food_spending, transport_spending, entertainment_spending, shopping_spending
                    )
                    
                    # Analyze with ML
                    analysis = transaction_analyzer.analyze_transactions(mock_transactions)
                    investment_capacity = analysis.get('investment_capacity', {})
                    
                    if investment_capacity:
                        recommended_investment = investment_capacity.get('recommended_monthly_investment', monthly_investment)
                        st.success(f"🤖 AI Recommendation: Based on your spending, consider investing ${recommended_investment:.0f}/month")
                        st.info(investment_capacity.get('investment_rationale', 'AI analysis complete'))
                        
                        # Store AI recommendation
                        st.session_state.ai_recommended_investment = recommended_investment
            
        # Submit button with enhanced styling
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "✨ Get My Investment Plan", 
            type="primary",
            use_container_width=True,
            help="Generate your personalized portfolio recommendation"
        )
        
        if submitted:
            # Show loading state
            with st.spinner("🤖 AI is analyzing your profile and generating recommendations..."):
                import time
                time.sleep(2)  # Simulate processing time
                
                # Store questionnaire data with AI enhancements
                st.session_state.questionnaire_data = {
                    'age': age,
                    'student_status': student_status,
                    'monthly_income': monthly_income,
                    'monthly_investment': monthly_investment,
                    'risk_tolerance': risk_tolerance,
                    'investment_goal': investment_goal,
                    'time_horizon': time_horizon,
                    'investment_experience': investment_experience
                }
                
                # Store additional data for ML
                st.session_state.user_age = age
                st.session_state.user_income = monthly_income
                st.session_state.user_experience = investment_experience
                
                # Use AI-recommended investment if available
                if hasattr(st.session_state, 'ai_recommended_investment'):
                    monthly_investment = st.session_state.ai_recommended_investment
                    st.session_state.questionnaire_data['monthly_investment'] = monthly_investment
                
                # Generate portfolio recommendation using ML-enhanced logic
                portfolio = generate_react_style_portfolio(monthly_investment, risk_tolerance, time_horizon, investment_goal)
                
                st.session_state.portfolio_data = portfolio
                st.session_state.current_page = "portfolio"
                st.rerun()
        

def show_portfolio_page():
    """Display the enhanced portfolio dashboard with React-style components."""
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← Modify Profile", help="Go back to questionnaire"):
            st.session_state.current_page = "questionnaire"
            st.rerun()
    with col3:
        if st.button("Start Over", help="Return to welcome page"):
            st.session_state.current_page = "welcome"
            st.rerun()
    
    # Check if portfolio data exists
    portfolio_data = st.session_state.get('portfolio_data', {})
    questionnaire_data = st.session_state.get('questionnaire_data', {})
    
    if not portfolio_data:
        st.warning("Please complete the questionnaire first to see your personalized portfolio.")
        if st.button("Go to Questionnaire"):
            st.session_state.current_page = 'questionnaire'
            st.rerun()
        return
    
    # Portfolio overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 15px; margin: 0.5rem 0;'>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;'>${portfolio_data.get('monthlyAmount', 0)}</div>
            <div style='font-size: 0.9rem; opacity: 0.9;'>Monthly Investment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #28a745, #20c997); color: white; border-radius: 15px; margin: 0.5rem 0;'>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;'>{portfolio_data.get('totalExpectedReturn', 0):.1f}%</div>
            <div style='font-size: 0.9rem; opacity: 0.9;'>Expected Annual Return</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        projected_value = round(portfolio_data.get('projectedValue', 0), 2)
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #007bff, #6610f2); color: white; border-radius: 15px; margin: 0.5rem 0;'>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;'>${projected_value:,.2f}</div>
            <div style='font-size: 0.9rem; opacity: 0.9;'>Projected Value</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        time_horizon = portfolio_data.get('timeHorizon', 0)
        time_display = f"{time_horizon:.1f} years" if time_horizon >= 1 else f"{int(time_horizon * 12)} months"
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #fd7e14, #e83e8c); color: white; border-radius: 15px; margin: 0.5rem 0;'>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;'>{time_display}</div>
            <div style='font-size: 0.9rem; opacity: 0.9;'>Time Horizon</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show additional metrics if available from real data
    if 'portfolioMetrics' in portfolio_data or any(key in portfolio_data for key in ['volatility', 'sharpeRatio', 'maxDrawdown']):
        st.markdown("---")
        st.markdown("### 📊 Portfolio Risk Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            volatility = portfolio_data.get('volatility', 0)
            if volatility == 0 and 'portfolioMetrics' in portfolio_data:
                volatility = portfolio_data['portfolioMetrics'].get('annual_volatility', 0) * 100
            st.metric("Volatility", f"{volatility:.1f}%")
        
        with col2:
            sharpe_ratio = portfolio_data.get('sharpeRatio', 0)
            if sharpe_ratio == 0 and 'portfolioMetrics' in portfolio_data:
                sharpe_ratio = portfolio_data['portfolioMetrics'].get('sharpe_ratio', 0)
            st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
        
        with col3:
            max_drawdown = portfolio_data.get('maxDrawdown', 0)
            if max_drawdown == 0 and 'portfolioMetrics' in portfolio_data:
                max_drawdown = portfolio_data['portfolioMetrics'].get('max_drawdown', 0) * 100
            st.metric("Max Drawdown", f"{max_drawdown:.1f}%")
    
    # ML-powered insights section
    if ML_FEATURES_AVAILABLE and 'ml_confidence' in portfolio_data:
        st.markdown("---")
        st.markdown("### 🤖 AI Investment Insights")
        
        col1, col2 = st.columns(2)
        with col1:
            ml_confidence = portfolio_data.get('ml_confidence', 0.7)
            st.metric("AI Confidence", f"{ml_confidence:.1%}", help="How confident our AI is in this recommendation")
        
        with col2:
            # Generate market prediction
            market_prediction = ml_advisor.predict_market_trends(pd.DataFrame())
            trend_direction = market_prediction.get('trend_direction', 'neutral')
            trend_emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}
            st.metric("Market Outlook", f"{trend_emoji.get(trend_direction, '➡️')} {trend_direction.title()}")
        
        # AI reasoning
        ml_reasoning = portfolio_data.get('ml_reasoning', 'Portfolio optimized using machine learning algorithms')
        st.info(f"🧠 **AI Analysis:** {ml_reasoning}")
        
        # Market predictions
        if market_prediction:
            bullish_prob = market_prediction.get('bullish_probability', 0.5)
            st.markdown(f"**Market Prediction:** {bullish_prob:.1%} bullish probability")
            st.write(market_prediction.get('outlook', ''))
            
            # Show top AI recommendations
            recommendations = market_prediction.get('recommended_actions', [])
            if recommendations:
                st.markdown("**AI Recommendations:**")
                for i, rec in enumerate(recommendations[:3], 1):
                    st.write(f"{i}. {rec}")
    
    # Recommended Portfolio Allocation
    st.markdown("---")
    st.markdown("## 🎯 Recommended Portfolio Allocation")
    st.markdown("*Based on your risk tolerance and investment goals*")
    
    investments = portfolio_data.get('investments', [])
    
    for investment in investments:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{investment['name']}** ({investment['symbol']})")
                description = investment.get('description', 'No description available')
                if len(description) > 100:
                    description = description[:100] + "..."
                st.markdown(f"*{description}*")
            
            with col2:
                allocation_pct = investment['allocation'] * 100
                st.metric("Allocation", f"{allocation_pct:.1f}%")
                st.progress(investment['allocation'])
            
            with col3:
                monthly_amount = portfolio_data['monthlyAmount'] * investment['allocation']
                st.metric("Monthly Amount", f"${monthly_amount:.2f}")
                
                # Show additional info if available from real data
                if 'expense_ratio' in investment:
                    st.write(f"Expense Ratio: {investment['expense_ratio']:.2%}")
                
                risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                risk_level = investment.get('riskLevel', 'medium')
                st.write(f"{risk_colors.get(risk_level, '🟡')} {risk_level.title()} Risk")
        
        st.markdown("---")
    
    # Investment growth projection
    st.markdown("### 📈 Growth Projection")
    
    years = portfolio_data.get('timeHorizon', 10)
    monthly_amount = portfolio_data.get('monthlyAmount', 0)
    annual_return = portfolio_data.get('totalExpectedReturn', 8) / 100
    
    # Calculate year-by-year growth
    months_data = []
    portfolio_values = []
    contributions_data = []
    
    total_months = max(1, int(years * 12))  # Ensure at least 1 month
    
    for month in range(1, total_months + 1):
        # Calculate portfolio value with compound growth
        monthly_return = annual_return / 12
        
        # For very short periods, use simple calculation
        if years < 1:
            portfolio_value = monthly_amount * month * (1 + annual_return * (month / 12))
        elif monthly_return > 0:
            portfolio_value = monthly_amount * (((1 + monthly_return) ** month - 1) / monthly_return)
        else:
            portfolio_value = monthly_amount * month
        
        total_contributions = monthly_amount * month
        
        months_data.append(month / 12)
        portfolio_values.append(portfolio_value)
        contributions_data.append(total_contributions)
    
    # Create the growth chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months_data,
        y=portfolio_values,
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months_data,
        y=contributions_data,
        mode='lines',
        name='Total Contributions',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Portfolio Growth Over Time",
        xaxis_title="Years",
        yaxis_title="Value ($)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary metrics
    final_value = portfolio_values[-1]
    total_contributions = contributions_data[-1]
    total_gains = final_value - total_contributions
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Contributions", f"${total_contributions:,.0f}")
    
    with col2:
        st.metric("Projected Gains", f"${total_gains:,.0f}")
    
    with col3:
        roi_percentage = (total_gains / total_contributions) * 100 if total_contributions > 0 else 0
        st.metric("Return on Investment", f"{roi_percentage:.1f}%")
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📊 View Analysis", use_container_width=True):
            st.session_state.current_page = "analysis"
            st.rerun()
    
    with col2:
        if st.button("🎯 Set Goals", use_container_width=True):
            st.session_state.current_page = "goals"
            st.rerun()
    
    with col3:
        if st.button("🔄 Modify Portfolio", use_container_width=True):
            st.session_state.current_page = "questionnaire"
            st.rerun()

def show_analysis_page():
    """Display detailed portfolio analysis."""
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← Back to Portfolio", help="Return to portfolio dashboard"):
            st.session_state.current_page = "portfolio"
            st.rerun()
    with col3:
        if st.button("🎯 Goals", help="Go to investment goals"):
            st.session_state.current_page = "goals"
            st.rerun()
    
    st.title("📊 Portfolio Analysis")
    
    # Check if portfolio data exists
    portfolio_data = st.session_state.get('portfolio_data', {})
    questionnaire_data = st.session_state.get('questionnaire_data', {})
    
    if not portfolio_data:
        st.warning("Please complete the questionnaire first to see your portfolio analysis.")
        if st.button("Go to Questionnaire"):
            st.session_state.current_page = 'questionnaire'
            st.rerun()
        return
    
    
    # Portfolio Overview
    st.markdown("## 📈 Portfolio Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Expected Return", f"{portfolio_data.get('totalExpectedReturn', 0):.1f}%")
    with col2:
        st.metric("Risk Score", f"{portfolio_data.get('riskScore', 0)}/10")
    with col3:
        st.metric("Diversification", f"{len(portfolio_data.get('investments', []))} Assets")
    with col4:
        st.metric("Time Horizon", portfolio_data.get('timeframe', 'N/A'))
    
    # Risk Analysis
    st.markdown("## ⚠️ Risk Analysis")
    
    investments = portfolio_data.get('investments', [])
    if investments:
        # Risk distribution pie chart
        risk_distribution = {}
        for inv in investments:
            risk_level = inv.get('riskLevel', 'medium')
            allocation = inv.get('allocation', 0)
            if risk_level in risk_distribution:
                risk_distribution[risk_level] += allocation
            else:
                risk_distribution[risk_level] = allocation
        
        if risk_distribution:
            fig_risk = px.pie(
                values=list(risk_distribution.values()),
                names=list(risk_distribution.keys()),
                title="Portfolio Risk Distribution",
                color_discrete_map={'low': '#28a745', 'medium': '#ffc107', 'high': '#dc3545'}
            )
            st.plotly_chart(fig_risk, use_container_width=True)
    
    # Monte Carlo Simulation
    st.markdown("## 🎲 Monte Carlo Simulation")
    
    # Generate Monte Carlo simulation data
    monthly_investment = portfolio_data.get('monthlyAmount', 100)
    expected_return = portfolio_data.get('totalExpectedReturn', 8) / 100
    timeframe = portfolio_data.get('timeframe', '5+ years')
    
    # Time periods mapping
    time_periods = {"3 months": 3, "6 months": 6, "1 year": 12, "2 years": 24, "5+ years": 60}
    total_months = time_periods.get(timeframe, 60)
    
    # Run Monte Carlo simulation
    num_simulations = 1000
    np.random.seed(42)
    
    final_values = []
    for _ in range(num_simulations):
        portfolio_value = 0
        for month in range(total_months):
            monthly_return = np.random.normal(expected_return/12, 0.15/np.sqrt(12))
            portfolio_value = (portfolio_value + monthly_investment) * (1 + monthly_return)
        final_values.append(max(0, portfolio_value))
    
    # Create histogram
    fig_hist = px.histogram(
        x=final_values,
        nbins=50,
        title=f"Portfolio Value Distribution After {timeframe} (1,000 simulations)",
        labels={'x': 'Portfolio Value ($)', 'y': 'Frequency'}
    )
    fig_hist.add_vline(x=np.mean(final_values), line_dash="dash", line_color="red", 
                       annotation_text=f"Mean: ${np.mean(final_values):,.0f}")
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Simulation statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mean Value", f"${np.mean(final_values):,.0f}")
    with col2:
        st.metric("Median Value", f"${np.median(final_values):,.0f}")
    with col3:
        st.metric("Best Case (95%)", f"${np.percentile(final_values, 95):,.0f}")
    with col4:
        st.metric("Worst Case (5%)", f"${np.percentile(final_values, 5):,.0f}")
    
    # Risk metrics
    st.markdown("## 📊 Risk Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_score = portfolio_data.get('riskScore', 5)
        st.metric("Risk Score", f"{risk_score}/10")
    with col2:
        volatility = 0.12 if 'Conservative' in questionnaire_data.get('risk_tolerance', '') else 0.16 if 'Balanced' in questionnaire_data.get('risk_tolerance', '') else 0.20
        st.metric("Portfolio Volatility", f"{volatility:.1%}")
    with col3:
        sharpe = 0.6 if 'Conservative' in questionnaire_data.get('risk_tolerance', '') else 0.8 if 'Balanced' in questionnaire_data.get('risk_tolerance', '') else 1.0
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")

def show_goals_page():
    """Display investment goals tracking."""
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← Back to Portfolio", help="Return to portfolio dashboard"):
            st.session_state.current_page = "portfolio"
            st.rerun()
    with col3:
        if st.button("📊 Analysis", help="Go to portfolio analysis"):
            st.session_state.current_page = "analysis"
            st.rerun()
    
    st.title("🎯 Investment Goals")
    
    # Check if portfolio data exists
    portfolio_data = st.session_state.get('portfolio_data', {})
    questionnaire_data = st.session_state.get('questionnaire_data', {})
    
    if not portfolio_data:
        st.warning("Please complete the questionnaire first to set investment goals.")
        if st.button("Go to Questionnaire"):
            st.session_state.current_page = 'questionnaire'
            st.rerun()
        return
    
    # Initialize goals if not exists
    if 'investment_goals' not in st.session_state:
        st.session_state.investment_goals = []
    
    # Add new goal
    st.markdown("## ➕ Add New Goal")
    
    with st.form("add_goal"):
        col1, col2 = st.columns(2)
        with col1:
            goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund, New Laptop")
            target_amount = st.number_input("Target Amount ($)", min_value=100, value=1000, step=100)
        with col2:
            target_date = st.date_input("Target Date")
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        goal_description = st.text_area("Description (Optional)", placeholder="Why is this goal important to you?")
        
        if st.form_submit_button("Add Goal", type="primary"):
            new_goal = {
                'id': len(st.session_state.investment_goals),
                'name': goal_name,
                'target_amount': target_amount,
                'target_date': target_date,
                'priority': priority,
                'description': goal_description,
                'current_progress': 0
            }
            st.session_state.investment_goals.append(new_goal)
            st.success(f"Goal '{goal_name}' added successfully!")
            st.rerun()
    
    # Display existing goals
    if st.session_state.investment_goals:
        st.markdown("## 📋 Your Investment Goals")
        
        for goal in st.session_state.investment_goals:
            with st.expander(f"🎯 {goal['name']} - ${goal['target_amount']:,}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Target:** ${goal['target_amount']:,}")
                    st.markdown(f"**Target Date:** {goal['target_date']}")
                    st.markdown(f"**Priority:** {goal['priority']}")
                    if goal['description']:
                        st.markdown(f"**Description:** {goal['description']}")
                
                with col2:
                    # Progress tracking
                    progress = goal.get('current_progress', 0)
                    progress_percent = (progress / goal['target_amount']) * 100 if goal['target_amount'] > 0 else 0
                    
                    st.metric("Progress", f"${progress:,.0f}")
                    st.progress(min(progress_percent / 100, 1.0))
                    st.markdown(f"*{progress_percent:.1f}% complete*")
                
                # Update progress
                new_progress = st.number_input(
                    f"Update progress for {goal['name']}", 
                    min_value=0, 
                    max_value=goal['target_amount'], 
                    value=progress,
                    key=f"progress_{goal['id']}"
                )
                
                if st.button(f"Update Progress", key=f"update_{goal['id']}"):
                    goal['current_progress'] = new_progress
                    st.success("Progress updated!")
                    st.rerun()
                
                # Calculate time to goal
                monthly_investment = portfolio_data.get('monthlyAmount', 100)
                expected_return = portfolio_data.get('totalExpectedReturn', 8) / 100
                
                if monthly_investment > 0:
                    remaining_amount = goal['target_amount'] - progress
                    if remaining_amount > 0:
                        # Simple calculation assuming monthly contributions
                        months_needed = remaining_amount / monthly_investment
                        st.info(f"📅 At ${monthly_investment}/month, you'll reach this goal in approximately {months_needed:.0f} months")
    else:
        st.info("No investment goals set yet. Add your first goal above!")
    
    # Goal insights
    if st.session_state.investment_goals:
        st.markdown("## 📊 Goal Insights")
        
        total_goals = len(st.session_state.investment_goals)
        total_target = sum(goal['target_amount'] for goal in st.session_state.investment_goals)
        total_progress = sum(goal.get('current_progress', 0) for goal in st.session_state.investment_goals)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Goals", total_goals)
        with col2:
            st.metric("Total Target", f"${total_target:,}")
        with col3:
            st.metric("Total Progress", f"${total_progress:,}", f"{(total_progress/total_target*100) if total_target > 0 else 0:.1f}%")

def show_stocks_page():
    """Display major stock market data and analysis."""
    st.title("📈 Major Stock Market")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← Back to Portfolio"):
            st.session_state.current_page = "portfolio"
            st.rerun()
    
    # Major Stocks Market Data
    import numpy as np
    major_stocks = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc.',
        'AMZN': 'Amazon.com Inc.',
        'TSLA': 'Tesla Inc.',
        'NVDA': 'NVIDIA Corporation',
        'META': 'Meta Platforms Inc.',
        'NFLX': 'Netflix Inc.',
        'NKE': 'Nike Inc.',
        'DIS': 'The Walt Disney Company',
        'JPM': 'JPMorgan Chase & Co.',
        'V': 'Visa Inc.',
        'JNJ': 'Johnson & Johnson',
        'WMT': 'Walmart Inc.',
        'PG': 'Procter & Gamble Co.',
        'UNH': 'UnitedHealth Group Inc.',
        'HD': 'The Home Depot Inc.',
        'MA': 'Mastercard Inc.',
        'BAC': 'Bank of America Corp.',
        'XOM': 'Exxon Mobil Corporation'
    }
    
    # Add search functionality
    search_term = st.text_input("🔍 Search stocks (e.g., Apple, Nike, Tesla):", placeholder="Type company name or symbol...")
    
    # Filter stocks based on search
    filtered_stocks = major_stocks
    if search_term:
        filtered_stocks = {k: v for k, v in major_stocks.items() 
                          if search_term.lower() in v.lower() or search_term.upper() in k}
    
    # Display stocks in expandable format
    for ticker, company in filtered_stocks.items():
        # Generate realistic mock data
        np.random.seed(hash(ticker) % 2**32)  # Consistent data per ticker
        base_price = np.random.uniform(50, 300)
        change = np.random.uniform(-10, 10)
        change_percent = (change / base_price) * 100
        market_cap = np.random.uniform(100, 3000)
        volume = np.random.randint(10000000, 100000000)
        pe_ratio = np.random.uniform(15, 35)
        
        # Determine risk level based on volatility (using change_percent as proxy)
        if abs(change_percent) < 2:
            risk_level = 'low'
        elif abs(change_percent) < 5:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        with st.expander(f"{ticker} - {company}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                price_color = "green" if change >= 0 else "red"
                st.markdown(f"""
                **Current Price**  
                <span style='font-size: 1.5em; color: {price_color}; font-weight: bold;'>${base_price:.2f}</span>
                
                **Daily Change**  
                <span style='color: {price_color}; font-weight: bold;'>{change:+.2f} ({change_percent:+.1f}%)</span>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **Market Cap**  
                ${market_cap:.1f}B
                
                **Volume**  
                {volume:,}
                """)
            
            with col3:
                risk_color = "green" if risk_level == 'low' else "orange" if risk_level == 'medium' else "red"
                st.markdown(f"""
                **Risk Level**  
                <span style='color: {risk_color}; font-weight: bold;'>{risk_level.title()}</span>
                
                **52-Week Range**  
                ${base_price * 0.8:.2f} - ${base_price * 1.3:.2f}
                """, unsafe_allow_html=True)
            
            with col4:
                sector = 'Technology' if ticker in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX'] else 'Consumer' if ticker in ['NKE', 'DIS', 'WMT', 'PG', 'HD'] else 'Financial' if ticker in ['JPM', 'V', 'MA', 'BAC'] else 'Healthcare' if ticker in ['JNJ', 'UNH'] else 'Energy'
                st.markdown(f"""
                **P/E Ratio**  
                {pe_ratio:.1f}
                
                **Sector**  
                {sector}
                """)
            
            col_risk1, col_risk2 = st.columns(2)
            with col_risk1:
                st.write("**Volatility Level:**")
                if risk_level == 'low':
                    st.success("Low volatility - Stable price movements")
                elif risk_level == 'medium':
                    st.warning("Medium volatility - Moderate price swings")
                else:
                    st.error("High volatility - Significant price fluctuations")
            
            with col_risk2:
                st.write("**Investment Horizon:**")
                if risk_level == 'low':
                    st.info("Suitable for short to medium-term goals")
                elif risk_level == 'medium':
                    st.info("Best for medium to long-term investing")
                else:
                    st.info("Recommended for long-term growth strategies")
    
    # Market Summary
    st.markdown("## 📈 Market Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 10px;'>
            <div style='font-size: 1.5rem; font-weight: bold; color: lightgreen;'>+1.2%</div>
            <div>Average Change</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #28a745, #20c997); color: white; border-radius: 10px;'>
            <div style='font-size: 1.5rem; font-weight: bold;'>15/20</div>
            <div>Stocks Up Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #fd7e14, #e83e8c); color: white; border-radius: 10px;'>
            <div style='font-size: 1.5rem; font-weight: bold; color: lightgreen;'>Bullish</div>
            <div>Market Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sector Analysis
    st.markdown("## 🏭 Sector Performance")
    
    sectors = ['Technology', 'Consumer', 'Financial', 'Healthcare', 'Energy']
    sector_performance = [2.1, 0.8, -0.3, 1.5, 3.2]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for i, (sector, perf) in enumerate(zip(sectors, sector_performance)):
        color = "green" if perf >= 0 else "red"
        with [col1, col2, col3, col4, col5][i]:
            st.markdown(f"""
            <div style='text-align: center; padding: 0.8rem; background: white; border: 2px solid {color}; border-radius: 8px;'>
                <div style='font-weight: bold; color: {color};'>{perf:+.1f}%</div>
                <div style='font-size: 0.9rem;'>{sector}</div>
            </div>
            """, unsafe_allow_html=True)
    
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Analysis", use_container_width=True):
            st.session_state.current_page = "analysis"
            st.rerun()
    
    with col2:
        if st.button("💼 Back to Portfolio", use_container_width=True):
            st.session_state.current_page = "portfolio"
            st.rerun()
    
    with col3:
        if st.button("🔄 Modify Portfolio", use_container_width=True):
            st.session_state.current_page = "questionnaire"
            st.rerun()

# Use the main function defined earlier in the file
    
if __name__ == "__main__":
    main()
