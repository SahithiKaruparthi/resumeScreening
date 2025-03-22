# import streamlit as st
# import os
# from pathlib import Path
# from database.models import init_db
# from database.db_manager import init_default_admin
# from auth.login import login_page
# from auth.register import register_page
# from company.dashboard import admin_dashboard
# from company.role_management import role_management_page
# from company.resume_view import view_resume_page
# from user.apply import apply_page
# from database.db_manager import get_resumes_by_user, get_role, get_resumes_by_role
# from resume_analyzer.ranking import ResumeRanker
# import pandas as pd

# os.environ['STREAMLIT_WATCHDOG_RUN_DIRECTLY'] = 'true'


# def initialize():
#     """Initialize the application"""
#     # Initialize database
#     init_db()
    
#     # Create default admin
#     init_default_admin()
    
#     # Set default page if not set
#     if "page" not in st.session_state:
#         st.session_state.page = "login"
    
#     # Set default admin page if not set
#     if "admin_page" not in st.session_state:
#         st.session_state.admin_page = "dashboard"

# def user_dashboard():
#     """Dashboard for regular users"""
#     st.title(f"Welcome, {st.session_state.username}!")
    
#     # Sidebar for navigation
#     with st.sidebar:
#         st.title("Navigation")
#         apply_btn = st.button("Apply for Jobs", key="apply_nav")
#         applications_btn = st.button("My Applications", key="apps_nav")
#         logout_btn = st.button("Logout", key="logout")
        
#         if apply_btn:
#             st.session_state.page = "apply"
#             st.rerun()
        
#         if applications_btn:
#             st.session_state.page = "my_applications"
#             st.rerun()
        
#         if logout_btn:
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.session_state.page = "login"
#             st.rerun()
    
#     # Display user dashboard content
#     st.header("Job Application System")
#     st.write("Use this platform to apply for open positions and track your applications.")
    
#     # Quick actions
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Browse Open Positions"):
#             st.session_state.page = "apply"
#             st.rerun()
    
#     with col2:
#         if st.button("Check Application Status"):
#             st.session_state.page = "my_applications"
#             st.rerun()

# def my_applications_page():
#     """Page for users to view their submitted applications"""
#     if not st.session_state.get("is_authenticated", False):
#         st.error("Please log in to view your applications.")
#         if st.button("Go to Login"):
#             st.session_state.page = "login"
#             st.rerun()
#         return
    
#     st.title("My Applications")
    
#     # Sidebar for navigation
#     with st.sidebar:
#         st.title("Navigation")
#         dashboard_btn = st.button("Dashboard", key="dash_nav")
#         apply_btn = st.button("Apply for Jobs", key="apply_nav")
#         logout_btn = st.button("Logout", key="logout")
        
#         if dashboard_btn:
#             st.session_state.page = "user_dashboard"
#             st.rerun()
        
#         if apply_btn:
#             st.session_state.page = "apply"
#             st.rerun()
        
#         if logout_btn:
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.session_state.page = "login"
#             st.rerun()
    
#     # Get user's resumes
#     resumes = get_resumes_by_user(st.session_state.user_id)
    
#     if not resumes:
#         st.info("You haven't submitted any applications yet.")
#         if st.button("Apply Now"):
#             st.session_state.page = "apply"
#             st.rerun()
#         return
    
#     # Create dataframe for display
#     application_data = []
#     for resume in resumes:
#         # Get role information
#         role = get_role(resume.role_id)
        
#         application_data.append({
#             "Position": role.title if role else "Unknown",
#             "Submitted Date": resume.submitted_at.strftime("%Y-%m-%d"),
#             "Status": "Shortlisted" if resume.is_shortlisted else "Under Review",
#             "Match Score": f"{resume.similarity_score:.2f}" if resume.similarity_score is not None else "N/A"
#         })
    
#     df = pd.DataFrame(application_data)
    
#     # Display as table
#     st.dataframe(df, use_container_width=True)

# def shortlist_page():
#     """Page for shortlisting candidates"""
#     if not st.session_state.get("is_admin", False):
#         st.error("Access denied. You need admin privileges to view this page.")
#         if st.button("Return to login"):
#             st.session_state.page = "login"
#             st.rerun()
#         return
    
#     st.title("Shortlist Candidates")
    
#     # Sidebar for navigation
#     with st.sidebar:
#         st.title("Navigation")
#         dashboard_btn = st.button("Back to Dashboard", key="dash_nav")
#         logout_btn = st.button("Logout", key="logout")
        
#         if dashboard_btn:
#             st.session_state.admin_page = "dashboard"
#             st.rerun()
        
#         if logout_btn:
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.session_state.page = "login"
#             st.rerun()
    
#     # Get role info
#     role_id = st.session_state.get("shortlist_role_id")
#     role = get_role(role_id)
    
#     if not role:
#         st.error("Role not found.")
#         return
    
#     st.header(f"Shortlisting for: {role.title}")
    
#     # Get resumes
#     resumes = get_resumes_by_role(role_id)
    
#     if not resumes:
#         st.info("No applications found for this role.")
#         return
    
#     # Number of top candidates to shortlist
#     top_n = st.slider("Number of candidates to shortlist", 
#                        min_value=1, 
#                        max_value=min(20, len(resumes)), 
#                        value=10)
    
#     # Display preview
#     ranker = ResumeRanker()
#     top_resumes = ranker.rank_resumes(role_id, top_n=top_n)
    
#     # Create dataframe for display
#     resume_data = []
#     for idx, resume in enumerate(top_resumes, 1):
#         resume_data.append({
#             "Rank": idx,
#             "Applicant": resume.user.username,
#             "Filename": resume.filename,
#             "Submitted": resume.submitted_at.strftime("%Y-%m-%d"),
#             "Score": f"{resume.similarity_score:.2f}" if resume.similarity_score is not None else "N/A"
#         })
    
#     df = pd.DataFrame(resume_data)
    
#     st.write(f"Preview of top {top_n} candidates:")
#     st.dataframe(df, use_container_width=True)
    
#     # Shortlist button
#     if st.button("Confirm Shortlist"):
#         shortlisted = ranker.shortlist_top_resumes(role_id, top_n=top_n)
#         st.success(f"Successfully shortlisted {len(shortlisted)} candidates!")
        
#         # Button to go back to dashboard
#         if st.button("Return to Dashboard"):
#             st.session_state.admin_page = "dashboard"
#             st.rerun()

# def export_page():
#     """Page for exporting results"""
#     if not st.session_state.get("is_admin", False):
#         st.error("Access denied. You need admin privileges to view this page.")
#         if st.button("Return to login"):
#             st.session_state.page = "login"
#             st.rerun()
#         return
    
#     st.title("Export Results")
    
#     # Sidebar for navigation
#     with st.sidebar:
#         st.title("Navigation")
#         dashboard_btn = st.button("Back to Dashboard", key="dash_nav")
#         logout_btn = st.button("Logout", key="logout")
        
#         if dashboard_btn:
#             st.session_state.admin_page = "dashboard"
#             st.rerun()
        
#         if logout_btn:
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.session_state.page = "login"
#             st.rerun()
    
#     # Get role info
#     role_id = st.session_state.get("export_role_id")
#     role = get_role(role_id)
    
#     if not role:
#         st.error("Role not found.")
#         return
    
#     st.header(f"Export Results for: {role.title}")
    
#     # Get resumes
#     resumes = get_resumes_by_role(role_id)
    
#     if not resumes:
#         st.info("No applications found for this role.")
#         return
    
#     # Create dataframe for display and export
#     resume_data = []
#     for resume in resumes:
#         resume_data.append({
#             "Applicant": resume.user.username,
#             "Email": resume.user.email,
#             "Filename": resume.filename,
#             "Submitted": resume.submitted_at.strftime("%Y-%m-%d"),
#             "Score": resume.similarity_score if resume.similarity_score is not None else 0.0,
#             "Shortlisted": "Yes" if resume.is_shortlisted else "No"
#         })
    
#     df = pd.DataFrame(resume_data)
    
#     # Sort by score
#     df = df.sort_values(by="Score", ascending=False)
    
#     st.dataframe(df, use_container_width=True)
    
#     # Download link
#     csv = df.to_csv(index=False).encode('utf-8')
    
#     st.download_button(
#         label="Download CSV",
#         data=csv,
#         file_name=f"{role.title.replace(' ', '_')}_applications.csv",
#         mime="text/csv"
#     )
    
#     # Button to go back to dashboard
#     if st.button("Return to Dashboard"):
#         st.session_state.admin_page = "dashboard"
#         st.rerun()

# def main():
#     """Main application entry point"""
#     # Set page config
#     st.set_page_config(
#         page_title="Resume Analyzer",
#         page_icon="📄",
#         layout="wide"
#     )
    
#     # Initialize application
#     initialize()
    
#     # Page routing
#     if st.session_state.page == "login":
#         login_page()
#     elif st.session_state.page == "register":
#         register_page()
#     elif st.session_state.page == "user_dashboard":
#         user_dashboard()
#     elif st.session_state.page == "apply":
#         apply_page()
#     elif st.session_state.page == "my_applications":
#         my_applications_page()
#     elif st.session_state.page == "admin_dashboard":
#         # Admin pages are handled through admin_page state
#         if st.session_state.admin_page == "dashboard":
#             admin_dashboard()
#         elif st.session_state.admin_page == "roles":
#             role_management_page()
#         elif st.session_state.admin_page == "shortlist":
#             shortlist_page()
#         elif st.session_state.admin_page == "export":
#             export_page()
#         else:
#             admin_dashboard()  # Default to dashboard
#     else:
#         login_page()  # Default to login

# if __name__ == "__main__":
#     main()

import streamlit as st
import os
from pathlib import Path
from database.models import init_db
from database.db_manager import init_default_admin
from auth.login import login_page
from auth.register import register_page
from company.dashboard import admin_dashboard
from company.role_management import role_management_page
from company.resume_view import view_resume_page
from user.apply import apply_page
from database.db_manager import get_resumes_by_user, get_role, get_resumes_by_role
from resume_analyzer.ranking import ResumeRanker
from rag.vector_store import VectorStore  # Import VectorStore
import pandas as pd


os.environ['STREAMLIT_WATCHDOG_RUN_DIRECTLY'] = 'true'


def initialize():
    """Initialize the application"""
    # Initialize database
    init_db()
    
    # Create default admin
    init_default_admin()
    
    # Initialize VectorStore (singleton)
    VectorStore()
    
    # Set default page if not set
    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    # Set default admin page if not set
    if "admin_page" not in st.session_state:
        st.session_state.admin_page = "dashboard"

def user_dashboard():
    """Dashboard for regular users"""
    st.title(f"Welcome, {st.session_state.username}!")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        apply_btn = st.button("Apply for Jobs", key="apply_nav")
        applications_btn = st.button("My Applications", key="apps_nav")
        logout_btn = st.button("Logout", key="logout")
        
        if apply_btn:
            st.session_state.page = "apply"
            st.rerun()
        
        if applications_btn:
            st.session_state.page = "my_applications"
            st.rerun()
        
        if logout_btn:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "login"
            st.rerun()
    
    # Display user dashboard content
    st.header("Job Application System")
    st.write("Use this platform to apply for open positions and track your applications.")
    
    # Quick actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Browse Open Positions"):
            st.session_state.page = "apply"
            st.rerun()
    
    with col2:
        if st.button("Check Application Status"):
            st.session_state.page = "my_applications"
            st.rerun()

def my_applications_page():
    """Page for users to view their submitted applications"""
    if not st.session_state.get("is_authenticated", False):
        st.error("Please log in to view your applications.")
        if st.button("Go to Login"):
            st.session_state.page = "login"
            st.rerun()
        return
    
    st.title("My Applications")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        dashboard_btn = st.button("Dashboard", key="dash_nav")
        apply_btn = st.button("Apply for Jobs", key="apply_nav")
        logout_btn = st.button("Logout", key="logout")
        
        if dashboard_btn:
            st.session_state.page = "user_dashboard"
            st.rerun()
        
        if apply_btn:
            st.session_state.page = "apply"
            st.rerun()
        
        if logout_btn:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "login"
            st.rerun()
    
    # Get user's resumes
    resumes = get_resumes_by_user(st.session_state.user_id)
    
    if not resumes:
        st.info("You haven't submitted any applications yet.")
        if st.button("Apply Now"):
            st.session_state.page = "apply"
            st.rerun()
        return
    
    # Create dataframe for display
    vector_store = VectorStore()  # Initialize VectorStore
    application_data = []
    for resume in resumes:
        # Get role information
        role = get_role(resume.role_id)
        
        # Calculate similarity score dynamically
        similarity_score = vector_store.calculate_similarity_score(resume.content_text, resume.role_id)
        
        application_data.append({
            "Position": role.title if role else "Unknown",
            "Submitted Date": resume.submitted_at.strftime("%Y-%m-%d"),
            "Status": "Shortlisted" if resume.is_shortlisted else "Under Review",
            "Match Score": f"{similarity_score:.2f}"  # Dynamically calculated score
        })
    
    df = pd.DataFrame(application_data)
    
    # Display as table
    st.dataframe(df, use_container_width=True)

def shortlist_page():
    """Page for shortlisting candidates"""
    if not st.session_state.get("is_admin", False):
        st.error("Access denied. You need admin privileges to view this page.")
        if st.button("Return to login"):
            st.session_state.page = "login"
            st.rerun()
        return
    
    st.title("Shortlist Candidates")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        dashboard_btn = st.button("Back to Dashboard", key="dash_nav")
        logout_btn = st.button("Logout", key="logout")
        
        if dashboard_btn:
            st.session_state.admin_page = "dashboard"
            st.rerun()
        
        if logout_btn:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "login"
            st.rerun()
    
    # Get role info
    role_id = st.session_state.get("shortlist_role_id")
    role = get_role(role_id)
    
    if not role:
        st.error("Role not found.")
        return
    
    st.header(f"Shortlisting for: {role.title}")
    
    # Get resumes
    resumes = get_resumes_by_role(role_id)
    
    if not resumes:
        st.info("No applications found for this role.")
        return
    
    # Number of top candidates to shortlist
    top_n = st.slider("Number of candidates to shortlist", 
                       min_value=1, 
                       max_value=min(20, len(resumes)), 
                       value=10)
    
    # Display preview
    ranker = ResumeRanker()
    top_resumes = ranker.rank_resumes(role_id, top_n=top_n)
    
    # Create dataframe for display
    vector_store = VectorStore()  # Initialize VectorStore
    resume_data = []
    for idx, resume in enumerate(top_resumes, 1):
        # Calculate similarity score dynamically
        similarity_score = vector_store.calculate_similarity_score(resume.content_text, role_id)
        
        resume_data.append({
            "Rank": idx,
            "Applicant": resume.user.username,
            "Filename": resume.filename,
            "Submitted": resume.submitted_at.strftime("%Y-%m-%d"),
            "Score": f"{similarity_score:.2f}"  # Dynamically calculated score
        })
    
    df = pd.DataFrame(resume_data)
    
    st.write(f"Preview of top {top_n} candidates:")
    st.dataframe(df, use_container_width=True)
    
    # Shortlist button
    if st.button("Confirm Shortlist"):
        shortlisted = ranker.shortlist_top_resumes(role_id, top_n=top_n)
        st.success(f"Successfully shortlisted {len(shortlisted)} candidates!")
        
        # Button to go back to dashboard
        if st.button("Return to Dashboard"):
            st.session_state.admin_page = "dashboard"
            st.rerun()

def export_page():
    """Page for exporting results"""
    if not st.session_state.get("is_admin", False):
        st.error("Access denied. You need admin privileges to view this page.")
        if st.button("Return to login"):
            st.session_state.page = "login"
            st.rerun()
        return
    
    st.title("Export Results")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        dashboard_btn = st.button("Back to Dashboard", key="dash_nav")
        logout_btn = st.button("Logout", key="logout")
        
        if dashboard_btn:
            st.session_state.admin_page = "dashboard"
            st.rerun()
        
        if logout_btn:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "login"
            st.rerun()
    
    # Get role info
    role_id = st.session_state.get("export_role_id")
    role = get_role(role_id)
    
    if not role:
        st.error("Role not found.")
        return
    
    st.header(f"Export Results for: {role.title}")
    
    # Get resumes
    resumes = get_resumes_by_role(role_id)
    
    if not resumes:
        st.info("No applications found for this role.")
        return
    
    # Create dataframe for display and export
    vector_store = VectorStore()  # Initialize VectorStore
    resume_data = []
    for resume in resumes:
        # Calculate similarity score dynamically
        similarity_score = vector_store.calculate_similarity_score(resume.content_text, role_id)
        
        resume_data.append({
            "Applicant": resume.user.username,
            "Email": resume.user.email,
            "Filename": resume.filename,
            "Submitted": resume.submitted_at.strftime("%Y-%m-%d"),
            "Score": similarity_score,  # Dynamically calculated score
            "Shortlisted": "Yes" if resume.is_shortlisted else "No"
        })
    
    df = pd.DataFrame(resume_data)
    
    # Sort by score
    df = df.sort_values(by="Score", ascending=False)
    
    st.dataframe(df, use_container_width=True)
    
    # Download link
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{role.title.replace(' ', '_')}_applications.csv",
        mime="text/csv"
    )
    
    # Button to go back to dashboard
    if st.button("Return to Dashboard"):
        st.session_state.admin_page = "dashboard"
        st.rerun()

def main():
    """Main application entry point"""
    # Set page config
    st.set_page_config(
        page_title="Resume Analyzer",
        page_icon="📄",
        layout="wide"
    )
    
    # Initialize application
    initialize()
    
    # Page routing
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
    elif st.session_state.page == "user_dashboard":
        user_dashboard()
    elif st.session_state.page == "apply":
        apply_page()
    elif st.session_state.page == "my_applications":
        my_applications_page()
    elif st.session_state.page == "admin_dashboard":
        # Admin pages are handled through admin_page state
        if st.session_state.admin_page == "dashboard":
            admin_dashboard()
        elif st.session_state.admin_page == "roles":
            role_management_page()
        elif st.session_state.admin_page == "shortlist":
            shortlist_page()
        elif st.session_state.admin_page == "export":
            export_page()
        else:
            admin_dashboard()  # Default to dashboard
    else:
        login_page()  # Default to login

if __name__ == "__main__":
    main()