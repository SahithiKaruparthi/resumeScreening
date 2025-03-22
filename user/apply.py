import streamlit as st
import os
from pathlib import Path
import shutil
from database.db_manager import get_active_roles, save_resume
from resume_analyzer.scorer import ResumeScorer
import config

# def apply_page():
#     """User application submission page"""
#     if not st.session_state.get("is_authenticated", False):
#         st.error("Please log in to submit your application.")
#         if st.button("Go to Login"):
#             st.session_state.page = "login"
#             st.rerun()
#         return
    
#     st.title("Submit Job Application")
    
#     # Sidebar for navigation
#     with st.sidebar:
#         st.title("Navigation")
#         dashboard_btn = st.button("Dashboard", key="dash_nav")
#         applications_btn = st.button("My Applications", key="apps_nav")
#         logout_btn = st.button("Logout", key="logout")
        
#         if dashboard_btn:
#             st.session_state.page = "user_dashboard"
#             st.rerun()
        
#         if applications_btn:
#             st.session_state.page = "my_applications"
#             st.rerun()
        
#         if logout_btn:
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.session_state.page = "login"
#             st.rerun()
    
#     # Get active roles
#     roles = get_active_roles()
    
#     if not roles:
#         st.warning("No active job positions available at the moment.")
#         return
    
#     # Create role mapping
#     role_titles = [role.title for role in roles]
#     role_dict = {role.title: role for role in roles}
    
#     with st.form("application_form"):
#         # Role selection
#         selected_role_title = st.selectbox("Position", role_titles)
#         selected_role = role_dict[selected_role_title]
        
#         # Display role details
#         st.subheader("Position Details")
#         st.write(f"**Deadline:** {selected_role.deadline.strftime('%Y-%m-%d')}")
        
#         with st.expander("Position Requirements"):
#             st.write(selected_role.requirements)
        
#         # Resume upload
#         st.subheader("Upload Your Resume")
#         st.write("Accepted formats: PDF, DOCX, TXT")
        
#         uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt"])
        
#         # Submit button
#         submit_button = st.form_submit_button("Submit Application")
        
#         if submit_button:
#             if not uploaded_file:
#                 st.error("Please upload your resume.")
#                 return
            
#             try:
#                 # Create user uploads directory if it doesn't exist
#                 user_uploads_dir = Path(config.UPLOADS_DIR) / str(st.session_state.user_id)
#                 user_uploads_dir.mkdir(exist_ok=True)
                
#                 # Save file
#                 file_path = user_uploads_dir / uploaded_file.name
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
                
#                 # Save resume to database
#                 resume_id = save_resume(
#                     user_id=st.session_state.user_id,
#                     role_id=selected_role.id,
#                     file_path=str(file_path),
#                     filename=uploaded_file.name
#                 )
                
#                 # Score resume
#                 scorer = ResumeScorer()
#                 score_result = scorer.score_resume(
#                     resume_id=resume_id,
#                     file_path=str(file_path),
#                     role_id=selected_role.id
#                 )
                
#                 if score_result["success"]:
#                     # Update resume with extracted text
#                     save_resume(
#                         user_id=st.session_state.user_id,
#                         role_id=selected_role.id,
#                         file_path=str(file_path),
#                         filename=uploaded_file.name,
#                         content_text=score_result["text"]
#                     )
                    
#                     st.success(f"Application submitted successfully! Your match score: {score_result['score']:.2f}")
#                     st.info("The closer your score is to 1.0, the better your resume matches the job requirements.")
#                 else:
#                     st.warning(f"Application submitted, but we had trouble analyzing your resume. It has been saved and will be reviewed.")
            
#             except Exception as e:
#                 st.error(f"Error submitting application: {str(e)}")

def apply_page():
    """User application submission page"""
    if not st.session_state.get("is_authenticated", False):
        st.error("Please log in to submit your application.")
        if st.button("Go to Login"):
            st.session_state.page = "login"
            st.rerun()
        return
    
    st.title("Submit Job Application")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        dashboard_btn = st.button("Dashboard", key="dash_nav")
        applications_btn = st.button("My Applications", key="apps_nav")
        logout_btn = st.button("Logout", key="logout")
        
        if dashboard_btn:
            st.session_state.page = "user_dashboard"
            st.rerun()
        
        if applications_btn:
            st.session_state.page = "my_applications"
            st.rerun()
        
        if logout_btn:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "login"
            st.rerun()
    
    # Get active roles
    roles = get_active_roles()
    
    if not roles:
        st.warning("No active job positions available at the moment.")
        return
    
    # Create role mapping
    role_titles = [role.title for role in roles]
    role_dict = {role.title: role for role in roles}
    
    with st.form("application_form"):
        # Role selection
        selected_role_title = st.selectbox("Position", role_titles)
        selected_role = role_dict[selected_role_title]
        
        # Display role details
        st.subheader("Position Details")
        st.write(f"**Deadline:** {selected_role.deadline.strftime('%Y-%m-%d')}")
        
        with st.expander("Position Requirements"):
            st.write(selected_role.requirements)
        
        # Resume upload
        st.subheader("Upload Your Resume")
        st.write("Accepted formats: PDF, DOCX, TXT")
        
        uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt"])
        
        # Submit button
        submit_button = st.form_submit_button("Submit Application")
        
        if submit_button:
            if not uploaded_file:
                st.error("Please upload your resume.")
                return
            
            try:
                # Create user uploads directory if it doesn't exist
                user_uploads_dir = Path(config.UPLOADS_DIR) / str(st.session_state.user_id)
                user_uploads_dir.mkdir(exist_ok=True)
                
                # Save file
                file_path = user_uploads_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Save resume to database
                resume_id = save_resume(
                    user_id=st.session_state.user_id,
                    role_id=selected_role.id,
                    file_path=str(file_path),
                    filename=uploaded_file.name
                )
                
                # Score resume
                scorer = ResumeScorer()
                score_result = scorer.score_resume(
                    resume_id=resume_id,
                    file_path=str(file_path),
                    role_id=selected_role.id
                )
                
                if score_result["success"]:
                    # Update resume with extracted text
                    save_resume(
                        user_id=st.session_state.user_id,
                        role_id=selected_role.id,
                        file_path=str(file_path),
                        filename=uploaded_file.name,
                        content_text=score_result["text"]
                    )
                    
                    st.success(f"Application submitted successfully! Your match score: {score_result['score']:.2f}")
                    st.info("The closer your score is to 1.0, the better your resume matches the job requirements.")
                else:
                    st.warning(f"Application submitted, but we had trouble analyzing your resume. It has been saved and will be reviewed.")
            
            except Exception as e:
                st.error(f"Error submitting application: {str(e)}")