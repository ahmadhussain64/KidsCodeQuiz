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
                st.session_state.GEMINI_MODEL = genai.GenerativeModel('gemini-1.5-flash')
            return True
        except Exception as e:
            print(f"Error setting up Gemini: {str(e)}")
            return False
    else:
        print("Gemini API key not found in environment variables.")
        return False

def get_fallback_response(message):
    """
    Get a fallback response when the API is not available
    
    Args:
        message (str): The user's message
        
    Returns:
        str: A fallback response
    """
    # Simple response dictionary
    fallback_responses = {
        "hi": "Hello there! I'm your Python learning assistant. What would you like to learn about Python today?",
        "hello": "Hi! I'm here to help you learn Python. Would you like to know about variables, loops, or functions?",
        "how are you": "I'm doing great! Ready to help you learn Python. What Python topic are you interested in?",
        "what is python": "Python is a popular programming language that's easy to learn! It's used for web development, data analysis, AI, and more. Would you like to learn some basic Python commands?",
        "help": "I can help you learn Python! Try asking about 'variables', 'loops', 'functions', or 'how to print in Python'.",
        "variables": "In Python, variables store data. For example: `name = 'Alex'` creates a variable called 'name' with the value 'Alex'. You can then use this variable in your code!",
        "loops": "Python has two main types of loops: 'for' loops and 'while' loops. A simple for loop looks like this: `for i in range(5): print(i)`. This will print numbers from 0 to 4.",
        "functions": "Functions in Python let you reuse code. Example: `def greet(name): return 'Hello, ' + name`. You can then call it with `greet('Sam')` which returns 'Hello, Sam'.",
        "print": "To display text in Python, use the print() function: `print('Hello, world!')`. This will output: Hello, world!",
        "if statement": "If statements in Python look like this: `if x > 5: print('x is more than 5')`. You can add `elif` and `else` for more conditions.",
        "list": "Python lists store multiple items: `fruits = ['apple', 'banana', 'cherry']`. Access items with: `fruits[0]` (gets 'apple'). Add items with: `fruits.append('orange')`.",
        "dictionary": "Python dictionaries store key-value pairs: `student = {'name': 'John', 'age': 10}`. Access values with: `student['name']` (gets 'John').",
        "pakistan": "I'm here to help with Python programming. Let me tell you about Python instead! Python is named after the comedy group Monty Python, not the snake. It was created in 1991 by Guido van Rossum and is designed to be easy to read and write."
    }
    
    message_lower = message.lower().strip()
    
    # Look for exact matches first
    if message_lower in fallback_responses:
        return fallback_responses[message_lower]
    
    # Look for partial matches
    for key in fallback_responses:
        if key in message_lower:
            return fallback_responses[key]
    
    # Default response if no matches
    return ("I'm here to help you learn Python programming! Try asking about variables, loops, functions, or other Python concepts. For example, try 'How do I create a variable in Python?' or 'What is a for loop?'")


def generate_response(message, persona="YOU ARE A PROFESSIONAL EDUCATION SPECIALIST"):
    """
    Generate a response from Google Gemini AI
    
    Args:
        message (str): The user's message
        persona (str): The persona for the AI
    
    Returns:
        str: The generated response
    """
    # Check if API is configured
    api_available = setup_gemini()
    
    if not api_available:
        print("API not available, using fallback response system")
        return get_fallback_response(message)
    
    try:
        # Build the prompt with the persona and strong focus on Python programming
        prompt = f"{persona}\n\nYou are helping a child learn Python programming. Provide simple, friendly, and clear explanations. If the question is not about Python or programming, gently redirect to Python topics by saying something like 'I'm here to help with Python programming. Let me teach you about Python instead...' and then teach a relevant Python concept for beginners.\n\nQuestion: {message}"
        
        # Generate response
        response = st.session_state.GEMINI_MODEL.generate_content(prompt)
        
        # Return the text
        return response.text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        # If API call fails, use our fallback system
        return get_fallback_response(message)

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