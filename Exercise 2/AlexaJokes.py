# Exercise 2: Alexa Jokes

# Imports
from tkinter import *
from PIL import ImageTk, Image
import random
import pygame
import os

# Find Assets2 beside this Python file, even when VS Code runs from another folder.
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_FOLDER, "Assets2")
FAVOURITES_FILE = os.path.join(BASE_FOLDER, "favourites.txt")

# Colours used in the app
DARK = "#0A0A14"
BG = "#14142A"
PANEL = "#1E1E3A"
WHITE = "#F5F5FF"
INK = "#14142A"
PURPLE = "#8B5CF6"
PINK = "#FF5C8A"
GREEN = "#3DDC97"
CORAL = "#FF7A59"
GREY = "#34345C"
YELLOW = "#F7C948"
FONT = "Segoe UI"

root = Tk()
root.title("Alexa Jokes - Alexa Tell Me a Joke")
root.geometry("1000x700")
root.resizable(False, False)
root.config(bg=DARK)

# Picture loader and for resizing
def load_picture(file_name, size):
    picture = Image.open(os.path.join(ASSETS, file_name))
    picture = picture.resize((size, size))
    return ImageTk.PhotoImage(picture, master=root)

# icons used inside the joke screen
heart_image = load_picture("icons/heart.png", 30)
comment_image = load_picture("icons/comment.png", 30)
share_image = load_picture("icons/share.png", 30)
save_image = load_picture("icons/save.png", 30)
save_filled_image = load_picture("icons/save2.png", 30)

# laughing emojis behind the background and for the program icon (replaces the feather icon) and in for in message box
laughing1_small = load_picture("laughing1.png", 54)
laughing2_small = load_picture("laughing2.png", 58)
laughing1_large = load_picture("laughing1.png", 72)
laughing2_large = load_picture("laughing2.png", 72)
logo_image = load_picture("laughing1.png", 90)
program_icon = load_picture("laughing2.png", 48)
root.iconphoto(True, program_icon)

# Button sfx and laughing sfx when the "Show Joke" is pressed
try:
    pygame.mixer.init()
    button_sound = pygame.mixer.Sound(os.path.join(ASSETS, "sfx", "button.mp3"))
    laugh1_sound = pygame.mixer.Sound(os.path.join(ASSETS, "sfx", "laugh1.mp3"))
    laugh2_sound = pygame.mixer.Sound(os.path.join(ASSETS, "sfx", "laugh2.mp3"))
    laugh3_sound = pygame.mixer.Sound(os.path.join(ASSETS, "sfx", "laugh3.mp3"))
    laugh_sounds = [laugh1_sound, laugh2_sound, laugh3_sound]
except:
    # The app can still open if sound is not available.
    button_sound = None
    laugh_sounds = []

# Play a button sound, then run its function.
def button_click(action):
    if button_sound != None:
        button_sound.play()
    action()

# Read the jokes from randomJokes.txt or the favourites file.
# Each line has a question mark between the setup and punchline.
def load_jokes(file_name):
    joke_list = []
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("?", 1)
                if len(parts) == 2:
                    setup = parts[0].strip().lstrip("-").strip()
                    punchline = parts[1].strip()
                    joke_list.append([setup + "?", punchline])
    except FileNotFoundError:
        return joke_list
    return joke_list

# Load jokes and saved favourites when the app starts.
jokes = load_jokes(os.path.join(ASSETS, "randomJokes.txt"))
favourites = load_jokes(FAVOURITES_FILE)

# Save favourites in a text file so they stay saved after closing the app.
def save_favourites():
    with open(FAVOURITES_FILE, "w", encoding="utf-8") as file:
        for joke in favourites:
            file.write(joke[0] + joke[1] + "\n")

# lists for the jokes like/comment numbers (and to remember the likes and comments if next joke is pressed and back to previous joke)
joke_history = []
likes_history = []
comments_history = []
history_position = 0
current_joke = None
punchline_visible = False

# Screen and button styles
def make_screen():
    screen = Frame(root, bg=BG)
    screen.place(relx=0.5, rely=0.5, anchor=CENTER, width=960, height=640)
    return screen

def make_panel(screen, width, height):
    panel = Frame(screen, bg=PANEL, highlightbackground=PURPLE, highlightthickness=2)
    panel.place(relx=0.5, rely=0.5, anchor=CENTER, width=width, height=height)
    return panel

# All app buttons use the same colours and plays button.mp3.
def make_button(parent, text, colour, action, text_colour=INK, width=20):
    return Button(parent, text=text, font=(FONT, 11, "bold"), bg=colour,
                  fg=text_colour, activebackground=WHITE, relief="flat",
                  cursor="hand2", width=width, padx=8, pady=6,
                  command=lambda: button_click(action))

# F11 turns fullscreen on or off. Escape leaves fullscreen.
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def leave_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", leave_fullscreen)

# Message boxes
def show_message(title, message, question=False):
    popup = Toplevel(root)
    popup.title(title)
    popup.geometry("400x210")
    popup.config(bg=PURPLE)
    popup.resizable(False, False)
    popup.transient(root)
    popup.iconphoto(True, program_icon)
    answer = BooleanVar(root, False)  # Remembers which button was pressed.

    heading = Frame(popup, bg=PURPLE)
    heading.pack(fill=X, padx=3, pady=3)
    Label(heading, image=program_icon, bg=PURPLE).pack(side=LEFT, padx=10, pady=6)
    Label(heading, text=title, font=(FONT, 14, "bold"), bg=PURPLE, fg=WHITE).pack(side=LEFT)
    Label(popup, text=message, font=(FONT, 11), bg=PANEL, fg=WHITE,
          wraplength=340, justify=CENTER, padx=20, pady=22).pack(fill=BOTH, padx=6)

    if question == True:
        make_button(popup, "Yes", GREEN, lambda: answer.set(True), INK, 10).pack(side=LEFT, padx=55, pady=10)
        make_button(popup, "No", PINK, lambda: answer.set(False), INK, 10).pack(side=RIGHT, padx=55, pady=10)
    else:
        make_button(popup, "OK", YELLOW, lambda: answer.set(True), INK, 12).pack(pady=10)

    popup.protocol("WM_DELETE_WINDOW", lambda: answer.set(False))
    popup.grab_set()                 # Wait until the user closes this message.
    root.wait_variable(answer)
    popup.destroy()
    return answer.get()

# Ask before closing the app.
def quit_program():
    answer = show_message("Quit Alexa Jokes", "Do you want to close the app?", True)
    if answer == True:
        root.destroy()

# the white card behind the joke text.
def draw_card(text, top):
    text_id = phone.create_text(44, top + 12, text=text, width=198, anchor="nw",
                                font=(FONT, 12, "bold"), fill=INK, tags="joke_card")
    left, upper, right, lower = phone.bbox(text_id)  # Find the size of the text.
    phone.create_rectangle(left - 14, upper - 8, right + 14, lower + 8,
                           fill="#C99700", outline="", tags="joke_card")
    phone.create_rectangle(left - 17, upper - 11, right + 11, lower + 5,
                           fill=WHITE, outline="", tags="joke_card")
    phone.tag_raise(text_id)  # Keep the words in front of the card.
    return lower + 12

# Show the joke, its numbers and its bookmark picture.
def show_joke():
    phone.delete("joke_card")  # Remove the old joke before drawing the new one.
    if current_joke == None:
        draw_card("Press Alexa tell me a Joke to begin!", 65)
        phone.itemconfig(likes_id, text="")
        phone.itemconfig(comments_id, text="")
        phone.itemconfig(caption_id, text="")
        phone.itemconfig(save_id, image=save_image)
    else:
        bottom = draw_card(current_joke[0], 55)
        if punchline_visible == True:
            draw_card(current_joke[1], bottom + 15)
        # These numbers are only changed inside next_joke().
        phone.itemconfig(likes_id, text=str(likes_history[history_position]))
        phone.itemconfig(comments_id, text=str(comments_history[history_position]))
        phone.itemconfig(caption_id, text="Joke " + str(history_position + 1))
        if current_joke in favourites:
            phone.itemconfig(save_id, image=save_filled_image)
        else:
            phone.itemconfig(save_id, image=save_image)

# Start the feed with a random joke.
def start_feed():
    global current_joke, history_position, punchline_visible
    if len(jokes) == 0:
        show_message("No jokes found", "Check randomJokes.txt inside the Assets2 folder.")
        return
    joke_history.clear()
    likes_history.clear()
    comments_history.clear()
    current_joke = random.choice(jokes)
    joke_history.append(current_joke)
    likes_history.append(125)       # The first joke starts with these numbers.
    comments_history.append(18)
    history_position = 0
    punchline_visible = False
    show_joke()
    feed_screen.tkraise()

# Next Joke selects a joke and randomises its like and comment numbers.
def next_joke():
    global current_joke, history_position, punchline_visible
    if len(jokes) == 0:
        return
    if history_position < len(joke_history) - 1:
        history_position = history_position + 1
        current_joke = joke_history[history_position]
    else:
        current_joke = random.choice(jokes)
        joke_history.append(current_joke)
        likes_history.append(0)
        comments_history.append(0)
        history_position = history_position + 1
    likes_history[history_position] = random.randint(100, 99000)
    comments_history[history_position] = random.randint(3, 900)
    punchline_visible = False
    show_joke()

# Previous Joke keeps the old like and comment numbers.
def previous_joke():
    global current_joke, history_position, punchline_visible
    if history_position > 0:
        history_position = history_position - 1
        current_joke = joke_history[history_position]
        punchline_visible = False
        show_joke()

# Show the punchline and play one random laugh sound.
def show_punchline():
    global punchline_visible
    if current_joke != None:
        punchline_visible = True
        show_joke()
        if len(laugh_sounds) > 0:
            laugh = random.choice(laugh_sounds)
            laugh.play()

# Save the joke or remove it if it is already saved.
def toggle_favourite():
    if current_joke != None:
        if current_joke in favourites:
            favourites.remove(current_joke)
        else:
            favourites.append(current_joke)
        save_favourites()
        show_joke()  # Update the bookmark picture.

def save_button_clicked(event):
    button_click(toggle_favourite) 

# Display the saved jokes in the favourites screen.
def show_favourites():
    favourites_text.config(state=NORMAL)
    favourites_text.delete("1.0", END)
    if len(favourites) == 0:
        favourites_text.insert(END, "No favourites yet.\nSave a joke using the bookmark icon.")
    else:
        for number in range(len(favourites)):
            joke = favourites[number]
            favourites_text.insert(END, str(number + 1) + ". " + joke[0] + "\n" + joke[1] + "\n\n")
    favourites_text.config(state=DISABLED)  # Stops the user changing the saved list.
    favourites_screen.tkraise()

def show_home():
    start_screen.tkraise()

# Favourites screen
favourites_screen = make_screen()
favourites_panel = make_panel(favourites_screen, 760, 580)
Label(favourites_panel, text="Favourites", font=(FONT, 28, "bold"), bg=PANEL, fg=WHITE).pack(pady=(20, 10))
list_frame = Frame(favourites_panel, bg=BG)
list_frame.pack(pady=5)
favourites_text = Text(list_frame, width=70, height=19, font=(FONT, 12), bg=BG, fg=WHITE, wrap=WORD, bd=0, padx=14, pady=10)
favourites_scrollbar = Scrollbar(list_frame, command=favourites_text.yview)
favourites_text.config(yscrollcommand=favourites_scrollbar.set)
favourites_scrollbar.pack(side=RIGHT, fill=Y)
favourites_text.pack(side=LEFT)
make_button(favourites_panel, "< Back to Menu", GREY, show_home, WHITE).pack(pady=16)

# Joke feed screen
feed_screen = make_screen()
top_bar = Frame(feed_screen, bg=PANEL)
top_bar.place(x=0, y=0, width=960, height=56)
Frame(feed_screen, bg=PURPLE).place(x=0, y=54, width=960, height=2)
make_button(top_bar, "< Menu", GREY, show_home, WHITE, 15).place(x=10, rely=0.5, anchor=W)
Label(top_bar, text="Alexa Jokes", font=(FONT, 16, "bold"), bg=PANEL, fg=WHITE).place(relx=0.5, rely=0.5, anchor=CENTER)
make_button(top_bar, "Fullscreen", GREY, toggle_fullscreen, WHITE, 15).place(relx=1.0, x=-10, rely=0.5, anchor=E)

# Canvas makes the phone shape and displays its pictures.
phone = Canvas(feed_screen, width=340, height=470, bg=BG, highlightthickness=0, bd=0)
phone.place(x=310, y=68)
phone.create_rectangle(2, 2, 338, 468, fill=DARK, outline=PURPLE, width=3)
phone.create_rectangle(14, 34, 326, 436, fill=YELLOW, outline="")
phone.create_image(298, 84, image=laughing1_small)
phone.create_image(54, 346, image=laughing2_small)
phone.create_image(222, 352, image=laughing1_small)
phone.create_oval(165, 14, 175, 24, fill=GREY, outline="")
phone.create_line(140, 452, 200, 452, width=5, fill=GREY)

# Heart, comment and share pictures are for display only.
phone.create_image(295, 170, image=heart_image)
likes_id = phone.create_text(295, 206, font=(FONT, 11, "bold"), fill=INK)
phone.create_image(295, 250, image=comment_image)
comments_id = phone.create_text(295, 286, font=(FONT, 11, "bold"), fill=INK)
phone.create_image(295, 395, image=share_image)

# The save picture changes when it is clicked.
save_id = phone.create_image(295, 335, image=save_image, tags="save")
phone.tag_bind("save", "<Button-1>", save_button_clicked)
phone.create_text(36, 396, text="alexa.jokes", anchor="w", font=(FONT, 12, "bold"), fill=INK)
caption_id = phone.create_text(30, 421, anchor="w", font=(FONT, 10), fill=INK)

# Joke buttons
button_row = Frame(feed_screen, bg=BG)
button_row.place(relx=0.5, y=556, anchor=N)
make_button(button_row, "< Previous Joke", GREY, previous_joke, WHITE, 15).grid(row=0, column=0, padx=6)
make_button(button_row, "Show Punchline", GREEN, show_punchline, INK, 15).grid(row=0, column=1, padx=6)
make_button(button_row, "Next Joke >", PINK, next_joke, INK, 15).grid(row=0, column=2, padx=6)
make_button(button_row, "Quit", CORAL, quit_program, INK, 15).grid(row=0, column=3, padx=6)

# Start menu
start_screen = make_screen()
backdrop = Canvas(start_screen, width=960, height=640, bg=BG, highlightthickness=0, bd=0)
backdrop.place(x=0, y=0)
backdrop.create_image(70, 90, image=laughing1_large)
backdrop.create_image(880, 80, image=laughing2_large)
backdrop.create_image(120, 550, image=laughing2_large)
backdrop.create_image(860, 540, image=laughing1_large)
backdrop.create_image(60, 330, image=laughing1_small)
backdrop.create_image(905, 320, image=laughing2_small)
backdrop.create_image(250, 40, image=laughing2_small)
backdrop.create_image(700, 604, image=laughing1_small)

start_panel = make_panel(start_screen, 460, 500)
Label(start_panel, image=logo_image, bg=PANEL).pack(pady=(26, 0))
Label(start_panel, text="Alexa Jokes", font=(FONT, 32, "bold"), bg=PANEL, fg=WHITE).pack(pady=(6, 0))
Label(start_panel, text="Swipe through jokes and save your favourites", font=(FONT, 11), bg=PANEL, fg="#A0A0C8").pack(pady=(0, 18))
make_button(start_panel, "Alexa tell me a Joke", PINK, start_feed).pack(pady=6)
make_button(start_panel, "Favourites", GREEN, show_favourites).pack(pady=6)
make_button(start_panel, "Fullscreen", GREY, toggle_fullscreen, WHITE).pack(pady=6)
make_button(start_panel, "Quit", CORAL, quit_program).pack(pady=6)

# Show the start menu and keep the window open.
start_screen.tkraise()
root.mainloop()
