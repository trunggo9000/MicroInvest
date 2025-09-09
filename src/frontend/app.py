import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
    """Generate portfolio recommendation using real market data or fallback to mock data."""
    
    if REAL_DATA_AVAILABLE:
        try:
            # Use real market data
            market_service = MarketDataService()
            investment_engine = InvestmentEngine(market_service)
            
            # Generate portfolio recommendation using real data
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
    page_title="MicroInvest - Student Investment Planner",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_welcome_page():
    """Display the welcome page with investment features."""
    # Hero section with enhanced styling and prominent CTA button
    st.markdown("""
    <div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
        <div style='background: rgba(255,255,255,0.15); display: inline-block; padding: 0.75rem 1.5rem; border-radius: 25px; margin-bottom: 1.5rem; backdrop-filter: blur(10px);'>
            ✨ AI-Powered Investment Advisor
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
            <strong>Disclaimer:</strong> This tool provides educational guidance and general investment suggestions. 
            Always consult with a financial advisor for personalized advice. 
            Past performance doesn't guarantee future results.
        </p>
    </div>
    """, unsafe_allow_html=True)

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
            with st.spinner("Analyzing your profile and generating recommendations..."):
                import time
                time.sleep(2)  # Simulate processing time
                
                # Store questionnaire data
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
                
                # Generate portfolio recommendation using React frontend logic
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

# Main navigation logic
def main():
    """Main application logic with navigation."""
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🏦 MicroInvest")
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Welcome", use_container_width=True):
            st.session_state.current_page = 'welcome'
            st.rerun()
        
        if st.button("📋 Questionnaire", use_container_width=True):
            st.session_state.current_page = 'questionnaire'
            st.rerun()
        
        if st.button("💼 Portfolio", use_container_width=True):
            st.session_state.current_page = 'portfolio'
            st.rerun()
        
        if st.button("📊 Analysis", use_container_width=True):
            st.session_state.current_page = 'analysis'
            st.rerun()
        
        if st.button("🎯 Goals", use_container_width=True):
            st.session_state.current_page = 'goals'
            st.rerun()
        
        if st.button("📈 Stocks", use_container_width=True):
            st.session_state.current_page = 'stocks'
            st.rerun()
        
        st.markdown("---")
        
        # Show current portfolio summary if available
        portfolio_data = st.session_state.get('portfolio_data', {})
        if portfolio_data:
            st.markdown("### 📈 Current Portfolio")
            st.metric("Monthly Investment", f"${portfolio_data.get('monthlyAmount', 0)}")
            st.metric("Expected Return", f"{portfolio_data.get('totalExpectedReturn', 0):.1f}%")
            st.metric("Projected Value", f"${portfolio_data.get('projectedValue', 0):,.2f}")
    
    # Display the appropriate page
    if st.session_state.current_page == 'welcome':
        show_welcome_page()
    elif st.session_state.current_page == 'questionnaire':
        show_questionnaire_page()
    elif st.session_state.current_page == 'portfolio':
        show_portfolio_page()
    elif st.session_state.current_page == 'analysis':
        show_analysis_page()
    elif st.session_state.current_page == 'goals':
        show_goals_page()
    elif st.session_state.current_page == 'stocks':
        show_stocks_page()

if __name__ == "__main__":
    main()
