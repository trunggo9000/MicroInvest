import streamlit as st
from typing import Dict, Any

def show_sidebar():
    """Display the application sidebar with navigation and user controls."""
    # Custom CSS for the sidebar
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background: #f8fafc;
        padding: 1.5rem 1rem;
    }
    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.375rem;
        color: #4b5563;
        text-decoration: none;
        transition: all 0.2s;
    }
    .nav-item:hover {
        background-color: #e2e8f0;
        color: #1e40af;
    }
    .nav-item.active {
        background-color: #dbeafe;
        color: #1e40af;
        font-weight: 500;
    }
    .nav-item i {
        margin-right: 0.75rem;
        width: 1.25rem;
        text-align: center;
    }
    .divider {
        height: 1px;
        background-color: #e2e8f0;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar content
    with st.sidebar:
        # User profile section (if logged in)
        if st.session_state.get('user_authenticated', False):
            st.markdown(
                f"""
                <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
                    <div style='width: 40px; height: 40px; border-radius: 50%; background-color: #2563eb; color: white; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; font-weight: 600;'>
                        {st.session_state.get('user_name', 'U')[0].upper()}
                    </div>
                    <div>
                        <div style='font-weight: 600;'>{st.session_state.get('user_name', 'User')}</div>
                        <div style='font-size: 0.75rem; color: #6b7280;'>Student Investor</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Navigation menu
        st.markdown("### Navigation")
        
        # Navigation items
        nav_items = [
            {"icon": "🏠", "label": "Dashboard", "page": "welcome"},
            {"icon": "📊", "label": "Portfolio", "page": "portfolio"},
            {"icon": "🎯", "label": "Goals", "page": "goals"},
            {"icon": "📈", "label": "Analysis", "page": "analysis"},
            {"icon": "❓", "label": "Questionnaire", "page": "questionnaire"},
        ]
        
        for item in nav_items:
            is_active = st.session_state.get('current_page', '') == item['page']
            st.markdown(
                f"""
                <a href='#' class='nav-item {'active' if is_active else ''}' 
                   onclick='window.event.preventDefault(); window.streamlitRunScript("st.session_state.current_page = '{item['page']}'")'>
                    <span>{item['icon']}</span>
                    <span>{item['label']}</span>
                </a>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Additional links
        st.markdown("### Resources")
        resource_items = [
            {"icon": "📚", "label": "Learn to Invest", "url": "#"},
            {"icon": "📱", "label": "Mobile App", "url": "#"},
            {"icon": "💬", "label": "Support", "url": "#"},
            {"icon": "⚙️", "label": "Settings", "url": "#"},
        ]
        
        for item in resource_items:
            st.markdown(
                f"""
                <a href='{item['url']}' class='nav-item'>
                    <span>{item['icon']}</span>
                    <span>{item['label']}</span>
                </a>
                """,
                unsafe_allow_html=True
            )
        
        # Footer
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='font-size: 0.75rem; color: #6b7280; margin-top: 1rem;'>
                <p>© 2025 MicroInvest</p>
                <p>v1.0.0</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add some spacing at the bottom
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

def get_sidebar_state() -> Dict[str, Any]:
    """Get the current state of sidebar components."""
    return {
        "risk_tolerance": st.session_state.get("risk_tolerance", "medium"),
        "investment_goal": st.session_state.get("investment_goal", "growth"),
        "time_horizon": st.session_state.get("time_horizon", 5),
    }

def update_sidebar_state(**kwargs):
    """Update the state of sidebar components."""
    for key, value in kwargs.items():
        st.session_state[key] = value
