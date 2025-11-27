"""
Simple Addition Quiz — Feature-rich Tkinter App (Upgraded with Difficulty Modes)

New Feature Added:
 - Difficulty Modes: Easy / Medium / Hard
 - Easy (1–20), Medium (20–99), Hard (100–999)

Other Features:
 - Simple addition questions
 - Visual feedback (green/red)
 - Progress bar
 - Theme selection
 - "Next Question" button
 - Restart button
 - User profiles (enter your name)
 - Local leaderboard
 - One-shot hint
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# -----------------------------
# Config & Data Storage Helpers
# -----------------------------
LEADERBOARD_FILE = "leaderboard.json"
TOTAL_QUESTIONS = 10

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_score_to_leaderboard(name, score):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "date": datetime.now().isoformat()})
    lb = sorted(lb, key=lambda x: x["score"], reverse=True)[:50]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(lb, f, indent=2)

# -----------------------------
# App Class
# -----------------------------
class AdditionQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Addition Quiz")
        self.root.geometry("760x520")
        self.root.resizable(False, False)

        # App state
        self.player_name = ""
        self.theme = "Colorful"
        self.difficulty = "Easy"
        self.font_choice = ("Arial", 14)
        self.score = 0
        self.q_index = 0
        self.attempt = 1
        self.current_q = None
        self.hint_used = False

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.show_menu()

    # -----------------------------
    # THEMES
    # -----------------------------
    def apply_theme(self):
        """Apply theme colors to the window."""
        if self.theme == "Colorful":
            self.colors = {
                "bg": "#70943D",
                "panel": "#234EB2",
                "accent": "#FF6B6B",
                "button": "#4D96FF",
                "text": "#222222",
                "good": "#2E8B57",
                "bad": "#C0392B",
            }
            self.font_choice = ("Comic Sans MS", 14)

        elif self.theme == "Dark":
            self.colors = {
                "bg": "#1f2933",
                "panel": "#0b1220",
                "accent": "#7dd3fc",
                "button": "#2563eb",
                "text": "#E6EEF3",
                "good": "#10b981",
                "bad": "#ef4444",
            }
            self.font_choice = ("Arial", 13)

        elif self.theme == "Pastel":
            self.colors = {
                "bg": "#FDF6F0",
                "panel": "#F0C4C4",
                "accent": "#F5C6C2",
                "button": "#F2D7D9",
                "text": "#4B4B4B",
                "good": "#7FB77E",
                "bad": "#FF6F6F",
            }
            self.font_choice = ("Arial", 14)

        self.root.configure(bg=self.colors["bg"])

    # -----------------------------
    # MENU SCREEN
    # -----------------------------
    def show_menu(self):
        self.clear_main()
        self.apply_theme()

        left = tk.Frame(self.main_frame, bg=self.colors["panel"], padx=20, pady=20)
        left.place(relx=0.05, rely=0.05, relwidth=0.45, relheight=0.9)

        tk.Label(left, text="Welcome!", font=(self.font_choice[0], 20, "bold"),
                 fg=self.colors["text"], bg=self.colors["panel"]).pack(anchor="w")

        tk.Label(left, text="Enter your name:", font=self.font_choice,
                 fg=self.colors["text"], bg=self.colors["panel"]).pack(anchor="w", pady=(12,4))
        self.name_entry = tk.Entry(left, font=self.font_choice, width=28)
        self.name_entry.pack(anchor="w")

        # Theme select
        tk.Label(left, text="Select Theme:", font=self.font_choice,
                 fg=self.colors["text"], bg=self.colors["panel"]).pack(anchor="w", pady=(12,4))
        self.theme_var = tk.StringVar(value=self.theme)
        theme_menu = ttk.Combobox(left, textvariable=self.theme_var,
                                  values=["Colorful", "Dark", "Pastel"], state="readonly", width=20)
        theme_menu.pack(anchor="w")
        theme_menu.bind("<<ComboboxSelected>>", self.on_theme_change)

        # Difficulty select
        tk.Label(left, text="Select Difficulty:", font=self.font_choice,
                 fg=self.colors["text"], bg=self.colors["panel"]).pack(anchor="w", pady=(12,4))
        self.diff_var = tk.StringVar(value=self.difficulty)
        diff_menu = ttk.Combobox(left, textvariable=self.diff_var,
                                 values=["Easy", "Medium", "Hard"], state="readonly", width=20)
        diff_menu.pack(anchor="w")
        diff_menu.bind("<<ComboboxSelected>>", self.on_difficulty_change)

        start_btn = tk.Button(left, text="Start Quiz", font=(self.font_choice[0], 14, "bold"),
                              bg=self.colors["button"], fg="white",
                              command=self.start_quiz)
        start_btn.pack(pady=18, anchor="w")

        lb_btn = tk.Button(left, text="View Leaderboard", font=self.font_choice,
                           bg="#f3f4f6", command=self.show_leaderboard)
        lb_btn.pack(anchor="w", pady=(6,0))

        clear_lb_btn = tk.Button(left, text="Clear Leaderboard (dangerous)",
                                 font=("Arial", 10), bg="#ffdddd",
                                 command=self.clear_leaderboard_confirm)
        clear_lb_btn.pack(anchor="w", pady=(12,0))

        # Right panel (instructions)
        right = tk.Frame(self.main_frame, bg=self.colors["panel"], padx=16, pady=20)
        right.place(relx=0.53, rely=0.05, relwidth=0.42, relheight=0.9)

        tk.Label(right, text="How it works", font=(self.font_choice[0], 18, "bold"),
                 fg=self.colors["text"], bg=self.colors["panel"]).pack(anchor="w")

        instructions = [
            "• Only addition questions.",
            f"• {TOTAL_QUESTIONS} questions per quiz.",
            "• 10 points first try, 5 points second try.",
            "• One hint per question.",
            "• Difficulty changes the number sizes.",
            "• Score saved in leaderboard.",
        ]
        for t in instructions:
            tk.Label(right, text=t, font=self.font_choice,
                     fg=self.colors["text"], bg=self.colors["panel"]
                     ).pack(anchor="w", pady=4)

    def on_theme_change(self, _evt):
        self.theme = self.theme_var.get()
        self.show_menu()

    def on_difficulty_change(self, _evt):
        self.difficulty = self.diff_var.get()
        self.show_menu()

    def clear_leaderboard_confirm(self):
        if messagebox.askyesno("Clear Leaderboard", "Erase all saved scores?"):
            try:
                if os.path.exists(LEADERBOARD_FILE):
                    os.remove(LEADERBOARD_FILE)
                messagebox.showinfo("Done", "Leaderboard cleared.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # -----------------------------
    # QUIZ CONTROL
    # -----------------------------
    def start_quiz(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Please enter your name.")
            return

        self.player_name = name
        self.score = 0
        self.q_index = 0
        self.attempt = 1
        self.hint_used = False
        self.questions = self.generate_questions(TOTAL_QUESTIONS)
        self.show_quiz_screen()

    # -----------------------------
    # DIFFICULTY LOGIC
    # -----------------------------
    def generate_questions(self, n):
        """Generate questions based on difficulty mode."""
        if self.difficulty == "Easy":
            low, high = 1, 20
        elif self.difficulty == "Medium":
            low, high = 20, 99
        else:  # Hard
            low, high = 100, 999

        return [(random.randint(low, high), random.randint(low, high)) for _ in range(n)]

    # -----------------------------
    # QUIZ UI
    # -----------------------------
    def show_quiz_screen(self):
        self.clear_main()
        self.apply_theme()

        top = tk.Frame(self.main_frame, bg=self.colors["panel"], padx=10, pady=10)
        top.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.16)

        self.progress_label = tk.Label(top, text=f"Question {self.q_index+1} of {TOTAL_QUESTIONS}",
                                       font=(self.font_choice[0], 14),
                                       fg=self.colors["text"], bg=self.colors["panel"])
        self.progress_label.pack(anchor="w")

        self.progress_var = tk.DoubleVar()
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", thickness=16,
                        troughcolor=self.colors["panel"], background=self.colors["accent"])
        self.progressbar = ttk.Progressbar(top, maximum=TOTAL_QUESTIONS,
                                           value=self.q_index, variable=self.progress_var,
                                           style="TProgressbar")
        self.progressbar.pack(fill="x", pady=(8,0))

        mid = tk.Frame(self.main_frame, bg=self.colors["panel"], padx=20, pady=10)
        mid.place(relx=0.02, rely=0.20, relwidth=0.96, relheight=0.56)

        self.question_label = tk.Label(mid, text="", font=(self.font_choice[0], 30, "bold"),
                                       fg=self.colors["text"], bg=self.colors["panel"])
        self.question_label.pack(pady=(10,10))

        entry_frame = tk.Frame(mid, bg=self.colors["panel"])
        entry_frame.pack()

        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(entry_frame, textvariable=self.answer_var,
                                     font=self.font_choice, width=8, justify="center")
        self.answer_entry.pack(side="left", padx=(0,10))

        check_btn = tk.Button(entry_frame, text="Check Answer",
                              bg=self.colors["button"], fg="white",
                              font=(self.font_choice[0], 12, "bold"),
                              command=self.check_answer)
        check_btn.pack(side="left")

        hint_btn = tk.Button(entry_frame, text="Hint", bg="#ffeaa7",
                             command=self.show_hint)
        hint_btn.pack(side="left", padx=(10,0))

        self.feedback_label = tk.Label(mid, text="", font=(self.font_choice[0], 14),
                                       fg=self.colors["text"], bg=self.colors["panel"])
        self.feedback_label.pack(pady=(12,6))

        bottom = tk.Frame(self.main_frame, bg=self.colors["panel"], padx=12, pady=8)
        bottom.place(relx=0.02, rely=0.79, relwidth=0.96, relheight=0.18)

        self.next_btn = tk.Button(bottom, text="Next Question ▶", font=self.font_choice,
                                  state="disabled", bg="#90ee90",
                                  command=self.next_question)
        self.next_btn.pack(side="right", padx=8)

        restart_btn = tk.Button(bottom, text="Restart Quiz", font=self.font_choice,
                                bg="#ffd1dc", command=self.confirm_restart)
        restart_btn.pack(side="left", padx=8)

        show_lb_btn = tk.Button(bottom, text="Leaderboard", font=self.font_choice,
                                bg="#dbeafe", command=self.show_leaderboard)
        show_lb_btn.pack(side="left", padx=8)

        self.load_current_question()

    def load_current_question(self):
        self.hint_used = False
        self.attempt = 1
        self.answer_var.set("")
        a, b = self.questions[self.q_index]
        self.current_q = (a, b)
        self.question_label.config(text=f"{a}  +  {b}  =")
        self.feedback_label.config(text="", fg=self.colors["text"])
        self.next_btn.config(state="disabled")
        self.answer_entry.config(state="normal")
        self.answer_entry.focus_set()
        self.progress_label.config(text=f"Question {self.q_index+1} of {TOTAL_QUESTIONS}")
        self.progressbar["value"] = self.q_index

    # -----------------------------
    # ANSWER LOGIC
    # -----------------------------
    def check_answer(self):
        raw = self.answer_var.get().strip()
        if raw == "":
            messagebox.showwarning("No answer", "Please enter an answer.")
            return
        try:
            val = int(raw)
        except ValueError:
            messagebox.showerror("Invalid", "Enter a whole number.")
            return

        a, b = self.current_q
        correct = a + b

        if val == correct:
            gained = 10 if self.attempt == 1 else 5
            self.score += gained
            self.feedback_label.config(text=f"Correct! +{gained} points", fg=self.colors["good"])
            self.answer_entry.config(state="disabled")
            self.next_btn.config(state="normal")
        else:
            if self.attempt == 1:
                self.feedback_label.config(text="Wrong — try again!", fg=self.colors["bad"])
                self.attempt = 2
                self.answer_var.set("")
                self.answer_entry.focus_set()
            else:
                self.feedback_label.config(text=f"Wrong again. Correct answer: {correct}",
                                           fg=self.colors["bad"])
                self.answer_entry.config(state="disabled")
                self.next_btn.config(state="normal")

    def show_hint(self):
        if self.hint_used:
            messagebox.showinfo("Hint", "You already used the hint.")
            return
        a, b = self.current_q
        big, small = max(a,b), min(a,b)
        hint_text = f"Hint: Start from {big} and add {small}."
        self.feedback_label.config(text=hint_text, fg="#b36b00")
        self.hint_used = True

    # -----------------------------
    # NAVIGATION
    # -----------------------------
    def next_question(self):
        self.q_index += 1
        if self.q_index >= TOTAL_QUESTIONS:
            self.finish_quiz()
        else:
            self.load_current_question()

    def finish_quiz(self):
        save_score_to_leaderboard(self.player_name, self.score)
        self.show_results_screen()

    def confirm_restart(self):
        if messagebox.askyesno("Restart", "Restart the quiz?"):
            self.start_quiz()

    # -----------------------------
    # RESULTS UI
    # -----------------------------
    def show_results_screen(self):
        self.clear_main()
        self.apply_theme()

        frame = tk.Frame(self.main_frame, bg=self.colors["panel"])
        frame.place(relx=0.05, rely=0.06, relwidth=0.9, relheight=0.88)

        tk.Label(frame, text="Quiz Complete!", font=(self.font_choice[0], 24, "bold"),
                 fg=self.colors["text"], bg=self.colors["panel"]).pack(pady=20)

        tk.Label(frame, text=f"{self.player_name}, your score: {self.score}/{TOTAL_QUESTIONS * 10}",
                 font=self.font_choice, fg=self.colors["text"], bg=self.colors["panel"]).pack(pady=6)

        grade = self.calculate_grade()
        tk.Label(frame, text=f"Grade: {grade}",
                 font=(self.font_choice[0], 16, "bold"),
                 fg=self.colors["accent"], bg=self.colors["panel"]).pack(pady=10)

        btn_frame = tk.Frame(frame, bg=self.colors["panel"])
        btn_frame.pack(pady=18)

        tk.Button(btn_frame, text="Play Again", font=self.font_choice,
                  bg="#90ee90", command=self.start_quiz).grid(row=0, column=0, padx=6)

        tk.Button(btn_frame, text="Main Menu", font=self.font_choice,
                  bg="#93c5fd", command=self.show_menu).grid(row=0, column=1, padx=6)

        tk.Button(btn_frame, text="Leaderboard", font=self.font_choice,
                  bg="#ffd7a8", command=self.show_leaderboard).grid(row=0, column=2, padx=6)

    def calculate_grade(self):
        pct = (self.score / (TOTAL_QUESTIONS * 10)) * 100
        if pct >= 90:
            return "A+"
        elif pct >= 80:
            return "A"
        elif pct >= 70:
            return "B"
        elif pct >= 60:
            return "C"
        else:
            return "D"

    # -----------------------------
    # LEADERBOARD
    # -----------------------------
    def show_leaderboard(self):
        self.clear_main()
        self.apply_theme()

        frame = tk.Frame(self.main_frame, bg=self.colors["panel"])
        frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        tk.Label(frame, text="Leaderboard", font=(self.font_choice[0], 20, "bold"),
                 fg=self.colors["text"], bg=self.colors["panel"]).pack(pady=12)

        lb = load_leaderboard()
        if not lb:
            tk.Label(frame, text="No scores yet.", font=self.font_choice,
                     fg=self.colors["text"], bg=self.colors["panel"]).pack(pady=10)
        else:
            for i, rec in enumerate(lb[:10], start=1):
                txt = f"{i}. {rec['name']} — {rec['score']} pts — {rec['date'][:19].replace('T',' ')}"
                tk.Label(frame, text=txt, font=self.font_choice,
                         fg=self.colors["text"], bg=self.colors["panel"], anchor="w"
                         ).pack(fill="x", padx=12)

        tk.Button(frame, text="Back to Menu", font=self.font_choice,
                  bg="#c7f9cc", command=self.show_menu).pack(pady=12)

    # -----------------------------
    # UTILITIES
    # -----------------------------
    def clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()


# -----------------------------
# Launch
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AdditionQuizApp(root)
    root.mainloop()
