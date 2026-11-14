from tkinter import *

root = Tk()
root.title("Alexa Joke Assistant")
root.geometry("700x400")
root.resizable(0, 0)
BG = '#234567' #gonna use the same background
root['bg'] = BG

#start screen
start_frame = Frame(root, bg=BG)
start_frame.place(x=0, y=0, width=700, height=400)
Label(start_frame, text="Joke Assistant", font=('Roboto', 28), bg=BG, fg='white').pack(pady=30)
Label(start_frame, text="Want to hear something funny?", font=('Roboto', 14), bg=BG, fg='yellow').pack(pady=10)

#adding joke generator buttons
Button(start_frame, text="Alexa tell me a Joke", width=25, font=('Roboto', 14),
       bg='#001111', fg='yellow').pack(pady=20)
Button(start_frame, text="Quit", width=25, font=('Roboto', 14),
       bg='#001111', fg='yellow').pack(pady=5)

root.mainloop()