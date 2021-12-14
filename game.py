# Hangman game by Amitay Cahalon
import os
from random import choice
from colorama import Fore

MAX_TRIES = 6
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
SECRET_WORDS_FILE = CURRENT_PATH + "words.txt"
PICTURE0 = "x-------x\n|        \n|\n|\n|\n|\n"
PICTURE1 = "x-------x\n|       |\n|       O\n|\n|\n|\n"
PICTURE2 = "x-------x\n|       |\n|       O\n|       |\n|\n|\n"
PICTURE3 = "x-------x\n|       |\n|       O\n|      /|\n|\n|\n"
PICTURE4 = "x-------x\n|       |\n|       O\n|      /|\\\n|\n|\n"
PICTURE5 = "x-------x\n|       |\n|       O\n|      /|\\\n|      /\n|\n"
PICTURE6 = "x-------x\n|       |\n|       0\n|      /|\\\n|      / \\\n|\n"

HANGMAN_PHOTOS = {0: PICTURE0, 1: PICTURE1, 2: PICTURE2, 3: PICTURE3, 4: PICTURE4, 5: PICTURE5, 6: PICTURE6}


def main():
    num_of_tries, old_letters_guessed, current_letter, winner = 0, [], "", False
    secret_word = choose_word()
    print_opening_screen(secret_word, old_letters_guessed)
    # as longs as the guesses are not over
    while MAX_TRIES > num_of_tries: 
        current_letter, is_letter_valid = guess_letter(old_letters_guessed)
        # if the attempt to add failed try again
        while not is_letter_valid: 
            current_letter, is_letter_valid = guess_letter(old_letters_guessed)
        # if the letter is valid but not in the secret word
        if current_letter not in secret_word:
            num_of_tries += 1 
            print(f"the letter '{current_letter}' is not in the word")
            print(f"You have {MAX_TRIES - num_of_tries} guesses left\n{show_hangman(num_of_tries)}")
        print(show_hidden_word(secret_word, old_letters_guessed))
        if check_win(secret_word, old_letters_guessed):
            winner = True
            break
    print_end_screen(winner, secret_word)
    play_again()


def is_one_number(string):
    """
     this function checks the string contains only one number
    :param string:a string 
    :type string: str
    :return: does the string contain only one number
    :rtype: bool
    """
    if len(string) == 1 and string.isdecimal():
        return True
    return False


def play_again():
    """
     this function checks if the player wants to play again
    :rtype: None
    """
    play = input("Play again? (y/n) ")
    if play.lower() == 'y':
        main()
    print("GoodBye! :-)")


def guess_letter(old_letters_guessed):
    """
     this function receives input from the player and returns it and if it is valid
    :param old_letters_guessed: the list contains the letters the player has guessed so far
    :type old_letters_guessed: list
    :return: a tuple that contains the input from the player and if it is valid
    :rtype: tuple
    """
    letter_guessed = input("Guess a letter: ").lower()
    is_letter_valid = try_update_letter_guessed(letter_guessed, old_letters_guessed)
    returned_tuple = (letter_guessed, is_letter_valid)
    return returned_tuple


def print_end_screen(winner, secret_word):
    """
     this function prints a win or loss message accordingly
    :param winner: a variable that represents whether you won or lost the game
    :param secret_word: 
    :type winner: bool
    :type secret_word: str
    :rtype: None
    """
    if winner:
        print(f"{Fore.GREEN}Well done! You won!\nYou guessed the word '{secret_word}'")
    else:
        print(f"{Fore.RED}You lost...\nbetter luck next time, the word was '{secret_word}'")
    print(Fore.RESET)


def print_opening_screen(secret_word, old_letters_guessed):
    """
     this function prints the opening screen of the game
    :param secret_word: the word the player has to guess
    :param old_letters_guessed: the list contains the letters the player has guessed so far
    :type secret_word: str
    :type old_letters_guessed: list
    :rtype: None
    """
    opening_screen = "_    _\n| |  | |\n| |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __\n|  __  |/ _' | '_ \\ / _' | " \
                     "'_ ' _ \\ / _' | '_ \\\n| |  | | (_| | | | | (_| | | | | | | (_| | | | |\n|_|  |_|\\__," \
                     "_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|\n\t\t     __/ |\n\t\t    |___/ "
    print(Fore.LIGHTMAGENTA_EX + opening_screen + Fore.RESET)  # add color, print, back to normal colors
    print("You have {0} guesses\nLet's start!\n{1}".format(MAX_TRIES, show_hangman(0)))
    print(show_hidden_word(secret_word, old_letters_guessed), "\n")


def is_valid_input(letter_guessed):
    """
     this function checks if the string is valid (one character in English)
    :param letter_guessed: string of characters
    :type letter_guessed: str
    :return: is the letter guessed valid or not
    :rtype: bool
    """
    is_valid = False
    if len(letter_guessed) == 1 and letter_guessed.isalpha():
        is_valid = True
    return is_valid


def check_valid_input(letter_guessed, old_letters_guessed):
    """
     this function checks the correctness of the string and whether the user has guessed the character before
    :param letter_guessed: the string represents the character received from the player
    :param old_letters_guessed: the list contains the letters the player has guessed so far
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return: a boolean value representing the correctness of the string and
            whether the user has guessed the character before
    :rtype: bool 
    """
    is_ok = is_valid_input(letter_guessed)
    if letter_guessed in old_letters_guessed:
        is_ok = False
    return is_ok


def try_update_letter_guessed(letter_guessed, old_letters_guessed): 
    """
     this function checks whether or not the new character can be added to the guess list
    :param letter_guessed: the new character the user guessed
    :param old_letters_guessed: the list contains the letters the player has guessed so far
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return: whether the character can be added to the guess list 
    :rtype: bool
    """
    is_ok = False
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        is_ok = True
    else:
        print("invalid input! try again")
        it_is_invalid(old_letters_guessed)
    return is_ok


def it_is_invalid(old_letters_guessed):
    """
     this function prints the list items sorted in ascending order and separated by "->"
    :param old_letters_guessed: the list contains the letters the player has guessed so far
    :type old_letters_guessed: list
    :rtype: None
    """
    if old_letters_guessed:
        sorted_list = sorted(old_letters_guessed)
        string = ""
        for char in sorted_list:
            string += char + " -> "
        print(string[:-3])  # remove the last ->


def show_hidden_word(secret_word, old_letters_guessed):
    """
     this function shows the player his progress in the game
    :param secret_word: the word the player has to guess
    :param old_letters_guessed: all the characters the player has already guessed
    :type secret_word: str
    :type old_letters_guessed: list
    :return: a string which consists of letters and underlines
            the string displays the letters from the old_letters_guessed list that
            are in the secret_word string in their appropriate position,
            and the rest of the letters in the string (which the player has not yet guessed) as underlines
    :rtype: str
    """
    returned_string = ""
    for char in secret_word:
        if char in old_letters_guessed:
            returned_string += char
        else:
            returned_string += "_"
    return " ".join(returned_string)


def check_win(secret_word, old_letters_guessed): 
    """
     this function checks whether the player was able to guess the secret word and thus won the game
    :param secret_word: the word the player has to guess
    :param old_letters_guessed: all the characters the player has already guessed
    :type secret_word: str
    :type old_letters_guessed: list
    :return: "TRUE" if all the letters that make up the secret word are included in the list of
            letters the user guessed otherwise, "FALSE"
    :rtype: bool
    """
    winner = True
    for char in secret_word:
        if char not in old_letters_guessed:
            winner = False
    return winner


def show_hangman(num_of_tries):
    """
     this function returns the snapshot of the game according to the num_of_tries value
    :param num_of_tries: the number of guesses the player has already guessed
    :type num_of_tries: int
    :return: the snapshot of the game
    :rtype: str
    """
    return HANGMAN_PHOTOS[num_of_tries]


def choose_word():
    """
     this function choose the secret word from the words file
    :return: the secret word 
    :rtype: str
    """
    all_file, word_list = [], []
    if os.path.isfile(SECRET_WORDS_FILE):
        with open(SECRET_WORDS_FILE, 'r') as words: 
            all_file = words.readlines()
        for word in all_file:
            word_list.append(word[1:-3])
        secret_word = choice(word_list)  
        return secret_word
    print("ERROR: Words file not found!\nMake sure:")
    print("\t1. Words file called words.txt\n\t2. Words file is located in the same directory as this script")
    exit(-1)


if __name__ == "__main__":
    main()
