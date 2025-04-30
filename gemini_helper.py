import google.generativeai as genai
import streamlit as st

def setup_gemini():
    """
    Configure the Google Generative AI with API key
    
    Returns:
        bool: True if setup was successful, False otherwise
    """
    # Check if API key is in session state
    if 'GEMINI_API_KEY' not in st.session_state:
        # We need to ask for the API key
        st.sidebar.warning("Gemini AI Assistant needs an API key to function.")
        st.session_state.GEMINI_API_KEY = st.sidebar.text_input(
            "Enter your Google Gemini API key:",
            type="password",
            help="Get an API key from https://ai.google.dev/",
            key="gemini_api_key_input"
        )
        
    # If we have an API key, configure Gemini
    if st.session_state.GEMINI_API_KEY:
        try:
            genai.configure(api_key=st.session_state.GEMINI_API_KEY)
            # Create generation config
            if 'GEMINI_MODEL' not in st.session_state:
                st.session_state.GEMINI_MODEL = genai.GenerativeModel('gemini-pro')
            return True
        except Exception as e:
            st.sidebar.error(f"Error setting up Gemini: {str(e)}")
            return False
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
        return "⚠️ Please provide a valid Google Gemini API key to use the AI assistant."
    
    try:
        # Build the prompt with the persona
        prompt = f"{persona}\n\nYou are helping a child learn Python programming. Provide simple, friendly, and clear explanations.\n\nQuestion: {message}"
        
        # Generate response
        response = st.session_state.GEMINI_MODEL.generate_content(prompt)
        
        # Return the text
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def display_chatbot(container):
    """
    Display the chatbot interface in the given container
    
    Args:
        container: The Streamlit container to use
    """
    # Title and introduction
    container.subheader("Got Questions? Ask Our AI Assistant! 🤖")
    container.info("Ask anything about Python programming, and our AI tutor will help you learn!")
    
    # Simple chat interface
    message = container.text_input("Ask a question about Python or programming:", key="ai_question")
    
    # Submit button
    if container.button("Ask") and message:
        # Display thinking message
        with st.spinner("Thinking..."):
            # Set education specialist persona
            persona = "YOU ARE A PROFESSIONAL EDUCATION SPECIALIST"
            
            # Get response
            response = generate_response(message, persona)
            
            # Add to chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
                
            st.session_state.chat_history.append({"user": message, "bot": response})
    
    # Display chat history
    if "chat_history" in st.session_state and st.session_state.chat_history:
        container.subheader("Conversation")
        
        for i, chat in enumerate(st.session_state.chat_history):
            # User message
            container.markdown(f"**You:** {chat['user']}")
            
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