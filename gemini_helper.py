import google.generativeai as genai
import streamlit as st

def setup_gemini():
    """
    Configure the Google Generative AI with API key
    
    Returns:
        bool: True if setup was successful, False otherwise
    """
    import os
    # Get API key from environment variable
    api_key = os.environ.get('AIzaSyDDEsUWzoaFdK-LgyVfJ-xWM5F_IzHq1hQ')
    
    if api_key:
        try:
            # Configure Gemini with the API key
            genai.configure(api_key=api_key)
            
            # Create generation config if not already created
            if 'GEMINI_MODEL' not in st.session_state:
                # Using gemini-1.5-pro which is widely available
                st.session_state.GEMINI_MODEL = genai.GenerativeModel('gemini-1.5-pro')
            return True
        except Exception as e:
            print(f"Error setting up Gemini: {str(e)}")
            return False
    else:
        print("Gemini API key not found in environment variables.")
        return False

def generate_response(message, persona="YOU ARE A PROFESSIONAL EDUCATION SPECIALIST"):
    """
    Generate a response from Google Gemini AI
    
    Args:
        message (str): The user's message
        persona (str): The persona for the AI
    
    Returns:
        str: The generated response
    """
    if not setup_gemini():
        return ("I'm currently offline due to a connection issue. Please try again later, "
                "or ask a teacher for help with your Python question.")
    
    try:
        # Build the prompt with the persona and strong focus on Python programming
        prompt = f"{persona}\n\nYou are helping a child learn Python programming. Provide simple, friendly, and clear explanations. If the question is not about Python or programming, gently redirect to Python topics by saying something like 'I'm here to help with Python programming. Let me teach you about Python instead...' and then teach a relevant Python concept for beginners.\n\nQuestion: {message}"
        
        # Generate response
        response = st.session_state.GEMINI_MODEL.generate_content(prompt)
        
        # Return the text
        return response.text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return ("Sorry, I couldn't generate a response at the moment. "
                "Try asking a different question or simplifying your current question.")

def display_chatbot(container):
    """
    Display the chatbot interface in the given container
    
    Args:
        container: The Streamlit container to use
    """
    # Title and introduction
    container.subheader("Got Questions? Ask Our AI Assistant! 🤖")
    container.info("Ask anything about Python programming, and our AI tutor will help you learn!")
    
    # Set up the input key in session state if not present
    if "ai_input_key" not in st.session_state:
        st.session_state.ai_input_key = 0
        
    # Simple chat interface with dynamic key to reset input
    message = container.text_input(
        "Ask a question about Python or programming:", 
        key=f"ai_question_{st.session_state.ai_input_key}"
    )
    
    # Submit button
    if container.button("Ask") and message:
        # Display thinking message
        with st.spinner("Thinking..."):
            # Set education specialist persona
            persona = """You are a Professional Education Specialist in a futuristic, AI-agentic world, where intelligent systems support every aspect of learning and development. You specialize in children’s counseling and education, blending traditional child psychology with advanced AI insights to personalize education and emotional support for children aged 3–16.

In this world, children interact with AI tutors, immersive VR classrooms, and cognitive enhancement tools — yet they still need empathetic human guidance. You serve as the bridge between human emotional intelligence and AI efficiency, ensuring that each child’s academic path, emotional health, and ethical development remain at the center of progress.

You advise parents, educators, and even AI systems on how to create adaptive, inclusive, and emotionally aware learning environments. Your responses are informed by neurodevelopmental science, digital behavior analytics, and emotional-AI feedback loops, always prioritizing the child’s well-being in this evolving educational landscape."""
            
            # Get response
            response = generate_response(message, persona)
            
            # Add to chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
                
            st.session_state.chat_history.append({"user": message, "bot": response})
            
            # Increment the key to create a new input field next time
            st.session_state.ai_input_key += 1
            
            # Force a rerun to clear the input
            st.rerun()
    
    # Display chat history
    if "chat_history" in st.session_state and st.session_state.chat_history:
        container.subheader("Conversation")
        
        # Get username for display
        if st.session_state.get("username"):
            display_name = f"You ({st.session_state.username})"
        else:
            display_name = "You (Anonymous)"
        
        for i, chat in enumerate(st.session_state.chat_history):
            # User message with proper display format
            container.markdown(f"**{display_name}:** {chat['user']}")
            
            # Bot response
            container.markdown(f"**AI Tutor:** {chat['bot']}")
            
            # Add separator except for the last message
            if i < len(st.session_state.chat_history) - 1:
                container.markdown("---")
                
    # Add a clear chat button
    if "chat_history" in st.session_state and st.session_state.chat_history:
        if container.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()