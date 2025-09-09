import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def show_portfolio_page():
    """Display the user's portfolio dashboard."""
    # Set the current page in session state
    st.session_state.current_page = 'portfolio'
    
    # Check if user has completed the questionnaire
    if not st.session_state.get('questionnaire_completed', False):
        st.warning("Please complete the questionnaire to view your portfolio.")
        if st.button("Go to Questionnaire"):
            st.session_state.current_page = 'questionnaire'
            st.rerun()
        return
    
    # Get portfolio data from session state
    portfolio = st.session_state.get('portfolio', {})
    
    # Page header
    st.title("My Investment Portfolio")
    
    # Portfolio summary cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Risk Profile", portfolio.get('risk_profile', 'N/A'))
    
    with col2:
        st.metric("Expected Return", f"{portfolio.get('expected_return', 0) * 100:.1f}%")
    
    with col3:
        st.metric("Portfolio Volatility", f"{portfolio.get('volatility', 0) * 100:.1f}%")
    
    # Portfolio allocation chart
    st.markdown("### Asset Allocation")
    
    # Create a donut chart for asset allocation
    if 'asset_allocation' in portfolio:
        df_allocation = pd.DataFrame({
            'Asset': list(portfolio['asset_allocation'].keys()),
            'Allocation': list(portfolio['asset_allocation'].values())
        })
        
        # Create a donut chart
        fig = px.pie(
            df_allocation, 
            values='Allocation', 
            names='Asset', 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        
        # Update layout
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="%{label}: <b>%{percent}</b>"
        )
        
        fig.update_layout(
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=0),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Portfolio performance section
    st.markdown("### Projected Performance")
    
    # Generate sample performance data
    def generate_performance_data(initial_investment, monthly_contribution, years, expected_return, volatility):
        months = years * 12
        dates = [datetime.now() + timedelta(days=30 * i) for i in range(months + 1)]
        
        # Generate random returns with the given expected return and volatility
        np.random.seed(42)  # For reproducibility
        monthly_returns = np.random.normal(
            (1 + expected_return) ** (1/12) - 1,  # Convert annual to monthly return
            volatility / np.sqrt(12),  # Convert annual to monthly volatility
            months
        )
        
        # Calculate portfolio values
        values = [initial_investment]
        for i in range(months):
            new_value = (values[-1] + monthly_contribution) * (1 + monthly_returns[i])
            values.append(new_value)
        
        return pd.DataFrame({
            'Date': dates[:len(values)],
            'Portfolio Value': values,
            'Cumulative Investment': [initial_investment + monthly_contribution * i for i in range(len(values))]
        })
    
    # Get user inputs from questionnaire
    initial_investment = st.session_state.questionnaire_data['financial_info'].get('savings', 1000)
    monthly_contribution = st.session_state.questionnaire_data['financial_info'].get('monthly_savings', 100)
    years = 10  # Default projection period
    
    # Generate performance data
    df_performance = generate_performance_data(
        initial_investment,
        monthly_contribution,
        years,
        portfolio.get('expected_return', 0.07),
        portfolio.get('volatility', 0.15)
    )
    
    # Create performance chart
    fig = px.area(
        df_performance,
        x='Date',
        y=['Portfolio Value', 'Cumulative Investment'],
        title=f"{years}-Year Projection",
        labels={'value': 'Value ($)', 'variable': 'Metric'},
        color_discrete_map={
            'Portfolio Value': '#2563eb',
            'Cumulative Investment': '#9ca3af'
        }
    )
    
    # Update layout
    fig.update_layout(
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        yaxis_tickprefix='$',
        yaxis_tickformat=',.0f',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Portfolio breakdown by asset class
    st.markdown("### Asset Class Breakdown")
    
    if 'asset_allocation' in portfolio:
        # Create a DataFrame for the asset classes
        df_assets = pd.DataFrame({
            'Asset Class': list(portfolio['asset_allocation'].keys()),
            'Allocation (%)': list(portfolio['asset_allocation'].values())
        })
        
        # Sort by allocation
        df_assets = df_assets.sort_values('Allocation (%)', ascending=False)
        
        # Display as a bar chart
        fig = px.bar(
            df_assets,
            x='Asset Class',
            y='Allocation (%)',
            text='Allocation (%)',
            color='Asset Class',
            color_discrete_sequence=px.colors.sequential.Blues_r,
            title="Portfolio Allocation by Asset Class"
        )
        
        # Update layout
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            hovertemplate='%{x}: <b>%{y:.1f}%</b>',
            marker_line_color='rgba(0,0,0,0.2)',
            marker_line_width=1
        )
        
        fig.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Allocation (%)",
            yaxis_ticksuffix='%',
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommended actions
    st.markdown("### Recommended Actions")
    
    # Create columns for action cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #f8fafc; border-radius: 0.5rem; padding: 1rem; height: 100%;'>
            <h4>Rebalance Portfolio</h4>
            <p>Consider rebalancing your portfolio to maintain your target asset allocation.</p>
            <button style='background-color: #2563eb; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer;'>Rebalance Now</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #f8fafc; border-radius: 0.5rem; padding: 1rem; height: 100%;'>
            <h4>Increase Contributions</h4>
            <p>Consider increasing your monthly contributions to reach your goals faster.</p>
            <button style='background-color: #2563eb; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer;'>Adjust Plan</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #f8fafc; border-radius: 0.5rem; padding: 1rem; height: 100%;'>
            <h4>Tax-Loss Harvesting</h4>
            <p>Consider tax-loss harvesting to offset capital gains.</p>
            <button style='background-color: #2563eb; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer;'>Learn More</button>
        </div>
        """, unsafe_allow_html=True)
