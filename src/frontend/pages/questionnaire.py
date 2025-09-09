import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any

def show_questionnaire_page():
    """Display the investment questionnaire page."""
    # Set the current page in session state
    st.session_state.current_page = 'questionnaire'
    
    # Page title and description
    st.title("Investment Questionnaire")
    st.markdown(
        "Answer a few questions to help us understand your financial situation "
        "and investment goals. This will help us create a personalized investment plan for you."
    )
    
    # Initialize session state for form data if it doesn't exist
    if 'questionnaire_data' not in st.session_state:
        st.session_state.questionnaire_data = {
            'personal_info': {},
            'financial_info': {},
            'investment_goals': {},
            'risk_assessment': {}
        }
    
    # Create form steps
    steps = ["Personal Information", "Financial Situation", "Investment Goals", "Risk Assessment"]
    current_step = st.session_state.get('current_questionnaire_step', 0)
    
    # Display progress bar
    progress = st.progress((current_step + 1) / len(steps))
    st.caption(f"Step {current_step + 1} of {len(steps)}: {steps[current_step]}")
    
    # Form container
    with st.form(key='questionnaire_form'):
        if current_step == 0:
            _render_personal_info_step()
        elif current_step == 1:
            _render_financial_info_step()
        elif current_step == 2:
            _render_goals_step()
        elif current_step == 3:
            _render_risk_assessment_step()
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if current_step > 0:
                if st.form_submit_button("← Previous", use_container_width=True):
                    st.session_state.current_questionnaire_step = current_step - 1
                    st.rerun()
        
        with col3:
            if current_step < len(steps) - 1:
                if st.form_submit_button("Next →", use_container_width=True, type="primary"):
                    # Validate current step before proceeding
                    if _validate_step(current_step):
                        st.session_state.current_questionnaire_step = current_step + 1
                        st.rerun()
            else:
                if st.form_submit_button("Get My Portfolio", type="primary", use_container_width=True):
                    if _validate_step(current_step):
                        _process_questionnaire()
                        st.session_state.current_page = 'portfolio'
                        st.rerun()

def _render_personal_info_step():
    """Render the personal information step of the questionnaire."""
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.questionnaire_data['personal_info']['first_name'] = st.text_input(
            "First Name",
            value=st.session_state.questionnaire_data['personal_info'].get('first_name', '')
        )
    
    with col2:
        st.session_state.questionnaire_data['personal_info']['last_name'] = st.text_input(
            "Last Name",
            value=st.session_state.questionnaire_data['personal_info'].get('last_name', '')
        )
    
    st.session_state.questionnaire_data['personal_info']['email'] = st.text_input(
        "Email Address",
        value=st.session_state.questionnaire_data['personal_info'].get('email', '')
    )
    
    st.session_state.questionnaire_data['personal_info']['age'] = st.slider(
        "Age",
        min_value=18,
        max_value=100,
        value=st.session_state.questionnaire_data['personal_info'].get('age', 25),
        step=1
    )
    
    st.session_state.questionnaire_data['personal_info']['education'] = st.selectbox(
        "Highest Level of Education",
        options=["High School", "Some College", "Bachelor's Degree", "Master's Degree", "PhD or Higher"],
        index=st.session_state.questionnaire_data['personal_info'].get('education_idx', 0)
    )
    
    # Store the index for the selectbox
    st.session_state.questionnaire_data['personal_info']['education_idx'] = [
        "High School", "Some College", "Bachelor's Degree", "Master's Degree", "PhD or Higher"
    ].index(st.session_state.questionnaire_data['personal_info']['education'])

def _render_financial_info_step():
    """Render the financial information step of the questionnaire."""
    st.subheader("Financial Situation")
    
    st.session_state.questionnaire_data['financial_info']['annual_income'] = st.selectbox(
        "Annual Income",
        options=[
            "Less than $20,000",
            "$20,000 - $40,000",
            "$40,001 - $70,000",
            "$70,001 - $100,000",
            "More than $100,000"
        ],
        index=st.session_state.questionnaire_data['financial_info'].get('income_idx', 1)
    )
    
    # Store the index for the selectbox
    st.session_state.questionnaire_data['financial_info']['income_idx'] = [
        "Less than $20,000",
        "$20,000 - $40,000",
        "$40,001 - $70,000",
        "$70,001 - $100,000",
        "More than $100,000"
    ].index(st.session_state.questionnaire_data['financial_info']['annual_income'])
    
    st.session_state.questionnaire_data['financial_info']['monthly_savings'] = st.number_input(
        "How much can you invest monthly? $",
        min_value=0,
        max_value=100000,
        value=st.session_state.questionnaire_data['financial_info'].get('monthly_savings', 100),
        step=10
    )
    
    st.session_state.questionnaire_data['financial_info']['savings'] = st.number_input(
        "Current Savings $",
        min_value=0,
        max_value=1000000,
        value=st.session_state.questionnaire_data['financial_info'].get('savings', 1000),
        step=100
    )
    
    st.session_state.questionnaire_data['financial_info']['debt'] = st.number_input(
        "Current Debt $",
        min_value=0,
        max_value=1000000,
        value=st.session_state.questionnaire_data['financial_info'].get('debt', 0),
        step=100
    )

def _render_goals_step():
    """Render the investment goals step of the questionnaire."""
    st.subheader("Investment Goals")
    
    st.session_state.questionnaire_data['investment_goals']['primary_goal'] = st.selectbox(
        "What is your primary investment goal?",
        options=[
            "Save for retirement",
            "Build an emergency fund",
            "Save for a house down payment",
            "Generate passive income",
            "Save for education",
            "Other"
        ],
        index=st.session_state.questionnaire_data['investment_goals'].get('primary_goal_idx', 0)
    )
    
    # Store the index for the selectbox
    st.session_state.questionnaire_data['investment_goals']['primary_goal_idx'] = [
        "Save for retirement",
        "Build an emergency fund",
        "Save for a house down payment",
        "Generate passive income",
        "Save for education",
        "Other"
    ].index(st.session_state.questionnaire_data['investment_goals']['primary_goal'])
    
    st.session_state.questionnaire_data['investment_goals']['time_horizon'] = st.select_slider(
        "Investment Time Horizon",
        options=["< 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
        value=st.session_state.questionnaire_data['investment_goals'].get('time_horizon', "5-10 years")
    )
    
    st.session_state.questionnaire_data['investment_goals']['target_amount'] = st.number_input(
        "Target Amount $",
        min_value=1000,
        max_value=10000000,
        value=st.session_state.questionnaire_data['investment_goals'].get('target_amount', 50000),
        step=1000
    )

def _render_risk_assessment_step():
    """Render the risk assessment step of the questionnaire."""
    st.subheader("Risk Assessment")
    
    st.markdown("### How would you react to a 20% drop in your investment value?")
    st.session_state.questionnaire_data['risk_assessment']['reaction_to_loss'] = st.radio(
        "",
        options=[
            "Sell all investments immediately",
            "Sell some investments to limit losses",
            "Hold and wait for recovery",
            "Invest more to take advantage of lower prices"
        ],
        index=st.session_state.questionnaire_data['risk_assessment'].get('reaction_to_loss_idx', 1),
        label_visibility="collapsed"
    )
    
    # Store the index for the radio button
    st.session_state.questionnaire_data['risk_assessment']['reaction_to_loss_idx'] = [
        "Sell all investments immediately",
        "Sell some investments to limit losses",
        "Hold and wait for recovery",
        "Invest more to take advantage of lower prices"
    ].index(st.session_state.questionnaire_data['risk_assessment']['reaction_to_loss'])
    
    st.markdown("### What is your experience with investing?")
    st.session_state.questionnaire_data['risk_assessment']['experience'] = st.select_slider(
        "",
        options=["None", "Beginner", "Intermediate", "Experienced", "Expert"],
        value=st.session_state.questionnaire_data['risk_assessment'].get('experience', "Beginner"),
        label_visibility="collapsed"
    )
    
    st.markdown("### What percentage of your investment are you willing to potentially lose in a year for higher returns?")
    risk_tolerance = st.slider(
        "",
        min_value=0,
        max_value=50,
        value=st.session_state.questionnaire_data['risk_assessment'].get('risk_tolerance', 10),
        step=5,
        format="%d%%",
        label_visibility="collapsed"
    )
    st.session_state.questionnaire_data['risk_assessment']['risk_tolerance'] = risk_tolerance
    
    # Display risk profile based on the slider
    risk_profile = ""
    if risk_tolerance < 10:
        risk_profile = "Conservative"
    elif risk_tolerance < 20:
        risk_profile = "Moderately Conservative"
    elif risk_tolerance < 30:
        risk_profile = "Moderate"
    elif risk_tolerance < 40:
        risk_profile = "Moderately Aggressive"
    else:
        risk_profile = "Aggressive"
    
    st.markdown(f"**Your risk profile:** {risk_profile}")
    
    # Store the risk profile
    st.session_state.questionnaire_data['risk_assessment']['risk_profile'] = risk_profile

def _validate_step(step: int) -> bool:
    """Validate the current step of the questionnaire."""
    if step == 0:  # Personal Info
        personal_info = st.session_state.questionnaire_data['personal_info']
        if not all([personal_info.get('first_name'), personal_info.get('last_name'), personal_info.get('email')]):
            st.error("Please fill in all required personal information.")
            return False
    
    return True

def _process_questionnaire():
    """Process the completed questionnaire and generate recommendations."""
    # Calculate risk score based on questionnaire responses
    risk_score = _calculate_risk_score()
    
    # Store the risk score in session state
    st.session_state.risk_score = risk_score
    
    # Generate portfolio recommendation based on risk score
    portfolio = _generate_portfolio_recommendation(risk_score)
    
    # Store the portfolio in session state
    st.session_state.portfolio = portfolio
    
    # Mark questionnaire as completed
    st.session_state.questionnaire_completed = True

def _calculate_risk_score() -> float:
    """Calculate a risk score based on questionnaire responses."""
    risk_factors = {
        'age': 0.2,
        'time_horizon': 0.25,
        'reaction_to_loss': 0.25,
        'experience': 0.15,
        'risk_tolerance': 0.15
    }
    
    # Age factor (younger = higher risk tolerance)
    age = st.session_state.questionnaire_data['personal_info']['age']
    age_score = min(1.0, (100 - age) / 80)  # Normalize to 0-1 range
    
    # Time horizon factor (longer = higher risk tolerance)
    time_horizon = st.session_state.questionnaire_data['investment_goals']['time_horizon']
    time_scores = {
        "< 1 year": 0.1,
        "1-3 years": 0.3,
        "3-5 years": 0.5,
        "5-10 years": 0.8,
        "10+ years": 1.0
    }
    time_score = time_scores.get(time_horizon, 0.5)
    
    # Reaction to loss factor
    reaction = st.session_state.questionnaire_data['risk_assessment']['reaction_to_loss']
    reaction_scores = {
        "Sell all investments immediately": 0.1,
        "Sell some investments to limit losses": 0.3,
        "Hold and wait for recovery": 0.7,
        "Invest more to take advantage of lower prices": 1.0
    }
    reaction_score = reaction_scores.get(reaction, 0.5)
    
    # Experience factor
    experience = st.session_state.questionnaire_data['risk_assessment']['experience']
    experience_scores = {
        "None": 0.2,
        "Beginner": 0.4,
        "Intermediate": 0.6,
        "Experienced": 0.8,
        "Expert": 1.0
    }
    experience_score = experience_scores.get(experience, 0.5)
    
    # Risk tolerance (from slider)
    risk_tolerance = st.session_state.questionnaire_data['risk_assessment']['risk_tolerance'] / 100.0
    
    # Calculate weighted risk score (0-1 scale)
    weighted_score = (
        age_score * risk_factors['age'] +
        time_score * risk_factors['time_horizon'] +
        reaction_score * risk_factors['reaction_to_loss'] +
        experience_score * risk_factors['experience'] +
        risk_tolerance * risk_factors['risk_tolerance']
    )
    
    # Ensure score is between 0 and 1
    return max(0.0, min(1.0, weighted_score))

def _generate_portfolio_recommendation(risk_score: float) -> Dict[str, Any]:
    """Generate a portfolio recommendation based on risk score."""
    # Define asset classes
    asset_classes = ["Stocks", "Bonds", "Real Estate", "Commodities", "Cash"]
    
    # Define portfolio templates based on risk score
    if risk_score < 0.2:
        # Very conservative
        allocation = {
            "Stocks": 20,
            "Bonds": 50,
            "Real Estate": 10,
            "Commodities": 5,
            "Cash": 15
        }
        profile = "Very Conservative"
    elif risk_score < 0.4:
        # Conservative
        allocation = {
            "Stocks": 40,
            "Bonds": 40,
            "Real Estate": 10,
            "Commodities": 5,
            "Cash": 5
        }
        profile = "Conservative"
    elif risk_score < 0.6:
        # Moderate
        allocation = {
            "Stocks": 60,
            "Bonds": 30,
            "Real Estate": 5,
            "Commodities": 3,
            "Cash": 2
        }
        profile = "Moderate"
    elif risk_score < 0.8:
        # Aggressive
        allocation = {
            "Stocks": 80,
            "Bonds": 15,
            "Real Estate": 3,
            "Commodities": 2,
            "Cash": 0
        }
        profile = "Aggressive"
    else:
        # Very aggressive
        allocation = {
            "Stocks": 95,
            "Bonds": 5,
            "Real Estate": 0,
            "Commodities": 0,
            "Cash": 0
        }
        profile = "Very Aggressive"
    
    # Calculate expected return and volatility based on risk profile
    expected_return = 0.03 + (risk_score * 0.08)  # 3% to 11% range
    volatility = 0.05 + (risk_score * 0.15)  # 5% to 20% range
    
    return {
        "asset_allocation": allocation,
        "risk_profile": profile,
        "expected_return": expected_return,
        "volatility": volatility,
        "sharpe_ratio": (expected_return - 0.02) / (volatility + 1e-10)  # Risk-free rate of 2%
    }
