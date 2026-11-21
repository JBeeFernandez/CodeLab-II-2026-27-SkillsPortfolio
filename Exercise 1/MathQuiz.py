#Exercise 1 - Maths Quiz
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random   # RNG
import os
import pygame

# ============================================================
# SETTINGS

PANEL_COLOUR = '#989898' 
BORDER_COLOUR = '#505058'
BOX_COLOUR = '#E0E0E0' 
WHITE_COLOUR = '#F8F8F8'
TEXT_COLOUR = '#484850' 
HP_TAG_COLOUR = '#F8B000'
PINK_BUTTON = '#F8A8B0'
GREEN_BUTTON = '#58A038'
GOLD_BUTTON = '#D89830'
BLUE_BUTTON = '#3088C0'

GAME_FONT = 'Courier New' # change this one word to use a different font

QUESTIONS_PER_QUIZ = 10
POINTS_FIRST_TRY = 10
POINTS_SECOND_TRY = 5
MAX_SCORE = 100

MAX_HEALTH = 100
HEALTH_LOST_PER_WRONG_ANSWER = 10
HP_BAR_WIDTH = 130 # how wide a full HP bar is (in pixels)

LEVEL_NAMES = ["Easy", "Moderate", "Advanced"]

#The Resources folder that sits next to this file, so it works from any folder
RESOURCES_FOLDER = os.path.join(os.path.dirname(__file__), "Resources")


# ============================================================
# WINDOW SETUP

root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.resizable(0, 0)
root['bg'] = PANEL_COLOUR


# ============================================================
# PICTURES AND MUSIC

def loadImage(file_name, width, height):
    # opens a picture from the Resources folder, resizes it, and keeps its see-through parts
    picture = Image.open(f"{RESOURCES_FOLDER}/{file_name}").convert("RGBA").resize((width, height))
    return ImageTk.PhotoImage(picture)

# each picture is kept in a variable so Tkinter does not lose it
easy_background = loadImage("grass_bg.png", 500, 280)
moderate_background = loadImage("rock_mountain_bg.png", 500, 280)
advanced_background = loadImage("water_bg.png", 500, 280)
backgrounds = [easy_background, moderate_background, advanced_background]

oak_image = loadImage("oak.png", 120, 120)    # the enemy
red_image = loadImage("red.png", 128, 128)    # the player (back view)

pygame.mixer.init()


# ============================================================
# QUIZ INFO
# The game's data. Functions can change what is inside a dictionary,
# so every function can read and update it as you play.

quiz = {
    "difficulty_level": 1,        # 1 = easy, 2 = moderate, 3 = advanced
    "question_number": 0,         # which question we are on (1 to 10)
    "attempt_number": 1,          # 1 = first try, 2 = second try
    "score": 0,                   # points so far (the enemy loses the same amount of health)
    "player_health": MAX_HEALTH,  # goes down 10 for every wrong answer
    "correct_answer": 0,          # the right answer to the current problem
}


# ============================================================
# FUNCTIONS

def playMusic(file_name):
    # plays a song from the Resources folder on repeat (it replaces the song playing now)
    pygame.mixer.music.load(f"{RESOURCES_FOLDER}/{file_name}")
    pygame.mixer.music.play(-1)


def displayMenu():
    # the menu has its own music
    playMusic("menutrack.mp3")
    menu_frame.tkraise()


def makeBox(parent, x, y, width, height, fill_colour):
    # a box with a dark outline: a dark frame with a lighter frame inside it
    outline = Frame(parent, bg=BORDER_COLOUR)
    outline.place(x=x, y=y, width=width, height=height)
    inside = Frame(outline, bg=fill_colour)
    inside.place(x=4, y=4, width=width - 8, height=height - 8)
    return inside


def makeScene(parent):
    # builds the battle scene: Oak on the enemy side, Red on the player side
    scene = Canvas(parent, width=500, height=280, highlightthickness=0)
    scene.place(x=0, y=0)
    background = scene.create_image(0, 0, anchor="nw", image=easy_background)
    scene.create_image(310, 46, anchor="nw", image=oak_image)
    scene.create_image(31, 142, anchor="nw", image=red_image)
    return scene, background


def makeBattleBox(x, y, name):
    # builds one name box and gives back its name label, level label and green HP bar
    box = makeBox(quiz_frame, x, y, 230, 62, BOX_COLOUR)

    name_label = Label(box, text=name, font=(GAME_FONT, 12, 'bold'), bg=BOX_COLOUR, fg=TEXT_COLOUR)
    name_label.place(x=8, y=4)
    level_label = Label(box, text="Lv1", font=(GAME_FONT, 12, 'bold'), bg=BOX_COLOUR, fg=TEXT_COLOUR)
    level_label.place(x=214, y=4, anchor=NE)

    Frame(box, bg=BORDER_COLOUR).place(x=50, y=28, width=164, height=18)   # dark holder for the bar
    Label(box, text="HP", font=(GAME_FONT, 9, 'bold'), bg=BORDER_COLOUR, fg=HP_TAG_COLOUR).place(x=54, y=29)
    hp_bar = Frame(box, bg='#18C020')                                      # the bar that shrinks
    hp_bar.place(x=80, y=32, width=HP_BAR_WIDTH, height=10)
    return name_label, level_label, hp_bar


def setHealthBar(bar, health):
    # makes the bar as wide as the health left (only the width changes)
    bar.place(width=int(HP_BAR_WIDTH * health / MAX_HEALTH))
    # green, then yellow below 70, then red below 50
    if health < 50:
        bar.config(bg='#E83030')
    elif health < 70:
        bar.config(bg='#F8D030')
    else:
        bar.config(bg='#18C020')


def updateHealthBars():
    # the enemy loses the same amount of health as the points scored
    setHealthBar(enemy_hp_bar, MAX_HEALTH - quiz["score"])
    setHealthBar(player_hp_bar, quiz["player_health"])


def randomInt(difficulty_level):
    # returns a random number with the right number of digits for the level
    if difficulty_level == 1:
        return random.randint(0, 9)          # easy: single digit
    elif difficulty_level == 2:
        return random.randint(10, 99)        # moderate: double digit
    else:
        return random.randint(1000, 9999)    # advanced: four digits


def decideOperation():
    # randomly returns '+' or '-'
    if random.randint(1, 2) == 1:
        return '+'
    else:
        return '-'


def startQuiz(difficulty_level):
    # runs when a difficulty button is clicked: reset everything and begin
    quiz["difficulty_level"] = difficulty_level
    quiz["score"] = 0
    quiz["question_number"] = 0
    quiz["player_health"] = MAX_HEALTH
    feedback_label.config(text="")

    # the background and names depend on the level (lists start at 0, so we use level - 1)
    quiz_scene.itemconfig(quiz_background, image=backgrounds[difficulty_level - 1])
    enemy_name_label.config(text=f"{LEVEL_NAMES[difficulty_level - 1]} Quiz")
    enemy_level_label.config(text=f"Lv{difficulty_level}")
    player_level_label.config(text=f"Lv{difficulty_level}")

    updateHealthBars()
    playMusic("soundtrack.mp3")
    quiz_frame.tkraise()
    displayProblem()


def displayProblem():
    # moves to the next question and shows it on the quiz screen
    quiz["question_number"] += 1
    quiz["attempt_number"] = 1

    # pick the two numbers and the operation for this question
    first_number = randomInt(quiz["difficulty_level"])
    second_number = randomInt(quiz["difficulty_level"])
    operation = decideOperation()

    # work out the real answer and keep it for checking later
    if operation == '+':
        quiz["correct_answer"] = first_number + second_number
    else:
        quiz["correct_answer"] = first_number - second_number

    # update the screen
    status_label.config(text=f"Question {quiz['question_number']} of {QUESTIONS_PER_QUIZ}\nScore: {quiz['score']}")
    problem_label.config(text=f"{first_number} {operation} {second_number} =")
    answer_entry.delete(0, END)   # empty the typing box


def isCorrect(typed_answer, correct_answer, attempt_number):
    # checks the answer, shows a message, and returns True or False
    if typed_answer.strip() == str(correct_answer):
        feedback_label.config(text="It's super effective!", fg='darkgreen')
        return True
    elif attempt_number == 1:
        feedback_label.config(text="It missed! Try once more!", fg='darkorange')
        return False
    else:
        feedback_label.config(text=f"It missed! The answer was {correct_answer}", fg='red')
        return False


def submitAnswer():
    # runs when Submit is clicked (or Enter is pressed)
    typed_answer = answer_entry.get()
    answered_correctly = isCorrect(typed_answer, quiz["correct_answer"], quiz["attempt_number"])

    if answered_correctly:
        # 10 points (10 enemy health lost) on the first try, 5 on the second
        if quiz["attempt_number"] == 1:
            quiz["score"] += POINTS_FIRST_TRY
        else:
            quiz["score"] += POINTS_SECOND_TRY
        updateHealthBars()
        nextQuestion()
    else:
        # every wrong answer costs the player 10 health, even on the second try
        quiz["player_health"] -= HEALTH_LOST_PER_WRONG_ANSWER
        updateHealthBars()
        if quiz["player_health"] <= 0:
            gameOver()
        elif quiz["attempt_number"] == 1:
            quiz["attempt_number"] = 2   # give one more chance
            answer_entry.delete(0, END)
        else:
            nextQuestion()               # both tries used, next question


def gameOver():
    # the player ran out of health, so tell them and go back to the menu
    messagebox.showinfo("Whited out!", "Player is out of usable Pokémon!\nPlayer whited out!")
    displayMenu()


def nextQuestion():
    # after question 10 show the results, otherwise show another problem
    if quiz["question_number"] == QUESTIONS_PER_QUIZ:
        displayResults()
    else:
        displayProblem()


def displayResults():
    # shows the final score and the rank (the music stops here)
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
    # asks the player if they want another go
    wants_to_play_again = messagebox.askyesno("Rematch?", "Want to battle again, Trainer?")
    if wants_to_play_again:
        displayMenu()
    else:
        rank_label.config(text="Take care, Trainer!")


# ============================================================
# MENU SCREEN

menu_frame = Frame(root, bg=PANEL_COLOUR)
menu_frame.place(x=0, y=0, width=500, height=400)

makeScene(menu_frame)   # the same battle scene as the quiz screen

title_box = makeBox(menu_frame, 10, 20, 230, 62, BOX_COLOUR)
Label(title_box, text="MATHS QUIZ", font=(GAME_FONT, 18, 'bold'), bg=BOX_COLOUR,
      fg=TEXT_COLOUR).place(relx=0.5, rely=0.5, anchor=CENTER)

difficulty_box = makeBox(menu_frame, 10, 288, 320, 102, WHITE_COLOUR)
Label(difficulty_box, text="DIFFICULTY LEVEL\nEasy: 1 digit\nModerate: 2 digits\nAdvanced: 4 digits",
      font=(GAME_FONT, 11, 'bold'), bg=WHITE_COLOUR, fg=TEXT_COLOUR, justify=LEFT).place(x=12, y=6)

# lambda lets each button pass its own level number to startQuiz
Button(menu_frame, text="1. EASY", font=(GAME_FONT, 12, 'bold'), bg=GREEN_BUTTON, fg='white',
       command=lambda: startQuiz(1)).place(x=340, y=288, width=150, height=30)
Button(menu_frame, text="2. MODERATE", font=(GAME_FONT, 12, 'bold'), bg=GOLD_BUTTON, fg='white',
       command=lambda: startQuiz(2)).place(x=340, y=322, width=150, height=30)
Button(menu_frame, text="3. ADVANCED", font=(GAME_FONT, 12, 'bold'), bg=BLUE_BUTTON, fg='white',
       command=lambda: startQuiz(3)).place(x=340, y=356, width=150, height=30)


# ============================================================
# QUIZ SCREEN

quiz_frame = Frame(root, bg=PANEL_COLOUR)
quiz_frame.place(x=0, y=0, width=500, height=400)

quiz_scene, quiz_background = makeScene(quiz_frame)

# question number and score (top right)
status_box = makeBox(quiz_frame, 340, 8, 150, 44, WHITE_COLOUR)
status_label = Label(status_box, text="", font=(GAME_FONT, 9, 'bold'), bg=WHITE_COLOUR,
                     fg=TEXT_COLOUR, justify=LEFT)
status_label.place(x=6, y=1)

# enemy box (top left) and player box (lower right)
enemy_name_label, enemy_level_label, enemy_hp_bar = makeBattleBox(10, 20, "Easy Quiz")
player_name_label, player_level_label, player_hp_bar = makeBattleBox(265, 200, "Player")

# question box (bottom left): the problem, with the attempt message under it
question_box = makeBox(quiz_frame, 10, 288, 320, 102, WHITE_COLOUR)
problem_label = Label(question_box, text="", font=(GAME_FONT, 20, 'bold'), bg=WHITE_COLOUR, fg=TEXT_COLOUR)
problem_label.place(x=12, y=8)
feedback_label = Label(question_box, text="", font=(GAME_FONT, 11, 'bold'), bg=WHITE_COLOUR, fg=TEXT_COLOUR)
feedback_label.place(x=12, y=56)

# answer entry and submit button (bottom right)
answer_box = makeBox(quiz_frame, 340, 288, 150, 46, WHITE_COLOUR)
answer_entry = Entry(answer_box, font=(GAME_FONT, 16, 'bold'), width=9)
answer_entry.place(x=6, y=5)
answer_entry.bind("<Return>", lambda event: submitAnswer())   # Enter key works like Submit

Button(quiz_frame, text="SUBMIT", font=(GAME_FONT, 12, 'bold'), bg=PINK_BUTTON, fg=TEXT_COLOUR,
       command=submitAnswer).place(x=340, y=342, width=150, height=48)


# ============================================================
# RESULTS SCREEN

results_frame = Frame(root, bg=PANEL_COLOUR)
results_frame.place(x=0, y=0, width=500, height=400)

makeScene(results_frame)   # the same battle scene again

finished_box = makeBox(results_frame, 10, 20, 230, 62, BOX_COLOUR)
Label(finished_box, text="QUIZ FINISHED!", font=(GAME_FONT, 16, 'bold'), bg=BOX_COLOUR,
      fg=TEXT_COLOUR).place(relx=0.5, rely=0.5, anchor=CENTER)

score_box = makeBox(results_frame, 10, 288, 320, 102, WHITE_COLOUR)
final_score_label = Label(score_box, text="", font=(GAME_FONT, 16, 'bold'), bg=WHITE_COLOUR, fg=TEXT_COLOUR)
final_score_label.place(x=12, y=12)
rank_label = Label(score_box, text="", font=(GAME_FONT, 16, 'bold'), bg=WHITE_COLOUR, fg=TEXT_COLOUR)
rank_label.place(x=12, y=52)

Button(results_frame, text="PLAY AGAIN", font=(GAME_FONT, 12, 'bold'), bg=PINK_BUTTON, fg=TEXT_COLOUR,
       command=playAgain).place(x=340, y=288, width=150, height=102)


# ============================================================
# COPYRIGHT SCREEN (shows first)

trademark_frame = Frame(root, bg='black')
trademark_frame.place(x=0, y=0, width=500, height=400)

Label(trademark_frame, text="©2004      Pokémon.\n©1995-2004 Nintendo\n©1995-2004 Creatures Inc.\n©1995-2004 GAME FREAK inc.",
      font=(GAME_FONT, 13, 'bold'), bg='black', fg='white', justify=LEFT).place(relx=0.5, rely=0.5, anchor=CENTER)


# ============================================================
# START THE PROGRAM

trademark_frame.tkraise()       
#show the copyright screen first
root.after(2500, displayMenu)   
#after 2.5 seconds (2500 milliseconds) go to the menu
root.mainloop()                 
#keep the window open and wait for clicks