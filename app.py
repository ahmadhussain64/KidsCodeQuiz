import streamlit as st
import pandas as pd
import random
import time
from tutorials import tutorials_data, display_tutorial
from challenges import challenges_data, display_challenge
from progress_tracker import load_progress, save_progress, display_progress
from user_management import create_user, login_user
from code_executor import execute_python_code
from database_manager import DatabaseManager, migrate_from_json_if_needed
from certificate_generator import display_certificate_page, verify_certificate_page
from gemini_helper import display_chatbot

# Create a database manager instance
db_manager = DatabaseManager()

# Page configuration
st.set_page_config(
    page_title="Python for Kids! 🐍",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Attempt to migrate data from JSON files to the database if needed
migrate_from_json_if_needed()

# Initialize session state variables if they don't exist
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "welcome"
if 'tutorial_index' not in st.session_state:
    st.session_state.tutorial_index = 0
if 'challenge_index' not in st.session_state:
    st.session_state.challenge_index = 0
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'completed_tutorials' not in st.session_state:
    st.session_state.completed_tutorials = []
if 'completed_challenges' not in st.session_state:
    st.session_state.completed_challenges = []
if 'emoji_collection' not in st.session_state:
    st.session_state.emoji_collection = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_user_id' not in st.session_state:
    st.session_state.selected_user_id = None

# Store tutorials and challenges data in session state for certificate requirements
st.session_state.all_tutorials = tutorials_data
st.session_state.all_challenges = challenges_data

# Emoji rewards
emojis = ["🐢", "🦊", "🐱", "🐶", "🦁", "🐯", "🦄", "🦋", "🐬", "🐙", "🦖", "🦕", "🐘", "🦒", "🐼"]

# Navigation functions
def go_to_page(page):
    st.session_state.current_page = page
    st.rerun()

def next_tutorial():
    if st.session_state.tutorial_index < len(tutorials_data) - 1:
        st.session_state.tutorial_index += 1
        
        # Mark as completed if not already done
        if st.session_state.tutorial_index - 1 not in st.session_state.completed_tutorials:
            st.session_state.completed_tutorials.append(st.session_state.tutorial_index - 1)
            st.session_state.points += 5
            # Give reward emoji
            reward_emoji = random.choice(emojis)
            if reward_emoji not in st.session_state.emoji_collection:
                st.session_state.emoji_collection.append(reward_emoji)
            
            # Save progress
            if st.session_state.username:
                save_progress(st.session_state.username, 
                             st.session_state.points,
                             st.session_state.completed_tutorials,
                             st.session_state.completed_challenges,
                             st.session_state.emoji_collection)
    st.rerun()

def prev_tutorial():
    if st.session_state.tutorial_index > 0:
        st.session_state.tutorial_index -= 1
        st.rerun()

def next_challenge():
    if st.session_state.challenge_index < len(challenges_data) - 1:
        st.session_state.challenge_index += 1
        st.rerun()

def prev_challenge():
    if st.session_state.challenge_index > 0:
        st.session_state.challenge_index -= 1
        st.rerun()

def complete_challenge():
    if st.session_state.challenge_index not in st.session_state.completed_challenges:
        st.session_state.completed_challenges.append(st.session_state.challenge_index)
        st.session_state.points += 10
        
        # Give reward emoji
        reward_emoji = random.choice(emojis)
        if reward_emoji not in st.session_state.emoji_collection:
            st.session_state.emoji_collection.append(reward_emoji)
        
        # Save progress
        if st.session_state.username:
            save_progress(st.session_state.username, 
                         st.session_state.points,
                         st.session_state.completed_tutorials,
                         st.session_state.completed_challenges,
                         st.session_state.emoji_collection)
        
        # Display celebration
        st.balloons()

# Sidebar
st.sidebar.title("Python for Kids! 🐍")

# User management in sidebar
if st.session_state.username:
    st.sidebar.write(f"Welcome, {st.session_state.username}! 👋")
    st.sidebar.write(f"Points: {st.session_state.points} ⭐")
    
    if st.session_state.emoji_collection:
        st.sidebar.write("Your emoji friends:")
        st.sidebar.write(" ".join(st.session_state.emoji_collection))
    
    if st.sidebar.button("Log Out"):
        st.session_state.username = None
        st.rerun()
else:
    login_tab, signup_tab = st.sidebar.tabs(["Log In", "Sign Up"])
    
    with login_tab:
        login_user()
        
    with signup_tab:
        create_user()

# Navigation menu in sidebar
st.sidebar.markdown("## Menu 📚")
st.sidebar.button("Home 🏠", on_click=go_to_page, args=("welcome",))
st.sidebar.button("Learn Python 🐍", on_click=go_to_page, args=("tutorials",))
st.sidebar.button("Coding Challenges 🎮", on_click=go_to_page, args=("challenges",))
st.sidebar.button("My Progress 📈", on_click=go_to_page, args=("progress",))

# Certificate options (only show for logged-in users)
if st.session_state.username:
    st.sidebar.markdown("## Certificates 🎓")
    st.sidebar.button("My Certificates 🏆", on_click=go_to_page, args=("certificates",))

# Certificate verification (available to all)
# Admin section
if st.session_state.username and st.session_state.is_admin:
    st.sidebar.markdown("## Admin Panel 🔧")
    st.sidebar.button("Admin Dashboard 👑", on_click=go_to_page, args=("admin_dashboard",))

st.sidebar.markdown("## Certificate Verification")
st.sidebar.button("Verify a Certificate 🔍", on_click=go_to_page, args=("verify_certificate",))

# Main content
if st.session_state.current_page == "welcome":
    st.title("Welcome to Python for Kids! 🐍")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        # Hello, future programmer! 👋
        
        Are you ready to learn how to code with Python? 🚀
        
        Python is a friendly programming language that's perfect for beginners like you!
        With Python, you can create games, solve puzzles, and tell the computer what to do.
        
        ### What can you do here?
        
        - 📚 **Learn Python** - Fun, easy-to-follow tutorials
        - 🎮 **Solve Challenges** - Test your skills with cool coding puzzles
        - 🏆 **Earn Points and Emoji Friends** - Collect fun emoji friends as you learn
        - 📈 **Track Your Progress** - See how much you've learned
        
        ### Ready to start your coding adventure?
        """)
        
        st.button("Start Learning Python! 🚀", on_click=go_to_page, args=("tutorials",))
    
    with col2:
        emojis_display = " ".join(["🐍", "🚀", "💻", "🎮", "🏆", "⭐", "🦄", "🐱", "🦖"])
        st.markdown(f"<h1 style='font-size: 2.5em; text-align: center;'>{emojis_display}</h1>", unsafe_allow_html=True)
        
        st.info("Python is used to build YouTube, Instagram, and even games! Soon you'll be coding like a pro! 🌟")

elif st.session_state.current_page == "tutorials":
    display_tutorial(st.session_state.tutorial_index, next_tutorial, prev_tutorial)

elif st.session_state.current_page == "challenges":
    display_challenge(st.session_state.challenge_index, 
                      execute_python_code, 
                      complete_challenge,
                      next_challenge, 
                      prev_challenge,
                      st.session_state.completed_challenges)

elif st.session_state.current_page == "progress":
    if st.session_state.username:
        display_progress(st.session_state.username, 
                        st.session_state.points,
                        st.session_state.completed_tutorials,
                        st.session_state.completed_challenges,
                        len(tutorials_data),
                        len(challenges_data))
    else:
        st.warning("Please log in to see your progress! 👆")
        st.button("Go Back to Home", on_click=go_to_page, args=("welcome",))

elif st.session_state.current_page == "certificates":
    if st.session_state.username and st.session_state.user_id:
        display_certificate_page(st.session_state.username, st.session_state.user_id)
    else:
        st.warning("Please log in to access your certificates! 👆")
        st.button("Go Back to Home", on_click=go_to_page, args=("welcome",))

elif st.session_state.current_page == "verify_certificate":
    verify_certificate_page()

elif st.session_state.current_page == "admin_dashboard":
    if st.session_state.username and st.session_state.is_admin:
        st.title("Admin Dashboard 👑")
        
        admin_tabs = st.tabs(["User Management", "Progress Tracking", "Statistics"])
        
        with admin_tabs[0]:
            st.subheader("User Management")
            
            # Get all users from database
            all_users = db_manager.get_all_users()
            
            # Display user table
            if all_users:
                user_df = pd.DataFrame([
                    {
                        "ID": user["id"],
                        "Username": user["username"],
                        "Full Name": user["full_name"],
                        "School": user["school"],
                        "Class": user["class"],
                        "Admin": "✓" if user["is_admin"] else "",
                        "Last Login": user["last_login"]
                    } for user in all_users
                ])
                
                st.dataframe(user_df, use_container_width=True)
                
                # User selection for details and editing
                st.subheader("Edit User")
                user_id = st.selectbox("Select User", 
                                      options=[user["id"] for user in all_users],
                                      format_func=lambda x: next((u["username"] for u in all_users if u["id"] == x), "Unknown"))
                
                if user_id:
                    st.session_state.selected_user_id = user_id
                    user_details = db_manager.get_user_by_id(user_id)
                    
                    if user_details:
                        # User profile editing
                        with st.form("edit_user_form"):
                            st.subheader(f"Edit User: {user_details['username']}")
                            
                            full_name = st.text_input("Full Name", value=user_details["full_name"] or "")
                            parent_name = st.text_input("Parent Name", value=user_details["parent_name"] or "")
                            dob = st.text_input("Date of Birth", value=user_details["dob"] or "")
                            class_name = st.text_input("Class", value=user_details["class"] or "")
                            section = st.text_input("Section", value=user_details["section"] or "")
                            school = st.text_input("School", value=user_details["school"] or "")
                            
                            is_admin = st.checkbox("Administrator", value=user_details["is_admin"])
                            
                            reset_password = st.checkbox("Reset Password")
                            new_password = ""
                            if reset_password:
                                new_password = st.text_input("New Password", type="password")
                                
                            submitted = st.form_submit_button("Save Changes")
                            
                            if submitted:
                                # Update profile
                                profile_data = {
                                    'full_name': full_name,
                                    'parent_name': parent_name,
                                    'dob': dob,
                                    'class': class_name,
                                    'section': section,
                                    'school': school
                                }
                                
                                db_manager.update_user_profile(user_id, profile_data)
                                
                                # Update admin status if it changed
                                if is_admin != user_details["is_admin"]:
                                    db_manager.set_admin_status(user_id, is_admin)
                                
                                # Reset password if requested
                                if reset_password and new_password:
                                    from user_management import hash_password
                                    new_password_hash = hash_password(new_password)
                                    db_manager.reset_user_password(user_id, new_password_hash)
                                
                                st.success("User updated successfully!")
                                st.rerun()
                        
                        # View user progress
                        st.subheader("User Progress")
                        progress = db_manager.get_user_progress(user_id)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Points", progress.get("points", 0))
                        with col2:
                            st.metric("Completed Tutorials", len(progress.get("completed_tutorials", [])))
                        with col3:
                            st.metric("Completed Challenges", len(progress.get("completed_challenges", [])))
                        
                        # View user recent events
                        st.subheader("Recent Activity")
                        events = db_manager.get_user_events(user_id, limit=10)
                        
                        if events:
                            events_df = pd.DataFrame([
                                {
                                    "Time": event["timestamp"],
                                    "Event": event["event_type"],
                                    "Details": event["event_details"]
                                } for event in events
                            ])
                            st.dataframe(events_df, use_container_width=True)
                        else:
                            st.info("No recent activity")
            else:
                st.info("No users found in the database")
                
        with admin_tabs[1]:
            st.subheader("Progress Tracking")
            
            # Display progress statistics
            all_users = db_manager.get_all_users()
            
            if all_users:
                progress_data = []
                for user in all_users:
                    progress = db_manager.get_user_progress(user["id"])
                    progress_data.append({
                        "Username": user["username"],
                        "Points": progress.get("points", 0),
                        "Tutorials Completed": len(progress.get("completed_tutorials", [])),
                        "Challenges Completed": len(progress.get("completed_challenges", [])),
                        "Emojis Collected": len(progress.get("emoji_collection", []))
                    })
                
                progress_df = pd.DataFrame(progress_data)
                st.dataframe(progress_df, use_container_width=True)
                
                # Visualization
                st.subheader("Visualizations")
                
                # Points Bar Chart
                st.bar_chart(progress_df.set_index("Username")["Points"])
                
                # Tutorials vs Challenges
                st.subheader("Tutorials vs Challenges Completion")
                tc_data = progress_df[["Username", "Tutorials Completed", "Challenges Completed"]]
                st.line_chart(tc_data.set_index("Username"))
            else:
                st.info("No users found in the database")
                
        with admin_tabs[2]:
            st.subheader("System Statistics")
            
            # Get various statistics from the database
            conn, cursor = db_manager.connect()
            try:
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM certificates")
                total_certificates = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM user_events")
                total_events = cursor.fetchone()[0]
                
                cursor.execute("SELECT SUM(points) FROM user_progress")
                total_points = cursor.fetchone()[0] or 0
                
                cursor.execute("SELECT COUNT(*) FROM users WHERE last_login > datetime('now', '-7 day')")
                active_users = cursor.fetchone()[0]
                
                # Display statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Users", total_users)
                    st.metric("Active Users (7d)", active_users)
                
                with col2:
                    st.metric("Total Certificates", total_certificates)
                    st.metric("Total Points Earned", total_points)
                
                with col3:
                    st.metric("Total Events", total_events)
                    
                # Get most recent events
                cursor.execute("""
                SELECT e.timestamp, e.event_type, e.event_details, u.username
                FROM user_events e
                JOIN users u ON e.user_id = u.id
                ORDER BY e.timestamp DESC
                LIMIT 20
                """)
                recent_events = cursor.fetchall()
                
                st.subheader("Recent System Events")
                if recent_events:
                    events_df = pd.DataFrame([
                        {
                            "Time": event[0],
                            "User": event[3],
                            "Event": event[1],
                            "Details": event[2]
                        } for event in recent_events
                    ])
                    st.dataframe(events_df, use_container_width=True)
            finally:
                db_manager.disconnect(conn)
    else:
        st.error("You don't have permission to access the admin dashboard")
        st.button("Go Back to Home", on_click=go_to_page, args=("welcome",))

# Add a chatbot to welcome page
if st.session_state.current_page == "welcome":
    st.markdown("---")
    # Create a container for the chatbot
    chat_container = st.container()
    # Display the chatbot in the container
    display_chatbot(chat_container)
