import streamlit as st
import hashlib
from database_manager import DatabaseManager

# Create a database manager instance
db_manager = DatabaseManager()
from progress_tracker import load_progress


def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user():
    """Function to create a new user account"""
    st.subheader("Create New Account")

    # Basic account information
    st.markdown("#### Account Information")
    new_username = st.text_input("Choose a Username:", key="new_username")
    new_password = st.text_input("Choose a Password:",
                                 type="password",
                                 key="new_password")
    confirm_password = st.text_input("Confirm Password:",
                                     type="password",
                                     key="confirm_password")

    # Student profile information
    st.markdown("#### Student Information")

    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full Name:", key="full_name")
        parent_name = st.text_input("Son/Daughter of:", key="parent_name")
        dob = st.date_input("Date of Birth:", key="dob")

    with col2:
        class_name = st.text_input("Class:", key="class_name")
        section = st.text_input("Section:", key="section")
        school = st.text_input("School/College Name:", key="school")

    if st.button("Create Account"):
        if not new_username or not new_password:
            st.error("Please fill in the username and password fields!")
            return

        if new_password != confirm_password:
            st.error("Passwords don't match!")
            return

        if not full_name:
            st.warning("Please enter your full name.")
            return

        # Hash the password
        hashed_password = hash_password(new_password)

        # Prepare profile data
        profile_data = {
            'full_name': full_name,
            'parent_name': parent_name,
            'dob': dob.strftime("%Y-%m-%d") if dob else "",
            'class': class_name,
            'section': section,
            'school': school
        }

        # Add user to database
        user_id = db_manager.add_user(new_username, hashed_password,
                                      profile_data)

        if user_id:
            st.success("Account created successfully!")

            # Auto-login the new user
            st.session_state.username = new_username
            st.session_state.user_id = user_id
            st.session_state.profile = profile_data

            # Initialize session state with default progress
            st.session_state.points = 0
            st.session_state.completed_tutorials = []
            st.session_state.completed_challenges = []
            st.session_state.emoji_collection = []

            # Log event
            db_manager.log_event(user_id, "user_login",
                                 "Initial login after account creation")

            st.rerun()
        else:
            st.error(
                "Username already exists or there was an error creating the account. Please try again."
            )


def login_user():
    """Function to log in a user"""
    st.subheader("Log In")

    username = st.text_input("Username:", key="login_username")
    password = st.text_input("Password:",
                             type="password",
                             key="login_password")

    if st.button("Log In"):
        if not username or not password:
            st.error("Please fill in all fields!")
            return

        # Get user from database
        user = db_manager.get_user(username)

        # Check if user exists
        if not user:
            st.error("Username not found!")
            return

        # Check password
        hashed_password = hash_password(password)
        if user["password_hash"] != hashed_password:
            st.error("Incorrect password!")
            return

        # Login successful
        st.success("Login successful!")

        # Update last login time
        db_manager.update_last_login(user["id"])

        # Set session state
        st.session_state.username = username
        st.session_state.user_id = user["id"]
        st.session_state.is_admin = user.get("is_admin", False)

        # Set user profile in session state
        st.session_state.profile = {
            'full_name': user.get('full_name', ''),
            'parent_name': user.get('parent_name', ''),
            'dob': user.get('dob', ''),
            'class': user.get('class', ''),
            'section': user.get('section', ''),
            'school': user.get('school', '')
        }

        # Load user progress
        progress = db_manager.get_user_progress(user["id"])

        # Update session state with progress
        st.session_state.points = progress.get("points", 0)
        st.session_state.completed_tutorials = progress.get(
            "completed_tutorials", [])
        st.session_state.completed_challenges = progress.get(
            "completed_challenges", [])
        st.session_state.emoji_collection = progress.get(
            "emoji_collection", [])

        # Log login event
        db_manager.log_event(user["id"], "user_login", "User logged in")

        st.rerun()
