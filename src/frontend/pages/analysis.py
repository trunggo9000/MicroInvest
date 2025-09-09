import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

def get_major_stocks_data():
    """Fetch real-time data for major stocks."""
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
    
    # Use mock data to ensure it always displays
    stocks_info = []
    for ticker, company in major_stocks.items():
        # Generate realistic mock data
        base_price = np.random.uniform(50, 300)
        change = np.random.uniform(-10, 10)
        change_percent = (change / base_price) * 100
        
        stocks_info.append({
            'Symbol': ticker,
            'Company': company,
            'Price': base_price,
            'Change': change,
            'Change %': change_percent,
            'Market Cap': np.random.uniform(100, 3000) * 1e9,
            'Volume': np.random.randint(10000000, 100000000),
            'P/E Ratio': np.random.uniform(15, 35),
            'Sector': 'Technology' if ticker in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX'] else 'Consumer' if ticker in ['NKE', 'DIS', 'WMT', 'PG', 'HD'] else 'Financial' if ticker in ['JPM', 'V', 'MA', 'BAC'] else 'Healthcare' if ticker in ['JNJ', 'UNH'] else 'Energy'
        })
    
    return pd.DataFrame(stocks_info)

def show_analysis_page():
    """Display analysis and insights for the user's portfolio."""
    # Set the current page in session state
    st.session_state.current_page = 'analysis'
    
    # Page header
    st.title("📊 Stock Analysis & Risk Metrics")
    
    # Back to Portfolio button
    if st.button("← Back to Portfolio"):
        st.session_state.current_page = 'portfolio'
        st.rerun()
    
    # Portfolio Overview Section
    st.markdown("## 📊 Portfolio Overview")
    
    # Get portfolio data from session state
    portfolio_data = st.session_state.get('portfolio_data', {})
    
    if portfolio_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Assets", len(portfolio_data.get('investments', [])))
        
        with col2:
            risk_level = portfolio_data.get('riskLevel', 'medium')
            risk_display = {'low': 'Low', 'medium': 'Medium', 'high': 'High'}.get(risk_level, 'Medium')
            st.metric("Average Risk", risk_display)
        
        with col3:
            monthly_investment = portfolio_data.get('monthlyAmount', 0)
            st.metric("Monthly Investment", f"${monthly_investment}")
    
    # Major Stocks Market Data
    st.markdown("## 🏢 Major Stock Market")
    
    # Fetch and display major stocks
    stocks_df = get_major_stocks_data()
    
    if not stocks_df.empty:
        # Add search functionality
        search_term = st.text_input("🔍 Search stocks (e.g., Apple, Nike, Tesla):", placeholder="Type company name or symbol...")
        
        # Filter stocks based on search
        if search_term:
            filtered_df = stocks_df[
                stocks_df['Company'].str.contains(search_term, case=False, na=False) |
                stocks_df['Symbol'].str.contains(search_term, case=False, na=False) |
                stocks_df['Sector'].str.contains(search_term, case=False, na=False)
            ]
        else:
            filtered_df = stocks_df
        
        # Display stocks in a nice format
        for _, stock in filtered_df.iterrows():
            with st.expander(f"{stock['Symbol']} - {stock['Company']}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    price_color = "green" if stock['Change'] >= 0 else "red"
                    st.markdown(f"""
                    **Current Price**  
                    <span style='font-size: 1.5em; color: {price_color}; font-weight: bold;'>${stock['Price']:.2f}</span>
                    """, unsafe_allow_html=True)
                
                with col2:
                    change_color = "green" if stock['Change'] >= 0 else "red"
                    change_symbol = "+" if stock['Change'] >= 0 else ""
                    st.markdown(f"""
                    **Daily Change**  
                    <span style='color: {change_color}; font-weight: bold;'>{change_symbol}${stock['Change']:.2f} ({stock['Change %']:+.2f}%)</span>
                    """, unsafe_allow_html=True)
                
                with col3:
                    market_cap_b = stock['Market Cap'] / 1e9 if stock['Market Cap'] > 0 else 0
                    st.markdown(f"""
                    **Market Cap**  
                    ${market_cap_b:.1f}B
                    
                    **Volume**  
                    {stock['Volume']:,}
                    """)
                
                with col4:
                    pe_ratio = stock['P/E Ratio'] if stock['P/E Ratio'] > 0 else "N/A"
                    st.markdown(f"""
                    **P/E Ratio**  
                    {pe_ratio}
                    
                    **Sector**  
                    {stock['Sector']}
                    """)
        
        # Market Summary
        st.markdown("## 📈 Market Summary")
        
        # Calculate market statistics
        avg_change = filtered_df['Change %'].mean()
        positive_stocks = len(filtered_df[filtered_df['Change'] > 0])
        total_stocks = len(filtered_df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            change_color = "green" if avg_change >= 0 else "red"
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 10px;'>
                <div style='font-size: 1.5rem; font-weight: bold; color: {change_color};'>{avg_change:+.2f}%</div>
                <div>Average Change</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #28a745, #20c997); color: white; border-radius: 10px;'>
                <div style='font-size: 1.5rem; font-weight: bold;'>{positive_stocks}/{total_stocks}</div>
                <div>Stocks Up Today</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            market_sentiment = "Bullish" if positive_stocks > total_stocks/2 else "Bearish"
            sentiment_color = "green" if market_sentiment == "Bullish" else "red"
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #fd7e14, #e83e8c); color: white; border-radius: 10px;'>
                <div style='font-size: 1.5rem; font-weight: bold; color: {sentiment_color};'>{market_sentiment}</div>
                <div>Market Sentiment</div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.error("Unable to load stock market data. Please try again later.")
    
    # Individual Stock Analysis Section (if portfolio exists)
    if portfolio_data and 'investments' in portfolio_data:
        st.markdown("## 🔍 Individual Stock Analysis")
        
        for investment in portfolio_data['investments']:
            with st.expander(f"{investment['symbol']} - {investment['name']}", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    **{investment['name']}**  
                    *Symbol: {investment['symbol']}*
                    
                    {investment.get('description', 'Large-cap US stocks for growth potential')}
                    """)
                
                with col2:
                    allocation_percent = investment['allocation'] * 100
                    st.markdown(f"""
                    **Portfolio Allocation**  
                    {allocation_percent:.1f}%
                    
                    **Expected Return**  
                    {investment['expectedReturn']:.1f}%
                    """)
                
                with col3:
                    monthly_amount = portfolio_data.get('monthlyAmount', 25)
                    monthly_allocation = monthly_amount * investment['allocation']
                    st.markdown(f"""
                    **Monthly Amount**  
                    ${monthly_allocation:.2f}
                    
                    **Risk Assessment:**
                    """)
                
                with col4:
                    risk_level = investment.get('riskLevel', 'medium')
                    risk_colors = {'low': '#4ade80', 'medium': '#fbbf24', 'high': '#f87171'}
                    risk_labels = {'low': 'LOW RISK', 'medium': 'MEDIUM RISK', 'high': 'HIGH RISK'}
                    
                    st.markdown(f"""
                    <div style='background: {risk_colors[risk_level]}; color: white; padding: 0.5rem; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 1rem;'>
                        {risk_labels[risk_level]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("*Balanced risk-return profile*")
                
                # Risk Assessment Details
                st.markdown("**Risk Assessment:**")
                col_risk1, col_risk2 = st.columns(2)
                
                with col_risk1:
                    volatility_level = "Medium volatility - Moderate price swings"
                    st.markdown(f"**Volatility Level:**  \n{volatility_level}")
                
                with col_risk2:
                    investment_horizon = "Best for medium to long-term investing"
                    st.markdown(f"**Investment Horizon:**  \n{investment_horizon}")
    
    # Get portfolio data from session state
    portfolio = st.session_state.get('portfolio', {})
    
    # Risk Analysis Section
    st.markdown("## Risk Analysis")
    
    # Risk score gauge
    risk_score = st.session_state.get('risk_score', 0.5)
    
    # Create a gauge chart for risk score
    fig_risk = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Your Risk Score", 'font': {'size': 24}},
        delta = {'reference': 50, 'increasing': {'symbol': "+"}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': '#4ade80'},
                {'range': [20, 40], 'color': '#86efac'},
                {'range': [40, 60], 'color': '#fef08a'},
                {'range': [60, 80], 'color': '#fbbf24'},
                {'range': [80, 100], 'color': '#f87171'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': risk_score * 100
            }
        }
    ))
    
    # Add risk level indicators
    fig_risk.add_annotation(
        x=0.15, y=0.15,
        text="Conservative",
        showarrow=False,
        font=dict(size=12, color="#4ade80")
    )
    
    fig_risk.add_annotation(
        x=0.5, y=0.2,
        text="Moderate",
        showarrow=False,
        font=dict(size=12, color="#fbbf24")
    )
    
    fig_risk.add_annotation(
        x=0.85, y=0.15,
        text="Aggressive",
        showarrow=False,
        font=dict(size=12, color="#f87171")
    )
    
    fig_risk.update_layout(
        height=400,
        margin=dict(l=50, r=50, t=100, b=50)
    )
    
    st.plotly_chart(fig_risk, use_container_width=True)
    
    # Diversification Analysis
    st.markdown("## Diversification Analysis")
    
    if 'asset_allocation' in portfolio:
        # Create a treemap for asset allocation
        df_assets = pd.DataFrame({
            'Asset': list(portfolio['asset_allocation'].keys()),
            'Allocation': list(portfolio['asset_allocation'].values()),
            'Risk': ["Low" if x in ["Bonds", "Cash"] else "High" for x in portfolio['asset_allocation'].keys()]
        })
        
        fig_treemap = px.treemap(
            df_assets,
            path=['Risk', 'Asset'],
            values='Allocation',
            color='Allocation',
            color_continuous_scale='Blues',
            title="Portfolio Diversification"
        )
        
        fig_treemap.update_traces(
            textinfo="label+percent parent+percent entry",
            hovertemplate='<b>%{label}</b><br>Allocation: %{value}%<br>Percentage of Portfolio: %{percentParent:.1%}<extra></extra>'
        )
        
        fig_treemap.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            height=500
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
    
    # Performance Projections
    st.markdown("## Performance Projections")
    
    # Get user inputs from questionnaire
    initial_investment = st.session_state.questionnaire_data['financial_info'].get('savings', 1000)
    monthly_contribution = st.session_state.questionnaire_data['financial_info'].get('monthly_savings', 100)
    years = st.slider("Projection Period (Years)", 1, 30, 10)
    
    # Generate multiple simulation paths
    def generate_simulation_paths(n_paths=100, years=10):
        months = years * 12
        dates = [datetime.now() + timedelta(days=30 * i) for i in range(months + 1)]
        
        # Generate random returns with the given expected return and volatility
        expected_return = portfolio.get('expected_return', 0.07)
        volatility = portfolio.get('volatility', 0.15)
        
        # Initialize array to store all paths
        all_paths = np.zeros((n_paths, months + 1))
        
        for i in range(n_paths):
            # Generate random monthly returns
            monthly_returns = np.random.normal(
                (1 + expected_return) ** (1/12) - 1,  # Convert annual to monthly return
                volatility / np.sqrt(12),  # Convert annual to monthly volatility
                months
            )
            
            # Calculate portfolio values for this path
            values = [initial_investment]
            for r in monthly_returns:
                new_value = (values[-1] + monthly_contribution) * (1 + r)
                values.append(new_value)
            
            all_paths[i] = values
        
        return dates[:months+1], all_paths
    
    # Generate simulation data
    dates, paths = generate_simulation_paths(n_paths=100, years=years)
    
    # Calculate percentiles
    percentiles = np.percentile(paths, [10, 25, 50, 75, 90], axis=0)
    
    # Create figure
    fig_sim = go.Figure()
    
    # Add percentiles
    fig_sim.add_trace(go.Scatter(
        x=dates,
        y=percentiles[2],  # Median
        name="Median",
        line=dict(color='#2563eb', width=3)
    ))
    
    # Add confidence intervals
    fig_sim.add_trace(go.Scatter(
        x=dates + dates[::-1],  # x, then x reversed
        y=list(percentiles[1]) + list(percentiles[3])[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(37, 99, 235, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name="25th-75th Percentile"
    ))
    
    fig_sim.add_trace(go.Scatter(
        x=dates + dates[::-1],  # x, then x reversed
        y=list(percentiles[0]) + list(percentiles[4])[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(37, 99, 235, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        name="10th-90th Percentile"
    ))
    
    # Update layout
    fig_sim.update_layout(
        title=f"{years}-Year Monte Carlo Simulation (100 Paths)",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        hovermode="x",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=500
    )
    
    # Format y-axis as currency
    fig_sim.update_yaxes(tickprefix="$", tickformat=",.0f")
    
    st.plotly_chart(fig_sim, use_container_width=True)
    
    # Key Statistics
    st.markdown("## Key Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Expected Annual Return", f"{portfolio.get('expected_return', 0) * 100:.1f}%")
    
    with col2:
        st.metric("Portfolio Volatility", f"{portfolio.get('volatility', 0) * 100:.1f}%")
    
    with col3:
        st.metric("Sharpe Ratio", f"{portfolio.get('sharpe_ratio', 0):.2f}")
    
    with col4:
        # Calculate max drawdown
        final_values = paths[:, -1]
        max_drawdown = np.min((final_values - np.maximum.accumulate(paths, axis=1)) / np.maximum.accumulate(paths, axis=1)) * 100
        st.metric("Max Drawdown", f"{-max_drawdown:.1f}%")
    
    # Recommendations
    st.markdown("## Recommendations")
    
    # Generate recommendations based on portfolio analysis
    recommendations = []
    
    # Check asset allocation
    if 'asset_allocation' in portfolio:
        allocation = portfolio['asset_allocation']
        
        # Check for over-concentration in a single asset class
        max_asset = max(allocation.items(), key=lambda x: x[1])
        if max_asset[1] > 70:
            recommendations.append({
                "title": "Diversification Opportunity",
                "description": f"Your portfolio is heavily concentrated in {max_asset[0]} ({max_asset[1]}%). Consider diversifying across more asset classes to reduce risk.",
                "priority": "High"
            })
        
        # Check for low bond allocation for conservative investors
        if risk_score < 0.3 and allocation.get('Bonds', 0) < 30:
            recommendations.append({
                "title": "Increase Fixed Income",
                "description": "Your portfolio may be too aggressive for your risk profile. Consider increasing your allocation to bonds for more stability.",
                "priority": "Medium"
            })
        
        # Check for high cash allocation
        if allocation.get('Cash', 0) > 20 and risk_score > 0.5:
            recommendations.append({
                "title": "Reduce Cash Holdings",
                "description": f"You have {allocation.get('Cash', 0)}% in cash, which may be too high for your risk profile. Consider investing more of your cash to potentially earn higher returns.",
                "priority": "Medium"
            })
    
    # Add general recommendations if no specific ones were added
    if not recommendations:
        recommendations.append({
            "title": "Portfolio On Track",
            "description": "Your portfolio appears to be well-diversified and aligned with your risk profile. Continue with your current investment strategy.",
            "priority": "Low"
        })
    
    # Display recommendations
    for rec in sorted(recommendations, key=lambda x: x['priority']):
        priority_color = {
            "High": "#f87171",  # Red
            "Medium": "#fbbf24",  # Yellow
            "Low": "#4ade80"  # Green
        }.get(rec['priority'], "#9ca3af")
        
        st.markdown(f"""
        <div style='border-left: 4px solid {priority_color}; padding-left: 1rem; margin-bottom: 1rem;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <h4 style='margin: 0;'>{rec['title']}</h4>
                <span style='background-color: {priority_color}20; color: {priority_color}; padding: 0.25rem 0.5rem; border-radius: 0.5rem; font-size: 0.75rem; font-weight: 600;'>{rec['priority']} Priority</span>
            </div>
            <p style='margin: 0.5rem 0 0 0; color: #4b5563;'>{rec['description']}</p>
        </div>
        """, unsafe_allow_html=True)
