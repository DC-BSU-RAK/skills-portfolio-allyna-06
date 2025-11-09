# We will be  using Tkinter to build a simple graphical quiz app.
# Tkinter is the standard GUI library for Python — it lets us make windows, buttons, labels, and so on.
import tkinter as tk
from tkinter import messagebox
import random
# This class defines our main Quiz Application.
# Everything (the window, the questions, the timer, etc.) lives inside this one class.

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("420x360")
        self.root.resizable(False, False)

        self.bg_color = "#F4F4F4"
        self.root.configure(bg=self.bg_color)

        self.font_title = ("Arial", 18, "bold")
        self.font_text = ("Arial", 14)
        self.font_small = ("Arial", 11)

        # quiz state variables
        self.difficulty = None
        self.score = 0
        self.question_number = 0
        self.attempt = 1
        self.current_problem = None
        self.timer_seconds = 10  # time per question
        self.time_left = self.timer_seconds
        self.timer_running = False

        self.display_menu()

    # ------------------ UTILITY ------------------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------ MENU ------------------
    def display_menu(self):
        self.clear_window()

        tk.Label(self.root, text="DIFFICULTY LEVEL", font=self.font_title, bg=self.bg_color).pack(pady=15)

        tk.Button(self.root, text="1. Easy", width=25, command=lambda: self.start_quiz("Easy")).pack(pady=6)
        tk.Button(self.root, text="2. Moderate", width=25, command=lambda: self.start_quiz("Moderate")).pack(pady=6)
        tk.Button(self.root, text="3. Advanced", width=25, command=lambda: self.start_quiz("Advanced")).pack(pady=6)

    # ------------------ QUIZ START ------------------
    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.question_number = 1
        self.attempt = 1
        self.display_problem()

    # ------------------ RANDOMIZATION ------------------
    def randomInt(self):
        """Return random numbers based on difficulty."""
        if self.difficulty == "Easy":
            return random.randint(1, 9), random.randint(1, 9)
        elif self.difficulty == "Moderate":
            return random.randint(10, 99), random.randint(10, 99)
        elif self.difficulty == "Advanced":
            return random.randint(1000, 9999), random.randint(1000, 9999)

    def decideOperation(self):
        """Return '+' or '-' randomly."""
        return random.choice(['+', '-'])

    # ------------------ QUESTION DISPLAY ------------------
    def display_problem(self):
        self.clear_window()
        self.attempt = 1
        self.time_left = self.timer_seconds

        # generate question
        num1, num2 = self.randomInt()
        op = self.decideOperation()
        self.current_problem = (num1, num2, op)

        # header
        tk.Label(self.root, text=f"Question {self.question_number} of 10", font=self.font_small, bg=self.bg_color).pack(pady=4)
        tk.Label(self.root, text=f"Score: {self.score}", font=self.font_small, bg=self.bg_color).pack(pady=2)

        # question label
        tk.Label(self.root, text=f"{num1} {op} {num2} =", font=self.font_text, bg=self.bg_color).pack(pady=10)

        # entry
        self.answer_entry = tk.Entry(self.root, font=self.font_text, justify="center")
        self.answer_entry.pack(pady=5)
        self.answer_entry.focus()

        # timer
        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}s", font=self.font_small, fg="red", bg=self.bg_color)
        self.timer_label.pack(pady=5)
        self.timer_running = True
        self.update_timer()

        # submit button
        tk.Button(self.root, text="Submit", command=self.check_answer).pack(pady=5)

        # feedback
        self.feedback_label = tk.Label(self.root, text="", font=self.font_small, bg=self.bg_color)
        self.feedback_label.pack(pady=6)

    # ------------------ TIMER ------------------
    def update_timer(self):
        if self.timer_running:
            if self.time_left > 0:
                self.timer_label.config(text=f"Time left: {self.time_left}s")
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.feedback_label.config(text="Time's up! Moving to next question.", fg="red")
                self.root.after(1500, self.next_question)

    # ------------------ ANSWER CHECK ------------------
    def isCorrect(self, user_answer, correct_answer):
        return user_answer == correct_answer

    def check_answer(self):
        if not self.timer_running:
            return  # prevent late answers after timer ends

        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.feedback_label.config(text="Enter a valid number.", fg="red")
            return

        num1, num2, op = self.current_problem
        correct_answer = num1 + num2 if op == '+' else num1 - num2

        if self.isCorrect(user_answer, correct_answer):
            self.timer_running = False
            if self.attempt == 1:
                self.score += 10
            else:
                self.score += 5
            self.feedback_label.config(text="Correct!", fg="green")
            self.root.after(1000, self.next_question)
        else:
            if self.attempt == 1:
                self.attempt += 1
                self.feedback_label.config(text="Wrong! Try again.", fg="red")
                self.answer_entry.delete(0, tk.END)
            else:
                self.timer_running = False
                self.feedback_label.config(
                    text=f"Wrong again! Correct answer: {correct_answer}", fg="red"
                )
                self.root.after(1500, self.next_question)

    # ------------------ NEXT QUESTION ------------------
    def next_question(self):
        self.question_number += 1
        if self.question_number <= 10:
            self.display_problem()
        else:
            self.display_results()

    # ------------------ RESULTS ------------------
    def display_results(self):
        self.clear_window()
        grade = self.calculate_grade()

        result_text = f"Final Score: {self.score}/100\nGrade: {grade}"
        tk.Label(self.root, text="Quiz Completed!", font=self.font_title, bg=self.bg_color).pack(pady=15)
        tk.Label(self.root, text=result_text, font=self.font_text, bg=self.bg_color).pack(pady=10)

        tk.Button(self.root, text="Play Again", command=self.display_menu).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def calculate_grade(self):
        if self.score >= 90:
            return "A+"
        elif self.score >= 80:
            return "A"
        elif self.score >= 70:
            return "B"
        elif self.score >= 60:
            return "C"
        else:
            return "D"


# ------------------ MAIN PROGRAM ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
