import streamlit as st
from database.db_manager import get_all_roles, get_resumes_for_role
from database.db_manager import get_db_session
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import joinedload  # Import joinedload for eager loading

def admin_dashboard():
    """Company admin dashboard"""
    if not st.session_state.get("is_admin", False):
        st.error("Access denied. You need admin privileges to view this page.")
        if st.button("Return to login"):
            st.session_state.page = "login"
            st.rerun()
        return
    
    st.title("Resume Analyzer - Admin Dashboard")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        dashboard_btn = st.button("Dashboard", key="dash_nav")
        roles_btn = st.button("Manage Roles", key="roles_nav")
        logout_btn = st.button("Logout", key="logout")
        
        if roles_btn:
            st.session_state.admin_page = "roles"
            st.rerun()
        
        if logout_btn:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "login"
            st.rerun()
    
    # Get all roles
    roles = get_all_roles()
    
    if not roles:
        st.warning("No job roles defined yet. Please create roles first.")
        if st.button("Create Roles"):
            st.session_state.admin_page = "roles"
            st.rerun()
        return
    
    # Role selection
    role_titles = [role.title for role in roles]
    role_dict = {role.title: role for role in roles}
    
    selected_role_title = st.selectbox("Select Job Role", role_titles)
    selected_role = role_dict[selected_role_title]
    
    # Display role information
    st.header(f"Role: {selected_role.title}")
    
    col1, col2, col3 = st.columns(3)
    
    # Format deadline
    deadline_str = selected_role.deadline.strftime("%Y-%m-%d")
    days_left = (selected_role.deadline - datetime.utcnow()).days
    
    with col1:
        st.metric("Status", "Active" if selected_role.is_active else "Inactive")
    with col2:
        st.metric("Deadline", deadline_str)
    with col3:
        st.metric("Days Left", days_left)
    
    st.subheader("Requirements")
    with st.expander("View Requirements"):
        st.write(selected_role.requirements)
    
    # Get resumes for selected role with eager loading
    resumes = get_resumes_for_role(selected_role.id)
    
    st.subheader(f"Applications ({len(resumes)})")
    
    if not resumes:
        st.info("No applications have been submitted for this role yet.")
        return
    
    # Create dataframe for display
    resume_data = []
    for resume in resumes:
        # Ensure the session is active while accessing relationships
        with get_db_session() as session:
            session.add(resume)  # Reattach the object to the session
            session.refresh(resume)  # Refresh the object
            resume_data.append({
                "Resume ID": resume.id,
                "Applicant": resume.user.username,  # Now this will work
                "Filename": resume.filename,
                "Submitted": resume.submitted_at.strftime("%Y-%m-%d"),
                "Score": f"{resume.similarity_score:.2f}" if resume.similarity_score is not None else "N/A",
                "Shortlisted": "Yes" if resume.is_shortlisted else "No"
            })
    
    df = pd.DataFrame(resume_data)
    
    # Sort by score (descending)
    if not df.empty and "Score" in df.columns:
        df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
        df = df.sort_values(by="Score", ascending=False)
    
    # Display as table
    st.dataframe(df, use_container_width=True)
    
    # View detailed resume button
    if st.button("View Selected Resume"):
        if "selected_resume" in st.session_state and st.session_state.selected_resume:
            st.session_state.admin_page = "view_resume"
            st.rerun()
        else:
            st.warning("Please select a resume to view.")
    
    # Shortlist top candidates button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Shortlist Top Candidates"):
            st.session_state.admin_page = "shortlist"
            st.session_state.shortlist_role_id = selected_role.id
            st.rerun()
    
    with col2:
        if st.button("Export Results"):
            st.session_state.admin_page = "export"
            st.session_state.export_role_id = selected_role.id
            st.rerun()