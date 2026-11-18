from tkinter import *
from tkinter import messagebox #For the quit box
import random #RNG

#WINDOW SETUP
root = Tk()
root.title("Alexa Joke Assistant")
root.geometry("700x400")
root.resizable(0, 0)
BG = '#234567'
root['bg'] = BG

#JOKE INFO
current = {"last": -1, "punchline": ""}

#FUNCTIONS
#This reads randomJokes.txt, then cleans each line, splits it at the first "?" and returns a list of [setup, punchline] pairs. I tested it by printing the list.
def loadJokes():
    joke_list = []
    with open("randomJokes.txt", "r", encoding="utf-8") as file_handler:
        lines = file_handler.readlines()
    for line in lines:
        line = line.strip().replace("- ", "", 1)
        if "?" in line:
            parts = line.split("?", 1)
            joke_list.append([parts[0] + "?", parts[1]])
    return joke_list

def pickJoke():
    number = random.randint(0, len(jokes) - 1)
    #the while loop re-picks a random number so the same joke never appears twice in a row.
    while number == current["last"] and len(jokes) > 1:
        number = random.randint(0, len(jokes) - 1)
    current["last"] = number
    return number

#it shows the setup, keeps the punchline in the current dictionary until "Show Punchline" is pressed, then switches to the joke screen.
def tellJoke():
    number = pickJoke()
    setup_label.config(text=jokes[number][0])
    punchline_label.config(text="")
    current["punchline"] = jokes[number][1]
    joke_frame.tkraise()

def showPunchline():
    punchline_label.config(text=current["punchline"])

def quitApp():
    answer = messagebox.askyesno("Quit", "Do you want to close the app?")
    if answer:
        root.destroy()

#LOADING THE JOKES
jokes = loadJokes()

#START SCREEN
start_frame = Frame(root, bg=BG)
start_frame.place(x=0, y=0, width=700, height=400)
Label(start_frame, text="Joke Assistant", font=('Roboto', 28), bg=BG, fg='white').pack(pady=30)
Label(start_frame, text="Want to hear something funny?", font=('Roboto', 14), bg=BG, fg='yellow').pack(pady=10)
Button(start_frame, text="Alexa tell me a Joke", width=25, font=('Roboto', 14),
       bg='#001111', fg='yellow', command=tellJoke).pack(pady=20)
Button(start_frame, text="Quit", width=25, font=('Roboto', 14),
       bg='#001111', fg='yellow', command=quitApp).pack(pady=5)

#JOKE SCREEN
joke_frame = Frame(root, bg=BG)
joke_frame.place(x=0, y=0, width=700, height=400)
setup_label = Label(joke_frame, text="", font=('Roboto', 14), bg=BG, fg='white')
setup_label.pack(pady=40)
punchline_label = Label(joke_frame, text="", font=('Roboto', 14), bg=BG, fg='yellow')
punchline_label.pack(pady=10)
Button(joke_frame, text="Show Punchline", width=20, font=('Roboto', 12),
       bg='#001111', fg='yellow', command=showPunchline).pack(pady=8)
Button(joke_frame, text="Next Joke", width=20, font=('Roboto', 12),
       bg='#001111', fg='yellow', command=tellJoke).pack(pady=8)
Button(joke_frame, text="Quit", width=20, font=('Roboto', 12),
       bg='#001111', fg='yellow', command=quitApp).pack(pady=8)

start_frame.tkraise()
root.mainloop()