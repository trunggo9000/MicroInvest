import streamlit as st

def show_header():
    """Display the application header with logo and navigation."""
    # Custom CSS for the header
    st.markdown("""
    <style>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 2rem;
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .header-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            """
            <div class="header">
                <div>
                    <h1 class="header-title">MicroInvest</h1>
                    <p class="header-subtitle">Smart Investment Planning for Students</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Show user status or login button
        if 'user_authenticated' in st.session_state and st.session_state.user_authenticated:
            st.markdown(
                f"""
                <div style='text-align: right; margin-top: 0.5rem;'>
                    <p style='margin: 0;'>Welcome back, <strong>{st.session_state.get('user_name', 'User')}</strong></p>
                    <a href='#' onclick='window.event.preventDefault(); window.streamlitRunScript("st.session_state.user_authenticated = False; st.session_state.user_name = ''")' style='color: #60a5fa; text-decoration: none; font-size: 0.9rem;'>Sign Out</a>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            if st.button("Sign In", key="sign_in_btn"):
                st.session_state.show_login_modal = True
    
    # Login modal
    if st.session_state.get('show_login_modal', False):
        show_login_modal()

def show_login_modal():
    """Display a login/signup modal."""
    # Custom CSS for the modal
    st.markdown("""
    <style>
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    .modal-content {
        background: white;
        padding: 2rem;
        border-radius: 0.5rem;
        width: 400px;
        max-width: 90%;
        position: relative;
    }
    .close-btn {
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        cursor: pointer;
    }
    .tab {
        display: inline-block;
        padding: 0.5rem 1rem;
        cursor: pointer;
        margin-right: 0.5rem;
        border-bottom: 2px solid transparent;
    }
    .tab.active {
        border-bottom: 2px solid #2563eb;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Modal content
    st.markdown("""
    <div class="modal">
        <div class="modal-content">
            <div class="close-btn" onclick='window.streamlitRunScript("st.session_state.show_login_modal = False")'>&times;</div>
            <h3 style='margin-top: 0;'>Welcome to MicroInvest</h3>
            
            <div style='margin-bottom: 1.5rem;'>
                <span class="tab active">Sign In</span>
                <span class="tab">Create Account</span>
            </div>
            
            <div>
                <div style='margin-bottom: 1rem;'>
                    <label style='display: block; margin-bottom: 0.25rem; font-weight: 500;'>Email</label>
                    <input type='email' id='login-email' style='width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 0.25rem;' placeholder='your@email.com'>
                </div>
                <div style='margin-bottom: 1.5rem;'>
                    <label style='display: block; margin-bottom: 0.25rem; font-weight: 500;'>Password</label>
                    <input type='password' id='login-password' style='width: 100%; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 0.25rem;' placeholder='••••••••'>
                </div>
                <button onclick='window.streamlitRunScript("""
                    f"""
                    st.session_state.user_authenticated = True;
                    st.session_state.user_name = document.getElementById('login-email').value.split('@')[0];
                    st.session_state.show_login_modal = False;
                    """
                """
                style='width: 100%; background-color: #2563eb; color: white; padding: 0.5rem; border: none; border-radius: 0.25rem; font-weight: 500; cursor: pointer;'>
                    Sign In
                </button>
                <p style='text-align: center; margin-top: 1rem; font-size: 0.875rem;'>
                    <a href='#' style='color: #2563eb; text-decoration: none;'>Forgot password?</a>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
