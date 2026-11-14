from tkinter import *

#setting up
root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.resizable(0, 0)
BG = '#234567'
root['bg'] = BG

#menu screen(framing then gonna switch screens later)
menu_frame = Frame(root, bg=BG)
menu_frame.place(x=0, y=0, width=500, height=400)

Label(menu_frame, text="Maths Quiz", font=('Roboto', 28), bg=BG, fg='white').pack(pady=20)
Label(menu_frame, text="DIFFICULTY LEVEL", font=('Roboto', 16), bg=BG, fg='yellow').pack(pady=10)

root.mainloop()