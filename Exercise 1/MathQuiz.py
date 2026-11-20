# Exercise 1 - Maths Quiz
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random   # RNG
import os
import pygame

# ============================================================
# SETTINGS

BACKGROUND_COLOUR = '#234567'
BUTTON_COLOUR = '#001111'
BUTTON_TEXT_COLOUR = 'yellow'
BOX_COLOUR = '#F8F8E8'
BOX_TEXT_COLOUR = '#303030'

QUESTIONS_PER_QUIZ = 10
POINTS_FIRST_TRY = 10
POINTS_SECOND_TRY = 5
MAX_SCORE = 100

MAX_HEALTH = 100
HEALTH_LOST_PER_WRONG_ANSWER = 10
HP_BAR_WIDTH = 150 #how wide a full HP bar is (in pixels)

LEVEL_NAMES = ["Easy", "Moderate", "Advanced"]

#the Resources folder that sits next to this file, so it works from any folder
RESOURCES_FOLDER = os.path.join(os.path.dirname(__file__), "Resources")


# ============================================================
# WINDOW SETUP

root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.resizable(0, 0)
root['bg'] = BACKGROUND_COLOUR


# ============================================================
# BACKGROUNDS AND MUSIC

# open each picture, stretch it to fill the battle area, and keep it in a variable
easy_picture = Image.open(f"{RESOURCES_FOLDER}/grass_bg.png")
easy_background = ImageTk.PhotoImage(easy_picture.resize((500, 280)))

moderate_picture = Image.open(f"{RESOURCES_FOLDER}/rock_mountain_bg.png")
moderate_background = ImageTk.PhotoImage(moderate_picture.resize((500, 280)))

advanced_picture = Image.open(f"{RESOURCES_FOLDER}/water_bg.png")
advanced_background = ImageTk.PhotoImage(advanced_picture.resize((500, 280)))

backgrounds = [easy_background, moderate_background, advanced_background]

#loads the battle music once (it is started and stopped later)
pygame.mixer.init()
pygame.mixer.music.load(f"{RESOURCES_FOLDER}/soundtrack.mp3")


# ============================================================
# QUIZ INFO
#the game's data. Functions can change what is inside a dictionary, so every function can read and update it as you play.

quiz = {
    "difficulty_level": 1,        
    # 1 = easy, 2 = moderate, 3 = advanced
    "question_number": 0,         
    # which question we are on (1 to 10)
    "attempt_number": 1,          
    # 1 = first try, 2 = second try
    "score": 0,                   
    # points so far (the enemy loses the same amount of health)
    "player_health": MAX_HEALTH,  
    # goes down 10 for every wrong answer
    "correct_answer": 0,          
    # the right answer to the current problem
}


# ============================================================
# FUNCTIONS

def displayMenu():
    #the music only plays in the quiz screen, so stop it here
    pygame.mixer.music.stop()
    menu_frame.tkraise()


def makeBattleBox(x, y):
    #builds one name box with an HP bar, and gives back the name label and the green bar
    box = Frame(quiz_frame, bg=BOX_COLOUR)
    box.place(x=x, y=y, width=220, height=60)

    name_label = Label(box, text="", font=('Roboto', 12), bg=BOX_COLOUR, fg=BOX_TEXT_COLOUR)
    name_label.place(x=10, y=6)
    Label(box, text="HP", font=('Roboto', 9), bg=BOX_COLOUR, fg='darkorange').place(x=10, y=34)

    Frame(box, bg='grey').place(x=35, y=36, width=HP_BAR_WIDTH, height=10)   
    #empty bar behind
    hp_bar = Frame(box, bg='green')                                          
    #the bar that shrinks
    hp_bar.place(x=35, y=36, width=HP_BAR_WIDTH, height=10)
    return name_label, hp_bar


def setHealthBar(bar, health):
    #makes the bar as wide as the health left (only the width changes)
    bar.place(width=int(HP_BAR_WIDTH * health / MAX_HEALTH))
    #green, then yellow below 70, then red below 50
    if health < 50:
        bar.config(bg='red')
    elif health < 70:
        bar.config(bg='yellow')
    else:
        bar.config(bg='green')


def updateHealthBars():
    #the enemy loses the same amount of health as the points scored
    setHealthBar(enemy_hp_bar, MAX_HEALTH - quiz["score"])
    setHealthBar(player_hp_bar, quiz["player_health"])


def randomInt(difficulty_level):
    #returns a random number with the right number of digits for the level
    if difficulty_level == 1:
        return random.randint(0, 9)          
    #easy: single digit
    elif difficulty_level == 2:
        return random.randint(10, 99)       
    #moderate: double digit
    else:
        return random.randint(1000, 9999)    
    #advanced: four digits


def decideOperation():
    #randomly returns '+' or '-'
    if random.randint(1, 2) == 1:
        return '+'
    else:
        return '-'


def startQuiz(difficulty_level):
    #runs when a difficulty button is clicked: reset everything and begin
    quiz["difficulty_level"] = difficulty_level
    quiz["score"] = 0
    quiz["question_number"] = 0
    quiz["player_health"] = MAX_HEALTH
    feedback_label.config(text="")

    #the background and names depend on the level (lists start at 0, so we use level - 1)
    battle_background_label.config(image=backgrounds[difficulty_level - 1])
    enemy_name_label.config(text=f"{LEVEL_NAMES[difficulty_level - 1]} Quiz Lv{difficulty_level}")
    player_name_label.config(text=f"Player Lv{difficulty_level}")

    updateHealthBars()
    pygame.mixer.music.play(-1)   #-1 means the music repeats while we are in the quiz
    quiz_frame.tkraise()
    displayProblem()


def displayProblem():
    #moves to the next question and shows it on the quiz screen
    quiz["question_number"] += 1
    quiz["attempt_number"] = 1

    #pick the two numbers and the operation for this question
    first_number = randomInt(quiz["difficulty_level"])
    second_number = randomInt(quiz["difficulty_level"])
    operation = decideOperation()

    #work out the real answer and keep it for checking later
    if operation == '+':
        quiz["correct_answer"] = first_number + second_number
    else:
        quiz["correct_answer"] = first_number - second_number

    #update the screen
    question_number_label.config(text=f"Question {quiz['question_number']} of {QUESTIONS_PER_QUIZ}")
    score_label.config(text=f"Score: {quiz['score']}")
    problem_label.config(text=f"{first_number} {operation} {second_number} =")
    answer_entry.delete(0, END)   #empty the typing box


def isCorrect(typed_answer, correct_answer, attempt_number):
    #checks the answer, shows a message, and returns True or False
    if typed_answer.strip() == str(correct_answer):
        feedback_label.config(text="Correct!", fg='darkgreen')
        return True
    elif attempt_number == 1:
        feedback_label.config(text="Wrong, try once more!", fg='darkorange')
        return False
    else:
        feedback_label.config(text=f"Wrong, the answer was {correct_answer}", fg='red')
        return False


def submitAnswer():
    #runs when Submit is clicked (or Enter is pressed)
    typed_answer = answer_entry.get()
    answered_correctly = isCorrect(typed_answer, quiz["correct_answer"], quiz["attempt_number"])

    if answered_correctly:
        #10 points (10 enemy health lost) on the first try, 5 on the second
        if quiz["attempt_number"] == 1:
            quiz["score"] += POINTS_FIRST_TRY
        else:
            quiz["score"] += POINTS_SECOND_TRY
        updateHealthBars()
        nextQuestion()
    else:
        #every wrong answer costs the player 10 health, even on the second try
        quiz["player_health"] -= HEALTH_LOST_PER_WRONG_ANSWER
        updateHealthBars()
        if quiz["player_health"] <= 0:
            gameOver()
        elif quiz["attempt_number"] == 1:
            quiz["attempt_number"] = 2   
            #give one more chance
            answer_entry.delete(0, END)
        else:
            nextQuestion()               
            #both attemps used, next question


def gameOver():
    #the player ran out of health, so tell them and go back to the menu
    messagebox.showinfo("Game Over", "Your HP reached 0!")
    displayMenu()


def nextQuestion():
    #after question 10 show the results, otherwise show another problem
    if quiz["question_number"] == QUESTIONS_PER_QUIZ:
        displayResults()
    else:
        displayProblem()


def displayResults():
    #shows the final score and the rank (the music stops here too)
    pygame.mixer.music.stop()
    final_score = quiz["score"]

    if final_score > 90:
        rank = "A+"
    elif final_score >= 80:
        rank = "A"
    elif final_score >= 70:
        rank = "B"
    elif final_score >= 60:
        rank = "C"
    elif final_score >= 50:
        rank = "D"
    else:
        rank = "F"

    final_score_label.config(text=f"Your score: {final_score} / {MAX_SCORE}")
    rank_label.config(text=f"Rank: {rank}")
    results_frame.tkraise()


def playAgain():
    #asks the player if they want another go
    wants_to_play_again = messagebox.askyesno("Play again?", "Would you like to play again?")
    if wants_to_play_again:
        displayMenu()
    else:
        rank_label.config(text="Thanks for playing!")


# ============================================================
#MENU SCREEN

menu_frame = Frame(root, bg=BACKGROUND_COLOUR)
menu_frame.place(x=0, y=0, width=500, height=400)

Label(menu_frame, text="Maths Quiz", font=('Roboto', 28), bg=BACKGROUND_COLOUR, fg='white').pack(pady=20)
Label(menu_frame, text="DIFFICULTY LEVEL", font=('Roboto', 16), bg=BACKGROUND_COLOUR, fg='yellow').pack(pady=10)

#lambda lets each button pass its own level number to startQuiz
Button(menu_frame, text="1. Easy (1 digit)", width=22, font=('Roboto', 12),
       bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=lambda: startQuiz(1)).pack(pady=8)
Button(menu_frame, text="2. Moderate (2 digits)", width=22, font=('Roboto', 12),
       bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=lambda: startQuiz(2)).pack(pady=8)
Button(menu_frame, text="3. Advanced (4 digits)", width=22, font=('Roboto', 12),
       bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=lambda: startQuiz(3)).pack(pady=8)


# ============================================================
# QUIZ SCREEN

quiz_frame = Frame(root, bg=BACKGROUND_COLOUR)
quiz_frame.place(x=0, y=0, width=500, height=400)

#battle background (the picture changes with the difficulty)
battle_background_label = Label(quiz_frame, image=easy_background)
battle_background_label.place(x=0, y=0)

#question number and score (top right)
question_number_label = Label(quiz_frame, text="", font=('Roboto', 10), bg=BOX_COLOUR, fg=BOX_TEXT_COLOUR)
question_number_label.place(x=350, y=15)
score_label = Label(quiz_frame, text="", font=('Roboto', 10), bg=BOX_COLOUR, fg=BOX_TEXT_COLOUR)
score_label.place(x=350, y=40)

#enemy box (top left) and player box (lower right)
enemy_name_label, enemy_hp_bar = makeBattleBox(10, 20)
player_name_label, player_hp_bar = makeBattleBox(270, 200)

#question box (bottom left): the problem, with the attempt message under it
question_box = Frame(quiz_frame, bg=BOX_COLOUR)
question_box.place(x=10, y=290, width=320, height=100)

problem_label = Label(question_box, text="", font=('Roboto', 22), bg=BOX_COLOUR, fg=BOX_TEXT_COLOUR)
problem_label.place(x=15, y=10)
feedback_label = Label(question_box, text="", font=('Roboto', 12), bg=BOX_COLOUR, fg=BOX_TEXT_COLOUR)
feedback_label.place(x=15, y=62)

#answer entry and submit button (bottom right)
answer_entry = Entry(quiz_frame, font=('Roboto', 18), width=9)
answer_entry.place(x=345, y=300)
answer_entry.bind("<Return>", lambda event: submitAnswer())   
#Enter key works like Submit

Button(quiz_frame, text="Submit", width=14, font=('Roboto', 12),
       bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=submitAnswer).place(x=345, y=350)


# ============================================================
# RESULTS SCREEN

results_frame = Frame(root, bg=BACKGROUND_COLOUR)
results_frame.place(x=0, y=0, width=500, height=400)

Label(results_frame, text="Quiz Finished!", font=('Roboto', 28), bg=BACKGROUND_COLOUR, fg='white').pack(pady=20)

final_score_label = Label(results_frame, text="", font=('Roboto', 18), bg=BACKGROUND_COLOUR, fg='yellow')
final_score_label.pack(pady=10)
rank_label = Label(results_frame, text="", font=('Roboto', 18), bg=BACKGROUND_COLOUR, fg='white')
rank_label.pack(pady=10)

Button(results_frame, text="Play Again", width=15, font=('Roboto', 12),
       bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=playAgain).pack(pady=20)


# ============================================================
# START THE PROGRAM

displayMenu()     
#show the menu first
root.mainloop()   
#keep the window open and wait for clicks