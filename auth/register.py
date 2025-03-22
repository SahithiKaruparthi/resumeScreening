import streamlit as st
import re
from database.db_manager import create_user

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_page():
    st.title("Register")
    
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            # Validation
            if not (username and email and password and confirm_password):
                st.error("Please fill in all fields.")
                return
                
            if len(username) < 3:
                st.error("Username must be at least 3 characters long.")
                return
                
            if not is_valid_email(email):
                st.error("Please enter a valid email address.")
                return
                
            if len(password) < 6:
                st.error("Password must be at least 6 characters long.")
                return
                
            if password != confirm_password:
                st.error("Passwords do not match.")
                return
            
            try:
                # Create user
                user_id = create_user(username, email, password)
                if user_id:
                    st.success("Registration successful! You can now log in.")
                    
                    # Add delay before redirecting
                    import time
                    time.sleep(1)
                    
                    # Redirect to login
                    st.session_state.page = "login"
                    st.rerun()
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    st.error("Username or email already exists.")
                else:
                    st.error(f"Registration failed: {str(e)}")
    
    # Login link
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Already have an account?")
    with col2:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()