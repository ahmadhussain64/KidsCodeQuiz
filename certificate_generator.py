import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
from database_manager import DatabaseManager

# Create a database manager instance
db_manager = DatabaseManager()

def generate_certificate_image(username, certificate_type, completion_date, certificate_code, profile_data=None):
    """
    Generate a certificate image for the user
    
    Args:
        username (str): The username to display on the certificate
        certificate_type (str): The type of certificate (e.g., "Python Basics")
        completion_date (str): The date when the certificate was completed
        certificate_code (str): The unique certificate code for verification
        profile_data (dict): Student profile information (name, school, etc.)
        
    Returns:
        BytesIO: The certificate image in a BytesIO object
    """
    # Get current working directory
    cwd = os.getcwd()
    
    # Create a blank certificate (width, height)
    width, height = 1200, 900  # Made it taller to fit more information
    certificate = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(certificate)
    
    # Try to load fonts - use default if not available
    try:
        # For font paths, try to locate fonts on the system or use default
        title_font = ImageFont.truetype(os.path.join(cwd, "arial.ttf"), 50)
        subtitle_font = ImageFont.truetype(os.path.join(cwd, "arial.ttf"), 30)
        body_font = ImageFont.truetype(os.path.join(cwd, "arial.ttf"), 20)
        name_font = ImageFont.truetype(os.path.join(cwd, "arial.ttf"), 40)
    except IOError:
        # If font files not found, use default
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
    
    # Add colorful border
    draw.rectangle(((20, 20), (width-20, height-20)), outline=(59, 89, 152), width=10)
    draw.rectangle(((40, 40), (width-40, height-40)), outline=(66, 133, 244), width=5)
    
    # Add emoji decorations
    emojis = "🐍 🚀 💻 ⭐ 🏆 "
    
    # Add title
    draw.text((width//2, 100), "Certificate of Achievement", 
              fill=(59, 89, 152), font=title_font, anchor="mm")
    
    # Add decorative line
    draw.line([(width//4, 140), (width*3//4, 140)], fill=(66, 133, 244), width=3)
    
    # Add certificate body
    draw.text((width//2, 180), f"This certifies that", 
              fill=(0, 0, 0), font=subtitle_font, anchor="mm")
    
    # Get student full name from profile if available
    student_name = profile_data.get('full_name', username) if profile_data else username
    
    # Add student name (larger and more prominent)
    draw.text((width//2, 240), f"{student_name}", 
              fill=(66, 133, 244), font=name_font, anchor="mm")
    
    # Add student details if available
    y_position = 300
    if profile_data:
        if profile_data.get('parent_name'):
            draw.text((width//2, y_position), f"Son/Daughter of: {profile_data.get('parent_name')}", 
                    fill=(0, 0, 0), font=body_font, anchor="mm")
            y_position += 40
        
        if profile_data.get('class') or profile_data.get('section'):
            class_text = f"Class: {profile_data.get('class', '')}"
            if profile_data.get('section'):
                class_text += f", Section: {profile_data.get('section')}"
            draw.text((width//2, y_position), class_text, 
                    fill=(0, 0, 0), font=body_font, anchor="mm")
            y_position += 40
            
        if profile_data.get('school'):
            draw.text((width//2, y_position), f"School/College: {profile_data.get('school')}", 
                    fill=(0, 0, 0), font=body_font, anchor="mm")
            y_position += 40
    else:
        y_position += 80  # Skip some space if no profile data
    
    # Add certificate description
    draw.text((width//2, y_position), f"has successfully completed the", 
              fill=(0, 0, 0), font=subtitle_font, anchor="mm")
    y_position += 60
    
    # Add certificate type
    draw.text((width//2, y_position), f"{certificate_type}", 
              fill=(59, 89, 152), font=title_font, anchor="mm")
    y_position += 80
    
    # Add footer text
    draw.text((width//2, y_position), f"Python for Kids Learning Platform", 
              fill=(66, 133, 244), font=subtitle_font, anchor="mm")
    y_position += 60
    
    # Add completion date
    draw.text((width//2, y_position), f"Completion Date: {completion_date}", 
              fill=(0, 0, 0), font=body_font, anchor="mm")
    y_position += 40
    
    # Add certificate ID/code
    draw.text((width//2, y_position), f"Certificate ID: {certificate_code}", 
              fill=(0, 0, 0), font=body_font, anchor="mm")
    y_position += 40
    
    # Add verification text
    draw.text((width//2, y_position), f"Verify this certificate at: kidscodequiz.com/verify", 
              fill=(0, 0, 0), font=body_font, anchor="mm")
    y_position += 60
    
    # Add decoration at the bottom
    draw.text((width//2, height-80), emojis, 
              fill=(66, 133, 244), font=subtitle_font, anchor="mm")
    
    # Save certificate to BytesIO
    img_byte_array = BytesIO()
    certificate.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)  # Move to the beginning of BytesIO
    
    return img_byte_array

def get_certificate_download_link(img_byte_array, filename="certificate.png", text="Download Certificate"):
    """
    Generates a download link for the certificate
    
    Args:
        img_byte_array (BytesIO): The certificate image in a BytesIO object
        filename (str): The filename for the downloaded certificate
        text (str): The text to display for the download link
        
    Returns:
        str: HTML for the download link
    """
    b64 = base64.b64encode(img_byte_array.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">📥 {text}</a>'
    return href

def display_certificate_page(username, user_id):
    """
    Display the certificate page for the user
    
    Args:
        username (str): The username to display on the certificate
        user_id (int): The user's ID in the database
    """
    st.title("🎓 Python for Kids Certificate 🎓")
    
    # Get user progress
    progress = db_manager.get_user_progress(user_id)
    
    # Check if the user has completed enough challenges/tutorials to earn a certificate
    total_tutorials = len(st.session_state.get("all_tutorials", []))
    total_challenges = len(st.session_state.get("all_challenges", []))
    
    completed_tutorials = progress.get("completed_tutorials", [])
    completed_challenges = progress.get("completed_challenges", [])
    
    # Calculate completion percentages
    tutorial_completion = len(completed_tutorials) / total_tutorials if total_tutorials > 0 else 0
    challenge_completion = len(completed_challenges) / total_challenges if total_challenges > 0 else 0
    
    # Display progress toward certificate
    st.subheader("Your Progress")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Tutorials Completed", 
            value=f"{len(completed_tutorials)}/{total_tutorials}",
            delta=f"{tutorial_completion:.0%}"
        )
    
    with col2:
        st.metric(
            label="Challenges Completed", 
            value=f"{len(completed_challenges)}/{total_challenges}",
            delta=f"{challenge_completion:.0%}"
        )
    
    # Get existing certificates
    certificates = db_manager.get_user_certificates(user_id)
    
    # Show existing certificates
    if certificates:
        st.subheader("Your Certificates")
        for cert in certificates:
            with st.expander(f"{cert['certificate_type']} - {cert['issue_date']}"):
                st.write(f"**Certificate Type:** {cert['certificate_type']}")
                st.write(f"**Issued:** {cert['issue_date']}")
                st.write(f"**Status:** {'Completed' if cert['is_completed'] else 'In Progress'}")
                st.write(f"**Certificate ID:** {cert['certificate_code']}")
                
                # If the certificate is completed, offer download
                if cert['is_completed']:
                    # Generate certificate image with profile data
                    img_byte_array = generate_certificate_image(
                        username, 
                        cert['certificate_type'], 
                        cert['completed_date'], 
                        cert['certificate_code'],
                        st.session_state.get('profile')
                    )
                    
                    # Display certificate preview
                    st.image(Image.open(img_byte_array), caption="Certificate Preview")
                    img_byte_array.seek(0)  # Reset to beginning for download link
                    
                    # Create download link
                    st.markdown(
                        get_certificate_download_link(
                            img_byte_array, 
                            f"{username}_{cert['certificate_type']}_Certificate.png", 
                            "Download Certificate"
                        ), 
                        unsafe_allow_html=True
                    )
    
    # Eligibility for new certificates
    st.subheader("Earn New Certificates")
    
    # Define certificate types and requirements
    certificate_types = [
        {
            "name": "Python Basics",
            "description": "Complete at least 3 tutorials and 2 challenges",
            "tutorial_req": 3,
            "challenge_req": 2
        },
        {
            "name": "Python Junior Developer",
            "description": "Complete at least 5 tutorials and 4 challenges",
            "tutorial_req": 5,
            "challenge_req": 4
        },
        {
            "name": "Python Master",
            "description": "Complete all tutorials and challenges",
            "tutorial_req": total_tutorials,
            "challenge_req": total_challenges
        }
    ]
    
    # Display available certificates
    for cert_type in certificate_types:
        # Check if the user already has this certificate
        has_cert = any(c['certificate_type'] == cert_type["name"] and c['is_completed'] for c in certificates)
        
        # Check if the user is eligible
        is_eligible = (
            len(completed_tutorials) >= cert_type["tutorial_req"] and 
            len(completed_challenges) >= cert_type["challenge_req"]
        )
        
        with st.expander(f"{cert_type['name']} Certificate"):
            st.write(f"**Description:** {cert_type['description']}")
            st.write(f"**Requirements:**")
            st.write(f"- Complete {cert_type['tutorial_req']} tutorials ({len(completed_tutorials)}/{cert_type['tutorial_req']} completed)")
            st.write(f"- Complete {cert_type['challenge_req']} challenges ({len(completed_challenges)}/{cert_type['challenge_req']} completed)")
            
            if has_cert:
                st.success("You've already earned this certificate! 🎉")
            elif is_eligible:
                # Create a button to generate certificate
                if st.button(f"Generate {cert_type['name']} Certificate", key=f"gen_{cert_type['name']}"):
                    # Create a new certificate
                    certificate_code = db_manager.create_certificate(user_id, cert_type["name"])
                    
                    if certificate_code:
                        # Mark certificate as completed immediately
                        db_manager.complete_certificate(certificate_code)
                        
                        # Log event
                        db_manager.log_event(
                            user_id, 
                            "certificate_earned",
                            f"Earned {cert_type['name']} Certificate"
                        )
                        
                        st.success(f"Congratulations! You've earned the {cert_type['name']} Certificate! 🎉")
                        st.rerun()  # Refresh to show the new certificate
                    else:
                        st.error("There was an error generating your certificate. Please try again.")
            else:
                st.info("Keep learning to earn this certificate! 📚")

def verify_certificate_page():
    """Display the certificate verification page"""
    st.title("🔍 Verify Certificate 🔍")
    
    st.write("""
    Enter a certificate code to verify its authenticity.
    Certificate codes are unique identifiers found on each certificate.
    """)
    
    certificate_code = st.text_input("Enter Certificate Code:")
    
    if st.button("Verify Certificate"):
        if certificate_code:
            # Verify the certificate
            verification = db_manager.verify_certificate(certificate_code)
            
            if verification["is_valid"]:
                st.success("Certificate is valid! ✓")
                
                st.markdown("### Certificate Details")
                st.write(f"**Type:** {verification['certificate_type']}")
                st.write(f"**Issued to:** {verification['username']}")
                st.write(f"**Issue Date:** {verification['issue_date']}")
                st.write(f"**Completion Date:** {verification['completed_date']}")
                st.write(f"**Status:** {'Completed' if verification['is_completed'] else 'In Progress'}")
                
                # Generate and display certificate image
                if verification['is_completed']:
                    img_byte_array = generate_certificate_image(
                        verification['username'], 
                        verification['certificate_type'], 
                        verification['completed_date'], 
                        certificate_code,
                        verification.get('profile_data')
                    )
                    
                    st.image(Image.open(img_byte_array), caption="Certificate Image")
                    
                    # Display student details
                    profile_data = verification.get('profile_data', {})
                    if profile_data and any(profile_data.values()):
                        st.markdown("### Student Information")
                        if profile_data.get('full_name'):
                            st.write(f"**Name:** {profile_data.get('full_name')}")
                        if profile_data.get('parent_name'):
                            st.write(f"**Son/Daughter of:** {profile_data.get('parent_name')}")
                        if profile_data.get('class') or profile_data.get('section'):
                            class_info = f"**Class:** {profile_data.get('class', '')}"
                            if profile_data.get('section'):
                                class_info += f", **Section:** {profile_data.get('section')}"
                            st.write(class_info)
                        if profile_data.get('school'):
                            st.write(f"**School/College:** {profile_data.get('school')}")
            else:
                st.error("Invalid certificate code. This certificate could not be verified.")
        else:
            st.warning("Please enter a certificate code to verify.")