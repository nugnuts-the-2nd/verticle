import os
import random
import re
from colorama import Fore, Back, Style
from collections import namedtuple

SOLUTIONS = open("possible_solutions.txt").read().splitlines()
ALLOWED_GUESSES = set(open("allowed_guesses.txt").read().splitlines())

WORD_LENGTH = 5  # needs to be length of the words

Theme = namedtuple('Theme', ['green', 'yellow', 'gray', 'default'])

THEMES = {
    '1': Theme(
        green=Fore.GREEN + Style.BRIGHT,
        yellow=Fore.LIGHTYELLOW_EX + Style.BRIGHT,
        gray=Fore.LIGHTBLACK_EX + Style.BRIGHT,
        default=Style.RESET_ALL + Style.BRIGHT
    ),
    '2': Theme(
        green=Fore.BLACK + Back.GREEN + Style.BRIGHT,
        yellow=Fore.BLACK + Back.LIGHTYELLOW_EX + Style.BRIGHT,
        gray=Fore.BLACK + Back.LIGHTBLACK_EX + Style.BRIGHT,
        default=Style.RESET_ALL + Style.BRIGHT
    ),
    '3': Theme(
        green=Fore.BLACK + Back.GREEN + Style.BRIGHT,
        yellow=Fore.BLACK + Back.LIGHTYELLOW_EX + Style.BRIGHT,
        gray=Fore.LIGHTBLACK_EX + Back.BLACK + Style.BRIGHT,
        default=Fore.BLACK + Back.WHITE + Style.BRIGHT
    )
}


def clear():
    os.system('clear')


def get_theme_choice():
    choice = input(
        f"Theme? 1 ({THEMES['1'].default}W{THEMES['1'].green}O{THEMES['1'].gray}R{THEMES['1'].yellow}D{THEMES['1'].default}L{THEMES['1'].gray}E{Style.RESET_ALL})"
        + f" or 2 ({THEMES['2'].default}W{THEMES['2'].green}O{THEMES['2'].gray}R{THEMES['2'].yellow}D{THEMES['2'].default}L{THEMES['2'].gray}E{Style.RESET_ALL})"
        + f" or 3 ({THEMES['3'].default}W{THEMES['3'].green}O{THEMES['3'].gray}R{THEMES['3'].yellow}D{THEMES['3'].default}L{THEMES['3'].gray}E{Style.RESET_ALL}): ")
    while choice not in ('1', '2', '3'):
        # clear()
        choice = input(
            f"Invalid input. 1 ({THEMES['1'].default}W{THEMES['1'].green}O{THEMES['1'].gray}R{THEMES['1'].yellow}D{THEMES['1'].default}L{THEMES['1'].gray}E{Style.RESET_ALL})"
            + f" or 2 ({THEMES['2'].default}W{THEMES['2'].green}O{THEMES['2'].gray}R{THEMES['2'].yellow}D{THEMES['2'].default}L{THEMES['2'].gray}E{Style.RESET_ALL})"
            + f" or 3 ({THEMES['3'].default}W{THEMES['3'].green}O{THEMES['3'].gray}R{THEMES['3'].yellow}D{THEMES['3'].default}L{THEMES['3'].gray}E{Style.RESET_ALL}): ")

    return THEMES[choice]


def get_guess_from_player(wins, losses, game_board, keyboard):
    guess = input("Guess: ").upper()

    while guess not in ALLOWED_GUESSES:
        # clear()
        guess = input("Invalid Guess. Try again: ").upper()

    return guess


def format_guess(solution, guess, guesses_used, theme):
    appearances = {}
    for char in solution:
        appearances[char] = appearances.get(char, 0) + 1

    parts = []

    for i in range(WORD_LENGTH):
        if guess[i] == solution[guesses_used] and i == guess.index(guess[i]):
            parts.append(f"{theme.green}{guess[i]}{Style.RESET_ALL}")
            appearances[guess[i]] -= 1
        elif guess[i] in solution and appearances.get(guess[i], 0) > 0:
            parts.append(f"{theme.yellow}{guess[i]}{Style.RESET_ALL}")
            appearances[guess[i]] -= 1
        else:
            parts.append(f"{theme.gray}{guess[i]}{Style.RESET_ALL}")

    return ''.join(parts)


def get_formatted_letter(formatted_string, position):
    if formatted_string == "_____":
        return "_"

    matches = list(re.finditer(r'(\x1b\[[0-9;]+m)*([A-Z])', formatted_string))

    if position < len(matches):
        match = matches[position]
        result = match.group(0)
        result += Style.RESET_ALL
        return result

    return "_"


def format_keyboard(solution, guess, guesses_used, letters, theme):
    for i in range(WORD_LENGTH):
        if guess[i] == solution[guesses_used]:
            letters[guess[i]] = 3
        elif guess[i] in solution and letters[guess[i]] < 3:
            letters[guess[i]] = max(letters[guess[i]], 2)
        else:
            letters[guess[i]] = max(letters[guess[i]], 1)

    keyboard_parts = []
    for char in "QWERTYUIOP\n ASDFGHJKL\n   ZXCVBNM":
        if not char.isalpha():
            keyboard_parts.append(char)
        else:
            state = letters[char]
            if state == 3:
                keyboard_parts.append(f"{theme.green}{char}{Style.RESET_ALL} ")
            elif state == 2:
                keyboard_parts.append(f"{theme.yellow}{char}{Style.RESET_ALL} ")
            elif state == 1:
                keyboard_parts.append(f"{theme.gray}{char}{Style.RESET_ALL} ")
            else:
                keyboard_parts.append(f"{theme.default}{char}{Style.RESET_ALL} ")

    return ''.join(keyboard_parts)


def play_again():
    choice = input("\nPlay again? YES or NO\n\n").upper()
    while choice not in ("Y", "YES", "N", "NO"):
        # clear()
        choice = input("Invalid input. Play again? YES or NO\n\n").upper()

    return choice in ("Y", "YES")


def verticle(wins, losses, theme):
    # clear()

    guesses_used = 0
    solution = "CAUSE"
    guess = ""
    letters = {chr(i): 0 for i in range(ord('A'), ord('Z') + 1)}

    guess_slots = ["_____"] * WORD_LENGTH
    game_board = '\n'.join(guess_slots)

    keyboard_parts = []
    for char in "QWERTYUIOP\n ASDFGHJKL\n   ZXCVBNM":
        if not char.isalpha():
            keyboard_parts.append(char)
        else:
            keyboard_parts.append(f"{theme.default}{char}{Style.RESET_ALL} ")
    keyboard = ''.join(keyboard_parts)

    while guesses_used < WORD_LENGTH and guess != solution:
        # clear()

        print(f"Verticle\n\nGames Won: {wins}\nGames Lost: {losses}\n\n{game_board}\n\n{keyboard}")
        guess = get_guess_from_player(wins, losses, game_board, keyboard)

        guess_slots[guesses_used] = format_guess(solution, guess, guesses_used, theme)
        game_board = '\n'.join(
            ''.join(get_formatted_letter(guess_slots[col], row) for col in range(WORD_LENGTH))
            for row in range(WORD_LENGTH)
        )

        keyboard = format_keyboard(solution, guess, guesses_used, letters, theme)

        guesses_used += 1

    # clear()

    winned = guess == solution

    if winned:
        wins += 1
    else:
        losses += 1

    print(f"Verticle\n\nGames Won: {wins}\nGames Lost: {losses}\n\n{game_board}")
    print("You win!" if winned else f"You lose! The solution was {solution}.")

    return wins, losses


def main():
    wins = 0
    losses = 0
    theme = get_theme_choice()

    while True:
        wins, losses = verticle(wins, losses, theme)

        if not play_again():
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()
