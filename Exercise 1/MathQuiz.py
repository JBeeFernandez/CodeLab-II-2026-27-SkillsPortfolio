from tkinter import *
import random #random number generator (from the resources folder)

root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.resizable(0, 0)
BG = '#234567'
root['bg'] = BG

#GAME INFOS
game = {"level": 1, "question": 0, "attempt": 1, "score": 0,
        "num1": 0, "num2": 0, "op": "+", "answer": 0}

#FUNCTIONS
def displayMenu():
    #brings the specific screen to the front
    #Replace with: quiz_frame.tkraise() or results_frame.tkraise() to preview it
    menu_frame.tkraise()

def randomInt(level):
    #min and max depend on the difficulty level
    if level == 1:
        return random.randint(0, 9)         #easy: single digit
    elif level == 2:
        return random.randint(10, 99)       #moderate: double digit
    else:
        return random.randint(1000, 9999)   #advanced: 4 digits

def decideOperation():
    #randomly picks addition or subtraction and returns the character
    if random.randint(1, 2) == 1:
        return '+'
    else:
        return '-'

#QUIZ SCREEN
quiz_frame = Frame(root, bg=BG)
quiz_frame.place(x=0, y=0, width=500, height=400)

question_label = Label(quiz_frame, text="Question 1 of 10", font=('Roboto', 14), bg=BG, fg='white')
question_label.pack(pady=10)
score_label = Label(quiz_frame, text="Score: 0", font=('Roboto', 12), bg=BG, fg='yellow')
score_label.pack()
problem_label = Label(quiz_frame, text="45 + 9 =", font=('Roboto', 30), bg=BG, fg='white')
problem_label.pack(pady=20)
answer_entry = Entry(quiz_frame, font=('Roboto', 18), width=10)
answer_entry.pack(pady=5)
submit_button = Button(quiz_frame, text="Submit", width=15, font=('Roboto', 12),
                       bg='#001111', fg='yellow')
submit_button.pack(pady=15)
feedback_label = Label(quiz_frame, text="", font=('Roboto', 14), bg=BG, fg='white')
feedback_label.pack()

#RESULTS SCREEN
results_frame = Frame(root, bg=BG)
results_frame.place(x=0, y=0, width=500, height=400)

Label(results_frame, text="Quiz Finished!", font=('Roboto', 28), bg=BG, fg='white').pack(pady=20)
result_label = Label(results_frame, text="Your score: 0 / 100", font=('Roboto', 18), bg=BG, fg='yellow')
result_label.pack(pady=10)
rank_label = Label(results_frame, text="Rank: -", font=('Roboto', 18), bg=BG, fg='white')
rank_label.pack(pady=10)
play_button = Button(results_frame, text="Play Again", width=15, font=('Roboto', 12),
                     bg='#001111', fg='yellow')
play_button.pack(pady=20)


menu_frame = Frame(root, bg=BG)
menu_frame.place(x=0, y=0, width=500, height=400)

Label(menu_frame, text="Maths Quiz", font=('Roboto', 28), bg=BG, fg='white').pack(pady=20)
Label(menu_frame, text="DIFFICULTY LEVEL", font=('Roboto', 16), bg=BG, fg='yellow').pack(pady=10)

#BUTTONS
Button(menu_frame, text="1. Easy (1 digit)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)
Button(menu_frame, text="2. Moderate (2 digits)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)
Button(menu_frame, text="3. Advanced (4 digits)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)

#calling the display menu for it to appear first
displayMenu()

#quick test
print(randomInt(1), randomInt(2), randomInt(3), decideOperation())

root.mainloop()