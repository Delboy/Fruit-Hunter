import gspread
from google.oauth2.service_account import Credentials
import os
import sys
import time
import random

"""
code taken from love-sandwiches project.
"""
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fruit_hunter')
WKS = SHEET.worksheet("users")
HOF = SHEET.worksheet("hof")
C = '{:^80}'.format
BR = '\n'



def clear_console():
    """
    Clears the console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome():
    """
    Displays the welcome message.
    Directs user to create user or log in functions
    """
    clear_console()
    print('{:^80}'.format('Welcome to FRUIT HUNTER!'))
    print(BR * 4)
    user_choice = input(' ' * 25 + 'Have you played before? Y/N: ')
    if user_choice.upper() == 'Y':
        clear_console()
        login()
    elif user_choice.upper() == 'N':
        clear_console()
        create_user()
    elif user_choice.upper() == 'X':
        sys.exit()
    else:
        clear_console()
        print(BR * 4)
        print(C('You must choose either Y or N or type X to exit.'))
        time.sleep(3)
        welcome()


def create_user():
    """
    Creates user log-in. 
    """
    users = WKS.col_values(1)
    clear_console()
    print(BR * 4)
    # Creates username
    user_name = input(' ' * 27 + 'Please choose a username: ')
    while (len(user_name) > 15) or (user_name in users) or (user_name == ''):
        if len(user_name) > 15:
            clear_console()
            print(BR * 4)
            print(C('Sorry, that name is too long. Please keep under 15 characters.'))
            user_name = input(' ' * 27 + 'Please choose a username: ')
        if user_name in users:
            clear_console()
            print(BR * 4)
            print(C('Sorry, that name is taken. Please try again'))
            user_name = input(' ' * 27 + 'Please choose a username: ')
        if user_name == '':
            clear_console()
            print(BR * 4)
            print(C('Sorry, tha name cannot be blank. Please try again'))
            user_name = input(' ' * 27 + 'Please choose a username: ')
    clear_console()
    print(BR * 4)
    print(C(f'You chose the username {user_name.capitalize()}. Is this correct?'))
    validate_name = input(' ' * 37 + 'Y/N: ')
    # Creates user's PIN number
    if validate_name.upper() == 'Y':
        clear_console()
        print(BR * 4)
        print(C('Please choose four digit PIN number: '))
        user_pin = input(' ' * 37 + 'PIN: ')
        while (user_pin.isdecimal() == False) or (len(user_pin) != 4):
            clear_console()
            print(BR * 4)
            print(C('Sorry, the PIN must be four digits long and only consist of numbers. Please try again.'))
            user_pin = input(' ' * 37 + 'PIN: ')
        clear_console()
        print(BR * 4)
        verify_pin = input(' ' * 28 + 'Please verify the PIN: ')
        while user_pin != verify_pin:
            clear_console()
            print(BR * 4)
            print(C('Sorry, the pins do not match. Please try again.'))
            user_pin = input(' ' * 34 + 'Input PIN: ')
            clear_console()
            print(BR * 4)
            verify_pin = input(' ' * 34 +'Verify PIN: ')
        new_user = [user_name.lower(), user_pin,'',0 ]   
        WKS.append_row(new_user)
        clear_console()
        print(BR * 2)
        print(C('Success! User created! Your log in details are:')) 
        print(C(f'User Name: {user_name}'))
        print(C(f'PIN: {user_pin}'))
        time.sleep(3)  
        login()
    else:
        create_user()


def login():
    """
    Logs in the user.
    """
    users = WKS.col_values(1)
    clear_console()
    print(BR * 4)
    print(C('Please log in'))
    user_name = input(' ' * 32 + 'User Name: ').lower()
    if user_name in users:
        clear_console()
        print(BR *4)
        pin_input = input(' ' * 29 + 'Please enter PIN: ')
        row_number = users.index(user_name) + 1
        users_info = WKS.row_values(row_number)
        users_pin = users_info[1]
        clear_console()
        if pin_input == users_pin:
            clear_console()
            print(BR * 4)
            print(C('Login successfull'))
            time.sleep(2)
            global user_num
            user_num = row_number
            check_fruits(user_num)
        else:
            clear_console()
            print(BR *4)
            print(C('Sorry the PIN is not correct. Please try again.'))
            time.sleep(3)
            login()
    else:
        clear_console()
        print(BR * 4)
        user_input = input(' ' * 4 + 'That username does not exist. Would you like to create a user login? Y/N: ')
        if user_input.upper() == 'Y':
            create_user()
        elif user_input.upper() == 'N':
            login()
        else:
            clear_console()
            print(BR * 4)
            print(C(f'{user_input.upper()} is not a valid input. Returning to login.'))
            time.sleep(2)
            login()



def check_fruits(user_num):
    """
    Checks what fruit the user has already collected if any and removes them from the fruit list.
    """
    global fruits 
    fruits = ['apple', 'banana', 'pear']
    user_info = WKS.row_values(user_num)
    global fruits_collected
    fruits_collected = user_info[2]
    global fruits_coll_li
    fruits_coll_li = list(fruits_collected.split(" "))
    new_list = []
    for fruit in fruits:
        if fruit not in fruits_coll_li:
            new_list.append(fruit)
    global fruits_left
    fruits_left = new_list
    menu()


def menu():
    clear_console()
    print(C('MENU'))
    print(BR)
    print(C('1. Play'))
    print(C('2. Rules'))
    print(C('3. Fruits Collected'))
    print(C('4. Hall of Fame'))
    print(C('5. Exit'))
    user_input = input(' ' * 40)
    if user_input == '1':
        play()
    elif user_input == '2':
        rules()
    elif user_input == '3':
        fruit_li()
    elif user_input == '4':
        hof()
    elif user_input == '5':
        sys.exit()
    else:
        clear_console()
        print(BR * 4)
        print(C('Sorry that input has not been recognised. Please try again.'))
        time.sleep(2)
        menu()


"""
TODO run game function.
    Runs the main game.
"""

def play():
    """
    Plays the game.
    """
    clear_console()
    fruit = random_fruit()
    lives = 5
    answer = '_' * len(fruit)
    guessed = []
    print(BR * 1)
    print(C((u'\u2764' + ' ') * lives))
    print(BR)
    print(C(answer))

    while lives > 0:
        
        guess = input(' ' * 25 + 'Guess the fruit or a letter: ')
        if len(guess) == 1:
            if guess.upper() not in fruit:
                clear_console()
                lives -= 1
                guessed.append(guess)
                print(BR * 1)
                lives_left = life_lost(lives)
                print(C(lives_left))
                print(BR)
                print(C(answer))
                print(C(f'Sorry, {guess} is not in the word. Try again.'))
    if lives == 0:
        clear_console()
        # Updates times user has died on googlesheet. Info used for Hall of fame leaderboard.
        user_info = WKS.row_values(user_num)
        user_deaths = int(user_info[3])
        user_deaths += 1
        WKS.update_cell(user_num,4,user_deaths)
        print(BR * 4)
        print(C('Oh no! You\'ve lost all your lives!'))
        user_input = input(' ' * 12 + 'Press Y to play again or N to go back to the main menu: ')
        while True:
            if user_input.upper() == 'Y':
                play()
            elif user_input.upper() == 'N':
                menu()
            else:
                clear_console()
                print(BR * 4)
                print(C('Sorry, that character is not recognised. Please input Y to play again or N to return to the main menu.'))
                user_input = input(' ' * 39 + ': ')


def random_fruit():
    """
    Generates a random fruit from the fruits left to find.
    """
    fruit = random.choice(fruits_left)
    return fruit.upper()


def life_lost(lives):
    lost_lives = 5 - lives
    return ((u'\u2764' + ' ') * lives) + ((u'\u2661' + ' ') * lost_lives)

def rules():
    """
    Displays the rules of the game to the user
    """
    clear_console()
    phrases = ['The aim of Fruit Hunter is to gather all the fruit!',
    'Fruit is gathered by trying to guess which name of the fruit is being displayed',
    'You can guess one letter at a time or try and guess the whole word',
    'The player has five lives. Incorrect guesses will lose you 1 life',
    'If all lives are lost you lose the game',
    "But dont worry as any fruit you've already found are saved!",
    'If you discover all the fruit you win the game and get entered into the hall of fame!',
    'Happy hunting!']
    for x in phrases:
        clear_console()
        print(C('RULES'))
        print(BR)
        print((C(x)))
        time.sleep(4)
    menu()


def fruit_li():
    """
    Prints out a list of all fruits found by the user if any.
    Enables the user to reset the list if all fruits have been found.
    """
    clear_console()
    print(C('Fruits Collected'))
    print(BR)
    if len(fruits_coll_li) == len(fruits):
        print(C('Well done! You have collected all the fruits and been entered into the hall of fame!'))
        user_input = input(' ' * 20 + 'Would you like to reset the list? Y/N: ')
        if user_input.upper() == 'Y':
            fruits_left = fruits
            WKS.update_cell(user_num,3,'')
            clear_console()
            print(4 * BR)
            print(C('List has been reset. Returning to main menu.'))
            time.sleep(2)
            check_fruits(user_num)
        elif user_input.upper == 'N':
            print(C("You selected 'NO'. Returning to the main menu"))
            time.sleep(2)
            menu()
        else:
            print(C("That character was not recogised. Returning to the main menu"))
            time.sleep(2)
            menu()
    elif fruits_collected == '':
        print(C("Sorry, you havn't collected any fruits yet!"))
        user_input = input(' ' * 22 + 'Enter Y to return to the main menu: ')
        if user_input.upper() == 'Y':
            menu()
        else:
            fruit_li()
    else:
        print(C(f'There are {len(fruits)} fruits to collect. You have found {len(fruits_coll_li)}! '))
        print(C('You have already found: ' + fruits_collected.upper()))
        print(BR)
        user_input = input(' ' * 22 + 'Enter Y to return to the main menu: ')
        if user_input.upper() == 'Y':
            menu()
        else:
            fruit_li()


"""
TODO Hall of fame function
    Displays users that have collected all fruit and lists how many attempts it took them.
"""

welcome()