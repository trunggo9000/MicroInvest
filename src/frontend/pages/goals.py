import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def show_goals_page():
    """Display and manage the user's investment goals."""
    # Set the current page in session state
    st.session_state.current_page = 'goals'
    
    # Check if user has completed the questionnaire
    if not st.session_state.get('questionnaire_completed', False):
        st.warning("Please complete the questionnaire to set and track your investment goals.")
        if st.button("Go to Questionnaire"):
            st.session_state.current_page = 'questionnaire'
            st.rerun()
        return
    
    # Initialize goals in session state if not exists
    if 'goals' not in st.session_state:
        st.session_state.goals = []
    
    # Page header
    st.title("My Investment Goals")
    
    # Add goal button
    if st.button("+ Add New Goal", type="primary"):
        st.session_state.show_goal_form = True
    
    # Add goal form
    if st.session_state.get('show_goal_form', False):
        with st.form("goal_form"):
            st.subheader("Create New Goal")
            
            col1, col2 = st.columns(2)
            
            with col1:
                goal_name = st.text_input("Goal Name", placeholder="e.g., Buy a House, Retirement")
                target_amount = st.number_input("Target Amount ($)", min_value=100, step=100, value=10000)
                
            with col2:
                goal_type = st.selectbox(
                    "Goal Type",
                    ["Wealth Accumulation", "Retirement", "Major Purchase", "Education", "Other"]
                )
                target_date = st.date_input("Target Date", min_value=datetime.now().date() + timedelta(days=30))
            
            priority = st.select_slider("Priority", ["Low", "Medium", "High"], value="Medium")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("Save Goal", type="primary"):
                    if goal_name and target_amount > 0:
                        new_goal = {
                            "id": len(st.session_state.goals) + 1,
                            "name": goal_name,
                            "type": goal_type,
                            "target_amount": target_amount,
                            "current_amount": 0,
                            "target_date": target_date,
                            "priority": priority,
                            "created_at": datetime.now().strftime("%Y-%m-%d"),
                            "status": "In Progress"
                        }
                        st.session_state.goals.append(new_goal)
                        st.session_state.show_goal_form = False
                        st.rerun()
            
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_goal_form = False
                    st.rerun()
    
    # Display goals
    if not st.session_state.goals:
        st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem; background-color: #f8fafc; border-radius: 0.5rem; margin-top: 1rem;'>
            <h3>No Goals Yet</h3>
            <p>Create your first investment goal to get started!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display goals in tabs by status
        tab1, tab2, tab3 = st.tabs(["All Goals", "In Progress", "Completed"])
        
        with tab1:
            _display_goals(st.session_state.goals)
        
        with tab2:
            in_progress_goals = [g for g in st.session_state.goals if g["status"] == "In Progress"]
            _display_goals(in_progress_goals)
        
        with tab3:
            completed_goals = [g for g in st.session_state.goals if g["status"] == "Completed"]
            _display_goals(completed_goals)

def _display_goals(goals):
    """Helper function to display a list of goals."""
    if not goals:
        st.info("No goals found in this category.")
        return
    
    for goal in goals:
        with st.container():
            # Calculate progress
            progress = min(100, (goal["current_amount"] / goal["target_amount"]) * 100) if goal["target_amount"] > 0 else 0
            days_left = (goal["target_date"] - datetime.now().date()).days if isinstance(goal["target_date"], datetime) else 0
            
            # Determine progress bar color based on priority
            priority_colors = {
                "High": "#f87171",  # Red
                "Medium": "#fbbf24",  # Yellow
                "Low": "#4ade80"  # Green
            }
            
            st.markdown(f"""
            <div style='background-color: white; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;'>
                    <div>
                        <h3 style='margin: 0 0 0.5rem 0;'>{goal['name']}</h3>
                        <div style='display: flex; gap: 1rem; font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;'>
                            <span>Target: ${goal['target_amount']:,.0f}</span>
                            <span>•</span>
                            <span>Due: {goal['target_date'].strftime('%b %d, %Y') if hasattr(goal['target_date'], 'strftime') else goal['target_date']}</span>
                            <span>•</span>
                            <span>{goal['type']}</span>
                        </div>
                    </div>
                    <span style='background-color: {priority_colors[goal['priority']]}20; color: {priority_colors[goal['priority']]}; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600;'>
                        {goal['priority']} Priority
                    </span>
                </div>
                
                <div style='margin-bottom: 1rem;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 0.25rem;'>
                        <span style='font-size: 0.875rem; color: #4b5563;'>Progress</span>
                        <span style='font-weight: 600;'>{progress:.1f}%</span>
                    </div>
                    <div style='height: 8px; background-color: #e5e7eb; border-radius: 4px; overflow: hidden;'>
                        <div style='width: {progress}%; height: 100%; background-color: {priority_colors[goal['priority']]};'></div>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-top: 0.5rem;'>
                        <span style='font-size: 0.75rem; color: #6b7280;'>${goal['current_amount']:,.0f} of ${goal['target_amount']:,.0f}</span>
                        <span style='font-size: 0.75rem; color: #6b7280;'>{days_left} days remaining</span>
                    </div>
                </div>
                
                <div style='display: flex; gap: 0.5rem;'>
                    <button style='flex: 1; background-color: #f3f4f6; border: none; border-radius: 0.375rem; padding: 0.5rem 1rem; font-size: 0.875rem; cursor: pointer;' 
                            onclick='window.streamlitRunScript(`st.session_state.edit_goal_id = {goal['id']}`)'>
                        Edit
                    </button>
                    <button style='flex: 1; background-color: #2563eb; color: white; border: none; border-radius: 0.375rem; padding: 0.5rem 1rem; font-size: 0.875rem; cursor: pointer;' 
                            onclick='window.streamlitRunScript(`st.session_state.add_funds_id = {goal['id']}`)'>
                        Add Funds
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Add some space at the bottom
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Goal statistics
    if len(goals) > 0:
        st.markdown("## Goal Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_goals = len(goals)
            completed_goals = len([g for g in goals if g["status"] == "Completed"])
            completion_rate = (completed_goals / total_goals) * 100 if total_goals > 0 else 0
            
            st.markdown("""
            <div style='background-color: white; border-radius: 0.5rem; padding: 1.5rem; text-align: center; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);'>
                <div style='font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;'>Completion Rate</div>
                <div style='font-size: 2rem; font-weight: 700; color: #2563eb;'>{:.1f}%</div>
                <div style='font-size: 0.75rem; color: #9ca3af;'>{}/{} goals completed</div>
            </div>
            """.format(completion_rate, completed_goals, total_goals), unsafe_allow_html=True)
        
        with col2:
            total_target = sum(g["target_amount"] for g in goals)
            total_saved = sum(g["current_amount"] for g in goals)
            savings_rate = (total_saved / total_target) * 100 if total_target > 0 else 0
            
            st.markdown("""
            <div style='background-color: white; border-radius: 0.5rem; padding: 1.5rem; text-align: center; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);'>
                <div style='font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;'>Total Saved</div>
                <div style='font-size: 1.5rem; font-weight: 700; color: #2563eb;'>${:,.0f}</div>
                <div style='font-size: 0.75rem; color: #9ca3af;'>of ${:,.0f} target</div>
            </div>
            """.format(total_saved, total_target), unsafe_allow_html=True)
        
        with col3:
            # Calculate average time to goal
            active_goals = [g for g in goals if g["status"] == "In Progress"]
            if active_goals:
                today = datetime.now().date()
                days_to_goals = [
                    (g["target_date"] - today).days 
                    for g in active_goals 
                    if hasattr(g["target_date"], 'strftime')
                ]
                avg_days = int(np.mean(days_to_goals)) if days_to_goals else 0
                
                st.markdown("""
                <div style='background-color: white; border-radius: 0.5rem; padding: 1.5rem; text-align: center; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);'>
                    <div style='font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;'>Avg. Time to Goal</div>
                    <div style='font-size: 1.5rem; font-weight: 700; color: #2563eb;'>{:,.0f} days</div>
                    <div style='font-size: 0.75rem; color: #9ca3af;'>{} active goals</div>
                </div>
                """.format(avg_days, len(active_goals)), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background-color: white; border-radius: 0.5rem; padding: 1.5rem; text-align: center; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);'>
                    <div style='font-size: 0.875rem; color: #6b7280;'>No active goals</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Goal distribution chart
        st.markdown("### Goal Distribution")
        
        if goals:
            # Group goals by type
            df_goals = pd.DataFrame(goals)
            goal_types = df_goals['type'].value_counts().reset_index()
            goal_types.columns = ['Type', 'Count']
            
            # Create pie chart
            fig = px.pie(
                goal_types,
                values='Count',
                names='Type',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            
            # Update layout
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='%{label}: <b>%{percent}</b>'
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=30, b=0),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
