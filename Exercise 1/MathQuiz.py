# 01-MathsQuiz
from tkinter import *
from tkinter import messagebox #Play again/quit box
import random #RNG

# ============================================================
# SETTINGS

BACKGROUND_COLOUR = '#234567'
BUTTON_COLOUR = '#001111'
BUTTON_TEXT_COLOUR = 'yellow'

QUESTIONS_PER_QUIZ = 10
POINTS_FIRST_TRY = 10
POINTS_SECOND_TRY = 5
MAX_SCORE = 100


# ============================================================
# WINDOW SETUP

root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.resizable(0, 0)
root['bg'] = BACKGROUND_COLOUR


# ============================================================
# QUIZ INFO
# This is basically the game's data. It tracks where the player is right now.
# Since it's a dictionary, all my functions can look at it and update it as you play.

quiz = {
    "difficulty_level": 1,    
    # 1 = easy, 2 = moderate, 3 = advanced
    "question_number": 0,     
    # which question we are on (1 to 10)
    "attempt_number": 1,      
    # 1 = first try, 2 = second try
    "score": 0,               
    # points so far
    "correct_answer": 0,      
    # the right answer to the current problem
}


# ============================================================
# FUNCTIONS


# ---------- Menu ----------
def displayMenu():
    # bring the difficulty menu screen to the front
    menu_frame.tkraise()


# ---------- Making a question ----------
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
    feedback_label.config(text="")
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

    #works out the real answer and keep it for checking later
    if operation == '+':
        quiz["correct_answer"] = first_number + second_number
    else:
        quiz["correct_answer"] = first_number - second_number

    #update the screen
    question_number_label.config(text=f"Question {quiz['question_number']} of {QUESTIONS_PER_QUIZ}")
    score_label.config(text=f"Score: {quiz['score']}")
    problem_label.config(text=f"{first_number} {operation} {second_number} =")
    answer_entry.delete(0, END) #just to empty the typing box


# ---------- Checking answers ----------
def isCorrect(typed_answer, correct_answer, attempt_number):
    #checks the answer then shows a message, and returns True or False
    if typed_answer.strip() == str(correct_answer):
        feedback_label.config(text="Correct!", fg='lightgreen')
        return True
    elif attempt_number == 1:
        feedback_label.config(text="Wrong, try once more!", fg='orange')
        return False
    else:
        feedback_label.config(text=f"Wrong, the answer was {correct_answer}", fg='red')
        return False


def submitAnswer():
    #runs when Submit is clicked (or Enter is pressed)
    typed_answer = answer_entry.get()
    answered_correctly = isCorrect(typed_answer, quiz["correct_answer"], quiz["attempt_number"])

    if answered_correctly:
        #10 points for the first try, 5 for the second
        if quiz["attempt_number"] == 1:
            quiz["score"] += POINTS_FIRST_TRY
        else:
            quiz["score"] += POINTS_SECOND_TRY
        nextQuestion()
    else:
        if quiz["attempt_number"] == 1:
            quiz["attempt_number"] = 2     
            #gives one more chance
            answer_entry.delete(0, END)
        else:
            nextQuestion()                 
            #if both attempts are used used then moves onto the next question


def nextQuestion():
    #if it didn't show the results after question 10, then it'll show another problem
    if quiz["question_number"] == QUESTIONS_PER_QUIZ:
        displayResults()
    else:
        displayProblem()


# ---------- Ending the quiz ----------
def displayResults():
    #shows the final score and the rank
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
# MENU SCREEN

menu_frame = Frame(root, bg=BACKGROUND_COLOUR)
menu_frame.place(x=0, y=0, width=500, height=400)

Label(menu_frame, text="Maths Quiz", font=('Roboto', 28),
      bg=BACKGROUND_COLOUR, fg='white').pack(pady=20)
Label(menu_frame, text="DIFFICULTY LEVEL", font=('Roboto', 16),
      bg=BACKGROUND_COLOUR, fg='yellow').pack(pady=10)

#lambda lets each button pass its own level number to startQuiz
easy_button = Button(menu_frame, text="1. Easy (1 digit)", width=22, font=('Roboto', 12),
                     bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=lambda: startQuiz(1))
easy_button.pack(pady=8)

moderate_button = Button(menu_frame, text="2. Moderate (2 digits)", width=22, font=('Roboto', 12),
                         bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=lambda: startQuiz(2))
moderate_button.pack(pady=8)

advanced_button = Button(menu_frame, text="3. Advanced (4 digits)", width=22, font=('Roboto', 12),
                         bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=lambda: startQuiz(3))
advanced_button.pack(pady=8)


# ============================================================
# QUIZ SCREEN

quiz_frame = Frame(root, bg=BACKGROUND_COLOUR)
quiz_frame.place(x=0, y=0, width=500, height=400)

# these widgets get names because the functions change them while the quiz runs
question_number_label = Label(quiz_frame, text="Question 1 of 10", font=('Roboto', 14),
                              bg=BACKGROUND_COLOUR, fg='white')
question_number_label.pack(pady=10)

score_label = Label(quiz_frame, text="Score: 0", font=('Roboto', 12),
                    bg=BACKGROUND_COLOUR, fg='yellow')
score_label.pack()

problem_label = Label(quiz_frame, text="", font=('Roboto', 30),
                      bg=BACKGROUND_COLOUR, fg='white')
problem_label.pack(pady=20)

answer_entry = Entry(quiz_frame, font=('Roboto', 18), width=10)
answer_entry.pack(pady=5)
answer_entry.bind("<Return>", lambda event: submitAnswer())   # Enter key works like Submit

submit_button = Button(quiz_frame, text="Submit", width=15, font=('Roboto', 12),
                       bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=submitAnswer)
submit_button.pack(pady=15)

feedback_label = Label(quiz_frame, text="", font=('Roboto', 14),
                       bg=BACKGROUND_COLOUR, fg='white')
feedback_label.pack()


# ============================================================
# RESULTS SCREEN

results_frame = Frame(root, bg=BACKGROUND_COLOUR)
results_frame.place(x=0, y=0, width=500, height=400)

Label(results_frame, text="Quiz Finished!", font=('Roboto', 28),
      bg=BACKGROUND_COLOUR, fg='white').pack(pady=20)

final_score_label = Label(results_frame, text="", font=('Roboto', 18),
                          bg=BACKGROUND_COLOUR, fg='yellow')
final_score_label.pack(pady=10)

rank_label = Label(results_frame, text="", font=('Roboto', 18),
                   bg=BACKGROUND_COLOUR, fg='white')
rank_label.pack(pady=10)

play_again_button = Button(results_frame, text="Play Again", width=15, font=('Roboto', 12),
                           bg=BUTTON_COLOUR, fg=BUTTON_TEXT_COLOUR, command=playAgain)
play_again_button.pack(pady=20)


# ============================================================
# STARTS THE PROGRAM

displayMenu()        
# show the menu first
root.mainloop()      
# keep the window open and wait for clicks