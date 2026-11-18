from tkinter import *

root = Tk()
root.title("Alexa Joke Assistant")
root.geometry("700x400")
root.resizable(0, 0)
BG = '#234567' #using the same background
root['bg'] = BG

#FUNCTIONS
def loadJokes():
    # reads randomJokes.txt and returns a list of [setup, punchline] pairs
    joke_list = []
    with open("randomJokes.txt", "r", encoding="utf-8") as file_handler:
        lines = file_handler.readlines()
    for line in lines:
        line = line.strip().replace("- ", "", 1)   #drop a leading "- " if the file has one
        if "?" in line:                            #also skips blank lines
            parts = line.split("?", 1)             #split at the first ? only
            joke_list.append([parts[0] + "?", parts[1]])   #put the ? back on the setup
    return joke_list

#Loading Jokes
jokes = loadJokes()

#start screen
start_frame = Frame(root, bg=BG)
start_frame.place(x=0, y=0, width=700, height=400)
Label(start_frame, text="Joke Assistant", font=('Roboto', 28), bg=BG, fg='white').pack(pady=30)
Label(start_frame, text="Want to hear something funny?", font=('Roboto', 14), bg=BG, fg='yellow').pack(pady=10)

#Joke screen
joke_frame = Frame(root, bg=BG)
joke_frame.place(x=0, y=0, width=700, height=400)

setup_label = Label(joke_frame, text="Setup shows here?", font=('Roboto', 14), bg=BG, fg='white')
setup_label.pack(pady=40)
punchline_label = Label(joke_frame, text="Punchline shows here", font=('Roboto', 14), bg=BG, fg='yellow')
punchline_label.pack(pady=10)
Button(joke_frame, text="Show Punchline", width=20, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)
Button(joke_frame, text="Next Joke", width=20, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)
Button(joke_frame, text="Quit", width=20, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)

#adding joke generator buttons
Button(start_frame, text="Alexa tell me a Joke", width=25, font=('Roboto', 14),
       bg='#001111', fg='yellow').pack(pady=20)
Button(start_frame, text="Quit", width=25, font=('Roboto', 14),
       bg='#001111', fg='yellow').pack(pady=5)

#start_frame & joke_frame
joke_frame.tkraise()

#added temp test
print(len(jokes), jokes[0])
root.mainloop()