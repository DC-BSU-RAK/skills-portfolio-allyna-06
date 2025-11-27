import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

FILE_PATH = "studentMarks.txt"

# ----------------------- THEMES -----------------------

DARK_THEME = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "frame": "#2a2a2a",
    "entry": "#2d2d2d",
    "button": "#3b3b3b",
    "accent": "#4ea3ff",
}

PASTEL_THEME = {
    "bg": "#f7f5ff",
    "fg": "#3a3a3a",
    "frame": "#ffffff",
    "entry": "#ffffff",
    "button": "#f0ebff",
    "accent": "#c3b6ff",
}

current_theme = DARK_THEME


def apply_theme(widget):
    """Apply theme to the entire window recursively"""
    widget.configure(bg=current_theme["bg"])

    for child in widget.winfo_children():
        if isinstance(child, (tk.Frame, tk.LabelFrame)):
            child.configure(bg=current_theme["frame"])
        if isinstance(child, tk.Label):
            child.configure(bg=current_theme["frame"], fg=current_theme["fg"])
        if isinstance(child, tk.Button):
            child.configure(
                bg=current_theme["button"], fg=current_theme["fg"], activebackground=current_theme["accent"]
            )
        if isinstance(child, tk.Entry):
            child.configure(
                bg=current_theme["entry"], fg=current_theme["fg"], insertbackground=current_theme["fg"]
            )
        if isinstance(child, ttk.Treeview):
            style = ttk.Style()
            style.theme_use("default")
            style.configure(
                "Treeview",
                background=current_theme["frame"],
                foreground=current_theme["fg"],
                fieldbackground=current_theme["frame"],
                rowheight=25,
                bordercolor=current_theme["fg"],
                borderwidth=1
            )
            style.configure("Treeview.Heading", background=current_theme["button"], foreground=current_theme["fg"])
            style.map("Treeview", background=[("selected", current_theme["accent"])])
        apply_theme(child)


def toggle_theme():
    global current_theme
    current_theme = PASTEL_THEME if current_theme == DARK_THEME else DARK_THEME
    apply_theme(root)


# ----------------------- Helper Functions -----------------------

def load_students():
    students = []
    if not os.path.exists(FILE_PATH):
        return students

    with open(FILE_PATH, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) < 7:
                continue
            s = {
                "code": parts[0],
                "name": parts[1],
                "course1": int(parts[2]),
                "course2": int(parts[3]),
                "course3": int(parts[4]),
                "exam": int(parts[5]),
                "attendance": int(parts[6])
            }
            students.append(s)
    return students


def save_students(students):
    with open(FILE_PATH, "w") as f:
        f.write(f"{len(students)}\n")
        for s in students:
            f.write(f"{s['code']},{s['name']},{s['course1']},{s['course2']},{s['course3']},{s['exam']},{s['attendance']}\n")


def total_coursework(s):
    return s["course1"] + s["course2"] + s["course3"]


def overall_total(s):
    return total_coursework(s) + s["exam"]


def overall_percentage(s):
    return (overall_total(s) / 160) * 100


def grade(s):
    pct = overall_percentage(s)
    if pct >= 70: return "A"
    elif pct >= 60: return "B"
    elif pct >= 50: return "C"
    elif pct >= 40: return "D"
    else: return "F"


# ----------------------- TABLE VIEW -----------------------

def update_table(students):
    for row in table.get_children():
        table.delete(row)

    for s in students:
        table.insert("", "end",
                     values=(
                         s["code"],
                         s["name"],
                         s["course1"], s["course2"], s["course3"],
                         s["exam"],
                         total_coursework(s),
                         overall_total(s),
                         f"{overall_percentage(s):.2f}",
                         grade(s),
                         f"{s['attendance']}%"
                     ))


# ----------------------- STUDENT DASHBOARD -----------------------

def open_dashboard(student):
    dash = tk.Toplevel()
    dash.title(f"Dashboard - {student['name']}")
    dash.geometry("700x500")
    apply_theme(dash)

    summary = tk.LabelFrame(dash, text="Student Summary", font=("Arial", 12, "bold"))
    summary.pack(fill="x", padx=10, pady=10)

    info = (
        f"Name: {student['name']}\n"
        f"Code: {student['code']}\n"
        f"Coursework Total: {total_coursework(student)} / 60\n"
        f"Exam: {student['exam']} / 100\n"
        f"Overall Total: {overall_total(student)} / 160\n"
        f"Percentage: {overall_percentage(student):.2f}%\n"
        f"Grade: {grade(student)}\n"
        f"Attendance: {student['attendance']}%"
    )

    tk.Label(summary, text=info, justify="left", font=("Arial", 11)).pack(padx=10, pady=10)

    graph_frame = tk.LabelFrame(dash, text="Marks Bar Graph", font=("Arial", 12, "bold"))
    graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(graph_frame, width=600, height=300, bg="white")
    canvas.pack(pady=10)

    marks = [student["course1"], student["course2"], student["course3"], student["exam"]]
    labels = ["C1", "C2", "C3", "Exam"]

    max_mark = max(marks)
    x = 60
    bar_width = 80

    for i, mark in enumerate(marks):
        height = (mark / max_mark) * 200
        y = 250 - height

        fill_color = current_theme["accent"]

        canvas.create_rectangle(x, y, x + bar_width, 250, fill=fill_color)
        canvas.create_text(x + bar_width / 2, 260, text=labels[i])
        canvas.create_text(x + bar_width / 2, y - 10, text=str(mark))

        x += bar_width + 20


# ----------------------- GUI FUNCTIONS -----------------------

def view_all():
    update_table(load_students())


def search_student(*args):
    query = search_var.get().lower()
    students = load_students()
    results = [s for s in students if query in s["name"].lower() or query in s["code"].lower()]
    update_table(results)


def view_individual():
    code = simpledialog.askstring("Search Student", "Enter student code:")
    if not code: return

    students = load_students()
    s = next((x for x in students if x["code"] == code), None)

    if s:
        open_dashboard(s)
    else:
        messagebox.showerror("Not Found", "Student not found!")


def add_student():
    students = load_students()

    code = simpledialog.askstring("Student Code", "Enter code:")
    if any(s["code"] == code for s in students):
        messagebox.showerror("Error", "Student code already exists!")
        return

    name = simpledialog.askstring("Name", "Enter name:")
    c1 = int(simpledialog.askstring("Course 1 (0–20)", "Enter mark:"))
    c2 = int(simpledialog.askstring("Course 2 (0–20)", "Enter mark:"))
    c3 = int(simpledialog.askstring("Course 3 (0–20)", "Enter mark:"))
    exam = int(simpledialog.askstring("Exam (0–100)", "Enter mark:"))
    attendance = int(simpledialog.askstring("Attendance %", "Enter %:"))

    students.append({
        "code": code, "name": name,
        "course1": c1, "course2": c2, "course3": c3,
        "exam": exam, "attendance": attendance
    })

    save_students(students)
    view_all()
    messagebox.showinfo("Success", "Student added!")


def delete_student():
    students = load_students()
    code = simpledialog.askstring("Delete Student", "Enter student code:")

    student = next((s for s in students if s["code"] == code), None)
    if student:
        students.remove(student)
        save_students(students)
        view_all()
        messagebox.showinfo("Deleted", "Student removed.")
    else:
        messagebox.showerror("Error", "Student not found.")


def update_student():
    students = load_students()
    code = simpledialog.askstring("Update Student", "Enter student code:")
    s = next((x for x in students if x["code"] == code), None)

    if not s:
        messagebox.showerror("Error", "Student not found!")
        return

    field = simpledialog.askstring("Field", "name, course1, course2, course3, exam, attendance")
    if field not in s:
        messagebox.showerror("Error", "Invalid field.")
        return

    new_val = simpledialog.askstring("New Value", f"Enter new value for {field}:")
    s[field] = int(new_val) if field != "name" else new_val

    save_students(students)
    view_all()
    messagebox.showinfo("Updated", "Student updated.")


# ------------------------- MAIN GUI -------------------------

root = tk.Tk()
root.title("Student Manager")
root.geometry("1100x600")

apply_theme(root)

# --- Search bar ---
search_var = tk.StringVar()
search_var.trace("w", search_student)

tk.Label(root, text="Search Student:").pack(pady=5)
search_entry = tk.Entry(root, textvariable=search_var, width=40)
search_entry.pack(pady=5)

# --- Table ---
columns = (
    "Code", "Name", "C1", "C2", "C3", "Exam",
    "Coursework", "Total", "%", "Grade", "Attendance"
)

table = ttk.Treeview(root, columns=columns, show="headings", height=20)
table.pack(fill="both", expand=True)

# Add gridlines
style = ttk.Style()
style.configure("Treeview", bordercolor="gray", borderwidth=1, relief="solid")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=90)

# --- Menu ---
menu = tk.Menu(root)
root.config(menu=menu)

m = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Options", menu=m)
m.add_command(label="View All", command=view_all)
m.add_command(label="View Individual Dashboard", command=view_individual)
m.add_separator()
m.add_command(label="Add Student", command=add_student)
m.add_command(label="Delete Student", command=delete_student)
m.add_command(label="Update Student", command=update_student)
m.add_separator()
m.add_command(label="Toggle Theme", command=toggle_theme)
m.add_separator()
m.add_command(label="Exit", command=root.quit)

view_all()
root.mainloop()
