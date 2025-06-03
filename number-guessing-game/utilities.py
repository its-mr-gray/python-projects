"""
utilities.py

Module containing all functionality for the number guessing game application.
"""

from variables import DIFFICULTY_SELECTION_DICT


def game_loop(computer_choice, difficulty_level) -> None:
    """
    The core game loop. Allows the user to guess a specified number of time dependent on the selected difficulty.

    Args:
        difficulty_level (int): An integer representation of the user-selected difficulty level.
        computer_choice (int): A number between 1 and 100 inclusive randomly selected by the application.

    Returns:
        None
    """
    get_difficulty_level(difficulty_level)

    _, total_guesses = DIFFICULTY_SELECTION_DICT[difficulty_level]

    for attempt in range(total_guesses):
        user_guess = int(input("Pick a number!\n"))
        hint = guess_low_or_high(user_guess, computer_choice)
        guesses_remaining = total_guesses - attempt - 1

        if user_guess == computer_choice:
            print(
                f"Winner! {user_guess} selected with {guesses_remaining} guesses remaining!\n"
            )
            break
        else:
            if guesses_remaining == 0:
                print(f"You lose! Computer was thinking of {computer_choice}\n")
            else:
                print(
                    f"Nope! Guess was {hint}! Guesses remaining: {guesses_remaining}.\n"
                )


def guess_low_or_high(user_guess: int, computer_choice: int) -> str:
    """
    Determines whether the user's guess was too low or two high.

    Args:
        user_guess (int): The value input by the user.
        computer_choice (int): The number chosen at random by the application.

    Returns:
        str: A message telling the user whether the guess was too high or too low.
    """

    if user_guess > computer_choice:
        result = "too high"
    else:
        result = "too low"

    return result


def continue_playing() -> None:
    """
    Allow the user to continue playing the guessing game.

    Args:
        None

    Returns:
        None
    """
    while True:
        choice = input("Continue playing? y/n\n").lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        print("Invalid choice. Please select 'y' or 'n'")


def get_difficulty_level(difficulty_selection) -> None:
    """
    Gets the difficulty level selected by the user.

    Args:
        difficulty_selection (int): The user-selected difficulty level.

    Returns:
        None
    """
    try:
        difficulty, _ = DIFFICULTY_SELECTION_DICT[difficulty_selection]
        print(f"Great! You have selected the {difficulty} difficulty level!")
    except KeyError:
        print(
            f"Error: {difficulty_selection} is an invalid choice! Please select from the given difficulty levels."
        )
