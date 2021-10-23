# Fruit Hunter

Fruit hunter is a Python terminal game, which runs on a mock terminal on Heroku.

User's try to find all the fruit by playing a hangman style game.

## How to play

Fruit Hunter is based on the classic game hangman except every word to be guessed is a fruit. There are 'x' different fruits to find. Each time the user guesses a new fruit it is added to their collection. Once all fruits are collected the game is won.

## Design 

I used [lucidchart.com](https://lucid.co/) to help design the project and create the following flow charts. 

### The main menu flow chart :
![Main Flow Chart](readme-assets/images/main-flow.png)

### The gameplay flow chart :
![Gameplay Flow Chart](readme-assets/images/game-flow.png)

## Features

### Create user page
- The create user page prompts the user to create a log-in username and a 4 digit pin code.
- It will check to make sure the username is not already taken before completing.
- It will also verify the user's pin code before allowing the user's info to be created.

### Log in page
- The log in page will ask the user for their log in name and pin code.
- If the user's name does not exist it will direct the user to the create user page.
- Once logged in the programme will grab the user's details and create certain variables with them such as the row number they are in the google spreadsheet and the fruits they've already collected if the user has played before.

### Main menu
- The main menu will have 5 options to direct the user to where they want to go.

### Fruits collected page
- The fruits collected page will display a list of all the fruits the user has collected if any, and inform the user how many more fruits they have yet to find.

### Hall of fame page
- The hall of fame page shows a list of the top 5 user's that have collected all fruit.
- The list will order the user's from least amount of attempts to most.

### Random fruit generator
- The random fruit generator generates a random fruit from any remaining fruit left to be found.

### Game play 
- The game consists of underscores representing how many letters are left to discover in the word.
- A lives display which shows filled hearts which deplete when an incorrect answer is given.
- A user input area where the user inputs their answers.

### Lives display
- The lives display shows 5 hearts representing 1 life.
- When a life is lost one heart will turn into an empty heart.
- When all lives are lost the game is over.
