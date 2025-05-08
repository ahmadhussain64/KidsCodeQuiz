import google.generativeai as genai
import streamlit as st
import os

def setup_gemini():
    """
    Configure the Google Generative AI with API key
    
    Returns:
        bool: True if setup was successful, False otherwise
    """
    # Get API key from environment variable
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if api_key:
        try:
            # Configure Gemini with the API key
            genai.configure(api_key=api_key)
            
            # Create generation config if not already created
            if 'GEMINI_MODEL' not in st.session_state:
                # Using gemini-2.0-flash which is widely available
                st.session_state.GEMINI_MODEL = genai.GenerativeModel('gemini-2.0-flash')
            return True
        except Exception as e:
            st.error(f"Error setting up Gemini: {str(e)}")
            return False
    else:
        st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
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
        "pakistan": "I'm here to help with Python programming. Let me tell you about Python instead! Python is named after the comedy group Monty Python, not the snake. It was created in 1991 by Guido van Rossum and is designed to be easy to read and write.",
        "fallback1": "Hmm, I'm not sure I caught that! Could you clarify your question about Python basics or advanced topics?",
        "fallback2": "Looks like I need a bit more context. Are you asking about functions, tools, or something else in Python?",
        "fallback3": "Whoops, my code's a bit tangled! Can you repeat your question about Python programming?",
        "fallback4": "That’s a new one for me! Could you specify if it’s about Python functions, operations, or agents?",
        "fallback5": "My Python interpreter’s confused! Can you rephrase your question about Python basics or advanced concepts?",
        "fallback6": "I might’ve missed a semicolon somewhere! What Python topic are you exploring—functions, tools, or ops?",
        "fallback7": "Let’s debug this! Could you share more details about the Python concept you’re asking about?",
        "fallback8": "My Python script crashed! Can you clarify if you’re asking about basic syntax or advanced tools?",
        "fallback9": "I’m getting a NameError here! Could you repeat your question about Python programming?",
        "fallback10": "Oops, looks like an indentation error! What specifically about Python would you like to know?",
        "fallback11": "My Python console’s blinking at me! Is your question about functions, agents, or operations?",
        "fallback12": "I think I need a `try-except` block! Can you rephrase your Python-related query?",
        "fallback13": "SyntaxError alert! Could you specify which Python topic—basics, advanced, or tools—you’re curious about?",
        "fallback14": "Let’s restart the kernel! What Python concept, like functions or ops, are you diving into?",
        "fallback15": "I’m stuck in a Python loop! Can you clarify your question about Python programming?",
        "fallback16": "My Python path’s not found! Is this about basic Python, advanced functions, or tools?",
        "fallback17": "Uh-oh, I hit a KeyError! Could you repeat your question about Python basics or agents?",
        "fallback18": "I need to `import clarity`! What Python topic are you exploring—functions, ops, or tools?",
        "fallback19": "My Python’s feeling a bit `NoneType`! Can you rephrase your question about Python concepts?",
        "fallback20": "Looks like I need to debug! Is your question about Python basics, advanced topics, or agents?",
        "fallback21": "I’m getting a TypeError! Could you clarify your Python question about functions or operations?",
        "fallback22": "My Python script’s on a coffee break! What topic—basics, tools, or agents—are you asking about?",
        "fallback23": "I think I forgot a `def`! Can you repeat your question about Python programming?",
        "fallback24": "My Python’s in a pickle! Is this about functions, operations, or advanced Python tools?",
        "fallback25": "I might’ve dropped a variable! Could you specify your Python question about basics or agents?",
        "fallback26": "My code’s throwing an exception! What Python topic are you curious about—functions or ops?",
        "fallback27": "I need to `pip install understanding`! Can you rephrase your Python-related query?",
        "fallback28": "My Python’s feeling recursive! Is your question about basic syntax, tools, or advanced concepts?",
        "fallback29": "I’m lost in a Python dictionary! Could you clarify your question about Python programming?",
        "fallback30": "My Python’s raising an AttributeError! What topic—functions, ops, or agents—are you exploring?",
        "fallback31": "I think I need a Python refresher! Can you repeat your question about Python basics or tools?",
        "fallback32": "My Python’s stuck in a `while` loop! Is this about advanced functions or operations?",
        "fallback33": "I’m getting a ModuleNotFoundError! Could you specify your Python question about agents or tools?",
        "fallback34": "My Python’s gone off-script! What concept—basics, functions, or ops—are you asking about?",
        "fallback35": "I need to check my Python docs! Can you rephrase your question about Python programming?",
        "fallback36": "My Python’s feeling a bit `async`! Is your question about basic syntax or advanced agents?",
        "fallback37": "I think I overwrote a variable! Could you clarify your Python question about tools or ops?",
        "fallback38": "My Python’s throwing a SyntaxError! What topic—functions, basics, or agents—are you curious about?",
        "fallback39": "I need to reboot my Python brain! Can you repeat your question about Python concepts?",
        "fallback40": "My Python’s in a `try-except` spiral! Is this about operations, tools, or advanced Python?",
        "fallback41": "I’m getting an IndexError! Could you specify your Python question about functions or basics?",
        "fallback42": "My Python script needs a rewrite! What topic—agents, ops, or tools—are you exploring?",
        "fallback43": "I think I forgot a `return` statement! Can you rephrase your Python-related query?",
        "fallback44": "My Python’s feeling object-oriented! Is your question about basic syntax or advanced functions?",
        "fallback45": "I need to clear my Python cache! Could you clarify your question about Python programming?",
        "fallback46": "My Python’s raising a ValueError! What concept—basics, tools, or agents—are you asking about?",
        "fallback47": "I’m stuck in a Python class! Can you repeat your question about Python operations or functions?",
        "fallback48": "My Python’s gone functional! Is this about advanced tools, agents, or basic syntax?",
        "fallback49": "I think I need a Python `lambda`! Could you specify your question about Python concepts?",
        "fallback50": "My Python’s in a virtual environment! What topic—ops, functions, or basics—are you curious about?",
        "fallback51": "I’m getting a ZeroDivisionError! Can you rephrase your Python question about tools or agents?",
        "fallback52": "My Python script’s feeling modular! Is your question about basic programming or advanced ops?",
        "fallback53": "I need `import help`! Could you clarify your Python question about functions or basics?",
        "fallback54": "My Python’s throwing an ImportError! What topic—agents, tools, or ops—are you exploring?",
        "fallback55": "I think I forgot a Python `list`! Can you repeat your question about Python programming?",
        "fallback56": "My Python’s feeling a bit `numpy`! Is this about basic syntax, functions, or advanced tools?",
        "fallback57": "I need to debug my Python logic! Could you specify your question about ops or agents?",
        "fallback58": "My Python’s in a `pandas` pickle! What concept—basics, functions, or tools—are you asking about?",
        "fallback59": "I’m getting a FileNotFoundError! Can you rephrase your Python question about programming?",
        "fallback60": "My Python’s gone multi-threaded! Is your question about advanced agents or basic operations?",
        "fallback61": "I think I need a Python `tuple`! Could you clarify your question about Python functions or tools?",
        "fallback62": "My Python’s raising an OverflowError! What topic—basics, ops, or agents—are you curious about?",
        "fallback63": "I need to restart my Python session! Can you repeat your question about Python concepts?",
        "fallback64": "My Python’s feeling a bit `matplotlib`! Is this about tools, functions, or basic syntax?",
        "fallback65": "I’m stuck in a Python `set`! Could you specify your question about advanced ops or agents?",
        "fallback66": "My Python script’s gone `django`! What topic—basics, tools, or functions—are you exploring?",
        "fallback67": "I think I dropped a Python `dict`! Can you rephrase your Python-related query?",
        "fallback68": "My Python’s throwing a RuntimeError! Is your question about basic programming or advanced tools?",
        "fallback69": "I need to `pip install patience`! Could you clarify your Python question about ops or agents?",
        "fallback70": "My Python’s in a `flask` frenzy! What concept—basics, functions, or tools—are you asking about?",
        "fallback71": "I’m getting a MemoryError! Can you repeat your question about Python programming?",
        "fallback72": "My Python’s feeling `tensorflow`! Is this about advanced agents, operations, or basic syntax?",
        "fallback73": "I think I need a Python `array`! Could you specify your Python question about functions or tools?",
        "fallback74": "My Python’s raising a SystemError! What topic—basics, ops, or agents—are you curious about?",
        "fallback75": "I need to reload my Python module! Can you rephrase your question about Python concepts?",
        "fallback76": "My Python’s gone `scikit-learn`! Is your question about tools, functions, or basic programming?",
        "fallback77": "I’m stuck in a Python `queue`! Could you clarify your question about advanced ops or agents?",
        "fallback78": "My Python script’s feeling `pytorch`! What topic—basics, tools, or functions—are you exploring?",
        "fallback79": "I think I forgot a Python `slice`! Can you repeat your question about Python programming?",
        "fallback80": "My Python’s throwing a UnicodeError! Is this about basic syntax, advanced tools, or agents?",
        "fallback81": "I need to debug my Python `regex`! Could you specify your question about ops or functions?",
        "fallback82": "My Python’s in a `keras` loop! What concept—basics, tools, or agents—are you asking about?",
        "fallback83": "I’m getting a TimeoutError! Can you rephrase your Python question about programming?",
        "fallback84": "My Python’s feeling `sqlalchemy`! Is your question about advanced operations or basic functions?",
        "fallback85": "I think I need a Python `generator`! Could you clarify your question about Python tools or agents?",
        "fallback86": "My Python’s raising a RecursionError! What topic—basics, ops, or functions—are you curious about?",
        "fallback87": "I need to restart my Python interpreter! Can you repeat your question about Python concepts?",
        "fallback88": "My Python’s gone `asyncio`! Is this about advanced tools, agents, or basic syntax?",
        "fallback89": "I’m stuck in a Python `heap`! Could you specify your question about operations or functions?",
        "fallback90": "My Python script’s feeling `opencv`! What topic—basics, tools, or agents—are you exploring?",
        "fallback91": "I think I dropped a Python `byte`! Can you rephrase your Python-related query?",
        "fallback92": "My Python’s throwing a BlockingIOError! Is your question about basic programming or advanced ops?",
        "fallback93": "I need to `pip install focus`! Could you clarify your Python question about tools or functions?",
        "fallback94": "My Python’s in a `seaborn` swirl! What concept—basics, agents, or ops—are you asking about?",
        "fallback95": "I’m getting a BrokenPipeError! Can you repeat your question about Python programming?",
        "fallback96": "My Python’s feeling `plotly`! Is this about advanced tools, functions, or basic syntax?",
        "fallback97": "I think I need a Python `deque`! Could you specify your question about ops or agents?",
        "fallback98": "My Python’s raising a ConnectionError! What topic—basics, tools, or functions—are you curious about?",
        "fallback99": "I need to clear my Python `buffer`! Can you rephrase your question about Python concepts?",
        "fallback100": "My Python’s gone `jupyter`! Is your question about basic programming, advanced tools, or agents?",
        "fallback101": "Whoops, my Python turtle got lost! Try this to say hi: `print(\"Hello, Python!\")`. What do you want to learn?",
        "fallback102": "My code’s acting shy! Here’s a variable: `name = \"Python\"` then `print(name)`. Ask me about Python basics!",
        "fallback103": "I think my Python forgot how to count! Try: `for i in range(5): print(i)`. What's your Python question?",
        "fallback104": "Oh no, my Python’s stuck! Here’s a fun function: `def say_hi(): print(\"Hi!\")`. What do you want to code?",
        "fallback105": "My Python’s daydreaming! Try: `x = 10; print(x + 5)`. Can you ask about variables or loops?",
        "fallback106": "Looks like my code needs a nap! Try: `print(2 * 3)`. What Python topic are you curious about?",
        "fallback107": "My Python’s playing hide-and-seek! Here’s a loop: `while x < 5: print(x); x += 1`. What’s your question?",
        "fallback108": "I dropped my Python blocks! Try: `if True: print(\"Yay!\")`. Ask me about conditions or functions!",
        "fallback109": "My Python’s a bit puzzled! Here’s a list: `fruits = [\"apple\", \"banana\"]; print(fruits)`. What’s up?",
        "fallback110": "Oh, my Python’s dancing! Try: `def add(a, b): return a + b; print(add(2, 3))`. What do you want to learn?",
        "fallback111": "My code’s got the giggles! Try: `print(\"I love coding!\")`. Can you ask about Python basics?",
        "fallback112": "My Python’s feeling loopy! Here’s a for loop: `for x in [1, 2, 3]: print(x)`. What’s your question?",
        "fallback113": "I think my Python ate my homework! Try: `x = \"kid\"; print(\"Hello, \" + x)`. Ask me something fun!",
        "fallback114": "My Python’s jumping around! Try: `if x > 5: print(\"Big number!\")`. What Python trick do you want?",
        "fallback115": "My code’s singing songs! Here’s a function: `def square(num): return num * num; print(square(4))`. Ask away!",
        "fallback116": "My Python’s on a treasure hunt! Try: `numbers = [1, 2, 3]; print(numbers[0])`. What’s your question?",
        "fallback117": "Oh no, my Python’s confused! Try: `print(10 - 4)`. Can you ask about math or variables in Python?",
        "fallback118": "My Python’s chasing its tail! Try: `for i in range(3): print(\"Loop!\")`. What do you want to explore?",
        "fallback119": "My code’s doing cartwheels! Try: `name = input(\"Your name: \"); print(name)`. Ask about input!",
        "fallback120": "My Python’s feeling super! Here’s a condition: `if x == 10: print(\"Ten!\")`. What’s your Python question?",
        "fallback121": "I think my Python’s napping! Try: `def greet(): print(\"Hello, coder!\"); greet()`. What do you want to code?",
        "fallback122": "My Python’s got butterflies! Try: `x = 7; print(x * 2)`. Can you ask about numbers or loops?",
        "fallback123": "My code’s playing tag! Here’s a list: `colors = [\"red\", \"blue\"]; print(colors[1])`. What’s up?",
        "fallback124": "My Python’s hopping around! Try: `while x > 0: print(x); x -= 1`. Ask me about loops or functions!",
        "fallback125": "Oh, my Python’s curious! Try: `print(\"3 + 4 =\", 3 + 4)`. What Python topic are you exploring?",
        "fallback126": "My Python’s feeling chatty! Try: `def say_bye(): print(\"Bye!\"); say_bye()`. What’s your question?",
        "fallback127": "My code’s bouncing! Try: `if False: print(\"Nope!\"); else: print(\"Yes!\")`. Ask about conditions!",
        "fallback128": "My Python’s on a roll! Try: `numbers = [10, 20]; print(numbers[-1])`. What do you want to learn?",
        "fallback129": "I think my Python’s dreaming! Try: `x = 5; print(x ** 2)`. Can you ask about math or variables?",
        "fallback130": "My Python’s super excited! Try: `for letter in \"hi\": print(letter)`. What Python trick do you want?",
        "fallback131": "My code’s sparkling! Try: `def double(x): return x * 2; print(double(5))`. Ask me something fun!",
        "fallback132": "My Python’s doing flips! Try: `print(\"Your score:\", 100)`. Can you ask about printing or loops?",
        "fallback133": "My Python’s feeling magical! Try: `if x != 0: print(\"Not zero!\")`. What’s your Python question?",
        "fallback134": "Oh no, my code’s lost! Try: `animals = [\"cat\", \"dog\"]; print(animals)`. Ask about lists or functions!",
        "fallback135": "My Python’s singing! Try: `x = 3; y = 4; print(x + y)`. What do you want to explore?",
        "fallback136": "My Python’s on an adventure! Try: `def count(): print(1, 2, 3); count()`. What’s your question?",
        "fallback137": "My code’s glowing! Try: `for i in range(4): print(i + 1)`. Can you ask about loops or numbers?",
        "fallback138": "My Python’s feeling bubbly! Try: `print(\"Python is fun!\")`. What Python topic are you curious about?",
        "fallback139": "I think my Python’s curious! Try: `if x < 10: print(\"Small number!\")`. Ask about conditions!",
        "fallback140": "My Python’s bouncing! Try: `def say_hello(name): print(\"Hi, \" + name); say_hello(\"Kid\")`. Ask away!",
        "fallback141": "My code’s doing somersaults! Try: `scores = [90, 80]; print(scores[0])`. What do you want to learn?",
        "fallback142": "My Python’s feeling speedy! Try: `x = 8; print(x // 2)`. Can you ask about math or variables?",
        "fallback143": "My Python’s on a quest! Try: `while x <= 3: print(\"Go!\"); x += 1`. What’s your Python question?",
        "fallback144": "Oh, my Python’s happy! Try: `print(\"5 * 6 =\", 5 * 6)`. Ask about numbers or functions!",
        "fallback145": "My code’s twinkling! Try: `def add_three(x): return x + 3; print(add_three(2))`. What’s up?",
        "fallback146": "My Python’s feeling awesome! Try: `if x == \"yes\": print(\"Cool!\")`. Can you ask about conditions?",
        "fallback147": "My Python’s zooming! Try: `items = [\"pen\", \"book\"]; print(items[-1])`. What do you want to code?",
        "fallback148": "I think my Python’s giggling! Try: `x = 9; print(x - 3)`. Ask about math or loops!",
        "fallback149": "My Python’s sparkling! Try: `for i in [1, 2]: print(\"Hi!\")`. What Python trick do you want?",
        "fallback150": "My code’s flying! Try: `def say_wow(): print(\"Wow!\"); say_wow()`. Can you ask about functions?",
        "fallback151": "My Python’s feeling sunny! Try: `print(\"Your age:\", 10)`. What topic are you exploring?",
        "fallback152": "My Python’s doing loops! Try: `if x > 0: print(\"Positive!\")`. Ask about conditions or lists!",
        "fallback153": "Oh no, my code’s sleepy! Try: `toys = [\"ball\", \"car\"]; print(toys[0])`. What’s your question?",
        "fallback154": "My Python’s jumping! Try: `x = 4; print(x * 3)`. Can you ask about numbers or loops?",
        "fallback155": "My Python’s on a mission! Try: `def print_star(): print(\"*\"); print_star()`. What do you want to learn?",
        "fallback156": "My code’s shining! Try: `for i in range(2): print(\"Code!\")`. Ask about loops or functions!",
        "fallback157": "My Python’s feeling great! Try: `print(\"2 + 2 =\", 2 + 2)`. What Python topic are you curious about?",
        "fallback158": "I think my Python’s ready! Try: `if x == 5: print(\"Five!\")`. Can you ask about conditions?",
        "fallback159": "My Python’s soaring! Try: `def greet_kid(): print(\"Hey, coder!\"); greet_kid()`. Ask away!",
        "fallback160": "My code’s buzzing! Try: `numbers = [5, 10]; print(numbers[1])`. What do you want to explore?",
        "fallback161": "My Python’s feeling fun! Try: `x = 6; print(x + 4)`. Can you ask about math or loops?",
        "fallback162": "My Python’s on a roll! Try: `while x < 4: print(\"Run!\"); x += 1`. What’s your Python question?",
        "fallback163": "Oh, my Python’s excited! Try: `print(\"7 - 2 =\", 7 - 2)`. Ask about numbers or functions!",
        "fallback164": "My code’s sparkling! Try: `def add_five(x): return x + 5; print(add_five(3))`. What’s up?",
        "fallback165": "My Python’s feeling cool! Try: `if x != 1: print(\"Not one!\")`. Can you ask about conditions?",
        "fallback166": "My Python’s zooming! Try: `items = [\"hat\", \"shoe\"]; print(items[0])`. What do you want to code?",
        "fallback167": "I think my Python’s happy! Try: `x = 10; print(x // 5)`. Ask about math or variables!",
        "fallback168": "My Python’s glowing! Try: `for i in [1, 2, 3]: print(\"Go!\")`. What Python trick do you want?",
        "fallback169": "My code’s dancing! Try: `def say_cool(): print(\"Cool!\"); say_cool()`. Can you ask about functions?",
        "fallback170": "My Python’s feeling super! Try: `print(\"Your points:\", 50)`. What topic are you exploring?",
        "fallback171": "My Python’s doing flips! Try: `if x < 5: print(\"Small!\")`. Ask about conditions or lists!",
        "fallback172": "Oh no, my code’s curious! Try: `foods = [\"pizza\", \"cake\"]; print(foods[-1])`. What’s your question?",
        "fallback173": "My Python’s bouncing! Try: `x = 3; print(x * 4)`. Can you ask about numbers or loops?",
        "fallback174": "My Python’s on an adventure! Try: `def print_heart(): print(\"<3\"); print_heart()`. What do you want to learn?",
        "fallback175": "My code’s twinkling! Try: `for i in range(3): print(\"Fun!\")`. Ask about loops or functions!",
        "fallback176": "My Python’s feeling awesome! Try: `print(\"8 + 1 =\", 8 + 1)`. What Python topic are you curious about?",
        "fallback177": "I think my Python’s ready! Try: `if x == 2: print(\"Two!\")`. Can you ask about conditions?",
        "fallback178": "My Python’s soaring! Try: `def greet_friend(): print(\"Hi, friend!\"); greet_friend()`. Ask away!",
        "fallback179": "My code’s buzzing! Try: `numbers = [15, 25]; print(numbers[0])`. What do you want to explore?",
        "fallback180": "My Python’s feeling fun! Try: `x = 5; print(x - 1)`. Can you ask about math or loops?",
        "fallback181": "My Python’s on a quest! Try: `while x > 1: print(\"Jump!\"); x -= 1`. What’s your Python question?",
        "fallback182": "Oh, my Python’s happy! Try: `print(\"9 * 2 =\", 9 * 2)`. Ask about numbers or functions!",
        "fallback183": "My code’s sparkling! Try: `def add_ten(x): return x + 10; print(add_ten(5))`. What’s up?",
        "fallback184": "My Python’s feeling cool! Try: `if x > 10: print(\"Big!\")`. Can you ask about conditions?",
        "fallback185": "My Python’s zooming! Try: `items = [\"bag\", \"pen\"]; print(items[1])`. What do you want to code?",
        "fallback186": "I think my Python’s giggling! Try: `x = 7; print(x + 3)`. Ask about math or variables!",
        "fallback187": "My Python’s glowing! Try: `for i in [1, weddings 2]: print(\"Yay!\")`. What Python trick do you want?",
        "fallback188": "My code’s dancing! Try: `def say_awesome(): print(\"Awesome!\"); say_awesome()`. Can you ask about functions?",
        "fallback189": "My Python’s feeling super! Try: `print(\"Your level:\", 3)`. What topic are you exploring?",
        "fallback190": "My Python’s doing loops! Try: `if x != 5: print(\"Not five!\")`. Ask about conditions or lists!",
        "fallback191": "Oh no, my code’s sleepy! Try: `toys = [\"doll\", \"robot\"]; print(toys[0])`. What’s your question?",
        "fallback192": "My Python’s jumping! Try: `x = 8; print(x * 2)`. Can you ask about numbers or loops?",
        "fallback193": "My Python’s on a mission! Try: `def print_smile(): print(\":)\"); print_smile()`. What do you want to learn?",
        "fallback194": "My code’s shining! Try: `for i in range(4): print(\"Wow!\")`. Ask about loops or functions!",
        "fallback195": "My Python’s feeling great! Try: `print(\"6 + 3 =\", 6 + 3)`. What Python topic are you curious about?",
        "fallback196": "I think my Python’s ready! Try: `if x == 10: print(\"Ten!\")`. Can you ask about conditions?",
        "fallback197": "My Python’s soaring! Try: `def greet_coder(): print(\"Hey, coder!\"); greet_coder()`. Ask away!",
        "fallback198": "My code’s buzzing! Try: `numbers = [30, 40]; print(numbers[1])`. What do you want to explore?",
        "fallback199": "My Python’s feeling fun! Try: `x = 4; print(x + 6)`. Can you ask about math or loops?",
        "fallback200": "My Python’s on a roll! Try: `while x < 5: print(\"Go!\"); x += 1`. What’s your Python question?"
    }
    
    message_lower = message.lower().strip()
    
    # Look for exact matches first
    if message_lower in fallback_responses:
        return fallback_responses[message_lower]
    
    # Look for keyword-based matches for specific topics
    for key in ["variables", "loops", "functions", "print", "if statement", "list", "dictionary", "what is python"]:
        if key in message_lower:
            return fallback_responses[key]
    
    # Return a generic fallback response
    return ("I'm here to help you learn Python programming! Try asking about variables, loops, functions, or other Python concepts. For example, try 'How do I create a variable in Python?' or 'What is a for loop?'")

def generate_response(message, persona="YOU ARE A FRIENDLY PYTHON TUTOR"):
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
        return get_fallback_response(message)
    
    try:
        # Build the prompt with the persona and focus on Python programming
        prompt = f"{persona}\n\nYou are helping a child learn Python programming. Provide simple, friendly, and clear explanations with examples where appropriate.\n\nQuestion: {message}"
        
        # Generate response
        response = st.session_state.GEMINI_MODEL.generate_content(prompt)
        
        # Return the text
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        # If API call fails, use our fallback system
        return get_fallback_response(message)

def display_chatbot(container):
    """
    Display the chatbot interface in the given container
    
    Args:
        container: The Streamlit container to use
    """
    # Title and introduction
    container.subheader("Got Questions? Ask Our AI Python Tutor! 🤖")
    container.info("Ask anything about Python programming, and our friendly AI tutor will help you learn in a fun way!")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Use a form for input to manage submission and clearing
    with container.form(key="chat_form", clear_on_submit=True):
        message = st.text_input("Ask a question about Python or programming:")
        submit_button = st.form_submit_button("Ask")
    
    if submit_button and message:
        with st.spinner("Thinking..."):
            # Set friendly Python tutor persona
            persona = "You are a friendly Python tutor who loves helping kids learn programming. You use simple words, fun examples, and a cheerful tone to make Python exciting and easy to understand."
            
            # Get response
            response = generate_response(message, persona)
            
            # Add to chat history
            st.session_state.chat_history.append({"user": message, "bot": response})
    
    # Display chat history
    if st.session_state.chat_history:
        container.subheader("Conversation")
        
        # Get username for display
        display_name = f"You ({st.session_state.username})" if st.session_state.get("username") else "You (Anonymous)"
        
        for i, chat in enumerate(st.session_state.chat_history):
            # User message
            container.markdown(f"**{display_name}:** {chat['user']}")
            
            # Bot response
            container.markdown(f"**AI Tutor:** {chat['bot']}")
            
            # Add separator except for the last message
            if i < len(st.session_state.chat_history) - 1:
                container.markdown("---")
    
    # Add a clear chat button
    if st.session_state.chat_history:
        if container.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
