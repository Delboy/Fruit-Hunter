import gspread
from google.oauth2.service_account import Credentials
import os
import time
import random

# code taken from love-sandwiches project.

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
    # This line is credited to 
    # https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome():
    """
    Displays the welcome message.
    Directs user to create user or log in functions
    """
    clear_console()
    print(BR * 4)
    print(C('Welcome to FRUIT HUNTER!'))
    print(BR * 4)
    user_choice = input(' ' * 25 + 'Have you played before? Y/N: ')
    if user_choice.upper() == 'Y':
        clear_console()
        login()
    elif user_choice.upper() == 'N':
        clear_console()
        create_user()
    else:
        clear_console()
        print(BR * 4)
        print(C('You must choose either Y or N.'))
        time.sleep(3)
        welcome()


def create_user():
    """
    Creates user log-in.
    """
    users = WKS.col_values(1)
    clear_console()
    print(BR * 8)
    # Creates username
    user_name = input(
        ' ' * 14 + 'Please choose a username or type LOGIN to sign in: '
        )
    while (len(user_name) > 15) or (user_name.lower() in users) or \
            (user_name == '') or (user_name.isalpha() is False) or \
            (user_name.upper() == 'LOGIN'):
        if len(user_name) > 15:
            clear_console()
            print(BR * 8)
            print(C(
                'Sorry, that name is too long. '
                'Please keep under 15 characters.'
                ))
            user_name = input(' ' * 27 + 'Please choose a username: ')
        if user_name.lower() in users:
            clear_console()
            print(BR * 8)
            print(C('Sorry, that name is taken. Please try again.'))
            user_name = input(' ' * 27 + 'Please choose a username: ')
        if user_name == '':
            clear_console()
            print(BR * 8)
            print(C('Sorry, the name cannot be blank. Please try again.'))
            user_name = input(' ' * 27 + 'Please choose a username: ')
        if user_name.isalpha() is False:
            clear_console()
            print(BR * 8)
            print(C('Sorry, only letters are allowed. Please try again.'))
            user_name = input(' ' * 27 + 'Please choose a username: ')
        if user_name.upper() == 'LOGIN':
            login()
    clear_console()
    print(BR * 8)
    print(C(
        f'You chose the username {user_name.capitalize()}. Is this correct?'
        ))
    validate_name = input(' ' * 37 + 'Y/N: ')
    # Creates user's PIN number
    if validate_name.upper() == 'Y':
        clear_console()
        print(BR * 8)
        print(C('Please choose four digit PIN number: '))
        user_pin = input(' ' * 37 + 'PIN: ')
        while (user_pin.isdecimal() is False) or (len(user_pin) != 4):
            clear_console()
            print(BR * 8)
            print(C(
                'Sorry, '
                'the PIN must be four digits long and only consist of numbers.'
                ))
            print(C('Please try again.'))
            user_pin = input(' ' * 37 + 'PIN: ')
        clear_console()
        print(BR * 8)
        verify_pin = input(' ' * 28 + 'Please verify the PIN: ')
        while user_pin != verify_pin:
            clear_console()
            print(BR * 8)
            print(C('Sorry, the pins do not match. Please try again.'))
            user_pin = input(' ' * 34 + 'Input PIN: ')
            while (user_pin.isdecimal() is False) or (len(user_pin) != 4):
                clear_console()
                print(BR * 8)
                print(C(
                    'Sorry, the PIN must be four digits long '
                    'and only consist of numbers.'
                    ))
                print(C('Please try again.'))
                user_pin = input(' ' * 37 + 'PIN: ')
            clear_console()
            print(BR * 8)
            verify_pin = input(' ' * 34 + 'Verify PIN: ')
        new_user = [user_name.lower(), user_pin, '', 0, 0]
        WKS.append_row(new_user)
        clear_console()
        print(BR * 8)
        print(C('Success! User created! Your log in details are:'))
        print(C(f'User Name: {user_name.capitalize()}'))
        print(C(f'PIN: {user_pin}'))
        time.sleep(3)
        users = WKS.col_values(1)
        global user_num
        user_num = users.index(user_name) + 1
        menu()
    else:
        create_user()


def login():
    """
    Logs in the user.
    """
    users = WKS.col_values(1)
    clear_console()
    print(BR * 8)
    print(C('Please log in'))
    user_name = input(' ' * 32 + 'User Name: ').lower()
    # Checks if user name exists.
    if user_name in users:
        clear_console()
        print(BR * 8)
        # Checks if users pin matches.
        pin_input = input(' ' * 29 + 'Please enter PIN: ')
        global user_num
        user_num = users.index(user_name) + 1
        users_info = WKS.row_values(user_num)
        users_pin = users_info[1]
        clear_console()
        if pin_input == users_pin:
            clear_console()
            print(BR * 8)
            print(C('Login successful'))
            time.sleep(2)
            menu()
        else:
            clear_console()
            print(BR * 8)
            print(C('Sorry the PIN is not correct. Please try again.'))
            time.sleep(3)
            login()
    else:
        clear_console()
        print(BR * 8)
        print(C('That username does not exist.'))
        user_input = input(
            ' ' * 18 + 'Would you like to create a user login? Y/N: '
            )
        if user_input.upper() == 'Y':
            create_user()
        elif user_input.upper() == 'N':
            login()
        else:
            clear_console()
            print(BR * 8)
            print(C(
                f'{user_input.upper()} is not a valid input. '
                'Returning to login.'
                ))
            time.sleep(2)
            login()


def check_fruits(user_num):
    """
    Checks what fruit the user has already collected if any
    and removes them from the fruits-to-find list.
    """
    global fruits
    fruits = [
        'apple', 'banana', 'pear', 'orange', 'lemon',
        'cherry', 'strawberry', 'melon', 'kiwi', 'pineapple',
        'peach', 'lime', 'blueberry', 'grape', 'plum'
        ]
    user_info = WKS.row_values(user_num)
    global fruits_collected
    fruits_collected = user_info[2]
    global fruits_coll_li
    fruits_coll_li = list(fruits_collected.split(" "))
    global fruits_left
    fruits_left = []
    for fruit in fruits:
        if fruit not in fruits_coll_li:
            fruits_left.append(fruit)


def menu():
    """
    Displays the main menu.
    """
    clear_console()
    print(BR)
    print(C('FRUIT HUNTER'))
    print(BR * 3)
    print(C('MENU'))
    print(BR)
    print(C('1. Play'))
    print(C('2. How to Play'))
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
        display_hof()
    elif user_input == '5':
        welcome()
    else:
        clear_console()
        print(BR * 4)
        print(C('Sorry that input has not been recognised. Please try again.'))
        time.sleep(2)
        menu()


def play():
    """
    Plays the game.
    """
    check_fruits(user_num)
    # Checks if the user has already collected all the fruit.
    # Enables user to reset list if all fruit found.
    if len(fruits_coll_li) > len(fruits):
        clear_console()
        print(BR * 8)
        print(C(
            'Oh no! It looks like you\'ve already collected all the fruit!'
            ))
        print(C('Check to see if you\'ve reached the hall of fame!'))
        print(C('Would you like to reset the list and play again?'))
        user_input = input(' ' * 37 + 'Y/N: ')
        if user_input.upper() == 'Y':
            WKS.update_cell(user_num, 3, '')
            WKS.update_cell(user_num, 4, 0)
            WKS.update_cell(user_num, 5, 0)
            clear_console()
            print(4 * BR)
            print(C('List has been reset.'))
            time.sleep(2)
            play()
        elif user_input.upper() == 'N':
            print(C("You selected 'NO'. Returning to the main menu"))
            time.sleep(2)
            menu()
        else:
            print(C(
                'That character was not recognised. Returning to the main menu'
                ))
            time.sleep(2)
            menu()

    clear_console()
    user_info = WKS.row_values(user_num)
    fruit = random_fruit()
    global lives
    lives = 5
    global answer
    answer = '_ ' * len(fruit)
    guessed = []
    print(BR * 6)
    print(C((u'\u2764' + ' ') * lives))
    print(BR)
    print(C(answer))
    print(C(BR))

    while lives > 0:
        guess = input(
            ' ' * 15 + 'Guess the fruit or a letter or type EXIT to leave: '
            ).upper()
        # Runs if users guess is one letter.
        if len(guess) == 1:
            if guess.isalpha() is False:
                update_game_screen('Sorry, only letters are allowed.')
            elif guess in guessed:
                update_game_screen(
                    f"You've already guessed {guess}. Please try again."
                    )
            elif guess not in fruit:
                lives -= 1
                lives_lost_counter()
                guessed.append(guess)
                update_game_screen(
                    f'Sorry, {guess} is not in the word. Try again.'
                    )
            elif guess in fruit:
                guessed.append(guess)
                answer = ''
                for x in fruit:
                    if x in guessed:
                        answer += str(x + ' ')
                    else:
                        answer += ('_ ')
                update_game_screen(
                    f'Success! The letter {guess} is in the word. Try another.'
                    )
            else:
                update_game_screen(
                    'Sorry that character is invalid. Please try again.'
                    )
        elif guess == '':
            update_game_screen(
                'Whoops! Looks like you didn\'t submit anything. Try again.'
                )
        elif guess.isalpha() is False:
            update_game_screen('Sorry, only letters are allowed.')
        # Runs if guess is longer then 1 character.
        elif guess == fruit:
            updated_fruits = f'{fruits_collected} {fruit.lower()}'
            WKS.update_cell(user_num, 3, updated_fruits)
            check_fruits(user_num)
            answer = fruit
            # Adds user to hall of fame if all fruits found.
            if len(fruits_coll_li) == len(fruits):
                add_to_hof(user_num)
            update_game_screen(
                f'Success! You found a {fruit}. '
                'It has been added to your basket.'
                )
            user_input = input(
                ' ' * 7 + 'Press ENTER to play again '
                'or type N to go back to the main menu: '
                )
            while True:
                if user_input == '':
                    play()
                elif user_input.upper() == 'N':
                    menu()
                else:
                    clear_console()
                    print(BR * 8)
                    print(C('Sorry, character not recognised.'))
                    print(C(
                        'Please hit ENTER to play again '
                        'or N to return to the main menu.'
                        ))
                    user_input = input(' ' * 39 + ': ')
        elif guess.upper() == 'EXIT':
            menu()
        else:
            lives -= 1
            lives_lost_counter()
            update_game_screen(
                f'Sorry, {guess} is not the word. Try again.'
                    )
        # Runs if each individual character has been found.
        if '_' not in answer:
            updated_fruits = f'{fruits_collected} {fruit.lower()}'
            WKS.update_cell(user_num, 3, updated_fruits)
            check_fruits(user_num)
            # Adds user to hall of fame if all fruits found.
            if len(fruits_coll_li) == len(fruits):
                add_to_hof(user_num)
                clear_console()
            update_game_screen(
                f'Success! You found a {fruit}. '
                'It has been added to your basket.'
                )
            user_input = input(
                ' ' * 7 + 'Press ENTER to play again '
                'or type N to go back to the main menu: '
                )
            while True:
                if user_input == '':
                    play()
                elif user_input.upper() == 'N':
                    menu()
                else:
                    clear_console()
                    print(BR * 4)
                    print(C('Sorry, that character is not recognised.'))
                    print(C(
                        'Please hit ENTER to play again '
                        'or N to return to the main menu.'
                        ))
                    user_input = input(' ' * 39 + ': ')
    # Runs if user loses all lives.
    if lives == 0:
        clear_console()
        user_deaths = int(user_info[3])
        user_deaths += 1
        # Updates times user has died on google sheets.
        WKS.update_cell(user_num, 4, user_deaths)
        print(BR * 8)
        print(C('Oh no! You\'ve lost all your lives!'))
        user_input = input(
            ' ' * 12 + 'Press Y to play again '
            'or N to go back to the main menu: '
            )
        while True:
            if user_input.upper() == 'Y':
                play()
            elif user_input.upper() == 'N':
                menu()
            else:
                clear_console()
                print(BR * 4)
                print(C('Sorry, that character is not recognised.'))
                print(C(
                    'Please input Y to play again '
                    'or N to return to the main menu.'
                    ))
                user_input = input(' ' * 39 + ': ')


def update_game_screen(msg):
    """
    Updates the lives, answer and message on the game screen.
    """
    clear_console()
    lost_lives = 5 - lives
    print(BR * 6)
    print(C(((u'\u2764' + ' ') * lives) + ((u'\u2661' + ' ') * lost_lives)))
    print(BR)
    print(C(answer))
    print(BR)
    print(C(msg))


def random_fruit():
    """
    Generates a random fruit from the fruits left to find.
    """
    fruit = random.choice(fruits_left)
    return fruit.upper()


def lives_lost_counter():
    """
    Updates a counter on google sheets every time the player loses a life.
    """
    user_info = WKS.row_values(user_num)
    user_lives_lost = int(user_info[4])
    user_lives_lost += 1
    WKS.update_cell(user_num, 5, user_lives_lost)


def rules():
    """
    Displays the rules of the game to the user
    """
    clear_console()
    phrases = [
        'The aim of Fruit Hunter is to gather all the fruit!',
        'Fruit is gathered by guessing the name of the fruit being displayed',
        'You can guess one letter at a time or try and guess the whole word',
        'The player has five lives. Incorrect guesses will lose you 1 life',
        'If all lives are lost you lose the game',
        "But dont worry as any fruit you've already found are saved!",
        'You can view the fruit you\'ve found in the fruits collected screen',
        'Find all the fruit you win the game '
        'and get entered into the hall of fame!',
        'Happy hunting!'
    ]
    for x in phrases:
        clear_console()
        print(BR * 4)
        print(C('HOW TO PLAY'))
        print(BR)
        print((C(x)))
        print(BR * 4)
        input(' ' * 30 + 'Hit enter to proceed ')
    menu()


def fruit_li():
    """
    Prints out a list of all fruits found by the user if any.
    Enables the user to reset the list if all fruits have been found.
    """
    check_fruits(user_num)
    # Removes the empty entry at start of list from when user was created.
    fruits_coll_li.remove('')
    # Sorts fruits collected to display 5 in each row.
    top_li = []
    mid_li = []
    bot_li = []
    y = 1
    for x in fruits_coll_li:
        if y < 6:
            top_li.append(x.capitalize())
            y += 1
        elif 5 < y < 11:
            mid_li.append(x.capitalize())
            y += 1
        else:
            bot_li.append(x.capitalize())
            y += 1

    clear_console()
    print(BR * 4)
    print(C('Fruits Collected'))
    print(BR)

    if len(fruits_coll_li) == len(fruits):
        print(C('Well done!'))
        print(C(
            'You have collected all the fruits '
            'and been entered into the hall of fame!'
            ))
        print(C(', '.join(top_li)))
        print(C(', '.join(mid_li)))
        print(C(', '.join(bot_li)))
        print(BR)
        user_input = input(
            ' ' * 20 + 'Would you like to reset the list? Y/N: '
            )
        if user_input.upper() == 'Y':
            WKS.update_cell(user_num, 3, '')
            WKS.update_cell(user_num, 4, 0)
            WKS.update_cell(user_num, 5, 0)
            clear_console()
            print(8 * BR)
            print(C('List has been reset. Returning to main menu.'))
            time.sleep(2)
            menu()
        elif user_input.upper() == 'N':
            print(C("You selected 'NO'. Returning to the main menu"))
            time.sleep(2)
            menu()
        else:
            print(C(
                'That character was not recognised. '
                'Returning to the main menu'))
            time.sleep(2)
            menu()
    elif fruits_collected == '':
        print(C("Sorry, you haven't collected any fruits yet!"))
        user_input = input(
            ' ' * 20 + 'Press Enter to return to the main menu: '
            )
        if user_input == '':
            menu()
        else:
            fruit_li()
    else:
        print(C(
            f'There are {len(fruits)} fruits to collect. '
            f'You have found {(len(fruits_coll_li))}! '
            ))
        print(C('You have already found:'))
        print(C(', '.join(top_li)))
        print(C(', '.join(mid_li)))
        print(C(', '.join(bot_li)))
        print(BR)
        user_input = input(
            ' ' * 21 + 'Press Enter to return to the main menu: '
            )
        if user_input.upper() == '':
            menu()
        else:
            fruit_li()


def add_to_hof(user_num):
    """
    Adds users name and death count to hall of fame worksheet
    """
    users_info = WKS.row_values(user_num)
    user_name = users_info[0]
    users_deaths = users_info[3]
    users_lives_lost = users_info[4]
    hof_info = [user_name.lower(), users_lives_lost, users_deaths]
    HOF.append_row(hof_info)


def display_hof():
    """
    Displays the top five people in the hall of fame.
    """
    clear_console()
    all = HOF.get_all_values()
    all.pop(0)
    # This line is credited to
    # https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
    all.sort(key=lambda all: all[1], reverse=True)
    x = slice(5)
    all = all[x]
    if len(all) < 5:
        for x in range(5 - len(all)):
            # This line stops the game throwing an error
            # when trying to obtain info from google sheets that is not there.
            all.append(['_____', '__', '__'])
    print(BR * 4)
    print(C('HALL OF FAME'))
    print(BR)
    index = 1
    for x in all:
        print(
            ' ' * 18 + str(index) +
            ': ', str(x[0].capitalize()) +
            '  -  Lives Lost: ' + str(x[1]) +
            '  -  Deaths: ' + str(x[2])
            )
        index += 1
    print(BR)
    user_input = input(' ' * 21 + 'Press Enter to return to the main menu: ')
    if user_input.upper() == '':
        menu()
    else:
        display_hof()


welcome()
