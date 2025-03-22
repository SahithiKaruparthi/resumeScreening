# import streamlit as st
# from database.db_manager import create_role, get_all_roles, update_role, get_role
# from rag.vector_store import VectorStore
# from datetime import datetime, timedelta
# import pandas as pd

# def role_management_page():
#     """Role management page for admin"""
#     if not st.session_state.get("is_admin", False):
#         st.error("Access denied. You need admin privileges to view this page.")
#         if st.button("Return to login"):
#             st.session_state.page = "login"
#             st.rerun()
#         return
    
#     st.title("Job Role Management")
    
#     # Sidebar for navigation
#     with st.sidebar:
#         st.title("Navigation")
#         dashboard_btn = st.button("Dashboard", key="dash_nav")
#         logout_btn = st.button("Logout", key="logout")
        
#         if dashboard_btn:
#             st.session_state.admin_page = "dashboard"
#             st.rerun()
        
#         if logout_btn:
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.session_state.page = "login"
#             st.rerun()
    
#     # Tabs for different operations
#     tab1, tab2 = st.tabs(["Create New Role", "Manage Existing Roles"])

#      # Initialize min_date to today's date
#     min_date = datetime.now().date()
    
#     with tab1:
#         st.header("Create New Job Role")
        
#         with st.form("create_role_form"):
#             title = st.text_input("Role Title")
#             description = st.text_area("Role Description")
#             requirements = st.text_area("Role Requirements (This will be used for matching resumes)")
            
#             deadline_date = st.date_input("Application Deadline (Date)", 
#                                         min_value=min_date,
#                                         max_value=max_date,
#                                         value=min_date + timedelta(days=30))

#             deadline_time = st.time_input("Application Deadline (Time)", 
#                                         value=datetime.time(23, 59))

#             # Combine date and time
#             deadline = datetime.datetime.combine(deadline_date, deadline_time)


            
#             submit_button = st.form_submit_button("Create Role")
            
#             if submit_button:
#                 if not title or not requirements:
#                     st.error("Role title and requirements cannot be empty.")
#                 else:
#                     try:
#                         # Create role in database
#                         role_id = create_role(title, description, requirements, deadline)
                        
#                         # Add role to vector store
#                         vector_store = VectorStore()
#                         vector_store.add_role(role_id, title, requirements)
                        
#                         st.success(f"Role '{title}' created successfully!")
                        
#                         # Clear form after submission
#                         st.session_state.admin_page = "roles"
#                         st.rerun()
#                     except Exception as e:
#                         st.error(f"Error creating role: {str(e)}")
    
#     with tab2:
#         st.header("Manage Existing Roles")
        
#         # Get all roles
#         roles = get_all_roles()
        
#         if not roles:
#             st.info("No job roles defined yet.")
#             return
        
#         # Create dataframe for display
#         role_data = []
#         for role in roles:
#             role_data.append({
#                 "ID": role.id,
#                 "Title": role.title,
#                 "Deadline": role.deadline.strftime("%Y-%m-%d"),
#                 "Status": "Active" if role.is_active else "Inactive"
#             })
        
#         role_df = pd.DataFrame(role_data)
        
#         # Display as table
#         st.dataframe(role_df, use_container_width=True)
        
#         # Role editing
#         st.subheader("Edit Role")
        
#         role_id = st.number_input("Enter Role ID to Edit", min_value=1, step=1)
        
#         if st.button("Load Role"):
#             role = get_role(role_id)
#             if role:
#                 st.session_state.edit_role = {
#                     "id": role.id,
#                     "title": role.title,
#                     "description": role.description,
#                     "requirements": role.requirements,
#                     "deadline": role.deadline.date(),
#                     "is_active": role.is_active
#                 }
#             else:
#                 st.error(f"Role with ID {role_id} not found.")
        
#         if "edit_role" in st.session_state:
#             with st.form("edit_role_form"):
#                 title = st.text_input("Role Title", value=st.session_state.edit_role["title"])
#                 description = st.text_area("Role Description", value=st.session_state.edit_role["description"] or "")
#                 requirements = st.text_area("Role Requirements", value=st.session_state.edit_role["requirements"])
                
#                 # Date picker for deadline
#                 min_date = datetime.now().date()
#                 max_date = min_date + timedelta(days=365)
                
#                 deadline_date = st.date_input("Application Deadline (Date)", 
#                                             min_value=min_date,
#                                             max_value=max_date,
#                                             value=min_date + timedelta(days=30))

#                 deadline_time = st.time_input("Application Deadline (Time)", 
#                                             value=datetime.time(23, 59))

#                 # Combine date and time
#                 deadline = datetime.datetime.combine(deadline_date, deadline_time)


                
#                 is_active = st.checkbox("Active", value=st.session_state.edit_role["is_active"])
                
#                 update_button = st.form_submit_button("Update Role")
                
#                 if update_button:
#                     if not title or not requirements:
#                         st.error("Role title and requirements cannot be empty.")
#                     else:
#                         try:
#                             # Update role in database
#                             update_success = update_role(
#                                 st.session_state.edit_role["id"],
#                                 title=title,
#                                 description=description,
#                                 requirements=requirements,
#                                 deadline=deadline,
#                                 is_active=is_active
#                             )
                            
#                             if update_success:
#                                 # Update role in vector store
#                                 vector_store = VectorStore()
#                                 vector_store.update_role(
#                                     st.session_state.edit_role["id"],
#                                     title,
#                                     requirements
#                                 )
                                
#                                 st.success(f"Role '{title}' updated successfully!")
#                                 del st.session_state.edit_role
#                                 st.rerun()
#                             else:
#                                 st.error(f"Failed to update role.")
#                         except Exception as e:
#                             st.error(f"Error updating role: {str(e)}")

import streamlit as st
from database.db_manager import create_role, get_all_roles, update_role, get_role
from rag.vector_store import VectorStore
from datetime import datetime, timedelta
import pandas as pd

def role_management_page():
    """Role management page for admin"""
    if not st.session_state.get("is_admin", False):
        st.error("Access denied. You need admin privileges to view this page.")
        if st.button("Return to login"):
            st.session_state.page = "login"
            st.rerun()
        return
    
    st.title("Job Role Management")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        dashboard_btn = st.button("Dashboard", key="dash_nav")
        logout_btn = st.button("Logout", key="logout")
        
        if dashboard_btn:
            st.session_state.admin_page = "dashboard"
            st.rerun()
        
        if logout_btn:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "login"
            st.rerun()
    
    # Tabs for different operations
    tab1, tab2 = st.tabs(["Create New Role", "Manage Existing Roles"])

    # Initialize min_date and max_date
    min_date = datetime.now().date()  # Today's date
    max_date = min_date + timedelta(days=365)  # One year from today
    
    with tab1:
        st.header("Create New Job Role")
        
        with st.form("create_role_form"):
            title = st.text_input("Role Title")
            description = st.text_area("Role Description")
            requirements = st.text_area("Role Requirements (This will be used for matching resumes)")
            
            deadline_date = st.date_input("Application Deadline (Date)", 
                                        min_value=min_date,
                                        max_value=max_date,
                                        value=min_date + timedelta(days=30))

            deadline_time = st.time_input("Application Deadline (Time)", 
                                        value=datetime.strptime("23:59", "%H:%M").time())  # Correct usage of datetime.time

            # Combine date and time
            deadline = datetime.combine(deadline_date, deadline_time)

            # Add a submit button
            submit_button = st.form_submit_button("Create Role")
            
            if submit_button:
                if not title or not requirements:
                    st.error("Role title and requirements cannot be empty.")
                else:
                    try:
                        # Create role in database
                        role_id = create_role(title, description, requirements, deadline)
                        
                        # Add role to vector store
                        vector_store = VectorStore()
                        vector_store.add_role(role_id, title, requirements)
                        
                        st.success(f"Role '{title}' created successfully!")
                        
                        # Clear form after submission
                        st.session_state.admin_page = "roles"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating role: {str(e)}")
    
    with tab2:
        st.header("Manage Existing Roles")
        
        # Get all roles
        roles = get_all_roles()
        
        if not roles:
            st.info("No job roles defined yet.")
            return
        
        # Create dataframe for display
        role_data = []
        for role in roles:
            role_data.append({
                "ID": role.id,
                "Title": role.title,
                "Deadline": role.deadline.strftime("%Y-%m-%d %H:%M:%S"),
                "Status": "Active" if role.is_active else "Inactive"
            })
        
        role_df = pd.DataFrame(role_data)
        
        # Display as table
        st.dataframe(role_df, use_container_width=True)
        
        # Role editing
        st.subheader("Edit Role")
        
        role_id = st.number_input("Enter Role ID to Edit", min_value=1, step=1)
        
        if st.button("Load Role"):
            role = get_role(role_id)
            if role:
                st.session_state.edit_role = {
                    "id": role.id,
                    "title": role.title,
                    "description": role.description,
                    "requirements": role.requirements,
                    "deadline": role.deadline,
                    "is_active": role.is_active
                }
            else:
                st.error(f"Role with ID {role_id} not found.")
        
        if "edit_role" in st.session_state:
            with st.form("edit_role_form"):
                title = st.text_input("Role Title", value=st.session_state.edit_role["title"])
                description = st.text_area("Role Description", value=st.session_state.edit_role["description"] or "")
                requirements = st.text_area("Role Requirements", value=st.session_state.edit_role["requirements"])
                
                # Date picker for deadline
                deadline_date = st.date_input("Application Deadline (Date)", 
                                            min_value=min_date,
                                            max_value=max_date,
                                            value=st.session_state.edit_role["deadline"].date())

                deadline_time = st.time_input("Application Deadline (Time)", 
                                            value=st.session_state.edit_role["deadline"].time())

                # Combine date and time
                deadline = datetime.combine(deadline_date, deadline_time)

                is_active = st.checkbox("Active", value=st.session_state.edit_role["is_active"])
                
                # Add a submit button
                update_button = st.form_submit_button("Update Role")
                
                if update_button:
                    if not title or not requirements:
                        st.error("Role title and requirements cannot be empty.")
                    else:
                        try:
                            # Update role in database
                            update_success = update_role(
                                st.session_state.edit_role["id"],
                                title=title,
                                description=description,
                                requirements=requirements,
                                deadline=deadline,
                                is_active=is_active
                            )
                            
                            if update_success:
                                # Update role in vector store
                                vector_store = VectorStore()
                                vector_store.update_role(
                                    st.session_state.edit_role["id"],
                                    title,
                                    requirements
                                )
                                
                                st.success(f"Role '{title}' updated successfully!")
                                del st.session_state.edit_role
                                st.rerun()
                            else:
                                st.error(f"Failed to update role.")
                        except Exception as e:
                            st.error(f"Error updating role: {str(e)}")