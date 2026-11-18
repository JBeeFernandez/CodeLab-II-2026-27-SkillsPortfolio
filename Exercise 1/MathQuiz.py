from tkinter import *
from tkinter import messagebox
import random #RNG

#===============
#WINDOW SETUP

root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.resizable(0, 0)
BG = '#234567'
root['bg'] = BG

#===============
#GAME INFO (a dictionary so functions can change it)

game = {"level": 1, "question": 0, "attempt": 1, "score": 0,
        "num1": 0, "num2": 0, "op": "+", "answer": 0}

#===============
#FUNCTIONS

def displayMenu():
    menu_frame.tkraise()

def randomInt(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)

def decideOperation():
    if random.randint(1, 2) == 1:
        return '+'
    else:
        return '-'

def startQuiz(level):
    game["level"] = level
    game["score"] = 0
    game["question"] = 0
    feedback_label.config(text="")
    quiz_frame.tkraise()
    displayProblem()

#AI reference: Claude | fixed structure and error fixed of this function (working out the answer, then updating the labels) was supported on how to do
def displayProblem():
    game["question"] += 1
    game["attempt"] = 1
    game["num1"] = randomInt(game["level"])
    game["num2"] = randomInt(game["level"])
    game["op"] = decideOperation()
    if game["op"] == '+':
        game["answer"] = game["num1"] + game["num2"]
    else:
        game["answer"] = game["num1"] - game["num2"]
    question_label.config(text=f"Question {game['question']} of 10")
    score_label.config(text=f"Score: {game['score']}")
    problem_label.config(text=f"{game['num1']} {game['op']} {game['num2']} =")
    answer_entry.delete(0, END)

def isCorrect(user_text, correct, attempt):
    if user_text.strip() == str(correct):
        feedback_label.config(text="Correct!", fg='lightgreen')
        return True
    elif attempt == 1:
        feedback_label.config(text="Wrong, try once more!", fg='orange')
        return False
    else:
        feedback_label.config(text=f"Wrong, the answer was {correct}", fg='red')
        return False


# AI reference: Claude | the 10/5 point scoring and the second attempt logic had a bit of help for this fixing errors
def submitAnswer():
    user_text = answer_entry.get()
    if isCorrect(user_text, game["answer"], game["attempt"]):
        if game["attempt"] == 1:
            game["score"] += 10
        else:
            game["score"] += 5
        nextQuestion()
    else:
        if game["attempt"] == 1:
            game["attempt"] = 2
            answer_entry.delete(0, END)
        else:
            nextQuestion()

def nextQuestion():
    if game["question"] == 10:
        displayResults()
    else:
        displayProblem()

def displayResults():
    score = game["score"]
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
    result_label.config(text=f"Your score: {score} / 100")
    rank_label.config(text=f"Rank: {rank}")
    results_frame.tkraise()

def playAgain():
    answer = messagebox.askyesno("Play again?", "Would you like to play again?")
    if answer:
        displayMenu()
    else:
        rank_label.config(text="Thanks for playing!")

#===============
#MENU SCREEN

menu_frame = Frame(root, bg=BG)
menu_frame.place(x=0, y=0, width=500, height=400)
Label(menu_frame, text="Maths Quiz", font=('Roboto', 28), bg=BG, fg='white').pack(pady=20)
Label(menu_frame, text="DIFFICULTY LEVEL", font=('Roboto', 16), bg=BG, fg='yellow').pack(pady=10)
Button(menu_frame, text="1. Easy (1 digit)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow', command=lambda: startQuiz(1)).pack(pady=8)
Button(menu_frame, text="2. Moderate (2 digits)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow', command=lambda: startQuiz(2)).pack(pady=8)
Button(menu_frame, text="3. Advanced (4 digits)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow', command=lambda: startQuiz(3)).pack(pady=8)

#===============
#QUIZ SCREEN

quiz_frame = Frame(root, bg=BG)
quiz_frame.place(x=0, y=0, width=500, height=400)
question_label = Label(quiz_frame, text="Question 1 of 10", font=('Roboto', 14), bg=BG, fg='white')
question_label.pack(pady=10)
score_label = Label(quiz_frame, text="Score: 0", font=('Roboto', 12), bg=BG, fg='yellow')
score_label.pack()
problem_label = Label(quiz_frame, text="", font=('Roboto', 30), bg=BG, fg='white')
problem_label.pack(pady=20)
answer_entry = Entry(quiz_frame, font=('Roboto', 18), width=10)
answer_entry.pack(pady=5)
answer_entry.bind("<Return>", lambda event: submitAnswer())
submit_button = Button(quiz_frame, text="Submit", width=15, font=('Roboto', 12),
                       bg='#001111', fg='yellow', command=submitAnswer)
submit_button.pack(pady=15)
feedback_label = Label(quiz_frame, text="", font=('Roboto', 14), bg=BG, fg='white')
feedback_label.pack()

#===============
#RESULTS SCREEN

results_frame = Frame(root, bg=BG)
results_frame.place(x=0, y=0, width=500, height=400)
Label(results_frame, text="Quiz Finished!", font=('Roboto', 28), bg=BG, fg='white').pack(pady=20)
result_label = Label(results_frame, text="", font=('Roboto', 18), bg=BG, fg='yellow')
result_label.pack(pady=10)
rank_label = Label(results_frame, text="", font=('Roboto', 18), bg=BG, fg='white')
rank_label.pack(pady=10)
play_button = Button(results_frame, text="Play Again", width=15, font=('Roboto', 12),
                     bg='#001111', fg='yellow', command=playAgain)
play_button.pack(pady=20)

displayMenu()#shows the menu first
root.mainloop()