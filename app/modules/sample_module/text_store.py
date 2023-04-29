class TextStore:
    """
    This class is for the text messages for the user
    """
    ask_agree = "Do you agree to be part of our shop?"
    ask_name = "Great! Thank you for being a part of our program. What is your name?"

    @staticmethod
    def greet_user(name: str) -> str:
        return f"Welcome {name}. You will start to get your first message tomorrow."

    say_np = "No problem. Thank you for considering our project."
