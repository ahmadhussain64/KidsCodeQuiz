import streamlit as st
import pandas as pd
from datetime import datetime
from database_manager import DatabaseManager

# Create a database manager instance
db_manager = DatabaseManager()

def load_progress(username):
    """Load user progress from storage"""
    if "user_id" in st.session_state:
        user_id = st.session_state.user_id
        return db_manager.get_user_progress(user_id)
    else:
        # Return default progress for non-logged-in users
        return {
            "points": 0,
            "completed_tutorials": [],
            "completed_challenges": [],
            "emoji_collection": [],
            "last_login": str(datetime.now())
        }

def save_progress(username, points, completed_tutorials, completed_challenges, emoji_collection):
    """Save user progress to storage"""
    if "user_id" in st.session_state:
        user_id = st.session_state.user_id
        success = db_manager.update_user_progress(
            user_id, 
            points, 
            completed_tutorials, 
            completed_challenges, 
            emoji_collection
        )
        
        if success:
            # Log progress update event
            db_manager.log_event(
                user_id, 
                "progress_updated", 
                f"Progress updated: {points} points, {len(completed_tutorials)} tutorials, {len(completed_challenges)} challenges"
            )
        
        return success
    return False

def display_progress(username, points, completed_tutorials, completed_challenges, total_tutorials, total_challenges):
    """Display the user's progress"""
    st.title(f"My Learning Progress 📈")
    
    # Overall progress card
    st.markdown("""
    <style>
    .progress-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Calculate percentages
    tutorial_percent = int((len(completed_tutorials) / total_tutorials) * 100) if total_tutorials > 0 else 0
    challenge_percent = int((len(completed_challenges) / total_challenges) * 100) if total_challenges > 0 else 0
    overall_percent = int((tutorial_percent + challenge_percent) / 2)
    
    # Display progress overview
    st.markdown(f"### Hello, {username}! 👋")
    st.markdown(f"You have earned **{points} points** so far! ⭐")
    
    # Progress bars
    st.markdown("### Your Learning Journey")
    st.markdown(f"**Overall Progress:** {overall_percent}%")
    st.progress(overall_percent/100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Tutorials:** {len(completed_tutorials)}/{total_tutorials}")
        st.progress(tutorial_percent/100)
        
    with col2:
        st.markdown(f"**Challenges:** {len(completed_challenges)}/{total_challenges}")
        st.progress(challenge_percent/100)
    
    # Emoji collection
    st.markdown("### Your Emoji Friends")
    
    emoji_collection = st.session_state.emoji_collection
    if emoji_collection:
        emoji_display = " ".join([f"<span style='font-size: 2em;'>{emoji}</span>" for emoji in emoji_collection])
        st.markdown(f"<div style='text-align: center;'>{emoji_display}</div>", unsafe_allow_html=True)
        
        # Count of collected emojis
        st.markdown(f"You've collected {len(emoji_collection)} emoji friends out of 15 possible friends!")
    else:
        st.info("You haven't collected any emoji friends yet. Complete tutorials and challenges to collect them!")
    
    # Achievements section
    st.markdown("### Achievements 🏆")
    
    achievements = []
    
    # Add achievements based on progress
    if len(completed_tutorials) >= 1:
        achievements.append("🎓 First Tutorial Completed!")
    
    if len(completed_challenges) >= 1:
        achievements.append("🏅 First Challenge Solved!")
    
    if points >= 50:
        achievements.append("⭐ Earned 50+ Points!")
    
    if len(completed_tutorials) >= total_tutorials:
        achievements.append("📚 Tutorial Master: Completed all tutorials!")
    
    if len(completed_challenges) >= total_challenges:
        achievements.append("🏆 Challenge Champion: Solved all challenges!")
    
    if len(emoji_collection) >= 5:
        achievements.append("🦄 Emoji Collector: Collected 5+ emoji friends!")
    
    if achievements:
        for achievement in achievements:
            st.markdown(f"- {achievement}")
    else:
        st.info("Complete tutorials and challenges to earn achievements!")
    
    # What to do next
    st.markdown("### What to do next? 🚀")
    
    suggested_tutorial = None
    for i in range(total_tutorials):
        if i not in completed_tutorials:
            suggested_tutorial = i
            break
            
    suggested_challenge = None
    for i in range(total_challenges):
        if i not in completed_challenges:
            suggested_challenge = i
            break
    
    col1, col2 = st.columns(2)
    
    with col1:
        if suggested_tutorial is not None:
            st.button(f"Continue with Tutorial {suggested_tutorial + 1}", 
                    on_click=lambda: go_to_tutorial(suggested_tutorial))
        else:
            st.success("You've completed all tutorials! 🎉")
    
    with col2:
        if suggested_challenge is not None:
            st.button(f"Try Challenge {suggested_challenge + 1}", 
                    on_click=lambda: go_to_challenge(suggested_challenge))
        else:
            st.success("You've solved all challenges! 🎉")

def go_to_tutorial(index):
    """Navigate to a specific tutorial"""
    st.session_state.current_page = "tutorials"
    st.session_state.tutorial_index = index
    st.rerun()

def go_to_challenge(index):
    """Navigate to a specific challenge"""
    st.session_state.current_page = "challenges"
    st.session_state.challenge_index = index
    st.rerun()
