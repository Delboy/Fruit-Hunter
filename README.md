# Fruit Hunter

Fruit hunter is a Python terminal game, which runs on a mock terminal on Heroku.

User's try to find all the fruit by playing a hangman style game.

## How to play

Fruit Hunter is based on the classic game hangman except every word to be guessed is a fruit. There are 15 different fruits to find. Each time the user guesses a new fruit it is added to their collection. Once all fruits are collected the game is won and the users score is added to the hall of fame.

## Design 

I used [lucidchart.com](https://lucid.co/) to help design the project and create the following flow charts. 

### The main menu flow chart :
![Main Flow Chart](readme-assets/images/main-flow.png)

### The gameplay flow chart :
![Gameplay Flow Chart](readme-assets/images/game-flow.png)

## Features

### Welcome page

- The welcome page will display the name of the game and ask the user if they have played before.
- Depending on the user's choice they are directed to either the login or create user page.

![welcome](readme-assets/images/welcome.png)

### Create user page
- The create user page prompts the user to create a log-in username and a 4 digit pin code.
- If the user has made a mistake at the welcome screen and instead wants to log in they can type 'login' to be directed to the login page. 

![choose_username](readme-assets/images/choose_username.png)
![choose_pin](readme-assets/images/choose_pin.png)

- It will check to make sure the username is not already taken before completing.

![username_taken](readme-assets/images/username_taken.png)

- It will also not allow the user to create a login name over 15 characters long, or to input nothing.

![Username too long](readme-assets/images/username_too_long.png)
![Username Blank](readme-assets/images/blank_username.png)

- It will also verify the user's pin code before allowing the user's info to be created.

![verify_pin](readme-assets/images/verify_pin.png)

- Once the user has chosen a valid name and pin code their user details will be created and uploaded to google sheets.
- The user will then be logged in and sent to the main menu.

![user_created](readme-assets/images/user_created.png)

### Log in page
- The log in page will ask the user for their log in name and pin code.

![login](readme-assets/images/login.png)
![login_pin](readme-assets/images/login_pin.png)

- If the user's name does not exist it will ask the user if they want to create a new login.

![login_no_username](readme-assets/images/login_no_username.png)

- If the user's pin is incorrect it will notify the user and restart the login.

![login_incorrect_pin](readme-assets/images/login_incorrect_pin.png)

- If the user's name is recognised and the pin is correct the user will be logged in and sent to the main menu.

![login_success](readme-assets/images/login_success.png)

### Main menu
- The main menu will have 5 options that direct the user to where they want to go.

![Main Menu](readme-assets/images/main_menu.png)

### How to play page

- The how to play page shows the user the rules of the game. Hitting enter cycles through each point.

![How to play](readme-assets/images/how_to_play.gif)

### Fruits collected page
- The fruits collected page will display a list of all the fruits the user has collected, if any, and informs the user how many more fruits they have yet to find.

![Fruits Collected](readme-assets/images/fruits_collected.png)

- If the user has found all the fruits they can reset the list and play again from here.

![All Fruits Collected](readme-assets/images/fruits_collected_all.png)

### Hall of Fame page
- The hall of fame page shows a list of the top 5 users that have collected all fruit.
- The list will sort the users from least amount of lives lost to most.

![Hall of fame](readme-assets/images/hall_of_fame.png)

### Game play 
- When playing the game the user's play area consists of: 
    - A 'lives' display which shows filled hearts which deplete when an incorrect answer is given.
    - Underscores representing how many letters are left to discover in the word.
    - A user input area where the user inputs their answers.
    - Feedback that informs if the user has answered correctly or if they've tried a letter twice.

![Game Area](readme-assets/images/game_area.png)

![Already Guessed](readme-assets/images/already_guessed.png)

- The user can guess one letter at a time or they can try to guess the whole word in one.

![Correct](readme-assets/images/correct_letter.png)

- If all lives are lost the game ends and the user is asked if they'd like to try again. This will generate a new fruit from the remaining fruit needed to be found.

![Death](readme-assets/images/death.png)

- If the user guesses all letters in the word, or guesses the word itself, then the game is won and the fruit they found is added to their user's info in google sheets.

![Fruit Found](readme-assets/images/fruit_found.png)

- If the user has gathered all the fruit and tries to play a game, a message appears informing them that they have collected all the fruit and to check to see if they've reached the hall of fame. They will also be asked if they would like to reset the list and play again.

![All fruit found](readme-assets/images/game_area_all_fruit.png)

### Future Features

- Enable user to spend a life for a hint, or multiple lives to solve a letter.
- Different difficulty modes. Harder would entail less lives or if the player dies the fruits collected list is reset.

## Testing

I have tested this project by running the code through a validator at [Pep8online.com](http://pep8online.com/).

I have also manually tested the game by trying to input invalid characters as well as trying to leave the input blank, or by inputting too many characters at any point where the user is asked for an input.

I have also asked friends and family and anybody with the code institute on slack to try and find any bugs within the game.

## Bugs

### Solved Bugs

- The length of the fruits collected list would always be one over. This is because when the user is created in the create_user function the cell containing the fruits collected could not be left blank, so you would have to input an empty string. This would then be read as an entry meaning the length of the list would always read that empty string as 1. Fixed this issue by removing the blank string with the line 'fruits_coll_li.remove('')'.

- When creating the game I originally had no spaces between the underscores where the unsolved word was displayed. I found that this was hard for the user to distinguish how many letters were in the word, so I inserted a space in between each underscore. This introduced a bug where the game wouldn't end if you guessed each letter of the word individually. This was because in order for the game to recognise that you had guessed the word I had an if statement that read 'if answer == fruit', so that if anytime the answer that was being updated with each guess matched the fruit trying to be guessed then you would win. But because I now had put spaces in between the characters the answer would never match the fruit exactly. I solved this by changing what the game was looking for to determine a correct answer. I updated the if statement to see if there were no underscores left in the answer, as that would also mean every letter had been discovered. 

- When creating a new user if the pins didn't match the user would be asked again for the pin. On this second go the user could create a pin any length with any characters. This happened because I had forgotten to insert the same while loop that checked the pins length and to make sure it was only numbers.

- When creating a new user you could enter the same name as an exiting user if you capitalised the first letter. Fixed by using the .lower() method on the users input to check against the names on google sheets.

- Originally I had the code to update the lives display inside the play function but found that it wouldnt update correctly. I ran print logs to check that the lives and lives lost counter was updating correctly which they were but it wasn't transferring over to the display. I couldn't figure out why but once I had created the update_game_screen function and implemented the lives display into it, it worked fine.

- When creating the hall of fame function the game would crash if there weren't at least 5 names to be displayed. This was because the game is trying to retrieve information from google sheets that is not there. I fixed this by creating an if and a for loop. Which stated that if the length of all the information gathered was less then 5 (meaning there were less then 5 entries on google sheets), to append the list with blank information until there is 5 entries.

### Unsolved Bugs

- No bugs remaining.

