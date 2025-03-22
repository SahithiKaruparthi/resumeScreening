import streamlit as st
from database.db_manager import authenticate_user

def login_page():
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if not username or not password:
                st.error("Please fill in all fields.")
                return None
            
            user = authenticate_user(username, password)
            if user:
                st.success(f"Welcome back, {username}!")
                
                # Store user info in session state
                st.session_state.user_id = user.id
                st.session_state.username = user.username
                st.session_state.is_admin = user.is_admin
                st.session_state.is_authenticated = True
                
                # Redirect based on user type
                if user.is_admin:
                    st.session_state.page = "admin_dashboard"
                else:
                    st.session_state.page = "user_dashboard"
                
                # This will cause a rerun
                st.rerun()
            else:
                st.error("Invalid username or password.")
                return None
                
    # Register link
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Don't have an account?")
    with col2:
        if st.button("Register"):
            st.session_state.page = "register"
            st.rerun()