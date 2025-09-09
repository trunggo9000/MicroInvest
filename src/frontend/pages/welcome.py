import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

def show_welcome_page():
    """Display the welcome/introductory page."""
    # Set the current page in session state
    st.session_state.current_page = 'welcome'
    
    # Hero section
    st.markdown("""
    <style>
    .hero {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        padding: 4rem 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .hero p {
        font-size: 1.25rem;
        opacity: 0.9;
        margin-bottom: 2rem;
        max-width: 800px;
    }
    .btn {
        display: inline-block;
        background: white;
        color: #2563eb;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s;
    }
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .feature-card {
        background: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #2563eb;
    }
    .stat-card {
        background: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2563eb;
        margin: 0.5rem 0;
    }
    .stat-label {
        font-size: 0.875rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
    
    <div class='hero'>
        <h1>Start Investing Smarter Today</h1>
        <p>MicroInvest helps students build wealth through smart, automated investing. Get personalized portfolio recommendations based on your goals and risk tolerance.</p>
        <a href='#' class='btn' onclick='window.streamlitRunScript("st.session_state.current_page = \"questionnaire\"")'>Get Started</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("## Why Choose MicroInvest?")
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <h3>Smart Portfolio</h3>
            <p>Get AI-powered portfolio recommendations tailored to your risk tolerance and financial goals.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎯</div>
            <h3>Goal Tracking</h3>
            <p>Set and track your financial goals with personalized investment plans to help you achieve them.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🤖</div>
            <h3>AI Advisor</h3>
            <p>Get answers to all your investment questions with our AI-powered financial advisor.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("## Trusted by Students Worldwide")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-value'>10K+</div>
            <div class='stat-label'>Active Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-value'>$5M+</div>
            <div class='stat-label'>Invested</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-value'>4.9★</div>
            <div class='stat-label'>Average Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-value'>24/7</div>
            <div class='stat-label'>Support</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Investment growth visualization
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("## See Your Money Grow")
    
    # Generate sample investment growth data
    def generate_growth_data(initial_investment, monthly_contribution, years, return_rate):
        months = years * 12
        dates = [datetime.now() + timedelta(days=30 * i) for i in range(months + 1)]
        
        values = [initial_investment]
        for i in range(1, months + 1):
            previous_value = values[-1]
            monthly_return = 1 + (return_rate / 12) + np.random.normal(0, 0.02)  # Add some randomness
            new_value = (previous_value + monthly_contribution) * monthly_return
            values.append(new_value)
            
        return pd.DataFrame({
            'Date': dates[:len(values)],
            'Portfolio Value': values
        })
    
    # Create tabs for different scenarios
    tab1, tab2, tab3 = st.tabs(["Conservative", "Moderate", "Aggressive"])
    
    with tab1:
        df = generate_growth_data(1000, 100, 5, 0.05)  # 5% annual return
        fig = px.area(df, x='Date', y='Portfolio Value', title="Conservative Growth (5% annual return)")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        df = generate_growth_data(1000, 100, 5, 0.08)  # 8% annual return
        fig = px.area(df, x='Date', y='Portfolio Value', title="Moderate Growth (8% annual return)")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        df = generate_growth_data(1000, 100, 5, 0.12)  # 12% annual return
        fig = px.area(df, x='Date', y='Portfolio Value', title="Aggressive Growth (12% annual return)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Call to action
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("## Ready to Start Your Investment Journey?")
    st.markdown("Take our quick questionnaire to get personalized investment recommendations.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Get Started Now", type="primary", use_container_width=True):
            st.session_state.current_page = 'questionnaire'
