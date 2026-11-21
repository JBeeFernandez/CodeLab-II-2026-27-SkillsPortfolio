# Exercise 2 - Alexa Joke Assistant (Brock Theme)
from tkinter import *
from tkinter import messagebox #For the quit box
from PIL import ImageTk, Image #For Brock's picture
import random #RNG
import os #To find the files that sit next to this file

#WINDOW SETUP
root = Tk()
root.title("Alexa Joke Assistant")
root.geometry("700x400")
root.resizable(0, 0)
BG = '#C49A6C'
root['bg'] = BG

#COLOURS AND FONT (Brock theme)
BORDER_COLOUR = '#5A3E28' #dark brown outline
BOX_COLOUR = '#F8F0D8' #cream
TEXT_COLOUR = '#4A3420' #dark brown text
PUNCHLINE_COLOUR = '#B05010' #rusty orange so the punchline stands out
ORANGE_BUTTON = '#E08830' #Brock's orange shirt
GREEN_BUTTON = '#58A038' #Brock's green vest
BROWN_BUTTON = '#8B5E3C'
GAME_FONT = 'Courier New'
FOLDER = os.path.dirname(__file__) #the folder this file is in, so the files are found from anywhere

#JOKE INFO
current = {"last": -1, "punchline": ""}

#BROCK'S PICTURE
brock_picture = Image.open(f"{FOLDER}/JokeAssistant/brock.png").convert("RGBA")
width, height = brock_picture.size
scale = min(176 / width, 270 / height) #as big as it can get without leaving the box
brock_picture = brock_picture.resize((int(width * scale), int(height * scale)))
brock_image = ImageTk.PhotoImage(brock_picture) #kept in a variable so Tkinter does not lose it

#FUNCTIONS
#This reads randomJokes.txt, then cleans each line, splits it at the first "?" and returns a list of [setup, punchline] pairs. I tested it by printing the list.
def loadJokes():
    joke_list = []
    with open(f"{FOLDER}/randomJokes.txt", "r", encoding="utf-8") as file_handler:
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
    answer = messagebox.askyesno("Leaving already?", "Brock says: come back for more rock solid jokes!\nDo you want to close the app?")
    if answer:
        root.destroy()

#This makes a box with a dark outline (a dark frame with a lighter frame inside it) and gives back the inside one.
def makeBox(parent, x, y, width, height, fill_colour):
    outline = Frame(parent, bg=BORDER_COLOUR)
    outline.place(x=x, y=y, width=width, height=height)
    inside = Frame(outline, bg=fill_colour)
    inside.place(x=4, y=4, width=width - 8, height=height - 8)
    return inside

#This puts Brock's picture and name on the left side of a screen (both screens use it).
def makeBrockBox(parent):
    box = makeBox(parent, 20, 20, 200, 360, BOX_COLOUR)
    Label(box, image=brock_image, bg=BOX_COLOUR).place(relx=0.5, y=150, anchor=CENTER)
    Label(box, text="BROCK", font=(GAME_FONT, 18, 'bold'), bg=BOX_COLOUR, fg=TEXT_COLOUR).place(relx=0.5, y=300, anchor=N)
    Label(box, text="Pewter City Gym Leader", font=(GAME_FONT, 8, 'bold'), bg=BOX_COLOUR, fg=TEXT_COLOUR).place(relx=0.5, y=330, anchor=N)

#LOADING THE JOKES
jokes = loadJokes()

#START SCREEN
start_frame = Frame(root, bg=BG)
start_frame.place(x=0, y=0, width=700, height=400)
makeBrockBox(start_frame)

title_box = makeBox(start_frame, 240, 20, 440, 80, BOX_COLOUR)
Label(title_box, text="BROCK'S JOKE GYM", font=(GAME_FONT, 22, 'bold'), bg=BOX_COLOUR,
      fg=TEXT_COLOUR).place(relx=0.5, rely=0.5, anchor=CENTER)

hello_box = makeBox(start_frame, 240, 115, 440, 160, BOX_COLOUR)
Label(hello_box, text="Hi! I'm Brock, the Pewter City Gym Leader!\n\nMy jokes are rock solid. Want to hear one?",
      font=(GAME_FONT, 14, 'bold'), bg=BOX_COLOUR, fg=TEXT_COLOUR, wraplength=400, justify=LEFT).place(x=14, y=14)

Button(start_frame, text="Brock, tell me a Joke", font=(GAME_FONT, 16, 'bold'), bg=ORANGE_BUTTON,
       fg='white', command=tellJoke).place(x=240, y=295, width=440, height=45)
Button(start_frame, text="Quit", font=(GAME_FONT, 12, 'bold'), bg=BROWN_BUTTON,
       fg='white', command=quitApp).place(x=240, y=350, width=440, height=30)

#JOKE SCREEN
joke_frame = Frame(root, bg=BG)
joke_frame.place(x=0, y=0, width=700, height=400)
makeBrockBox(joke_frame)

#wraplength makes long jokes go onto a new line instead of running off the box
joke_box = makeBox(joke_frame, 240, 20, 440, 260, BOX_COLOUR)
setup_label = Label(joke_box, text="", font=(GAME_FONT, 16, 'bold'), bg=BOX_COLOUR, fg=TEXT_COLOUR,
                    wraplength=400, justify=LEFT)
setup_label.place(x=14, y=14)
punchline_label = Label(joke_box, text="", font=(GAME_FONT, 16, 'bold'), bg=BOX_COLOUR, fg=PUNCHLINE_COLOUR,
                        wraplength=400, justify=LEFT)
punchline_label.place(x=14, y=130)

Button(joke_frame, text="Show Punchline", font=(GAME_FONT, 11, 'bold'), bg=GREEN_BUTTON,
       fg='white', command=showPunchline).place(x=240, y=300, width=140, height=80)
Button(joke_frame, text="Next Joke", font=(GAME_FONT, 11, 'bold'), bg=ORANGE_BUTTON,
       fg='white', command=tellJoke).place(x=390, y=300, width=140, height=80)
Button(joke_frame, text="Quit", font=(GAME_FONT, 11, 'bold'), bg=BROWN_BUTTON,
       fg='white', command=quitApp).place(x=540, y=300, width=140, height=80)

start_frame.tkraise()
root.mainloop()