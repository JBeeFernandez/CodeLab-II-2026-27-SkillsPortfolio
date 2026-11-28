# Exercise 1 - Math Quiz 

# Imports
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image, ImageOps
import random
import os
import pygame

# Game settings
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_FOLDER, "Assets")
QUESTIONS_PER_SHIFT = 10
FONT = "Trebuchet MS"
RECEIPT_FONT = "Courier New"

# Cafe colours
CREAM = "#FFF1E0"
WHITE = "#FFFAF2"
PEACH = "#F6C39F"
PINK = "#EB9588"
GREEN = "#B5D6A7"
BROWN = "#6B4230"
BORDER = "#7E4A32"
TEXT = "#5A3626"
GOOD = "#3F7D3E"
OKAY = "#B8691A"
BAD = "#B5453F"

# Lists used in the game
LEVEL_NAMES = ["Easy", "Moderate", "Advanced"]
LEVEL_HINTS = ["1-digit numbers", "2-digit numbers", "4-digit numbers"]
COFFEE_ITEMS = ["Espresso", "Black Coffee", "Latte", "Cappuccino", "Mocha", "Iced Coffee", "Matcha Latte", "Caramel Macchiato"]
STAR_FILES = ["empty.png", "fourth.png", "half.png", "three_fourths.png", "full.png"]

# dictionary to use for in game progress
game = {
    "history": [],
    "orders": [],
    "level": 1,
    "day": 1,
    "customer": 0,
    "attempt": 1,
    "score": 0,
    "answer": 0,
    "last_customer": -1,
    "song": "menu"
}
settings = {"music": True, "sfx": True}

# Main window
root = Tk()
root.title("Little Latte Cafe - Maths Quiz")
root.geometry("1000x700")
root.minsize(1000, 700)
root.config(bg=BROWN)

# Opens up a picture and remove its empty border and resize it.
def load_picture(file_name, new_height):
    picture = Image.open(file_name).convert("RGBA")
    picture = picture.crop(picture.getbbox())
    new_width = int(picture.width * new_height / picture.height)
    picture = picture.resize((new_width, new_height), Image.LANCZOS)
    return ImageTk.PhotoImage(picture)

# The window icon and customer pictures.
app_icon = load_picture(os.path.join(ASSETS, "icon.png"), 64)
root.iconphoto(True, app_icon)
customer_pictures = [
    load_picture(os.path.join(ASSETS, "customers", "1.png"), 300),
    load_picture(os.path.join(ASSETS, "customers", "2.png"), 300),
    load_picture(os.path.join(ASSETS, "customers", "3.png"), 300),
    load_picture(os.path.join(ASSETS, "customers", "4.png"), 300),
    load_picture(os.path.join(ASSETS, "customers", "5.png"), 300)
]

# Small stars are used on the game screen. Big stars are used on results.
small_stars = []
big_stars = []
for star_file in STAR_FILES:
    small_stars.append(load_picture(os.path.join(ASSETS, "stars", star_file), 32))
    big_stars.append(load_picture(os.path.join(ASSETS, "stars", star_file), 64))

# Background pictures for the menu and cafe scene.
scene_picture = Image.open(os.path.join(ASSETS, "bg.png")).convert("RGB")
scene_picture = scene_picture.resize((960, 540), Image.LANCZOS)
scene_image = ImageTk.PhotoImage(scene_picture)
counter_picture = scene_picture.crop((305, 423, 690, 540))
counter_image = ImageTk.PhotoImage(counter_picture)
menu_picture = Image.open(os.path.join(ASSETS, "menubg.jpg")).convert("RGB")
menu_picture = ImageOps.fit(menu_picture, (960, 640), Image.LANCZOS)
menu_image = ImageTk.PhotoImage(menu_picture)

# Sounds
# Pygame is used to play the cafe music and sound effects.
pygame.mixer.init()
sounds = {}
sounds["bell"] = pygame.mixer.Sound(os.path.join(ASSETS, "audio", "sfx", "bell.mp3"))
sounds["correct"] = pygame.mixer.Sound(os.path.join(ASSETS, "audio", "sfx", "correct.mp3"))
sounds["wrong"] = pygame.mixer.Sound(os.path.join(ASSETS, "audio", "sfx", "wrong.mp3"))
sounds["button"] = pygame.mixer.Sound(os.path.join(ASSETS, "audio", "sfx", "button.mp3"))

# Play a sound if sound effects are turned on.
def play_sound(sound_name):
    if settings["sfx"] == True:
        sounds[sound_name].play()

# Play the menu music or game music.
def play_music(song_name):
    game["song"] = song_name
    pygame.mixer.music.stop()
    if settings["music"] == True:
        song_file = os.path.join(ASSETS, "audio", "music", song_name + ".mp3")
        pygame.mixer.music.load(song_file)
        pygame.mixer.music.play(-1)

# Play the button sound before doing the button's job.
def button_clicked(action):
    play_sound("button")
    action()

# Make a button with the same style and click sound.
def make_button(parent, button_text, button_colour, action, width=16):
    button = Button(parent, text=button_text, font=(FONT, 11, "bold"),
                    bg=button_colour, fg=TEXT, activebackground=WHITE,
                    relief="flat", width=width, pady=4,
                    command=lambda: button_clicked(action))
    return button

# Make a screen and a panel for each page.
def make_screen():
    screen = Frame(root, bg=CREAM)
    screen.place(relx=0.5, rely=0.5, anchor=CENTER, width=960, height=640)
    Label(screen, image=menu_image, bd=0).place(x=0, y=0)
    return screen

def make_panel(screen, width, height):
    panel = Frame(screen, bg=CREAM, highlightbackground=BORDER, highlightthickness=4)
    panel.place(relx=0.5, rely=0.5, anchor=CENTER, width=width, height=height)
    return panel

# Ask before leaving the cafe or closing the game.
def confirm_action(title, message, action):
    answer = messagebox.askyesno(title, message)
    if answer == True:
        action()

# Turn fullscreen on or off with F11. Escape leaves fullscreen.
def toggle_fullscreen(event=None):
    if int(root.attributes("-fullscreen")) == 1:
        root.attributes("-fullscreen", False)
    else:
        root.attributes("-fullscreen", True)

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Quiz functions
# Choose a random number based on the difficulty level.
def random_int(chosen_level):
    if chosen_level == 1:
        number = random.randint(0, 9)
    elif chosen_level == 2:
        number = random.randint(10, 99)
    else:
        number = random.randint(1000, 9999)
    return number

# Randomly choose addition or subtraction.
def decide_operation():
    operation = random.choice(["+", "-"])
    return operation

# Give the player a grade based on the final score.
def get_grade(final_score):
    if final_score >= 91:
        return "A+"
    elif final_score >= 80:
        return "A"
    elif final_score >= 70:
        return "B"
    elif final_score >= 60:
        return "C"
    elif final_score >= 50:
        return "D"
    else:
        return "F"

# Work out the average score from all completed days.
def get_average_score():
    total_score = 0
    for day_record in game["history"]:
        total_score = total_score + day_record["score"]
    if len(game["history"]) > 0:
        return total_score / len(game["history"])
    else:
        return 0

# Update the five stars using the average score.
def show_stars(star_labels, star_pictures):
    average = get_average_score()
    quarters = int(average / 5 + 0.5)
    for number in range(5):
        fill = quarters - number * 4
        if fill > 4:
            fill = 4
        elif fill < 0:
            fill = 0
        star_labels[number].config(image=star_pictures[fill])

# Show the main menu.
def display_menu():
    play_music("menu")
    menu_screen.tkraise()

# Restart the game from Day 1.
def quit_to_menu():
    game["day"] = 1
    game["history"].clear()
    display_menu()

# Start a new day of the quiz.
def start_shift(next_day=0):
    game["day"] = game["day"] + next_day
    game["level"] = level_choice.get()
    game["score"] = 0
    game["customer"] = 0
    game["orders"] = []
    day_label.config(text="Day " + str(game["day"]) + " - " + LEVEL_NAMES[game["level"] - 1])
    show_stars(top_stars, small_stars)
    feedback_label.config(text="Shift started. Good luck!", fg=TEXT)
    play_music("game")
    game_screen.tkraise()
    display_problem()

# Show another customer, or show the results after 10 customers.
def next_customer():
    if game["customer"] >= QUESTIONS_PER_SHIFT:
        display_results()
    else:
        display_problem()

# Make a new question and show the next customer.
def display_problem():
    game["customer"] = game["customer"] + 1
    game["attempt"] = 1

    # Pick a different customer picture from the last question.
    picture_number = random.randint(0, 4)
    while picture_number == game["last_customer"]:
        picture_number = random.randint(0, 4)
    game["last_customer"] = picture_number

    first_number = random_int(game["level"])
    second_number = random_int(game["level"])
    operation = decide_operation()

    if operation == "+":
        game["answer"] = first_number + second_number
        first_item = random.choice(COFFEE_ITEMS)
        second_item = random.choice(COFFEE_ITEMS)
        while first_item == second_item:
            second_item = random.choice(COFFEE_ITEMS)
        sentence = "Hi! Can I please have " + first_item + " and " + second_item + "?"
        second_price = str(second_number)
    else:
        game["answer"] = first_number - second_number
        first_item = random.choice(COFFEE_ITEMS)
        second_item = "Coupon"
        sentence = "Can I have one " + first_item + "? I have a coupon!"
        second_price = "-" + str(second_number)

    # Save the order so it can appear on the receipt later.
    order = {"number": game["customer"], "name": first_item + " " + operation + " " + second_item,
             "question": str(first_number) + " " + operation + " " + str(second_number),
             "answer": game["answer"], "typed": [], "points": 0}
    game["orders"].append(order)

    # Draw the customer behind the counter.
    scene.delete("customer")
    scene.create_image(480, 468, image=customer_pictures[picture_number], anchor="s", tags="customer")
    scene.tag_raise("front")
    scene.itemconfig(order_text_id, text=sentence)
    scene.itemconfig(price_text_id, text=first_item + ": " + str(first_number) + "\n" + second_item + ": " + second_price)
    problem_label.config(text=str(first_number) + " " + operation + " " + str(second_number) + " =")
    status_label.config(text="Customer " + str(game["customer"]) + " of 10     Score: " + str(game["score"]))
    answer_entry.delete(0, END)
    answer_entry.focus_set()
    play_sound("bell")

# Check the answer and add points if it is correct.
def check_answer(user_answer):
    if user_answer == game["answer"]:
        play_sound("correct")
        if game["attempt"] == 1:
            points = 10
            feedback_label.config(text="Perfect! +10 points", fg=GOOD)
        else:
            points = 5
            feedback_label.config(text="Got it this time! +5 points", fg=OKAY)
        game["score"] = game["score"] + points
        game["orders"][len(game["orders"]) - 1]["points"] = points
        return True
    else:
        play_sound("wrong")
        return False

# Read the player's answer from the Entry box.
def submit_answer(event=None):
    typed_answer = answer_entry.get().strip()
    try:
        user_answer = int(typed_answer)
    except ValueError:
        messagebox.showerror("Not a number", "Please type a whole number, like 12 or -7.")
        answer_entry.focus_set()
        return

    game["orders"][len(game["orders"]) - 1]["typed"].append(typed_answer)
    if check_answer(user_answer) == True:
        next_customer()
    elif game["attempt"] == 1:
        game["attempt"] = 2
        feedback_label.config(text="Oops! Try one more time.", fg=OKAY)
        answer_entry.delete(0, END)
    else:
        feedback_label.config(text="Missed! The answer was " + str(game["answer"]) + ".", fg=BAD)
        next_customer()

# Show the score and grade when the day is finished.
def display_results():
    day_record = {"day": game["day"], "level": LEVEL_NAMES[game["level"] - 1],
                  "score": game["score"], "orders": game["orders"]}
    game["history"].append(day_record)
    result_title.config(text="Day " + str(game["day"]) + " Complete!")
    final_score_label.config(text="Score: " + str(game["score"]) + " / 100")
    rank_label.config(text="Grade: " + get_grade(game["score"]))
    show_stars(result_stars, big_stars)
    play_music("menu")
    results_screen.tkraise()

# Receipts
# Show the orders from every day that has been completed.
def show_receipts():
    receipts_text.config(state=NORMAL)
    receipts_text.delete("1.0", END)

    if len(game["history"]) == 0:
        receipts_text.insert(END, "No receipts yet. Complete a day first.")

    for day_record in game["history"]:
        receipts_text.insert(END, "DAY " + str(day_record["day"]) + " - " + day_record["level"] + "\n")
        receipts_text.insert(END, "Score: " + str(day_record["score"]) + " / 100    Grade: " + get_grade(day_record["score"]) + "\n\n")

        for order in day_record["orders"]:
            if order["points"] == 10:
                result = "1st try +10 points"
            elif order["points"] == 5:
                result = "2nd try +5 points"
            else:
                result = "Missed +0 points"
            typed_answers = ""
            for answer in order["typed"]:
                typed_answers = typed_answers + answer + " "
            receipt_line = order["name"] + "\n"
            receipt_line = receipt_line + order["question"] + " = " + str(order["answer"]) + "\n"
            receipt_line = receipt_line + "Your answer: " + typed_answers + "   " + result + "\n\n"
            receipts_text.insert(END, receipt_line)

        receipts_text.insert(END, "\n")

    receipts_text.config(state=DISABLED)
    receipts_screen.tkraise()

# Settings
# Switch music or sound effects on and off.
def toggle_setting(name, button, label):
    settings[name] = not settings[name]
    if settings[name] == True:
        button.config(text=label + ": ON")
    else:
        button.config(text=label + ": OFF")

    if name == "music":
        if settings["music"] == True:
            play_music(game["song"])
        else:
            pygame.mixer.music.stop()

# How to Play text
HOW_TO = [
    ("THE GOAL", "Serve 10 customers every day. Each customer asks a maths question."),
    ("ANSWERING", "Read the order and prices. Type your answer and press Submit or Enter."),
    ("POINTS", "First try = 10 points. Second try = 5 points. Each day is out of 100."),
    ("STARS AND RECEIPTS", "Stars show your average score. View Receipts shows your past orders."),
    ("KEYS", "Enter = submit        F11 = fullscreen        Esc = leave fullscreen")
]

# Settings screen
settings_screen = make_screen()
settings_panel = make_panel(settings_screen, 620, 340)
Label(settings_panel, text="Settings", font=(FONT, 32, "bold"), bg=CREAM, fg=BORDER).pack(pady=(25, 10))
music_button = make_button(settings_panel, "Music: ON", PINK, lambda: toggle_setting("music", music_button, "Music"))
music_button.pack(pady=8)
sfx_button = make_button(settings_panel, "Sound FX: ON", PINK, lambda: toggle_setting("sfx", sfx_button, "Sound FX"))
sfx_button.pack(pady=8)
make_button(settings_panel, "< Back to Menu", PEACH, display_menu).pack(pady=(20, 0))

# How to Play screen
howto_screen = make_screen()
howto_panel = make_panel(howto_screen, 740, 590)
Label(howto_panel, text="How to Play", font=(FONT, 32, "bold"), bg=CREAM, fg=BORDER).pack(pady=(18, 4))
for heading, body in HOW_TO:
    Label(howto_panel, text=heading, font=(FONT, 11, "bold"), bg=CREAM, fg=BORDER).pack(anchor=W, padx=45, pady=(10, 0))
    Label(howto_panel, text=body, font=(FONT, 11), bg=CREAM, fg=TEXT, justify=LEFT).pack(anchor=W, padx=45)
make_button(howto_panel, "< Back to Menu", PEACH, display_menu).pack(pady=(18, 0))

# Results screen
results_screen = make_screen()
results_panel = make_panel(results_screen, 560, 540)
result_title = Label(results_panel, font=(FONT, 30, "bold"), bg=CREAM, fg=BORDER)
result_title.pack(pady=(30, 6))
final_score_label = Label(results_panel, font=(FONT, 24, "bold"), bg=CREAM, fg=TEXT)
final_score_label.pack(pady=4)
rank_label = Label(results_panel, font=(FONT, 36, "bold"), bg=CREAM, fg=PINK)
rank_label.pack(pady=4)
star_row = Frame(results_panel, bg=CREAM)
star_row.pack(pady=20)
result_stars = []
for number in range(5):
    star_label = Label(star_row, image=big_stars[0], bg=CREAM)
    star_label.grid(row=0, column=number, padx=4)
    result_stars.append(star_label)
result_buttons = Frame(results_panel, bg=CREAM)
result_buttons.pack(pady=10)
make_button(result_buttons, "Next Day >", GREEN, lambda: start_shift(1)).grid(row=0, column=0, padx=6, pady=6)
make_button(result_buttons, "Quit to Menu", PINK, quit_to_menu).grid(row=0, column=1, padx=6, pady=6)
make_button(result_buttons, "View Receipts", PEACH, show_receipts).grid(row=1, column=0, columnspan=2, pady=6)

# Receipts screen. A Text box and scrollbar show the saved orders.
receipts_screen = make_screen()
receipts_panel = make_panel(receipts_screen, 840, 600)
Label(receipts_panel, text="Receipts", font=(FONT, 30, "bold"), bg=CREAM, fg=BORDER).pack(pady=(14, 0))
Label(receipts_panel, text="Your completed days and orders", font=(FONT, 11), bg=CREAM, fg=TEXT).pack(pady=(0, 8))
receipts_frame = Frame(receipts_panel, bg=WHITE)
receipts_frame.pack()
receipts_text = Text(receipts_frame, width=85, height=22, font=(RECEIPT_FONT, 10), bg=WHITE, fg=TEXT, wrap=WORD)
receipts_scrollbar = Scrollbar(receipts_frame, command=receipts_text.yview)
receipts_text.config(yscrollcommand=receipts_scrollbar.set)
receipts_scrollbar.pack(side=RIGHT, fill=Y)
receipts_text.pack(side=LEFT)
make_button(receipts_panel, "< Back to Results", PEACH, lambda: results_screen.tkraise()).pack(pady=10)

# Game screen
# The top bar shows the day, stars and menu button.
game_screen = make_screen()
top_bar = Frame(game_screen, bg=CREAM)
top_bar.place(x=0, y=0, width=960, height=56)
Frame(game_screen, bg=BORDER).place(x=0, y=53, width=960, height=3)
make_button(top_bar, "< Menu", PEACH, lambda: confirm_action("Leave the cafe?", "Your day and receipts will reset. Leave anyway?", quit_to_menu)).place(x=10, rely=0.5, anchor=W)
make_button(top_bar, "Fullscreen", PEACH, toggle_fullscreen).place(relx=1.0, x=-10, rely=0.5, anchor=E)
day_label = Label(top_bar, font=(FONT, 12, "bold"), bg=CREAM, fg=TEXT)
day_label.place(x=200, rely=0.5, anchor=W)
stars_box = Frame(top_bar, bg=CREAM)
stars_box.place(relx=0.5, rely=0.5, anchor=CENTER)
top_stars = []
for number in range(5):
    star_label = Label(stars_box, image=small_stars[0], bg=CREAM)
    star_label.pack(side=LEFT, padx=2)
    top_stars.append(star_label)

# Canvas is used to draw the cafe background, counter and customer.
scene = Canvas(game_screen, width=960, height=540, highlightthickness=0, bd=0)
scene.place(x=0, y=56)
scene.create_image(0, 0, image=scene_image, anchor="nw")
scene.create_image(305, 423, image=counter_image, anchor="nw", tags="front")
scene.create_polygon(329, 118, 356, 140, 329, 158, fill=WHITE, outline=BORDER, width=3, tags="front")
scene.create_rectangle(20, 50, 330, 195, fill=WHITE, outline=BORDER, width=3, tags="front")
order_text_id = scene.create_text(175, 88, width=275, justify="center", font=(FONT, 13, "bold"), fill=TEXT, tags="front")
scene.create_line(45, 123, 305, 123, fill=PEACH, width=2, tags="front")
price_text_id = scene.create_text(175, 158, width=275, justify="center", font=(FONT, 12, "bold"), fill=BORDER, tags="front")

# The answer card contains the question, answer box and Submit button.
answer_card = Frame(game_screen, bg=CREAM, highlightbackground=BORDER, highlightthickness=3)
answer_card.place(x=305, y=486, width=370, height=100)
problem_label = Label(answer_card, font=(FONT, 18, "bold"), bg=CREAM, fg=TEXT)
problem_label.place(x=12, y=10)
answer_entry = Entry(answer_card, font=(FONT, 16, "bold"), justify=CENTER, bg=WHITE, fg=TEXT)
answer_entry.place(x=190, y=8, width=165, height=34)
answer_entry.bind("<Return>", submit_answer)
Label(answer_card, text="1st try = 10 points\n2nd try = 5 points", font=(FONT, 9, "bold"), bg=CREAM, fg=OKAY, justify=LEFT).place(x=12, y=52)
make_button(answer_card, "Submit", GREEN, submit_answer).place(x=190, y=50)

# Feedback and score appear along the bottom.
bottom_strip = Frame(game_screen, bg=CREAM)
bottom_strip.place(x=0, y=596, width=960, height=44)
Frame(game_screen, bg=BORDER).place(x=0, y=596, width=960, height=3)
feedback_label = Label(bottom_strip, font=(FONT, 12, "bold"), bg=CREAM, fg=TEXT)
feedback_label.place(x=15, rely=0.5, anchor=W)
status_label = Label(bottom_strip, font=(FONT, 12, "bold"), bg=CREAM, fg=TEXT)
status_label.place(relx=1.0, x=-15, rely=0.5, anchor=E)

# Main menu
menu_screen = make_screen()
menu_panel = make_panel(menu_screen, 480, 540)
Label(menu_panel, text="Little Latte Cafe", font=(FONT, 33, "bold"), bg=CREAM, fg=BORDER).pack(pady=(28, 0))
Label(menu_panel, text="Maths Quiz - serve 10 customers a day", font=(FONT, 12), bg=CREAM, fg=TEXT).pack(pady=(0, 12))

# The player chooses one of the three difficulty levels.
level_choice = IntVar(value=1)
level_box = LabelFrame(menu_panel, text=" DIFFICULTY LEVEL ", font=(FONT, 12, "bold"), bg=CREAM, fg=BORDER, padx=25, pady=8)
level_box.pack(pady=8)
for number in range(3):
    choice_text = str(number + 1) + ". " + LEVEL_NAMES[number] + " (" + LEVEL_HINTS[number] + ")"
    Radiobutton(level_box, text=choice_text, variable=level_choice, value=number + 1,
                font=(FONT, 13), bg=CREAM, fg=TEXT, selectcolor=PEACH,
                activebackground=CREAM).pack(anchor=W, pady=2)
make_button(menu_panel, "Start Shift", GREEN, start_shift).pack(pady=(16, 6))
menu_buttons = Frame(menu_panel, bg=CREAM)
menu_buttons.pack(pady=4)
make_button(menu_buttons, "How to Play", PEACH, lambda: howto_screen.tkraise()).grid(row=0, column=0, padx=6, pady=6)
make_button(menu_buttons, "Settings", PEACH, lambda: settings_screen.tkraise()).grid(row=0, column=1, padx=6, pady=6)
make_button(menu_buttons, "Fullscreen", PEACH, toggle_fullscreen).grid(row=1, column=0, padx=6, pady=6)
make_button(menu_buttons, "Quit", PINK, lambda: confirm_action("Close the cafe?", "Do you really want to quit?", root.destroy)).grid(row=1, column=1, padx=6, pady=6)

# Open the menu and keep the program running.
display_menu()
root.mainloop()
