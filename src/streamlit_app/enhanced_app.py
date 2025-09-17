"""
Enhanced MicroInvest App with Plaid Integration and ML Features
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend services to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from services.plaid_service import PlaidService
    from ai.ml_investment_advisor import MLInvestmentAdvisor
    from ai.transaction_analyzer import TransactionAnalyzer
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError as e:
    ENHANCED_FEATURES_AVAILABLE = False
    st.error(f"Enhanced features not available: {e}")

# Page configuration
st.set_page_config(
    page_title="MicroInvest - AI-Powered Investment Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
if ENHANCED_FEATURES_AVAILABLE:
    plaid_service = PlaidService()
    ml_advisor = MLInvestmentAdvisor()
    transaction_analyzer = TransactionAnalyzer()

def main():
    """Main application entry point."""
    # Sidebar navigation
    st.sidebar.title("🤖 MicroInvest AI")
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'connected_accounts' not in st.session_state:
        st.session_state.connected_accounts = []
    if 'transaction_data' not in st.session_state:
        st.session_state.transaction_data = pd.DataFrame()
    
    # Navigation menu
    pages = {
        'welcome': '🏠 Welcome',
        'connect_bank': '🏦 Connect Bank',
        'questionnaire': '📋 Investment Profile',
        'ai_insights': '🧠 AI Insights',
        'portfolio': '📊 Portfolio',
        'spending_analysis': '💳 Spending Analysis',
        'market_predictions': '📈 Market Predictions',
        'goals': '🎯 Goals'
    }
    
    selected_page = st.sidebar.selectbox(
        "Navigate to:",
        options=list(pages.keys()),
        format_func=lambda x: pages[x],
        index=list(pages.keys()).index(st.session_state.current_page)
    )
    
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()
    
    # Display current page
    if st.session_state.current_page == 'welcome':
        show_welcome_page()
    elif st.session_state.current_page == 'connect_bank':
        show_connect_bank_page()
    elif st.session_state.current_page == 'questionnaire':
        show_questionnaire_page()
    elif st.session_state.current_page == 'ai_insights':
        show_ai_insights_page()
    elif st.session_state.current_page == 'portfolio':
        show_portfolio_page()
    elif st.session_state.current_page == 'spending_analysis':
        show_spending_analysis_page()
    elif st.session_state.current_page == 'market_predictions':
        show_market_predictions_page()
    elif st.session_state.current_page == 'goals':
        show_goals_page()

def show_welcome_page():
    """Enhanced welcome page with ML features."""
    st.markdown("""
    <div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem; color: white;'>
        <div style='background: rgba(255,255,255,0.15); display: inline-block; padding: 0.75rem 1.5rem; border-radius: 25px; margin-bottom: 1.5rem;'>
            🤖 AI-Powered Investment Platform
        </div>
        <h1 style='font-size: 3.5rem; margin: 1.5rem 0; color: white; font-weight: 700;'>Smart Investing with <span style='color: #4CAF50;'>Machine Learning</span></h1>
        <p style='font-size: 1.3rem; margin: 1.5rem 0; opacity: 0.95; max-width: 600px; margin-left: auto; margin-right: auto;'>Connect your bank account for real-time spending analysis and get ML-powered investment recommendations tailored to your financial behavior.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🏦</div>
            <h3>Bank Integration</h3>
            <p>Securely connect your bank accounts via Plaid for real-time transaction analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🧠</div>
            <h3>ML Predictions</h3>
            <p>Advanced machine learning algorithms predict optimal investment strategies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📊</div>
            <h3>Smart Analytics</h3>
            <p>Automated spending categorization and personalized financial insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Call to action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Your AI Investment Journey", type="primary", use_container_width=True):
            st.session_state.current_page = "connect_bank"
            st.rerun()

def show_connect_bank_page():
    """Bank connection page with Plaid integration."""
    st.title("🏦 Connect Your Bank Account")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.error("Enhanced features are not available. Please install required dependencies.")
        return
    
    st.markdown("""
    Connect your bank account securely through Plaid to enable:
    - **Real-time transaction analysis**
    - **Automated spending categorization**
    - **ML-powered investment recommendations**
    - **Personalized financial insights**
    """)
    
    # Connection status
    if st.session_state.connected_accounts:
        st.success(f"✅ Connected {len(st.session_state.connected_accounts)} account(s)")
        
        for account in st.session_state.connected_accounts:
            with st.expander(f"Account: {account['name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Balance", f"${account['balance']:,.2f}")
                with col2:
                    st.metric("Available", f"${account['available_balance']:,.2f}")
    else:
        st.info("No accounts connected yet")
    
    # Connection options
    st.markdown("### Connection Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔗 Connect Real Bank Account", type="primary", use_container_width=True):
            st.info("In production, this would open Plaid Link for secure bank connection.")
            # In a real implementation, this would:
            # 1. Create a link token
            # 2. Open Plaid Link
            # 3. Exchange public token for access token
            # 4. Store access token securely
            
    with col2:
        if st.button("📊 Use Demo Data", use_container_width=True):
            # Load demo data
            demo_accounts = plaid_service.get_accounts("")  # Empty token for mock data
            demo_transactions = plaid_service.get_transactions("", days=90)
            
            st.session_state.connected_accounts = demo_accounts
            st.session_state.transaction_data = demo_transactions
            
            st.success("Demo data loaded successfully!")
            st.rerun()
    
    # Show transaction preview if data exists
    if not st.session_state.transaction_data.empty:
        st.markdown("### Recent Transactions Preview")
        preview_df = st.session_state.transaction_data.head(10)
        st.dataframe(preview_df[['date', 'name', 'amount', 'category']], use_container_width=True)
        
        if st.button("Continue to AI Analysis →", type="primary"):
            st.session_state.current_page = "ai_insights"
            st.rerun()

def show_ai_insights_page():
    """AI-powered insights page."""
    st.title("🧠 AI Financial Insights")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.error("AI features are not available.")
        return
    
    if st.session_state.transaction_data.empty:
        st.warning("Please connect your bank account first to see AI insights.")
        if st.button("Connect Bank Account"):
            st.session_state.current_page = "connect_bank"
            st.rerun()
        return
    
    # Analyze transactions with ML
    with st.spinner("🤖 AI is analyzing your financial data..."):
        analysis = transaction_analyzer.analyze_transactions(st.session_state.transaction_data)
    
    # Display insights
    st.markdown("## 📊 Spending Analysis")
    
    # Summary metrics
    summary = analysis['summary_stats']
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Transactions", summary['total_transactions'])
        with col2:
            st.metric("Total Spending", f"${summary['total_spending']:,.2f}")
        with col3:
            st.metric("Avg Transaction", f"${summary['average_transaction']:,.2f}")
        with col4:
            st.metric("Categories", summary['categories_count'])
    
    # Spending patterns
    patterns = analysis['spending_patterns']
    if patterns:
        st.markdown("### 💳 Spending Patterns")
        
        # Category breakdown
        if 'spending_by_category' in patterns:
            fig_cat = px.pie(
                values=list(patterns['spending_by_category'].values()),
                names=list(patterns['spending_by_category'].keys()),
                title="Spending by Category"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        
        # Daily spending pattern
        if 'spending_by_day' in patterns:
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_spending = patterns['spending_by_day']
            
            fig_days = px.bar(
                x=[day for day in days_order if day in day_spending],
                y=[day_spending[day] for day in days_order if day in day_spending],
                title="Spending by Day of Week"
            )
            st.plotly_chart(fig_days, use_container_width=True)
    
    # Anomalies
    anomalies = analysis['anomalies']
    if anomalies:
        st.markdown("### 🚨 Unusual Transactions")
        for anomaly in anomalies[:5]:
            severity_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            st.write(f"{severity_color.get(anomaly['severity'], '🟡')} {anomaly['description']}")
    
    # Investment capacity prediction
    investment_capacity = analysis['investment_capacity']
    if investment_capacity and investment_capacity['recommended_monthly_investment'] > 0:
        st.markdown("### 💰 AI Investment Recommendation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Recommended Monthly Investment", 
                f"${investment_capacity['recommended_monthly_investment']:,.0f}",
                help="Based on your spending patterns and income analysis"
            )
        with col2:
            st.metric(
                "Confidence Level", 
                f"{investment_capacity['confidence']:.0f}%",
                help="AI confidence in this recommendation"
            )
        
        st.info(investment_capacity.get('investment_rationale', ''))
    
    # Optimization tips
    optimization_tips = analysis['optimization_tips']
    if optimization_tips:
        st.markdown("### 💡 AI Optimization Tips")
        for tip in optimization_tips[:3]:
            priority_emoji = {"high": "🔥", "medium": "⚡", "low": "💡"}
            st.write(f"{priority_emoji.get(tip['priority'], '💡')} {tip['suggestion']}")
            if 'potential_savings' in tip:
                st.write(f"   💰 Potential monthly savings: ${tip['potential_savings']:,.0f}")

def show_spending_analysis_page():
    """Detailed spending analysis page."""
    st.title("💳 Advanced Spending Analysis")
    
    if st.session_state.transaction_data.empty:
        st.warning("Please connect your bank account to see spending analysis.")
        return
    
    # Time period selector
    col1, col2 = st.columns(2)
    with col1:
        days_back = st.selectbox("Analysis Period", [30, 60, 90, 180], index=2)
    with col2:
        category_filter = st.multiselect(
            "Filter Categories",
            options=st.session_state.transaction_data['category'].unique(),
            default=[]
        )
    
    # Filter data
    filtered_data = st.session_state.transaction_data.copy()
    if category_filter:
        filtered_data = filtered_data[filtered_data['category'].isin(category_filter)]
    
    # Analyze filtered data
    if ENHANCED_FEATURES_AVAILABLE:
        analysis = transaction_analyzer.analyze_transactions(filtered_data)
        
        # Spending trends
        st.markdown("## 📈 Spending Trends")
        
        # Create daily spending chart
        daily_spending = filtered_data[filtered_data['amount'] > 0].groupby('date')['amount'].sum().reset_index()
        daily_spending['date'] = pd.to_datetime(daily_spending['date'])
        
        fig_trend = px.line(daily_spending, x='date', y='amount', title="Daily Spending Trend")
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Category analysis
        st.markdown("## 🏷️ Category Deep Dive")
        
        spending_by_cat = filtered_data[filtered_data['amount'] > 0].groupby('category').agg({
            'amount': ['sum', 'mean', 'count']
        }).round(2)
        
        spending_by_cat.columns = ['Total', 'Average', 'Count']
        st.dataframe(spending_by_cat, use_container_width=True)
        
        # Merchant analysis
        st.markdown("## 🏪 Top Merchants")
        
        merchant_spending = filtered_data[filtered_data['amount'] > 0].groupby('merchant_name')['amount'].sum().nlargest(10)
        
        fig_merchants = px.bar(
            x=merchant_spending.values,
            y=merchant_spending.index,
            orientation='h',
            title="Top 10 Merchants by Spending"
        )
        st.plotly_chart(fig_merchants, use_container_width=True)

def show_market_predictions_page():
    """Market predictions using ML."""
    st.title("📈 AI Market Predictions")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.error("ML features are not available.")
        return
    
    # Generate market predictions
    with st.spinner("🤖 AI is analyzing market trends..."):
        # Use empty DataFrame to trigger synthetic data generation
        market_prediction = ml_advisor.predict_market_trends(pd.DataFrame())
    
    # Display predictions
    st.markdown("## 🔮 Market Outlook")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bullish_prob = market_prediction['bullish_probability']
        st.metric("Bullish Probability", f"{bullish_prob:.1%}")
        
        # Color-coded indicator
        if bullish_prob > 0.6:
            st.success("🟢 Bullish Market")
        elif bullish_prob < 0.4:
            st.error("🔴 Bearish Market")
        else:
            st.warning("🟡 Neutral Market")
    
    with col2:
        st.metric("Trend Direction", market_prediction['trend_direction'].title())
    
    with col3:
        st.metric("Confidence", f"{market_prediction['confidence']:.0f}%")
    
    # Market outlook
    st.markdown("### 📊 AI Analysis")
    st.info(market_prediction['outlook'])
    
    # Recommendations
    st.markdown("### 💡 AI Recommendations")
    for i, recommendation in enumerate(market_prediction['recommended_actions'], 1):
        st.write(f"{i}. {recommendation}")
    
    # Simulated market data visualization
    st.markdown("### 📈 Market Trend Visualization")
    
    # Generate sample market data for visualization
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    
    # Simulate market data based on prediction
    trend_factor = 1.0005 if bullish_prob > 0.5 else 0.9995
    prices = [100]
    
    for _ in range(len(dates)-1):
        daily_return = np.random.normal(0.001 * trend_factor, 0.02)
        prices.append(prices[-1] * (1 + daily_return))
    
    market_df = pd.DataFrame({
        'Date': dates,
        'Price': prices
    })
    
    fig_market = px.line(market_df, x='Date', y='Price', title="Predicted Market Trend")
    st.plotly_chart(fig_market, use_container_width=True)

def show_portfolio_page():
    """Enhanced portfolio page with ML recommendations."""
    st.title("📊 AI-Optimized Portfolio")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.warning("Enhanced ML features are not available. Using basic recommendations.")
        return
    
    # Get user profile data
    user_profile = st.session_state.get('questionnaire_data', {})
    transaction_data = st.session_state.transaction_data
    
    if not user_profile:
        st.warning("Please complete the investment questionnaire first.")
        if st.button("Go to Questionnaire"):
            st.session_state.current_page = "questionnaire"
            st.rerun()
        return
    
    # Generate ML-powered portfolio recommendation
    with st.spinner("🤖 AI is optimizing your portfolio..."):
        portfolio_allocation = ml_advisor.predict_optimal_allocation(user_profile, transaction_data)
        
        # Mock market conditions for return prediction
        market_conditions = {
            'volatility': 0.15,
            'interest_rate': 0.05,
            'inflation': 0.03
        }
        
        return_prediction = ml_advisor.predict_return_prediction(portfolio_allocation, market_conditions)
    
    # Display portfolio allocation
    st.markdown("## 🎯 AI-Recommended Allocation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stocks_pct = portfolio_allocation['stocks'] * 100
        st.metric("Stocks", f"{stocks_pct:.1f}%")
        st.progress(portfolio_allocation['stocks'])
    
    with col2:
        bonds_pct = portfolio_allocation['bonds'] * 100
        st.metric("Bonds", f"{bonds_pct:.1f}%")
        st.progress(portfolio_allocation['bonds'])
    
    with col3:
        alts_pct = portfolio_allocation.get('alternatives', 0) * 100
        st.metric("Alternatives", f"{alts_pct:.1f}%")
        st.progress(portfolio_allocation.get('alternatives', 0))
    
    # AI reasoning
    st.markdown("### 🧠 AI Reasoning")
    st.info(portfolio_allocation.get('reasoning', 'Portfolio optimized based on your profile and spending patterns.'))
    
    # Expected returns
    st.markdown("### 📈 Expected Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        expected_return = return_prediction.get('expected_annual_return', 0.08)
        st.metric("Expected Annual Return", f"{expected_return:.1%}")
    
    with col2:
        volatility = return_prediction.get('volatility', 0.12)
        st.metric("Expected Volatility", f"{volatility:.1%}")
    
    with col3:
        sharpe_ratio = return_prediction.get('sharpe_ratio', 0.5)
        st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
    
    # Risk assessment
    risk_level = return_prediction.get('risk_level', 'Medium')
    risk_colors = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
    st.markdown(f"**Risk Level:** {risk_colors.get(risk_level, '🟡')} {risk_level}")

def show_questionnaire_page():
    """Enhanced questionnaire with ML-powered suggestions."""
    st.title("📋 Investment Profile Questionnaire")
    
    # Pre-fill with transaction insights if available
    suggested_investment = 100
    if not st.session_state.transaction_data.empty and ENHANCED_FEATURES_AVAILABLE:
        with st.spinner("Analyzing your spending patterns..."):
            analysis = transaction_analyzer.analyze_transactions(st.session_state.transaction_data)
            investment_capacity = analysis.get('investment_capacity', {})
            suggested_investment = investment_capacity.get('recommended_monthly_investment', 100)
    
    with st.form("enhanced_questionnaire"):
        # Basic information
        st.markdown("### 👤 Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=25)
            monthly_income = st.number_input("Monthly Income ($)", min_value=0, value=2000)
        
        with col2:
            student_status = st.selectbox("Status", 
                ["Undergraduate", "Graduate", "Recent Graduate", "Working Professional"])
            investment_experience = st.selectbox("Investment Experience", 
                ["Beginner", "Some Experience", "Experienced"])
        
        # Investment details with AI suggestion
        st.markdown("### 💰 Investment Details")
        
        if suggested_investment != 100:
            st.info(f"💡 AI Suggestion: Based on your spending patterns, we recommend ${suggested_investment:.0f}/month")
        
        monthly_investment = st.number_input(
            "Monthly Investment Amount ($)", 
            min_value=10, 
            max_value=5000, 
            value=int(suggested_investment),
            help="AI-suggested amount based on your transaction analysis"
        )
        
        risk_tolerance = st.radio(
            "Risk Tolerance:",
            ["Conservative (Low Risk)", "Balanced (Medium Risk)", "Growth-Focused (High Risk)"]
        )
        
        investment_goal = st.selectbox(
            "Primary Investment Goal:",
            ["Build Emergency Fund", "Save for Laptop/Electronics", "Build Long-term Wealth", 
             "Save for Textbooks", "Save for Travel", "Graduation Goal"]
        )
        
        time_horizon = st.selectbox(
            "Time Horizon:",
            ["3 months", "6 months", "1 year", "2 years", "5+ years"]
        )
        
        submitted = st.form_submit_button("🤖 Get AI-Powered Recommendations", type="primary")
        
        if submitted:
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
            
            st.success("Profile saved! Redirecting to AI insights...")
            st.session_state.current_page = "portfolio"
            st.rerun()

def show_goals_page():
    """Investment goals tracking page."""
    st.title("🎯 Investment Goals")
    
    # Goal setting interface
    st.markdown("### Set Your Financial Goals")
    
    with st.form("goal_form"):
        goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund")
        target_amount = st.number_input("Target Amount ($)", min_value=100, value=1000)
        target_date = st.date_input("Target Date", value=datetime.now() + timedelta(days=365))
        
        if st.form_submit_button("Add Goal"):
            if 'goals' not in st.session_state:
                st.session_state.goals = []
            
            st.session_state.goals.append({
                'name': goal_name,
                'target_amount': target_amount,
                'target_date': target_date,
                'current_amount': 0
            })
            st.success(f"Goal '{goal_name}' added!")
    
    # Display existing goals
    if 'goals' in st.session_state and st.session_state.goals:
        st.markdown("### Your Goals")
        
        for i, goal in enumerate(st.session_state.goals):
            with st.expander(f"📌 {goal['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Target", f"${goal['target_amount']:,.2f}")
                    st.metric("Progress", f"${goal['current_amount']:,.2f}")
                
                with col2:
                    progress = goal['current_amount'] / goal['target_amount']
                    st.metric("Completion", f"{progress:.1%}")
                    st.progress(min(1.0, progress))
                
                # Update progress
                new_amount = st.number_input(
                    f"Update progress for {goal['name']}", 
                    min_value=0.0, 
                    value=float(goal['current_amount']),
                    key=f"goal_{i}"
                )
                
                if st.button(f"Update {goal['name']}", key=f"update_{i}"):
                    st.session_state.goals[i]['current_amount'] = new_amount
                    st.rerun()

if __name__ == "__main__":
    main()
