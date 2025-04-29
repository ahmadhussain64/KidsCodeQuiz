import streamlit as st
import sys
from io import StringIO
import traceback

def execute_python_code(code):
    """
    Execute Python code and return output and any errors
    
    Args:
        code (str): Python code to execute
        
    Returns:
        tuple: (output, error)
    """
    # Create StringIO objects for capturing stdout
    stdout_capture = StringIO()
    
    # Store the original stdout
    original_stdout = sys.stdout
    
    output = ""
    error = None
    
    try:
        # Redirect stdout
        sys.stdout = stdout_capture
        
        # Execute the code
        exec(code)
        
        # Get the captured output
        output = stdout_capture.getvalue()
        
    except Exception as e:
        # Get the full traceback
        error_msg = traceback.format_exc()
        
        # Simplify the error message for kids
        simple_error = simplify_error(str(e))
        error = simple_error
        
    finally:
        # Restore stdout
        sys.stdout = original_stdout
        
    return output, error

def simplify_error(error_message):
    """
    Simplify Python error messages to be more kid-friendly
    
    Args:
        error_message (str): The original error message
        
    Returns:
        str: A simplified, kid-friendly error message
    """
    # Common errors and their simplified explanations
    error_types = {
        "NameError": "Oops! You're trying to use something that doesn't exist yet. Did you forget to create a variable?",
        "SyntaxError": "Hmm, there's something wrong with how you wrote your code. Check for missing punctuation or spelling!",
        "TypeError": "Oops! You're trying to mix different types of things that don't go together, like adding a number to a word.",
        "IndexError": "You're trying to get an item that doesn't exist in your list. Remember, lists start counting at 0!",
        "ZeroDivisionError": "Oops! You can't divide by zero - even computers can't do that!",
        "IndentationError": "Check your spacing at the beginning of the line. Python is picky about that!",
        "ValueError": "The value you're using isn't right for what you're trying to do.",
        "FileNotFoundError": "The file you're looking for doesn't exist. Check the name and location!",
        "KeyError": "You're looking for something in a dictionary that isn't there.",
        "AttributeError": "You're trying to use a property or method that doesn't exist for that type of object."
    }
    
    # Check if the error message contains any of the known error types
    for error_type, simplified_msg in error_types.items():
        if error_type in error_message:
            return f"{simplified_msg} ({error_type})"
    
    # If we don't recognize the error, return a generic message with the original error
    return f"Oops! Something went wrong: {error_message}"
