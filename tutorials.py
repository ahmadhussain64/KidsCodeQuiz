import streamlit as st

# Function to display a tutorial
def display_tutorial(index, next_callback, prev_callback):
    """
    Display a tutorial at the given index
    
    Args:
        index (int): The index of the tutorial to display
        next_callback (function): Function to call for the "Next" button
        prev_callback (function): Function to call for the "Previous" button
    """
    # Get the tutorial data
    tutorial = tutorials_data[index]
    
    # Display tutorial title
    st.title(f"{tutorial['title']} {tutorial['emoji']}")
    
    # Display tutorial content
    st.markdown(tutorial["content"])
    
    # Code editor
    user_code = st.text_area("Try the code here:", tutorial["example"], height=200)
    
    # Run code button
    if st.button("Run Code ▶️"):
        from code_executor import execute_python_code
        
        output, error = execute_python_code(user_code)
        
        if error:
            st.error(f"Oops! Something went wrong:\n\n{error}")
        else:
            st.success("Code ran successfully! 🎉")
            st.code(output, language="")
            
            # Check if output matches expected output
            if output.strip() == tutorial["expected_output"].strip():
                st.balloons()
                st.success("Perfect! You got it right! ⭐")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if index > 0:
            st.button("← Previous", on_click=prev_callback)
            
    with col3:
        if index < len(tutorials_data) - 1:
            st.button("Next →", on_click=next_callback)
            
    # Tutorial progress
    st.progress((index + 1) / len(tutorials_data))
    st.caption(f"Tutorial {index + 1} of {len(tutorials_data)}")

# Tutorial data
tutorials_data = [
    {
        "title": "Let's Meet Python! 👋",
        "emoji": "🐍",
        "content": """
        # Hello, Python! 👋
        
        Python is a friendly programming language that makes it easy to tell computers what to do!
        
        ### Your First Python Program
        
        Let's start with a simple program that prints "Hello, World!" to the screen:
        
        ```python
        print("Hello, World!")
        ```
        
        This is what this program does:
        - `print()` is a Python function that displays text on the screen
        - Inside the parentheses `()`, we put what we want to display
        - The text is inside quotes `"..."` so Python knows it's text
        
        ### Try it yourself!
        
        Type the code below and see what happens:
        """,
        "example": 'print("Hello, World!")',
        "expected_output": "Hello, World!"
    },
    {
        "title": "Numbers and Math 🔢",
        "emoji": "🧮",
        "content": """
        # Python Loves Math! 🔢
        
        Python is great at doing math calculations. You can use Python just like a calculator!
        
        ### Basic Math Operations
        
        - Addition: `+`
        - Subtraction: `-`
        - Multiplication: `*`
        - Division: `/`
        
        ### Example
        
        ```python
        print(5 + 3)   # Addition: 8
        print(10 - 4)  # Subtraction: 6
        print(3 * 5)   # Multiplication: 15
        print(10 / 2)  # Division: 5.0
        ```
        
        ### Try it yourself!
        
        Write a program that calculates how many cookies each person gets if you have 20 cookies and 4 friends:
        """,
        "example": "cookies = 20\nfriends = 4\ncookies_per_friend = cookies / friends\nprint(f'Each friend gets {cookies_per_friend} cookies!')",
        "expected_output": "Each friend gets 5.0 cookies!"
    },
    {
        "title": "Variables - Name and Remember! 📝",
        "emoji": "🏷️",
        "content": """
        # Variables: Python's Memory 📝
        
        Variables are like labeled boxes where Python can store information for later use.
        
        ### How to Create a Variable
        
        You create a variable by giving it a name and using `=` to assign a value to it:
        
        ```python
        age = 10
        name = "Alex"
        is_happy = True
        ```
        
        Once you create a variable, you can use it in your code:
        
        ```python
        print(name)  # Prints: Alex
        print("My age is", age)  # Prints: My age is 10
        ```
        
        ### Variable Names
        
        Good variable names:
        - Describe what they contain
        - Use lowercase letters and underscores for spaces
        - Examples: `my_age`, `favorite_color`, `player_score`
        
        ### Try it yourself!
        
        Create variables for your name and your favorite animal, then print a sentence using both:
        """,
        "example": 'name = "Kim"\nfavorite_animal = "dolphin"\nprint(f"My name is {name} and I love {favorite_animal}s!")',
        "expected_output": "My name is Kim and I love dolphins!"
    },
    {
        "title": "If Statements - Making Decisions! 🤔",
        "emoji": "🔀",
        "content": """
        # If Statements: Making Decisions 🤔
        
        Sometimes your program needs to make decisions based on certain conditions. That's where `if` statements come in!
        
        ### Basic If Statement
        
        ```python
        age = 10
        
        if age >= 8:
            print("You're old enough for this ride!")
        else:
            print("Sorry, you need to be at least 8 years old.")
        ```
        
        ### Comparison Operators
        
        - Equal to: `==`
        - Not equal to: `!=`
        - Greater than: `>`
        - Less than: `<`
        - Greater than or equal to: `>=`
        - Less than or equal to: `<=`
        
        ### Indentation is Important!
        
        In Python, we use spaces (usually 4) to show which code belongs inside the if statement. This is called "indentation."
        
        ### Try it yourself!
        
        Write a program that checks if a number is positive, negative, or zero:
        """,
        "example": "number = 7\n\nif number > 0:\n    print(f'{number} is positive!')\nelif number < 0:\n    print(f'{number} is negative!')\nelse:\n    print('The number is zero!')",
        "expected_output": "7 is positive!"
    },
    {
        "title": "Loops - Repeating Things! 🔄",
        "emoji": "🔁",
        "content": """
        # Loops: Doing Things Over and Over 🔄
        
        Loops let you repeat code without having to write it multiple times.
        
        ### For Loops
        
        A `for` loop repeats code for a specific number of times:
        
        ```python
        for i in range(5):
            print(f"Count: {i}")
        ```
        
        This will print:
        ```
        Count: 0
        Count: 1
        Count: 2
        Count: 3
        Count: 4
        ```
        
        ### While Loops
        
        A `while` loop repeats code as long as a condition is true:
        
        ```python
        count = 0
        while count < 5:
            print(f"Count: {count}")
            count = count + 1
        ```
        
        ### Try it yourself!
        
        Write a program that prints a countdown from 5 to 1, then prints "Blast off! 🚀":
        """,
        "example": "for i in range(5, 0, -1):\n    print(i)\nprint('Blast off! 🚀')",
        "expected_output": "5\n4\n3\n2\n1\nBlast off! 🚀"
    },
    {
        "title": "Lists - Storing Multiple Items! 📋",
        "emoji": "📝",
        "content": """
        # Lists: Collections of Items 📋
        
        Lists allow you to store multiple items in a single variable.
        
        ### Creating a List
        
        ```python
        fruits = ["apple", "banana", "orange", "grape"]
        numbers = [1, 2, 3, 4, 5]
        mixed = ["hello", 42, True, 3.14]
        ```
        
        ### Accessing List Items
        
        You can access items in a list by their position (index). Remember, Python starts counting at 0!
        
        ```python
        fruits = ["apple", "banana", "orange", "grape"]
        print(fruits[0])  # Prints: apple
        print(fruits[2])  # Prints: orange
        ```
        
        ### Common List Operations
        
        ```python
        fruits = ["apple", "banana"]
        
        # Add an item to the end
        fruits.append("orange")  # Now: ["apple", "banana", "orange"]
        
        # Get the length of a list
        print(len(fruits))  # Prints: 3
        
        # Loop through a list
        for fruit in fruits:
            print(f"I like {fruit}s!")
        ```
        
        ### Try it yourself!
        
        Create a list of three of your favorite things, then loop through and print them:
        """,
        "example": 'favorite_things = ["robots", "ice cream", "swimming"]\n\nfor thing in favorite_things:\n    print(f"I really love {thing}!")',
        "expected_output": "I really love robots!\nI really love ice cream!\nI really love swimming!"
    },
    {
        "title": "Functions - Create Your Own Commands! 🧩",
        "emoji": "🔧",
        "content": """
        # Functions: Your Own Custom Commands 🧩
        
        Functions are like mini-programs within your program. They help you organize your code and reuse it.
        
        ### Creating a Function
        
        ```python
        def greet(name):
            print(f"Hello, {name}! How are you today?")
            
        # Using the function
        greet("Alex")  # Prints: Hello, Alex! How are you today?
        greet("Sam")   # Prints: Hello, Sam! How are you today?
        ```
        
        ### Function Parameters
        
        Functions can take inputs (called parameters) that change how they work:
        
        ```python
        def add_numbers(a, b):
            result = a + b
            print(f"{a} + {b} = {result}")
            return result
        ```
        
        ### Return Values
        
        Functions can also give back (return) values that you can use later:
        
        ```python
        def double(number):
            return number * 2
            
        result = double(5)  # result will be 10
        ```
        
        ### Try it yourself!
        
        Create a function that takes a person's name and their favorite color, and prints a message about them:
        """,
        "example": 'def describe_person(name, favorite_color):\n    print(f"{name}\'s favorite color is {favorite_color}!")\n\ndescribe_person("Max", "blue")\ndescribe_person("Lily", "purple")',
        "expected_output": "Max's favorite color is blue!\nLily's favorite color is purple!"
    }
]