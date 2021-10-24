import gspread
from google.oauth2.service_account import Credentials
import os
import sys
import time

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
    while (len(user_name) > 15) or (user_name in users):
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


"""
TODO create login function.
    Ask user for login in name and pin.
    Once logged in gets users info and creates a usernumber variable that is used when updating users info.
    Checks if any fruits have already been collected and if so deletes them from the fruit list.
"""

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
    fruits_collected = user_info[2]
    fruits_coll_li = list(fruits_collected.split(" "))
    new_list = []
    for fruit in fruits:
        if fruit not in fruits_coll_li:
            new_list.append(fruit)
    fruits = new_list
    # play game function
    




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
TODO Hall of fame function
    Displays users that have collected all fruit and lists how many attempts it took them.
"""

welcome()