# Student Manager - Exercise 3

# Imports
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pygame
import os

# File location and colours
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
ASSETS_FOLDER = os.path.join(BASE_FOLDER, "Assets3")
STUDENT_FILE = os.path.join(ASSETS_FOLDER, "studentMarks.txt")
NAVY = "#17324D"
BLUE = "#244C68"
TEAL = "#159D9A"
LIGHT = "#F2F6FA"
WHITE = "#FFFFFF"
TEXT = "#203247"
GREY = "#718096"
BORDER = "#DCE5ED"
RED = "#D9534F"
FONT = "Segoe UI"

students = []  # All student records are kept in this list.

# Main window and program icon
root = Tk()
root.title("Student Manager")
root.geometry("1240x780")
root.minsize(1100, 700)
root.config(bg=LIGHT)
app_icon = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_FOLDER, "icon.png")))
root.iconphoto(True, app_icon)
# Button sound from Assets3
button_sound = None
try:
    pygame.mixer.init()
    button_sound = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, "button.mp3"))
except:
    button_sound = None
def play_sound(event=None):
    if button_sound != None:
        button_sound.play()
def make_button(parent, text, command, colour=TEAL):
    button = Button(parent, text=text, command=command, bg=colour, fg=WHITE,
                    activebackground=BLUE, activeforeground=WHITE,
                    font=(FONT, 10, "bold"), relief=FLAT, padx=14, pady=9)
    button.bind("<Button-1>", play_sound, add="+")
    return button

# Read the student information from the text file.
def load_students():
    students.clear()
    if os.path.exists(STUDENT_FILE) == False:
        with open(STUDENT_FILE, "w") as file:
            file.write("0\n")
    with open(STUDENT_FILE, "r") as file:
        lines = file.readlines()
    # The first line is the number of students. Records start on the next line.
    for line in lines[1:]:
        details = line.strip().split(",")
        if len(details) == 6:
            try:
                student = {"code": int(details[0]), "name": details[1],
                           "course1": int(details[2]), "course2": int(details[3]),
                           "course3": int(details[4]), "exam": int(details[5])}
                students.append(student)
            except ValueError:
                messagebox.showwarning("File warning", "A record has invalid numbers and was skipped.")

# Save the records and update the student count on the first line.
def save_students():
    with open(STUDENT_FILE, "w") as file:
        file.write(str(len(students)) + "\n")
        for student in students:
            line = "{},{},{},{},{},{}\n".format(
                student["code"], student["name"], student["course1"],
                student["course2"], student["course3"], student["exam"]
            )
            file.write(line)

# Calculate a student's marks and grade.
def coursework_total(student):
    return student["course1"] + student["course2"] + student["course3"]
def overall_total(student):
    return coursework_total(student) + student["exam"]
def percentage(student):
    return overall_total(student) / 160 * 100
def grade(student):
    mark = percentage(student)
    if mark >= 70:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 40:
        return "D"
    else:
        return "F"
def find_student(code):
    for student in students:
        if student["code"] == code:
            return student
    return None
def student_report(student):
    return ("STUDENT RESULT\n\nName: {}\nStudent code: {}\nCoursework: {} / 60\n"
            "Exam mark: {} / 100\nOverall mark: {} / 160\nPercentage: {:.2f}%\nGrade: {}"
            ).format(student["name"], student["code"], coursework_total(student),
                     student["exam"], overall_total(student), percentage(student), grade(student))

# Main screen layout
header = Frame(root, bg=NAVY, height=70)
header.pack(fill=X)
header.pack_propagate(False)
Label(header, text="STUDENT MANAGER", bg=NAVY, fg=WHITE, font=(FONT, 21, "bold")).pack(side=LEFT, padx=28)
Label(
    header, text="STUDENT RECORDS  |  RESULTS  |  REPORTS",
    bg=NAVY, fg="#C7D8E6", font=(FONT, 9, "bold")
).pack(side=RIGHT, padx=28)
body = Frame(root, bg=LIGHT)
body.pack(fill=BOTH, expand=YES)
sidebar = Frame(body, bg=BLUE, width=220)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)
content = Frame(body, bg=LIGHT)
content.pack(side=LEFT, fill=BOTH, expand=YES, padx=26, pady=20)
page_title = Label(content, text="Dashboard", bg=LIGHT, fg=TEXT, font=(FONT, 23, "bold"))
page_title.pack(anchor=W)
page_description = Label(
    content, text="Manage student records and review class results.",
    bg=LIGHT, fg=GREY, font=(FONT, 10)
)
page_description.pack(anchor=W, pady=(3, 15))
page_area = Frame(content, bg=LIGHT)
page_area.pack(fill=BOTH, expand=YES)

def show_page(title, description):
    # Remove the old page when a new menu option is selected.
    for widget in page_area.winfo_children():
        widget.destroy()
    page_title.config(text=title)
    page_description.config(text=description)

def report_box(parent, report):
    # A large, scrollable text area displays the student list and reports.
    panel = Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    panel.pack(fill=BOTH, expand=YES, pady=(8, 0))
    scroll_bar = Scrollbar(panel)
    scroll_bar.pack(side=RIGHT, fill=Y)
    report_text = Text(panel, font=("Consolas", 13), bg=WHITE, fg=TEXT,
                       wrap=NONE, padx=18, pady=16, yscrollcommand=scroll_bar.set)
    report_text.pack(side=LEFT, fill=BOTH, expand=YES)
    scroll_bar.config(command=report_text.yview)
    report_text.insert(END, report)
    report_text.config(state=DISABLED)

def result_table(record_list):
    report = "STUDENT NAME                 CODE     COURSEWORK     EXAM     TOTAL       PERCENT    GRADE\n"
    report += "-" * 100 + "\n"
    for student in record_list:
        line = "{:<28} {:<8} {:<14} {:<8} {:<11} {:<10} {}\n".format(
            student["name"][:27], student["code"], str(coursework_total(student)) + "/60",
            student["exam"], str(overall_total(student)) + "/160",
            format(percentage(student), ".1f") + "%", grade(student))
        report += line
    return report

# 1. View all student records and the class average.
def show_all_students():
    show_page("All student records", "The full student list. Scroll to see every student.")
    if len(students) == 0:
        report_box(page_area, "There are no student records yet.")
        return
    report = result_table(students)
    average = 0
    for student in students:
        average += percentage(student)
    average = average / len(students)
    report += "\nNumber of students: " + str(len(students))
    report += "\nClass average: " + format(average, ".2f") + "%"
    report_box(page_area, report)

# 2. Search for a student by name or student code.
def show_find_student():
    show_page("Find a student", "Search by student name or student code.")
    panel = Frame(
        page_area, bg=WHITE, padx=18, pady=18,
        highlightbackground=BORDER, highlightthickness=1
    )
    panel.pack(fill=X)
    Label(panel, text="Student name or code", bg=WHITE, fg=TEXT, font=(FONT, 10, "bold")).pack(side=LEFT)
    search_entry = Entry(panel, font=(FONT, 12), width=27)
    search_entry.pack(side=LEFT, padx=14, ipady=6)
    result_area = Frame(page_area, bg=LIGHT)
    result_area.pack(fill=BOTH, expand=YES)
    def search_student():
        for widget in result_area.winfo_children():
            widget.destroy()
        value = search_entry.get().strip().lower()
        found = None
        for student in students:
            if value == str(student["code"]) or value == student["name"].lower():
                found = student
        if found == None:
            report_box(result_area, "No student found. Check the name or code.")
        else:
            report_box(result_area, student_report(found))
    make_button(panel, "Search", search_student).pack(side=LEFT)

# 3 and 4. Show the student with the highest or lowest total mark.
def show_top_or_bottom(highest):
    if highest == True:
        title = "Highest overall mark"
        description = "The student with the highest total mark out of 160."
    else:
        title = "Lowest overall mark"
        description = "The student with the lowest total mark out of 160."
    show_page(title, description)
    if len(students) == 0:
        report_box(page_area, "There are no student records yet.")
        return
    chosen = students[0]
    for student in students:
        if highest == True and overall_total(student) > overall_total(chosen):
            chosen = student
        elif highest == False and overall_total(student) < overall_total(chosen):
            chosen = student
    report_box(page_area, student_report(chosen))

# 5. Sort records from highest to lowest or lowest to highest.
def show_sort_page():
    show_page("Sort student records", "Choose how to arrange students by their overall mark.")
    panel = Frame(
        page_area, bg=WHITE, padx=18, pady=16,
        highlightbackground=BORDER, highlightthickness=1
    )
    panel.pack(fill=X)
    result_area = Frame(page_area, bg=LIGHT)
    result_area.pack(fill=BOTH, expand=YES)
    def sort_records(high_to_low):
        sorted_students = []
        for student in students:
            sorted_students.append(student)
        # Compare neighbours and swap them if they are in the wrong order.
        for i in range(len(sorted_students)):
            for j in range(len(sorted_students) - 1):
                first = overall_total(sorted_students[j])
                second = overall_total(sorted_students[j + 1])
                if high_to_low == True and first < second:
                    sorted_students[j], sorted_students[j + 1] = sorted_students[j + 1], sorted_students[j]
                elif high_to_low == False and first > second:
                    sorted_students[j], sorted_students[j + 1] = sorted_students[j + 1], sorted_students[j]
        for widget in result_area.winfo_children():
            widget.destroy()
        if len(sorted_students) == 0:
            report_box(result_area, "There are no student records to sort.")
        else:
            report_box(result_area, result_table(sorted_students))
    make_button(panel, "Highest to lowest", lambda: sort_records(True)).pack(side=LEFT, padx=(0, 10))
    make_button(panel, "Lowest to highest", lambda: sort_records(False), BLUE).pack(side=LEFT)

# Create the six entry boxes for adding and updating a student.
def make_student_form(parent):
    fields = {}
    labels = ["Student code", "Student name", "Course mark 1", "Course mark 2", "Course mark 3", "Exam mark"]
    keys = ["code", "name", "course1", "course2", "course3", "exam"]
    for i in range(6):
        row = i // 2
        column = (i % 2) * 2
        Label(
            parent, text=labels[i], bg=WHITE, fg=TEXT,
            font=(FONT, 9, "bold")
        ).grid(row=row, column=column, sticky=W, padx=(0, 8), pady=9)
        entry = Entry(parent, font=(FONT, 11), width=24)
        entry.grid(row=row, column=column + 1, sticky=W, padx=(0, 25), pady=9, ipady=5)
        fields[keys[i]] = entry
    return fields

# Check the information before saving a student.
def read_student_form(fields):
    try:
        code = int(fields["code"].get())
        course1 = int(fields["course1"].get())
        course2 = int(fields["course2"].get())
        course3 = int(fields["course3"].get())
        exam = int(fields["exam"].get())
    except ValueError:
        messagebox.showerror("Invalid information", "Enter numbers in the code and mark boxes.")
        return None
    name = fields["name"].get().strip()
    if code < 1000 or code > 9999:
        messagebox.showerror("Invalid code", "Student code must be between 1000 and 9999.")
        return None
    if name == "" or "," in name:
        messagebox.showerror("Invalid name", "Enter a name without commas.")
        return None
    for mark in [course1, course2, course3]:
        if mark < 0 or mark > 20:
            messagebox.showerror("Invalid coursework", "Each course mark must be between 0 and 20.")
            return None
    if exam < 0 or exam > 100:
        messagebox.showerror("Invalid exam mark", "Exam mark must be between 0 and 100.")
        return None
    return {"code": code, "name": name, "course1": course1,
            "course2": course2, "course3": course3, "exam": exam}

# 6 and 7. Use one form to add a new student or update an existing one.
def show_student_form(update):
    if update == True:
        show_page("Update a student", "Find a student by code, edit their details and save.")
        search_panel = Frame(page_area, bg=WHITE, padx=18, pady=14)
        search_panel.pack(fill=X, pady=(0, 10))
        Label(search_panel, text="Student code", bg=WHITE, fg=TEXT).pack(side=LEFT)
        search_entry = Entry(search_panel, font=(FONT, 11), width=18)
        search_entry.pack(side=LEFT, padx=12, ipady=5)
    else:
        show_page("Add a student", "Enter the student's details and marks.")
    panel = Frame(page_area, bg=WHITE, padx=22, pady=20, highlightbackground=BORDER, highlightthickness=1)
    panel.pack(fill=X)
    Label(panel, text="STUDENT DETAILS", bg=WHITE, fg=BLUE, font=(FONT, 11, "bold")).pack(anchor=W)
    fields = make_student_form(panel)
    selected_code = {"value": None}
    def load_record():
        try:
            code = int(search_entry.get())
        except ValueError:
            messagebox.showerror("Invalid code", "Enter a student code using numbers.")
            return
        student = find_student(code)
        if student == None:
            messagebox.showerror("Not found", "No student has that code.")
            return
        selected_code["value"] = code
        for key in fields:
            fields[key].delete(0, END)
            fields[key].insert(0, str(student[key]))
    def save_record():
        new_student = read_student_form(fields)
        if new_student == None:
            return
        if update == True and selected_code["value"] == None:
            messagebox.showwarning("Load a student", "Find a student before saving changes.")
            return
        for student in students:
            if student["code"] == new_student["code"] and student["code"] != selected_code["value"]:
                messagebox.showerror("Duplicate code", "That student code is already in use.")
                return
        if update == True:
            for i in range(len(students)):
                if students[i]["code"] == selected_code["value"]:
                    students[i] = new_student
            messagebox.showinfo("Updated", "The student record has been updated.")
        else:
            students.append(new_student)
            messagebox.showinfo("Added", "The student record has been saved.")
        save_students()
        show_all_students()
    if update == True:
        make_button(search_panel, "Load student", load_record, BLUE).pack(side=LEFT)
        make_button(panel, "Save changes", save_record).pack(anchor=W, pady=(12, 0))
    else:
        make_button(panel, "Add student", save_record).pack(anchor=W, pady=(12, 0))

# 8. Delete a student after confirmation.
def show_delete_student():
    show_page("Delete a student", "Enter a student code and confirm before removing the record.")
    panel = Frame(page_area, bg=WHITE, padx=22, pady=22, highlightbackground=BORDER, highlightthickness=1)
    panel.pack(fill=X)
    Label(panel, text="Student code", bg=WHITE, fg=TEXT, font=(FONT, 10, "bold")).pack(anchor=W)
    code_entry = Entry(panel, font=(FONT, 12), width=25)
    code_entry.pack(anchor=W, pady=10, ipady=6)
    def delete_record():
        try:
            code = int(code_entry.get())
        except ValueError:
            messagebox.showerror("Invalid code", "Enter a student code using numbers.")
            return
        student = find_student(code)
        if student == None:
            messagebox.showerror("Not found", "No student has that code.")
            return
        answer = messagebox.askyesno("Confirm deletion", "Delete " + student["name"] + "'s record?")
        if answer == True:
            students.remove(student)
            save_students()
            messagebox.showinfo("Deleted", "The student record has been removed.")
            show_all_students()
    make_button(panel, "Delete student", delete_record, RED).pack(anchor=W)

# Dashboard summary
def show_dashboard():
    show_page("Dashboard", "A quick overview of student records and class performance.")
    count, average, highest = len(students), 0, 0
    highest_name = "No students yet"
    for student in students:
        average += percentage(student)
        if overall_total(student) > highest:
            highest = overall_total(student)
            highest_name = student["name"]
    if count > 0:
        average = average / count
    cards = Frame(page_area, bg=LIGHT)
    cards.pack(fill=X, pady=(0, 16))
    values = [("TOTAL STUDENTS", str(count)), ("CLASS AVERAGE", format(average, ".1f") + "%"),
              ("HIGHEST MARK", str(highest) + " / 160")]
    for title, value in values:
        card = Frame(cards, bg=WHITE, padx=18, pady=17, highlightbackground=BORDER, highlightthickness=1)
        card.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)
        Label(
            card, text=title + "\n" + value, bg=WHITE, fg=NAVY,
            font=(FONT, 15, "bold"), justify=LEFT
        ).pack(anchor=W)
    welcome = Frame(page_area, bg=WHITE, padx=22, pady=20, highlightbackground=BORDER, highlightthickness=1)
    welcome.pack(fill=BOTH, expand=YES)
    welcome_text = (
        "WELCOME TO STUDENT MANAGER\n"
        "Use the menu to view results or manage student records.\n\n"
        "TOP STUDENT\n" + highest_name +
        "\n\nGRADE GUIDE\n"
        "A: 70%+   B: 60-69%   C: 50-59%   D: 40-49%   F: Below 40%"
    )
    Label(
        welcome, text=welcome_text, bg=WHITE, fg=TEXT,
        justify=LEFT, font=(FONT, 12)
    ).pack(anchor=W)

# Navigation menu
Label(sidebar, text="OVERVIEW", bg=BLUE, fg="#C7D8E6", font=(FONT, 9, "bold")).pack(anchor=W, padx=20, pady=(25, 8))
menu_items = [("Dashboard", show_dashboard), ("All student records", show_all_students),
              ("Find a student", show_find_student), ("Highest overall mark", lambda: show_top_or_bottom(True)),
              ("Lowest overall mark", lambda: show_top_or_bottom(False)), ("Sort records", show_sort_page)]
for text, command in menu_items:
    make_button(sidebar, text, command, BLUE).pack(fill=X, padx=8, pady=2)
Label(
    sidebar, text="MANAGE RECORDS", bg=BLUE, fg="#C7D8E6",
    font=(FONT, 9, "bold")
).pack(anchor=W, padx=20, pady=(24, 8))
manage_items = [
    ("Add student", lambda: show_student_form(False)),
    ("Update student", lambda: show_student_form(True)),
    ("Delete student", show_delete_student)
]
for text, command in manage_items:
    make_button(sidebar, text, command, BLUE).pack(fill=X, padx=8, pady=2)
Label(sidebar, text="DATA FILE\nAssets3 / studentMarks.txt", bg=BLUE, fg="#C7D8E6",
      font=(FONT, 9), justify=LEFT).pack(side=BOTTOM, anchor=W, padx=20, pady=22)

# Load the records and open the dashboard.
load_students()
show_dashboard()
root.mainloop()
