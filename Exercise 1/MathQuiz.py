# Exercise 1 - Maths Quiz

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import os       # used only to find the Resources folder
import pygame   # used only to play the music and sounds

# ---------- SETTINGS (things we use many times, so they are saved in variables) ----------
RESOURCES_FOLDER = os.path.join(os.path.dirname(__file__), "Resources")   # the Resources folder sits next to this file
GAME_FONT = "Courier New"   # change this one word to use a different font

PANEL_COLOUR = "#989898"
BORDER_COLOUR = "#505058"
BOX_COLOUR = "#E0E0E0"
WHITE_COLOUR = "#F8F8F8"
TEXT_COLOUR = "#484850"
HP_TAG_COLOUR = "#F8B000"
PINK_BUTTON = "#F8A8B0"
GREEN_BUTTON = "#58A038"
GOLD_BUTTON = "#D89830"
BLUE_BUTTON = "#3088C0"

QUESTIONS_PER_QUIZ = 10
MAX_HEALTH = 100
HP_BAR_WIDTH = 130   # how wide a full HP bar is (in pixels)
LEVEL_NAMES = ["Easy", "Moderate", "Advanced"]

# ---------- WINDOW SETUP ----------
root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.resizable(0, 0)
root.config(bg=PANEL_COLOUR)

# ---------- PICTURES AND SOUNDS ----------
def loadImage(file_name, width, height):
    # opens a picture from the Resources folder and resizes it
    picture = Image.open(f"{RESOURCES_FOLDER}/{file_name}").convert("RGBA").resize((width, height))
    return ImageTk.PhotoImage(picture)

# each picture is kept in a variable so Tkinter does not lose it
backgrounds = [loadImage("grass_bg.png", 500, 280), loadImage("rock_mountain_bg.png", 500, 280),
               loadImage("water_bg.png", 500, 280)]
oak_image = loadImage("oak.png", 120, 120)   # the enemy
red_image = loadImage("red.png", 128, 128)   # the player 

pygame.mixer.init()
hit_sound = pygame.mixer.Sound(f"{RESOURCES_FOLDER}/Hit.mp3")     # super effective (right on the first try)
hit2_sound = pygame.mixer.Sound(f"{RESOURCES_FOLDER}/Hit2.mp3")   # not very effective (right on the second try)

def playMusic(file_name):
    # plays a song on repeat (it replaces the song that is playing now)
    pygame.mixer.music.load(f"{RESOURCES_FOLDER}/{file_name}")
    pygame.mixer.music.play(-1)

# ---------- QUIZ INFO ----------
# The game's data is kept in this dictionary, so every function can read and change it.
quiz = {
    "level": 1,           # 1 = easy, 2 = moderate, 3 = advanced
    "question_number": 0, # which question we are on (1 to 10)
    "attempt": 1,         # 1 = first try, 2 = second try
    "score": 0,           # points so far (the enemy loses the same amount of health)
    "health": MAX_HEALTH, # the player's health, goes down 10 for every wrong answer
    "answer": 0           # the right answer to the current problem
}

# ---------- FUNCTIONS FOR BUILDING THE SCREENS ----------
def makeBox(parent, x, y, width, height, fill_colour):
    # a box with an outline: a dark frame with a lighter frame inside it
    outline = Frame(parent, bg=BORDER_COLOUR)
    outline.place(x=x, y=y, width=width, height=height)
    inside = Frame(outline, bg=fill_colour)
    inside.place(x=4, y=4, width=width - 8, height=height - 8)
    return inside

def makeScene(parent):
    # builds the battle scene: Oak on the enemy side, Red on the player side
    scene = Canvas(parent, width=500, height=280, highlightthickness=0)
    scene.place(x=0, y=0)
    background = scene.create_image(0, 0, anchor="nw", image=backgrounds[0])
    scene.create_image(310, 46, anchor="nw", image=oak_image)
    scene.create_image(31, 142, anchor="nw", image=red_image)
    return scene, background

def makeBattleBox(x, y, name):
    # builds one name box with a green HP bar. Gives back the name label and the HP bar
    box = makeBox(quiz_frame, x, y, 230, 62, BOX_COLOUR)
    name_label = Label(box, text=name, font=(GAME_FONT, 12, "bold"), bg=BOX_COLOUR, fg=TEXT_COLOUR)
    name_label.place(x=8, y=4)

    Frame(box, bg=BORDER_COLOUR).place(x=50, y=28, width=164, height=18)   # dark holder for the bar
    Label(box, text="HP", font=(GAME_FONT, 9, "bold"), bg=BORDER_COLOUR, fg=HP_TAG_COLOUR).place(x=54, y=29)
    hp_bar = Frame(box, bg="#18C020")                                      # the bar that shrinks
    hp_bar.place(x=80, y=32, width=HP_BAR_WIDTH, height=10)
    return name_label, hp_bar

def setHealthBar(bar, health):
    # makes the bar as wide as the health left, and changes its colour
    bar.place(width=int(HP_BAR_WIDTH * health / MAX_HEALTH))
    if health < 50:
        bar.config(bg="#E83030")   # red
    elif health < 70:
        bar.config(bg="#F8D030")   # yellow
    else:
        bar.config(bg="#18C020")   # green

def updateHealthBars():
    # the enemy loses the same amount of health as the points scored
    setHealthBar(enemy_bar, MAX_HEALTH - quiz["score"])
    setHealthBar(player_bar, quiz["health"])

# ---------- FUNCTIONS FOR THE QUIZ ----------
def displayMenu():
    # shows the menu screen, with its own music
    playMusic("menutrack.mp3")
    menu_frame.tkraise()

def startQuiz(level):
    # runs when a difficulty button is clicked: reset everything and begin
    quiz["level"] = level
    quiz["score"] = 0
    quiz["question_number"] = 0
    quiz["health"] = MAX_HEALTH
    feedback_label.config(text="")

    # lists start at 0, so we use level - 1
    quiz_scene.itemconfig(quiz_background, image=backgrounds[level - 1])
    enemy_name_label.config(text=f"{LEVEL_NAMES[level - 1]} Quiz")
    updateHealthBars()
    playMusic("soundtrack.mp3")
    quiz_frame.tkraise()
    displayProblem()

def displayProblem():
    # moves to the next question and shows it on the screen
    quiz["question_number"] += 1
    quiz["attempt"] = 1

    # the numbers have 1 digit (easy), 2 digits (moderate) or 4 digits (advanced)
    if quiz["level"] == 1:
        first_number = random.randint(0, 9)
        second_number = random.randint(0, 9)
    elif quiz["level"] == 2:
        first_number = random.randint(10, 99)
        second_number = random.randint(10, 99)
    else:
        first_number = random.randint(1000, 9999)
        second_number = random.randint(1000, 9999)

    # pick + or - and work out the real answer
    if random.randint(1, 2) == 1:
        operation = "+"
        quiz["answer"] = first_number + second_number
    else:
        operation = "-"
        quiz["answer"] = first_number - second_number

    status_label.config(text=f"Question {quiz['question_number']} of {QUESTIONS_PER_QUIZ}\nScore: {quiz['score']}")
    problem_label.config(text=f"{first_number} {operation} {second_number} =")
    answer_entry.delete(0, END)   # empty the typing box

def submitAnswer():
    # runs when Submit is clicked (or Enter is pressed)
    if answer_entry.get().strip() == str(quiz["answer"]):
        # right answer: 10 points on the first try, 5 points on the second
        if quiz["attempt"] == 1:
            quiz["score"] += 10
            hit_sound.play()
            feedback_label.config(text="It's super effective!", fg="darkgreen")
        else:
            quiz["score"] += 5
            hit2_sound.play()
            feedback_label.config(text="It's not very effective...", fg="darkorange")
        updateHealthBars()
        nextQuestion()
    else:
        # wrong answer: the player loses 10 health, even on the second try
        quiz["health"] -= 10
        updateHealthBars()
        if quiz["health"] <= 0:
            messagebox.showinfo("Whited out!", "Player is out of health!\nPlayer whited out!")
            displayMenu()
        elif quiz["attempt"] == 1:
            quiz["attempt"] = 2   # give one more chance
            feedback_label.config(text="It missed! Try once more!", fg="darkorange")
            answer_entry.delete(0, END)
        else:
            feedback_label.config(text=f"It missed! The answer was {quiz['answer']}", fg="red")
            nextQuestion()

def nextQuestion():
    # after question 10 show the results, otherwise show another problem
    if quiz["question_number"] == QUESTIONS_PER_QUIZ:
        displayResults()
    else:
        displayProblem()

def displayResults():
    # shows the final score and the rank (the music stops here)
    pygame.mixer.music.stop()
    score = quiz["score"]

    if score > 90:
        rank = "A+"
    elif score >= 80:
        rank = "A"
    elif score >= 70:
        rank = "B"
    elif score >= 60:
        rank = "C"
    elif score >= 50:
        rank = "D"
    else:
        rank = "F"

    final_score_label.config(text=f"Your score: {score} / 100")
    rank_label.config(text=f"Rank: {rank}")
    results_frame.tkraise()

# ---------- MENU SCREEN ----------
menu_frame = Frame(root, bg=PANEL_COLOUR)
menu_frame.place(x=0, y=0, width=500, height=400)
makeScene(menu_frame)   # the same battle scene as the quiz screen

title_box = makeBox(menu_frame, 10, 20, 230, 62, BOX_COLOUR)
Label(title_box, text="MATHS QUIZ", font=(GAME_FONT, 18, "bold"), bg=BOX_COLOUR,
      fg=TEXT_COLOUR).place(relx=0.5, rely=0.5, anchor=CENTER)

difficulty_box = makeBox(menu_frame, 10, 288, 320, 102, WHITE_COLOUR)
Label(difficulty_box, text="DIFFICULTY LEVEL\nEasy: 1 digit\nModerate: 2 digits\nAdvanced: 4 digits",
      font=(GAME_FONT, 11, "bold"), bg=WHITE_COLOUR, fg=TEXT_COLOUR, justify=LEFT).place(x=12, y=6)

# lambda lets each button send its own level number to startQuiz
Button(menu_frame, text="1. EASY", font=(GAME_FONT, 12, "bold"), bg=GREEN_BUTTON, fg="white",
       command=lambda: startQuiz(1)).place(x=340, y=288, width=150, height=30)
Button(menu_frame, text="2. MODERATE", font=(GAME_FONT, 12, "bold"), bg=GOLD_BUTTON, fg="white",
       command=lambda: startQuiz(2)).place(x=340, y=322, width=150, height=30)
Button(menu_frame, text="3. ADVANCED", font=(GAME_FONT, 12, "bold"), bg=BLUE_BUTTON, fg="white",
       command=lambda: startQuiz(3)).place(x=340, y=356, width=150, height=30)

# ---------- QUIZ SCREEN ----------
quiz_frame = Frame(root, bg=PANEL_COLOUR)
quiz_frame.place(x=0, y=0, width=500, height=400)
quiz_scene, quiz_background = makeScene(quiz_frame)

# question number and score (top right)
status_box = makeBox(quiz_frame, 340, 8, 150, 44, WHITE_COLOUR)
status_label = Label(status_box, text="", font=(GAME_FONT, 9, "bold"), bg=WHITE_COLOUR, fg=TEXT_COLOUR, justify=LEFT)
status_label.place(x=6, y=1)

# enemy box (top left) and player box (lower right)
enemy_name_label, enemy_bar = makeBattleBox(10, 20, "Easy Quiz")
player_name_label, player_bar = makeBattleBox(265, 200, "Player")

# question box (bottom left): the problem, with the message under it
question_box = makeBox(quiz_frame, 10, 288, 320, 102, WHITE_COLOUR)
problem_label = Label(question_box, text="", font=(GAME_FONT, 20, "bold"), bg=WHITE_COLOUR, fg=TEXT_COLOUR)
problem_label.place(x=12, y=8)
feedback_label = Label(question_box, text="", font=(GAME_FONT, 11, "bold"), bg=WHITE_COLOUR, fg=TEXT_COLOUR)
feedback_label.place(x=12, y=56)

# answer box and submit button (bottom right)
answer_box = makeBox(quiz_frame, 340, 288, 150, 46, WHITE_COLOUR)
answer_entry = Entry(answer_box, font=(GAME_FONT, 16, "bold"), width=9)
answer_entry.place(x=6, y=5)
answer_entry.bind("<Return>", lambda event: submitAnswer())   # the Enter key works like Submit
Button(quiz_frame, text="SUBMIT", font=(GAME_FONT, 12, "bold"), bg=PINK_BUTTON, fg=TEXT_COLOUR,
       command=submitAnswer).place(x=340, y=342, width=150, height=48)

# ---------- RESULTS SCREEN ----------
results_frame = Frame(root, bg=PANEL_COLOUR)
results_frame.place(x=0, y=0, width=500, height=400)
makeScene(results_frame)   # the same battle scene again

finished_box = makeBox(results_frame, 10, 20, 230, 62, BOX_COLOUR)
Label(finished_box, text="QUIZ FINISHED!", font=(GAME_FONT, 16, "bold"), bg=BOX_COLOUR,
      fg=TEXT_COLOUR).place(relx=0.5, rely=0.5, anchor=CENTER)

score_box = makeBox(results_frame, 10, 288, 320, 102, WHITE_COLOUR)
final_score_label = Label(score_box, text="", font=(GAME_FONT, 16, "bold"), bg=WHITE_COLOUR, fg=TEXT_COLOUR)
final_score_label.place(x=12, y=12)
rank_label = Label(score_box, text="", font=(GAME_FONT, 16, "bold"), bg=WHITE_COLOUR, fg=TEXT_COLOUR)
rank_label.place(x=12, y=52)
Button(results_frame, text="PLAY AGAIN", font=(GAME_FONT, 12, "bold"), bg=PINK_BUTTON, fg=TEXT_COLOUR,
       command=displayMenu).place(x=340, y=288, width=150, height=102)

# ---------- START THE PROGRAM ----------
displayMenu()
root.mainloop()