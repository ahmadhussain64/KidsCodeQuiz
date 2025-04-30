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
if st.session_state.username:
    st.sidebar.markdown("## Database Admin")
    if st.sidebar.button("Inspect Database"):
        db_info = db_manager.inspect_database()
        st.sidebar.json(db_info)

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
