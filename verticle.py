import os
import random
import re

from colorama import Fore, Back, Style


style1 = Fore.GREEN
style2 = Fore.LIGHTYELLOW_EX
style3 = Fore.LIGHTBLACK_EX
style4 = Style.RESET_ALL

WORD_LENGTH = 5  # needs to be length of the words
wins = 0
losses = 0

game_board = ""

letters = {
        'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0,
        'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
        'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0,
        'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
        'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0,
        'Z': 0
    }


def verticle():
    # clear()

    global wins, losses, game_board

    guesses_used = 0

    solution = random.choice(open("possible_solutions.txt").read().splitlines())
    guess = ""

    guess_slots = ["_____"] * WORD_LENGTH
    game_board = ""
    for i in guess_slots:
        game_board += f"{i}\n"

    if wins + losses == 0:
        global style1, style2, style3, style4
        answer = input(
            f"Theme? 1 ({Style.BRIGHT}W{Fore.GREEN}O{Fore.LIGHTBLACK_EX}R{Fore.LIGHTYELLOW_EX}D{Fore.RESET}L{Fore.LIGHTBLACK_EX}E{Style.RESET_ALL})"
            + f" or 2 ({Style.BRIGHT}W{Fore.BLACK + Back.GREEN}O{Back.LIGHTBLACK_EX}R{Back.LIGHTYELLOW_EX}D{Style.RESET_ALL + Style.BRIGHT}L{Fore.BLACK + Back.LIGHTBLACK_EX}E{Style.RESET_ALL})"
            + f" or 3 ({Style.BRIGHT + Fore.BLACK + Back.WHITE}W{Back.GREEN}O{Fore.LIGHTBLACK_EX + Back.BLACK}R{Fore.BLACK + Back.LIGHTYELLOW_EX}D{Back.WHITE}L{Fore.LIGHTBLACK_EX + Back.BLACK}E{Style.RESET_ALL}): ")
        while answer != "1" and answer != "2" and answer != "3":
            clear()
            answer = input(
                f"Invalid answer. 1 ({Style.BRIGHT}W{Fore.GREEN}O{Fore.LIGHTBLACK_EX}R{Fore.LIGHTYELLOW_EX}D{Fore.RESET}L{Fore.LIGHTBLACK_EX}E{Style.RESET_ALL})"
                + f" or 2 ({Style.BRIGHT}W{Fore.BLACK + Back.GREEN}O{Back.LIGHTBLACK_EX}R{Back.LIGHTYELLOW_EX}D{Style.RESET_ALL + Style.BRIGHT}L{Fore.BLACK + Back.LIGHTBLACK_EX}E{Style.RESET_ALL})"
                + f" or 3 ({Style.BRIGHT + Fore.BLACK + Back.WHITE}W{Back.GREEN}O{Fore.LIGHTBLACK_EX + Back.BLACK}R{Fore.BLACK + Back.LIGHTYELLOW_EX}D{Back.WHITE}L{Fore.LIGHTBLACK_EX + Back.BLACK}E{Style.RESET_ALL}): ")
        if answer == "2":
            style1 = Fore.BLACK + Back.GREEN
            style2 = Fore.BLACK + Back.LIGHTYELLOW_EX
            style3 = Fore.BLACK + Back.LIGHTBLACK_EX
            style4 = Style.RESET_ALL
        elif answer == "3":
            style1 = Fore.BLACK + Back.GREEN
            style2 = Fore.BLACK + Back.LIGHTYELLOW_EX
            style3 = Fore.LIGHTBLACK_EX + Back.BLACK
            style4 = Fore.BLACK + Back.WHITE

    keyboard = ""
    for i in "QWERTYUIOP\n ASDFGHJKL\n   ZXCVBNM":
        if i == "\n":
            keyboard += "\n"
        elif i == " ":
            keyboard += " "
        else:
            keyboard += style4 + Style.BRIGHT + i + Style.RESET_ALL + " "

    while guesses_used < WORD_LENGTH and guess != solution:
        # clear()

        print(f"Verticle\n\nGames Won: {wins}\nGames Lost: {losses}\n\n{game_board}\n\n{keyboard}")
        guess = get_guess_from_player()

        guess_slots[guesses_used] = format_guess(solution, guess, guesses_used)
        game_board = ""
        for row in range(WORD_LENGTH):
            for col in range(WORD_LENGTH):
                game_board += get_formatted_letter(guess_slots[col], row)
            game_board += "\n"

        keyboard = format_keyboard(solution, guess, guesses_used)

        guesses_used += 1
        
    # clear()

    winned = guess == solution

    if winned:
        wins += 1
    else:
        losses += 1

    print(f"Verticle\n\nGames Won: {wins}\nGames Lost: {losses}\n\n{game_board}")
    print("You win!" if winned else f"You lose! The solution was {solution}.")
    choice = input("\nPlay again? YES or NO\n\n").upper()
    while choice not in ("Y", "YES", "N", "NO"):
        # clear()
        print(f"Verticle\n\nGames Won: {wins}\nGames Lost: {losses}\n\n{game_board}")
        print("You win!" if winned else f"You lose! The solution was {solution}.")
        choice = input("\nInvalid input. Play again? YES or NO\n\n").upper()
    match choice:
        case "Y" | "YES":
            verticle()
        case "N" | "NO":
            # clear()
            print("\nThanks for playing!")


def clear():
    os.system('clear')


def get_guess_from_player():
    guess = input("Guess: ").upper()

    while guess not in open("allowed_guesses.txt").read().splitlines():
        # clear()
        print(f"Verticle\n\nGames Won: {wins}\nGames Lost: {losses}\n\n{game_board}")
        guess = input("Invalid Guess. Try again: ").upper()

    return guess


def format_guess(solution, guess, guesses_used):
    formatted_guess = ""
    match = ['W'] * 5
    appearances = {}

    for i in solution:
        if i in appearances:
            appearances[i] += 1
        else:
            appearances[i] = 1

    for i in range(WORD_LENGTH):
        if guess[i] == solution[guesses_used]:
            match[i] = 'G'
            appearances[guess[i]] -= 1

    for i in range(WORD_LENGTH):
        if guess[i] in solution and match[i] != 'G' and appearances[guess[i]] > 0:
            match[i] = 'Y'
            appearances[guess[i]] -= 1

    global style1, style2, style3

    for i in range(WORD_LENGTH):
        if match[i] == "G":
            formatted_guess += style1 + Style.BRIGHT + guess[i] + Style.RESET_ALL
        elif match[i] == "Y":
            formatted_guess += style2 + Style.BRIGHT + guess[i] + Style.RESET_ALL
        elif match[i] == "W":
            formatted_guess += style3 + Style.BRIGHT + guess[i] + Style.RESET_ALL

    return formatted_guess


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


def format_keyboard(solution, guess, guesses_used):
    formatted_keyboard = ""
    global letters, style1, style2, style3, style4

    for i in range(WORD_LENGTH):
        if guess[i] == solution[guesses_used]:
            letters[guess[i]] = 3
        elif guess[i] in solution:
            if letters[guess[i]] <= 2:
                letters[guess[i]] = 2
        elif guess[i] not in solution:
            letters[guess[i]] = 1

    for i in "QWERTYUIOP\n ASDFGHJKL\n   ZXCVBNM":
        if not i.isalpha():
            formatted_keyboard += i
        elif letters[i] == 3:
            formatted_keyboard += style1 + Style.BRIGHT + i + Style.RESET_ALL + " "
        elif letters[i] == 2:
            formatted_keyboard += style2 + Style.BRIGHT + i + Style.RESET_ALL + " "
        elif letters[i] == 1:
            formatted_keyboard += style3 + Style.BRIGHT + i + Style.RESET_ALL + " "
        elif letters[i] == 0:
            formatted_keyboard += style4 + i + Style.RESET_ALL + " "

    return formatted_keyboard


verticle()
