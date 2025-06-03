"""
variables.py

Stores constants for the number guessing game.
"""

DIFFICULTY_SELECTION_DICT = {
    1: ("Easy", 10),
    2: ("Medium", 5),
    3: ("Hard", 3),
}


WELCOME_MESSAGE = """
Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
Please select difficulty level using the options below:
1. Easy (10 guesses)
2. Medium (5 guesses)
3. Hard (3 guesses)\n
"""
