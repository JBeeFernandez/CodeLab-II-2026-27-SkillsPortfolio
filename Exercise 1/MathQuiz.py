from tkinter import *

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

#adding buttons for each difficulty
Button(menu_frame, text="1. Easy (1 digit)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)
Button(menu_frame, text="2. Moderate (2 digits)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)
Button(menu_frame, text="3. Advanced (4 digits)", width=22, font=('Roboto', 12),
       bg='#001111', fg='yellow').pack(pady=8)

root.mainloop()