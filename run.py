import gspread
from google.oauth2.service_account import Credentials
import os
import sys

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
BR = '\n'
C = '{:^80}'.format


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome():
    print('{:^80}'.format('Welcome to FRUIT HUNTER!'))
    print(BR * 4)
    while True:
        user_choice = input(' ' * 25 + 'Have you played before? Y/N: ')
        if user_choice.upper() == 'Y':
            clear_console()
            # direct to log in function
            break
        elif user_choice.upper() == 'N':
            os.system('cls' if os.name == 'nt' else 'clear')
            # direct to create user function
            break
        elif user_choice.upper() == 'X':
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit()
        else:
            clear_console()
            print(BR * 4)
            print(C('Must choose Y or N or type X to exit.'))
            print(BR)


"""
TODO create user function.
    Creates a user.
    Checks if username already exists.
    Verifies if pin is correct.
    If successfull directs user to log in page.
"""

"""
TODO create login function.
    Ask user for login in name and pin.
    Once logged in gets users info and creates a usernumber variable that is used when updating users info.
    Checks if any fruits have already been collected and if so deletes them from the fruit list.
"""

"""
TODO Main menu function
    Lists the options play, rules, collected fruits, hall of fame and exit.
    Directs user to option chosen.
"""

"""
TODO run game function.
    Runs the main game.
"""

"""
TODO random fruit generator function
    Generates a random fruit from fruit list.
"""

"""
TODO remove fruit function
    Removes fruit from fruit list.
"""


"""
TODO Check fruits collected function
    Checks what fruits has been collected and prints them in a list.
"""

"""
TODO Hall of fame function
    Displays users that have collected all fruit and lists how many attempts it took them.
"""

welcome()