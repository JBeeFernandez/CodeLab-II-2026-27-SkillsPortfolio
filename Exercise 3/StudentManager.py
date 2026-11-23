# Exercise 3 - Student Manager 

from tkinter import *
from tkinter import messagebox
import os       # used only to find the Items folder
import pygame   # used only to play the two sounds

# ---------- SETTINGS (things we use many times, so they are saved in variables) ----------
ITEMS_FOLDER = os.path.join(os.path.dirname(__file__), "Items")   # the Items folder sits next to this file
FILE_NAME = os.path.join(ITEMS_FOLDER, "studentMarks.txt")
FULL_MARKS = 160     # 3 course marks (3 x 20) + exam (100)
ROWS = 10            # how many students are shown in the table at once
FONT = "tahoma"      # change this one word to use a different font

BACKGROUND = "#8c7a5b"
DARK_COLOUR = "#4a3b2a"
HEADER_COLOUR = "#6e5a43"
ROW_COLOUR = "#5a4833"
SELECTED_COLOUR = "#8a6d2f"
GREEN_COLOUR = "#3fa34d"
BLUE_COLOUR = "#2f7fb0"

# where each table column starts and how wide it is (in pixels)
COLUMN_X = [0, 170, 290, 410, 500, 600, 660]
COLUMN_WIDTHS = [170, 120, 120, 90, 100, 60, 80]
HEADINGS = ["Name", "Student Number", "Coursework /60", "Exam /100", "Percentage", "Grade", "Select"]

# ---------- SOUND ----------
pygame.mixer.init()
select_sound = pygame.mixer.Sound(os.path.join(ITEMS_FOLDER, "select.mp3"))

def playSelect():
    # plays the click sound
    select_sound.play()

# ---------- THE DATA ----------
# Everything the program needs to remember is kept in this dictionary.
# Every student is also a dictionary, like: {"code": 1345, "name": "John Curry", ...}
class_data = {
    "students": [],   # the list of all students
    "shown": [],      # the students that are shown in the table right now
    "page": 0,        # which page of the table we are on (0 = page 1)
    "selected": -1,   # the student number of the chosen student (-1 = nobody)
    "mode": "add"     # the form is used for "add" or "update"
}

# ---------- FILE FUNCTIONS ----------
def loadStudents():
    # reads the text file and puts every student into the list
    students = []
    with open(FILE_NAME, "r") as file_handler:
        lines = file_handler.readlines()

    # line 0 is only the number of students, so we start from line 1
    for i in range(1, len(lines)):
        if lines[i].strip() != "":
            data = lines[i].strip().split(",")   # split the line at every comma
            students.append({"code": int(data[0]), "name": data[1], "mark1": int(data[2]),
                             "mark2": int(data[3]), "mark3": int(data[4]), "exam": int(data[5])})
    class_data["students"] = students

def saveStudents():
    # writes the whole list back into the text file
    students = class_data["students"]
    with open(FILE_NAME, "w") as file_handler:
        file_handler.write(f"{len(students)}\n")   # first line = how many students
        for s in students:
            file_handler.write(f"{s['code']},{s['name']},{s['mark1']},{s['mark2']},{s['mark3']},{s['exam']}\n")

# ---------- MARK FUNCTIONS ----------
def getCoursework(student):
    # adds the three course marks together
    return student["mark1"] + student["mark2"] + student["mark3"]

def getPercent(student):
    # total marks out of 160, turned into a percentage
    return (getCoursework(student) + student["exam"]) * 100 / FULL_MARKS

def getGrade(percent):
    # gives the grade letter for a percentage
    if percent >= 70:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C"
    elif percent >= 40:
        return "D"
    else:
        return "F"

# ---------- CHECKING FUNCTIONS ----------
def checkNumber(text, lowest, highest):
    # True if the text is a whole number between lowest and highest
    if text == "":
        return False
    for letter in text:
        if letter not in "0123456789":
            return False
    return int(text) >= lowest and int(text) <= highest

def findPosition(search_text):
    # looks for a student by name or student number
    # gives back their place in the list, or -1 if they are not found
    students = class_data["students"]
    for i in range(len(students)):
        if search_text == students[i]["name"] or search_text == str(students[i]["code"]):
            return i
    return -1

# ---------- SCREEN FUNCTIONS ----------
def refreshTable():
    # fills the table with the students on the current page
    shown = class_data["shown"]
    start = class_data["page"] * ROWS

    for r in range(ROWS):
        position = start + r
        colour = ROW_COLOUR
        if position < len(shown):
            s = shown[position]
            percent = getPercent(s)
            texts = [s["name"], str(s["code"]), str(getCoursework(s)), str(s["exam"]), f"{percent:.1f}%", getGrade(percent), ""]
            row_buttons[r].config(text="Select", bg=GREEN_COLOUR)
            if s["code"] == class_data["selected"]:
                colour = SELECTED_COLOUR   # the chosen student is gold
        else:
            texts = ["", "", "", "", "", "", ""]   # an empty row
            row_buttons[r].config(text="", bg=colour)

        for c in range(7):
            row_labels[r][c].config(text=texts[c], bg=colour)

    # the text under the table
    footer_label.config(text=f"Showing {len(shown)} students  (page {class_data['page'] + 1})")

    # the class summary line (number of students and average percentage)
    students = class_data["students"]
    total_percent = 0
    for s in students:
        total_percent += getPercent(s)
    average = 0
    if len(students) > 0:
        average = total_percent / len(students)
    summary_label.config(text=f"Class summary:  {len(students)} students   |   Average percentage: {average:.1f}%")
    table_frame.tkraise()

def showList(students):
    # shows a list of students in the table, starting at page 1
    class_data["shown"] = students
    class_data["page"] = 0
    refreshTable()

def selectRow(row):
    # runs when a green Select button is clicked
    position = class_data["page"] * ROWS + row
    if position < len(class_data["shown"]):
        playSelect()
        class_data["selected"] = class_data["shown"][position]["code"]
        refreshTable()

def changePage(step):
    # the << button uses -1 and the >> button uses +1
    playSelect()
    new_page = class_data["page"] + step
    if new_page >= 0 and new_page * ROWS < len(class_data["shown"]):
        class_data["page"] = new_page
        refreshTable()

# ---------- MENU FUNCTIONS (one for each tab on the right) ----------
def viewAll():
    # 1. View all student records
    playSelect()
    showList(class_data["students"])

def viewOne():
    # 2. View individual student record (also used by the Search button)
    playSelect()
    search_text = search_entry.get().strip()
    position = findPosition(search_text)
    if position == -1:
        messagebox.showerror("Error", f"No student found for '{search_text}'. Type a name or student number.")
    else:
        class_data["selected"] = class_data["students"][position]["code"]
        showList([class_data["students"][position]])

def showExtreme(want_highest):
    # 3 and 4. Show the student with the highest (or lowest) overall mark
    playSelect()
    students = class_data["students"]
    best_position = 0
    for i in range(len(students)):
        this_percent = getPercent(students[i])
        best_percent = getPercent(students[best_position])
        if (want_highest == True and this_percent > best_percent) or (want_highest == False and this_percent < best_percent):
            best_position = i
    if len(students) > 0:
        class_data["selected"] = students[best_position]["code"]
        showList([students[best_position]])

def sortStudents():
    # 5. Sort the students by overall percentage
    playSelect()
    ascending = messagebox.askyesno("Sort", "Sort in ascending order (lowest mark first)?\n\nYes = ascending\nNo = descending")

    # make a copy of the list, so the order in the file does not change
    sorted_students = []
    for s in class_data["students"]:
        sorted_students.append(s)

    # bubble sort: compare two students next to each other and swap them if needed
    count = len(sorted_students)
    for i in range(count):
        for j in range(count - 1 - i):
            first = getPercent(sorted_students[j])
            second = getPercent(sorted_students[j + 1])
            if (ascending == True and first > second) or (ascending == False and first < second):
                sorted_students[j], sorted_students[j + 1] = sorted_students[j + 1], sorted_students[j]
    showList(sorted_students)

def addStudent():
    # 6. Add a student record: show an empty form
    playSelect()
    class_data["mode"] = "add"
    for entry in form_entries:
        entry.delete(0, END)
    form_frame.tkraise()

def updateStudent():
    # 8. Update the chosen student: show the form with the old details already typed in
    playSelect()
    position = findPosition(str(class_data["selected"]))
    if position == -1:
        messagebox.showwarning("Warning", "Please choose a student first (click a green Select button).")
    else:
        s = class_data["students"][position]
        class_data["mode"] = "update"
        old_values = [str(s["code"]), s["name"], str(s["mark1"]), str(s["mark2"]), str(s["mark3"]), str(s["exam"])]
        for i in range(6):
            form_entries[i].delete(0, END)
            form_entries[i].insert(0, old_values[i])
        form_frame.tkraise()

def saveForm():
    # the Save button of the form (used for both Add and Update)
    playSelect()
    students = class_data["students"]
    # get what the user typed (strip() removes extra spaces)
    values = []
    for entry in form_entries:
        values.append(entry.get().strip())

    # when adding there is no old student, so we use -1
    if class_data["mode"] == "add":
        own_position = -1
    else:
        own_position = findPosition(str(class_data["selected"]))

    # check what the user typed. problem stays empty if everything is fine
    problem = ""
    if checkNumber(values[0], 1000, 9999) == False:
        problem = "Student number must be a whole number between 1000 and 9999."
    elif values[1] == "" or "," in values[1]:
        problem = "Please type a name (it cannot have a comma in it)."
    elif checkNumber(values[2], 0, 20) == False or checkNumber(values[3], 0, 20) == False or checkNumber(values[4], 0, 20) == False:
        problem = "Each course mark must be a whole number between 0 and 20."
    elif checkNumber(values[5], 0, 100) == False:
        problem = "The exam mark must be a whole number between 0 and 100."
    elif findPosition(values[0]) != -1 and findPosition(values[0]) != own_position:
        problem = "Another student already has that number."

    if problem != "":
        messagebox.showerror("Error", problem)
    else:
        if class_data["mode"] == "add":
            student = {}
            students.append(student)
        else:
            student = students[own_position]
        student["code"] = int(values[0])
        student["name"] = values[1]
        student["mark1"] = int(values[2])
        student["mark2"] = int(values[3])
        student["mark3"] = int(values[4])
        student["exam"] = int(values[5])
        saveStudents()
        class_data["selected"] = student["code"]
        showList([student])
        messagebox.showinfo("Saved", "The student record was saved in the file.")

def deleteStudent():
    # 7. Delete the chosen student
    playSelect()
    students = class_data["students"]
    position = findPosition(str(class_data["selected"]))
    if position == -1:
        messagebox.showwarning("Warning", "Please choose a student first (click a green Select button).")
    elif messagebox.askyesno("Delete", f"Are you sure you want to delete {students[position]['name']}?"):
        # build a new list with everyone EXCEPT the deleted student
        kept = []
        for i in range(len(students)):
            if i != position:
                kept.append(students[i])
        class_data["students"] = kept
        class_data["selected"] = -1
        saveStudents()
        showList(kept)

# ---------- WINDOW SETUP ----------
root = Tk()
root.title("Student Manager")
root.geometry("900x500")
root.resizable(0, 0)
root.config(bg=BACKGROUND)

# ---------- TOP BAR: title and search bar ----------
top_bar = Frame(root, bg=DARK_COLOUR)
top_bar.place(x=0, y=0, width=900, height=56)
Label(top_bar, text="Student Manager", font=(FONT, 16, "bold"), bg=DARK_COLOUR, fg="white").place(x=15, y=12)

search_entry = Entry(top_bar, font=(FONT, 12))
search_entry.place(x=250, y=14, width=300, height=28)
search_entry.bind("<Button-1>", lambda event: playSelect())   # clicking the search bar makes the click sound
Button(top_bar, text="Search", font=(FONT, 10, "bold"), bg=GREEN_COLOUR, fg="white",
       command=viewOne).place(x=560, y=14, width=90, height=28)

summary_label = Label(root, text="", font=(FONT, 10, "bold"), bg=BACKGROUND, fg="white")
summary_label.place(x=10, y=64)

# ---------- THE TABLE ----------
table_frame = Frame(root, bg=DARK_COLOUR)
table_frame.place(x=10, y=90, width=740, height=330)

# the heading row
for c in range(7):
    Label(table_frame, text=HEADINGS[c], font=(FONT, 9, "bold"), bg=HEADER_COLOUR, fg="white").place(
        x=COLUMN_X[c], y=0, width=COLUMN_WIDTHS[c] - 1, height=29)

# the 10 rows. Every row has 7 labels and one Select button
row_labels = []    # a list of rows, each row is a list of 7 labels
row_buttons = []   # the 10 Select buttons
for r in range(ROWS):
    one_row = []
    for c in range(7):
        label = Label(table_frame, text="", font=(FONT, 10), fg="white")
        label.place(x=COLUMN_X[c], y=30 + r * 30, width=COLUMN_WIDTHS[c] - 1, height=29)
        one_row.append(label)
    row_labels.append(one_row)

    # row=r saves this button's row number inside the lambda
    button = Button(table_frame, text="", font=(FONT, 9, "bold"), fg="white", command=lambda row=r: selectRow(row))
    button.place(x=COLUMN_X[6] + 6, y=30 + r * 30 + 3, width=67, height=24)
    row_buttons.append(button)

# under the table: "Showing 1 to 10" and the page buttons
footer_label = Label(root, text="", font=(FONT, 10, "bold"), bg=BACKGROUND, fg="white")
footer_label.place(x=10, y=426, width=740, height=22)
Button(root, text="<<", font=(FONT, 10, "bold"), bg=DARK_COLOUR, fg="white",
       command=lambda: changePage(-1)).place(x=300, y=455, width=70, height=32)
Button(root, text=">>", font=(FONT, 10, "bold"), bg=DARK_COLOUR, fg="white",
       command=lambda: changePage(1)).place(x=390, y=455, width=70, height=32)

# ---------- THE FORM (it sits on top of the table when it is needed) ----------
form_frame = Frame(root, bg=ROW_COLOUR)
form_frame.place(x=10, y=90, width=740, height=330)
Label(form_frame, text="Student details", font=(FONT, 14, "bold"), bg=ROW_COLOUR, fg="white").place(relx=0.5, y=10, anchor=N)

form_texts = ["Student Number", "Name", "Course Mark 1 (out of 20)", "Course Mark 2 (out of 20)",
              "Course Mark 3 (out of 20)", "Exam Mark (out of 100)"]
form_entries = []   # the 6 typing boxes
for i in range(6):
    Label(form_frame, text=form_texts[i], font=(FONT, 10), bg=ROW_COLOUR, fg="white").place(x=200, y=52 + i * 36)
    entry = Entry(form_frame, font=(FONT, 11))
    entry.place(x=380, y=50 + i * 36, width=200, height=26)
    form_entries.append(entry)
Button(form_frame, text="Save", font=(FONT, 11, "bold"), bg=GREEN_COLOUR, fg="white",
       command=saveForm).place(x=300, y=274, width=140, height=36)

# ---------- TABS ON THE RIGHT (the 8 menu options) ----------
tab_texts = ["1. View all records", "2. View one record", "3. Highest mark", "4. Lowest mark",
             "5. Sort records", "6. Add a record", "7. Delete a record", "8. Update a record"]
tab_functions = [viewAll, viewOne, lambda: showExtreme(True), lambda: showExtreme(False),
                 sortStudents, addStudent, deleteStudent, updateStudent]
for i in range(8):
    Button(root, text=tab_texts[i], font=(FONT, 10, "bold"), bg=BLUE_COLOUR, fg="white",
           command=tab_functions[i]).place(x=765, y=90 + i * 46, width=125, height=40)

# ---------- START THE PROGRAM ----------
loadStudents()                     # read the file when the program starts
showList(class_data["students"])   # show everyone in the table

# the opening sound plays ONE time, when the program starts (nothing else uses it)
pygame.mixer.music.load(os.path.join(ITEMS_FOLDER, "open.mp3"))
pygame.mixer.music.play()
root.mainloop()