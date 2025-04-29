import streamlit as st
import random

# Function to display a challenge
def display_challenge(index, execute_python_code, complete_callback, next_callback, prev_callback, completed_challenges):
    """
    Display a coding challenge at the given index
    
    Args:
        index (int): The index of the challenge to display
        execute_python_code (function): Function to execute Python code
        complete_callback (function): Function to call when the challenge is complete
        next_callback (function): Function to call for the "Next" button
        prev_callback (function): Function to call for the "Previous" button
        completed_challenges (list): List of indices of completed challenges
    """
    # Get the challenge data
    challenge = challenges_data[index]
    
    # Display challenge title
    st.title(f"Challenge: {challenge['title']} {challenge['emoji']}")
    
    # Check if challenge is already completed
    is_completed = index in completed_challenges
    if is_completed:
        st.success("You've already completed this challenge! 🎉")
    
    # Display challenge description
    st.markdown(challenge["description"])
    
    # Code editor
    user_code = st.text_area("Write your code here:", challenge["starter_code"], height=250)
    
    # Hint expander
    with st.expander("Need a hint?"):
        st.markdown(challenge["hint"])
    
    # Run code button
    if st.button("Run Code ▶️"):
        output, error = execute_python_code(user_code)
        
        if error:
            st.error(f"Oops! Something went wrong:\n\n{error}")
        else:
            st.success("Code ran successfully! 🎉")
            st.code(output, language="")
            
            # Check if challenge is solved
            if challenge["validation"](user_code, output):
                if not is_completed:
                    st.balloons()
                    st.success("🎯 Great job! You solved the challenge! 🎯")
                    st.button("Mark as Complete ✅", on_click=complete_callback)
                else:
                    st.success("🎮 You've already completed this challenge! 🎮")
            else:
                st.warning("Hmm, that's not quite right. Try again!")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if index > 0:
            st.button("← Previous", on_click=prev_callback)
            
    with col3:
        if index < len(challenges_data) - 1:
            st.button("Next →", on_click=next_callback)
            
    # Challenge progress
    st.progress((index + 1) / len(challenges_data))
    st.caption(f"Challenge {index + 1} of {len(challenges_data)}")

# Challenge data
challenges_data = [
    {
        "title": "Hello, Python!",
        "emoji": "👋",
        "description": """
        # Your First Challenge: Say Hello! 👋
        
        Can you write a program that says hello to your favorite animal?
        
        **Instructions:**
        1. Use the `print()` function
        2. Inside the print function, put a greeting message in quotes
        3. Make sure to include your favorite animal in the message
        
        **Example:** If your favorite animal is a dolphin, you might print:
        ```
        Hello, dolphin! You're awesome!
        ```
        """,
        "starter_code": '# Write your code here\nprint("Hello, ")',
        "hint": "Remember to put your text inside quotes in the print function!",
        "solution": 'print("Hello, tiger! You\'re awesome!")',
        "validation": lambda code, output: "hello" in output.lower() and any(animal in output.lower() for animal in ["dog", "cat", "tiger", "lion", "dolphin", "turtle", "rabbit", "bear", "bird", "fish", "panda", "monkey", "elephant", "giraffe", "zebra", "dinosaur", "dragon", "unicorn"])
    },
    {
        "title": "Math Magic",
        "emoji": "🧙‍♂️",
        "description": """
        # Math Magician Challenge 🧙‍♂️
        
        Can you create a spell (program) that calculates the total number of legs in a magical zoo?
        
        **Instructions:**
        1. Create variables for the number of each animal
        2. Calculate the total number of legs
        3. Print out the result
        
        **Animals in the zoo:**
        - 3 unicorns (4 legs each)
        - 2 dragons (4 legs each)
        - 5 fairies (2 legs each)
        
        **Your program should calculate and print the total number of legs.**
        """,
        "starter_code": "# Create your variables\nunicorns = 3\ndragons = 2\nfairies = 5\n\n# Calculate total legs\n\n\n# Print the result\n",
        "hint": "Multiply the number of each animal by their number of legs, then add them together!",
        "solution": "unicorns = 3\ndragons = 2\nfairies = 5\n\n# Calculate total legs\nunicorn_legs = unicorns * 4\ndragon_legs = dragons * 4\nfairy_legs = fairies * 2\ntotal_legs = unicorn_legs + dragon_legs + fairy_legs\n\n# Print the result\nprint(f\"The magical zoo has {total_legs} legs in total!\")",
        "validation": lambda code, output: "30" in output
    },
    {
        "title": "Name Wizard",
        "emoji": "✨",
        "description": """
        # Name Wizard Challenge ✨
        
        Can you create a program that turns any name into a magical wizard name?
        
        **Instructions:**
        1. Create a variable with your name
        2. Create a wizard name by:
           - Adding "the" in the middle
           - Adding a magical word at the end
        3. Print out the wizard name
        
        **Example:** If your name is "Alex", your wizard name might be "Alex the Magnificent"
        """,
        "starter_code": "# Set up your name\nmy_name = \"Alex\"\n\n# Create wizard name\n\n\n# Print the wizard name\n",
        "hint": "Use the + operator to combine strings together! Don't forget spaces between words.",
        "solution": 'my_name = "Alex"\n\n# Create wizard name\nwizard_title = "the"\nwizard_power = "Magnificent"\nwizard_name = my_name + " " + wizard_title + " " + wizard_power\n\n# Print the wizard name\nprint(wizard_name)',
        "validation": lambda code, output: " the " in output.lower() and len(output.split()) >= 3
    },
    {
        "title": "Secret Code Generator",
        "emoji": "🔐",
        "description": """
        # Secret Code Generator Challenge 🔐
        
        Can you create a program that turns words into secret code?
        
        **Instructions:**
        1. Ask for a secret word (we've done this part for you)
        2. Create a secret code by:
           - Reversing the word
           - Adding "00" to the end
        3. Print out the secret code
        
        **Example:** If the secret word is "python", the secret code would be "nohtyp00"
        """,
        "starter_code": "# We've created the secret word for you\nsecret_word = \"python\"\n\n# Your code to create the secret code goes here\n\n\n# Print the secret code\n",
        "hint": "You can reverse a string in Python using: reversed_word = secret_word[::-1]",
        "solution": 'secret_word = "python"\n\n# Create secret code\nreversed_word = secret_word[::-1]\nsecret_code = reversed_word + "00"\n\n# Print the secret code\nprint(f"The secret code is: {secret_code}")',
        "validation": lambda code, output: any(word[::-1] in output for word in ["python", "code", "secret"]) and "00" in output
    },
    {
        "title": "Treasure Hunt",
        "emoji": "🗺️",
        "description": """
        # Treasure Hunt Game 🗺️
        
        You're on a treasure hunt! Create a program that tells you if you've found the treasure.
        
        **Instructions:**
        1. Create variables for your current position (x, y) on the map
        2. The treasure is hidden at position (5, 3)
        3. Use an if statement to check if you're at the treasure's location
        4. Print a message telling if you found the treasure or not
        """,
        "starter_code": "# Your current position\nx = 5  # Try changing these values!\ny = 3\n\n# Treasure position\ntreasure_x = 5\ntreasure_y = 3\n\n# Check if you found the treasure\n\n",
        "hint": "Use an if statement to check if both x == treasure_x AND y == treasure_y",
        "solution": "# Your current position\nx = 5\ny = 3\n\n# Treasure position\ntreasure_x = 5\ntreasure_y = 3\n\n# Check if you found the treasure\nif x == treasure_x and y == treasure_y:\n    print(\"Hooray! You found the treasure! 💰\")\nelse:\n    print(f\"No treasure here. Keep looking! You're at ({x}, {y})\")",
        "validation": lambda code, output: ("found the treasure" in output.lower() and "hooray" in output.lower()) or ("no treasure" in output.lower() and "keep looking" in output.lower())
    },
    {
        "title": "Animal Sounds Loop",
        "emoji": "🔊",
        "description": """
        # Animal Sounds Challenge 🔊
        
        Can you create a program that makes different animal sounds in a loop?
        
        **Instructions:**
        1. Create a list of animal sounds
        2. Use a loop to print each sound three times
        3. Add the animal emoji before each sound
        
        **Example Output:**
        ```
        🐶 Woof! Woof! Woof!
        🐱 Meow! Meow! Meow!
        ```
        """,
        "starter_code": "# Create your animal dictionary (emoji and sound)\nanimals = {\n    '🐶': 'Woof!',\n    '🐱': 'Meow!',\n    '🐮': 'Moo!'\n}\n\n# Now loop through and print each sound three times\n",
        "hint": "Try using a for loop to go through the dictionary items(). For each emoji and sound, use another loop to repeat the sound 3 times.",
        "solution": "# Create your animal dictionary\nanimals = {\n    '🐶': 'Woof!',\n    '🐱': 'Meow!',\n    '🐮': 'Moo!'\n}\n\n# Loop through animals\nfor emoji, sound in animals.items():\n    # Print the emoji and the sound three times\n    print(f\"{emoji} {sound} {sound} {sound}\")",
        "validation": lambda code, output: all(animal in output for animal in ["🐶", "🐱"]) and all(sound in output for sound in ["Woof!", "Meow!"])
    },
    {
        "title": "Magic Potion Mixer",
        "emoji": "🧪",
        "description": """
        # Magic Potion Mixer Challenge 🧪
        
        Create a program that helps a wizard mix magical potions!
        
        **Instructions:**
        1. Create a function called `mix_potion`
        2. The function should take two ingredients as parameters
        3. It should return a string saying what potion was created
        4. Call the function with different ingredient combinations
        
        **Example:** 
        ```python
        result = mix_potion("dragon scales", "unicorn hair")
        print(result)  # Should print something like "You created a Potion of Flying!"
        ```
        """,
        "starter_code": "# Define your mix_potion function\ndef mix_potion(ingredient1, ingredient2):\n    # Your code here\n    pass\n    \n# Test your function\nresult1 = mix_potion(\"dragon scales\", \"unicorn hair\")\nprint(result1)\n\nresult2 = mix_potion(\"toad eyes\", \"butterfly wings\")\nprint(result2)",
        "hint": "You can use if/elif statements to check different ingredient combinations, or create a dictionary of recipe combinations!",
        "solution": "def mix_potion(ingredient1, ingredient2):\n    # Create a dictionary of ingredient combinations and their results\n    recipes = {\n        (\"dragon scales\", \"unicorn hair\"): \"Potion of Flying\",\n        (\"unicorn hair\", \"dragon scales\"): \"Potion of Flying\",\n        (\"toad eyes\", \"butterfly wings\"): \"Potion of Invisibility\",\n        (\"butterfly wings\", \"toad eyes\"): \"Potion of Invisibility\",\n    }\n    \n    # Check if this combination is in our recipes\n    if (ingredient1, ingredient2) in recipes:\n        return f\"You created a {recipes[(ingredient1, ingredient2)]}!\"\n    elif (ingredient2, ingredient1) in recipes:\n        return f\"You created a {recipes[(ingredient2, ingredient1)]}!\"\n    else:\n        return f\"You mixed {ingredient1} and {ingredient2} and created... a puff of smoke!\"",
        "validation": lambda code, output: "created a" in output.lower() and ("potion" in output.lower() or "smoke" in output.lower())
    }
]