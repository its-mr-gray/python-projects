"""
main.py

Entry point for the number guessing game.
"""

from random import randint

from utilities import continue_playing, game_loop
from variables import WELCOME_MESSAGE


def main():
    print(WELCOME_MESSAGE)
    while True:
        difficulty_selection = int(input("Enter your choice of difficulty: "))
        computer_choice = randint(1, 100)
        game_loop(computer_choice, difficulty_selection)
        if not continue_playing():
            print("Thanks for playing!\n")
            break


if __name__ == "__main__":
    main()
