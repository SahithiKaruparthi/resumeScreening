import streamlit as st
import os
from database.db_manager import get_role, get_user, mark_as_shortlisted
import pandas as pd

def view_resume_page(resume):
    """Page for viewing a single resume"""
    if not st.session_state.get("is_admin", False):
        st.error("Access denied. You need admin privileges to view this page.")
        if st.button("Return to login"):
            st.session_state.page = "login"
            st.rerun()
        return
    
    st.title("Resume Details")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        dashboard_btn = st.button("Back to Dashboard", key="dash_nav")
        roles_btn = st.button("Manage Roles", key="roles_nav")
        logout_btn = st.button("Logout", key="logout")
        
        if dashboard_btn:
            st.session_state.admin_page = "dashboard"
            st.rerun()
        
        if roles_btn:
            st.session_state.admin_page = "roles"
            st.rerun()
        
        if logout_btn:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "login"
            st.rerun()
    
    # Get related info
    role = get_role(resume.role_id)
    user = get_user(resume.user_id)
    
    # Display resume details
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Applicant Information")
        st.write(f"**Name:** {user.username}")
        st.write(f"**Email:** {user.email}")
        st.write(f"**Submission Date:** {resume.submitted_at.strftime('%Y-%m-%d %H:%M')}")
    
    with col2:
        st.subheader("Application Details")
        st.write(f"**Role:** {role.title}")
        st.write(f"**Filename:** {resume.filename}")
        st.write(f"**Match Score:** {resume.similarity_score:.2f}" if resume.similarity_score is not None else "**Match Score:** N/A")
        st.write(f"**Shortlisted:** {'Yes' if resume.is_shortlisted else 'No'}")
    
    # Resume content
    st.header("Resume Content")
    with st.expander("Show Resume Text", expanded=True):
        st.text_area("", value=resume.content_text or "No content available", height=300, disabled=True)
    
    # Role requirements for comparison
    st.header("Role Requirements")
    with st.expander("Show Requirements"):
        st.write(role.requirements)
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if not resume.is_shortlisted:
            if st.button("Shortlist Candidate"):
                if mark_as_shortlisted(resume.id):
                    st.success("Candidate shortlisted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to shortlist candidate.")
    
    with col2:
        if os.path.exists(resume.file_path):
            with open(resume.file_path, "rb") as file:
                st.download_button(
                    label="Download Resume",
                    data=file,
                    file_name=resume.filename,
                    mime="application/octet-stream"
                )
        else:
            st.error("Resume file not found.")