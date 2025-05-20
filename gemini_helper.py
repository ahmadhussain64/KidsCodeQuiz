import google.generativeai as genai
import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ChatMessage:
    role: str
    content: str

class PythonLearningAssistant:
    def __init__(self):
        self.model = None
        self.chat = None
        self.initialize_assistant()
        
    def initialize_assistant(self):
        """Initialize the Gemini model with specific instructions"""
        try:
            # Configure the model
            if 'GEMINI_MODEL' not in st.session_state:
                st.session_state.GEMINI_MODEL = genai.GenerativeModel('gemini-2.0-flash')
            self.model = st.session_state.GEMINI_MODEL
            
            # Initialize chat
            self.chat = self.model.start_chat(history=[])
            return True
                
        except Exception as e:
            st.error(f"Error initializing Gemini: {str(e)}")
            return False

    def setup_gemini(self):
        """Configure Gemini with API key"""
        api_key = st.session_state.get('GEMINI_API_KEY')
        if not api_key:
            import os
            api_key = os.environ.get('GEMINI_API_KEY')
            
        if api_key:
            try:
                genai.configure(api_key=api_key)
                return True
            except Exception as e:
                st.error(f"Error setting up Gemini: {str(e)}")
                return False
        return False

    def get_fallback_response(self, message: str) -> str:
        """Get a fallback response when the API is not available"""
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
            "dictionary": "Python dictionaries store key-value pairs: `student = {'name': 'John', 'age': 10}`. Access values with: `student['name']` (gets 'John')."
        }
        
        message_lower = message.lower().strip()
        if message_lower in fallback_responses:
            return fallback_responses[message_lower]
        
        for key in fallback_responses:
            if key in message_lower:
                return fallback_responses[key]
        
        return "I'm here to help you learn Python programming! Try asking about variables, loops, functions, or other Python concepts."

    def generate_response(self, message: str) -> str:
        """Generate a response using the Gemini model"""
        if not self.setup_gemini():
            return self.get_fallback_response(message)
            
        try:
            if not self.chat:
                self.initialize_assistant()
            
            # Build the prompt with context
            prompt = f"""You are a Professional Education Specialist specializing in teaching Python programming to children aged 3-16. 
            Your responses should be:
            1. Simple and friendly
            2. Include emojis and visual elements
            3. Focus on Python programming concepts
            4. Use age-appropriate language
            5. Provide clear examples
            6. Redirect non-programming questions to Python topics
            
            Always maintain a supportive and encouraging tone.
            
            User Question: {message}"""
            
            # Generate response
            response = self.chat.send_message(prompt)
            
            return response.text
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return self.get_fallback_response(message)

def display_api_key_input(container):
    """Display API key input field and handle API key management"""
    container.subheader("Gemini API Configuration 🔑")
    
    # Add helpful information and styled button
    container.markdown("""
        <div style="
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <p style="margin-bottom: 10px;">To use the AI tutor, you'll need a Gemini API key. Here's how to get one:</p>
            <ol style="margin-bottom: 15px;">
                <li>Click the button below to visit Google AI Studio</li>
                <li>Sign in with your Google account</li>
                <li>Navigate to the API section</li>
                <li>Create a new API key</li>
                <li>Copy and paste it below</li>
            </ol>
            <a href="https://aistudio.google.com/" target="_blank">
                <button style="
                    background-color: #4285F4;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    transition: background-color 0.3s;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <span>🚀</span>
                    Get Gemini API Key from Google AI Studio
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    if 'GEMINI_API_KEY' not in st.session_state:
        st.session_state.GEMINI_API_KEY = ""
    
    # Add a container for the API key input with better styling
    container.markdown("""
        <div style="
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
        ">
    """, unsafe_allow_html=True)
    
    api_key = container.text_input(
        "Enter your Gemini API Key:",
        value=st.session_state.GEMINI_API_KEY,
        type="password",
        help="Paste your API key from Google AI Studio here"
    )
    
    container.markdown("</div>", unsafe_allow_html=True)
    
    # Add status indicator
    if st.session_state.GEMINI_API_KEY:
        container.success("✅ API key is configured")
    else:
        container.warning("⚠️ Please enter your API key to use the AI tutor")
    
    if api_key != st.session_state.GEMINI_API_KEY:
        st.session_state.GEMINI_API_KEY = api_key
        if 'assistant' in st.session_state:
            del st.session_state.assistant
        st.rerun()

def display_chatbot(container):
    """Display the chatbot interface in the given container"""
    # Display API key input first
    display_api_key_input(container)
    
    # Initialize assistant if not exists
    if 'assistant' not in st.session_state:
        st.session_state.assistant = PythonLearningAssistant()
    
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
        with st.spinner("Thinking..."):
            # Get response from assistant
            response = st.session_state.assistant.generate_response(message)
            
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
