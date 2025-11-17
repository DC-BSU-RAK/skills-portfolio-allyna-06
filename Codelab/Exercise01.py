import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

# --- GLOBAL SETTINGS ---
NUM_QUESTIONS = 10
POINTS_FIRST_ATTEMPT = 10
POINTS_SECOND_ATTEMPT = 5

class MathsQuizApp:
    """
    Main class for the Tkinter Maths Quiz application.
    Manages the application state, question generation, and GUI updates.
    """
    def __init__(self, master):
        self.master = master
        master.title("Maths Quiz")
        master.geometry("800x600") # Set a fixed size for the window

        # Try to load the background image
        try:
            self.bg_image_pil = Image.open("bk.jpg").resize((800, 600), Image.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_pil)
            self.bg_label = tk.Label(master, image=self.bg_image_tk)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "Background image 'bk.jpg' not found. Running without background.")
            master.config(bg="#f0f0f0") # Default background color
            self.bg_label = None
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")
            master.config(bg="#f0f0f0")
            self.bg_label = None

        self.difficulty = None
        self.score = 0
        self.question_count = 0
        self.current_question = {}
        self.attempts = 0
        
        # Start the application by displaying the menu
        self.displayMenu()

    # --- Utility Functions ---

    def clear_frame(self):
        """Removes all widgets from the main window (except the background)."""
        for widget in self.master.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

    def decideOperation(self):
        """Decides whether the problem is addition ('+') or subtraction ('-')."""
        return random.choice(['+', '-'])

    def randomInt(self, min_val, max_val):
        """Determines a random integer within the specified range (inclusive)."""
        return random.randint(min_val, max_val)

    def setDifficulty(self, level):
        """
        Sets the difficulty level and the corresponding min/max range for numbers.
        Also starts the quiz.
        """
        self.difficulty = level
        if level == 'Easy':
            self.min_num, self.max_num = 1, 9
        elif level == 'Moderate':
            self.min_num, self.max_num = 10, 99
        elif level == 'Advanced':
            self.min_num, self.max_num = 1000, 9999
        
        self.score = 0
        self.question_count = 0
        self.startQuiz()

    # --- Screen Functions ---

    def displayMenu(self):
        """Displays the difficulty level menu at the beginning of the quiz."""
        self.clear_frame()
        
        # Center the widgets
        frame = tk.Frame(self.master, bg="#333333", bd=5) # Dark background for contrast
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="🧠 DIFFICULTY LEVEL 🧠", font=("Arial", 20, "bold"), fg="white", bg="#333333", pady=10).pack(pady=10)
        
        # Buttons for difficulty selection
        difficulties = [
            ("1. Easy (Single Digit)", 'Easy', "#4CAF50"), 
            ("2. Moderate (Double Digit)", 'Moderate', "#FFC107"), 
            ("3. Advanced (Four Digit)", 'Advanced', "#F44336")
        ]
        
        for text, level, color in difficulties:
            tk.Button(frame, text=text, font=("Arial", 16), command=lambda l=level: self.setDifficulty(l), 
                      bg=color, fg="white", activebackground=color, activeforeground="black",
                      width=25, height=2).pack(pady=5)
    
    def startQuiz(self):
        """Initializes the quiz and moves to the first problem."""
        self.question_count = 0
        self.score = 0
        self.nextProblem()

    def nextProblem(self):
        """
        Generates a new problem, resets attempts, and displays it.
        Ends the quiz if all questions are answered.
        """
        self.question_count += 1
        if self.question_count > NUM_QUESTIONS:
            self.displayResults()
            return

        self.attempts = 0 # Reset attempts for a new question
        
        # Generate the question components
        num1 = self.randomInt(self.min_num, self.max_num)
        num2 = self.randomInt(self.min_num, self.max_num)
        operation = self.decideOperation()
        
        # Calculate the correct answer
        if operation == '+':
            correct_answer = num1 + num2
        else: # subtraction
            correct_answer = num1 - num2
            
        self.current_question = {
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'answer': correct_answer
        }
        
        self.displayProblem()

    def displayProblem(self):
        """
        Displays the current arithmetic question to the user and accepts their answer.
        """
        self.clear_frame()

        # Center the widgets
        frame = tk.Frame(self.master, bg="#2196F3", bd=5) # Blue background for the quiz
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Question Number and Score Label
        tk.Label(frame, text=f"Question {self.question_count} of {NUM_QUESTIONS} | Score: {self.score}", 
                 font=("Arial", 16), fg="white", bg="#2196F3").pack(pady=10)

        # The Question Label
        question_text = f"{self.current_question['num1']} {self.current_question['operation']} {self.current_question['num2']} ="
        tk.Label(frame, text=question_text, font=("Arial", 30, "bold"), fg="yellow", bg="#2196F3").pack(pady=20)
        
        # Entry Widget for the Answer
        self.answer_entry = tk.Entry(frame, font=("Arial", 24), width=10, justify='center')
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        
        # Submit Button
        tk.Button(frame, text="Submit Answer", font=("Arial", 16), command=self.checkAnswer,
                  bg="#4CAF50", fg="white", activebackground="#388E3C", width=15).pack(pady=10)

        # Feedback Label
        self.feedback_label = tk.Label(frame, text="", font=("Arial", 14), fg="white", bg="#2196F3")
        self.feedback_label.pack(pady=5)
        
        # Attempt info
        if self.attempts == 1:
            self.feedback_label.config(text="Incorrect. One final attempt remaining (5 points possible).", fg="orange")


    def checkAnswer(self):
        """
        Checks whether the user's answer was correct and updates the score.
        Handles the two-attempt logic.
        """
        try:
            user_answer = float(self.answer_entry.get())
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number!", fg="red")
            return

        correct_answer = self.current_question['answer']
        
        if abs(user_answer - correct_answer) < 1e-6: # Use floating point comparison for safety
            self.isCorrect(True)
        else:
            self.isCorrect(False)

    def isCorrect(self, correct):
        """
        Handles the logic for correct/incorrect answers and attempt management.
        Outputs an appropriate message and proceeds to the next problem or re-attempt.
        """
        if correct:
            self.attempts += 1
            points = 0
            message = ""
            
            if self.attempts == 1:
                points = POINTS_FIRST_ATTEMPT
                message = "✅ Correct! (10 points awarded)"
            elif self.attempts == 2:
                points = POINTS_SECOND_ATTEMPT
                message = "✅ Correct on second attempt! (5 points awarded)"
            
            self.score += points
            messagebox.showinfo("Result", message)
            self.nextProblem()
            
        else: # Incorrect answer
            self.attempts += 1
            
            if self.attempts == 1:
                # First incorrect attempt - give another try
                self.feedback_label.config(text="❌ Incorrect. Try again!", fg="red")
                self.answer_entry.delete(0, tk.END) # Clear the entry field
                # Re-display problem with attempt hint
                self.displayProblem() 
            
            elif self.attempts == 2:
                # Second incorrect attempt - move to next question
                correct_ans = self.current_question['answer']
                messagebox.showerror("Result", f"❌ Incorrect again. The correct answer was {correct_ans}. (0 points awarded)")
                self.nextProblem()

    def displayResults(self):
        """
        Displays the user's final score out of a possible 100 and ranks the user.
        Prompts the user to play again.
        """
        self.clear_frame()
        
        max_score = NUM_QUESTIONS * POINTS_FIRST_ATTEMPT
        percentage = (self.score / max_score) * 100

        # Determine the rank
        if percentage >= 90:
            rank = "A+ (Excellent)"
            rank_color = "#4CAF50"
        elif percentage >= 75:
            rank = "A (Great)"
            rank_color = "#8BC34A"
        elif percentage >= 60:
            rank = "B (Good Effort)"
            rank_color = "#FFC107"
        else:
            rank = "C (Keep Practicing)"
            rank_color = "#F44336"
            
        # Center the widgets
        frame = tk.Frame(self.master, bg="#9C27B0", bd=5) # Purple background for results
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="🎉 QUIZ COMPLETE! 🎉", font=("Arial", 24, "bold"), fg="white", bg="#9C27B0").pack(pady=20)
        
        tk.Label(frame, text=f"Final Score: {self.score} / {max_score}", font=("Arial", 20), fg="white", bg="#9C27B0").pack(pady=10)
        tk.Label(frame, text=f"Percentage: {percentage:.2f}%", font=("Arial", 20), fg="white", bg="#9C27B0").pack(pady=10)
        tk.Label(frame, text=f"Your Rank: {rank}", font=("Arial", 22, "bold"), fg=rank_color, bg="#9C27B0").pack(pady=20)
        
        # Play Again Button
        tk.Button(frame, text="Play Again?", font=("Arial", 16), command=self.displayMenu,
                  bg="#00BCD4", fg="white", activebackground="#0097A7", width=15).pack(pady=20)

# --- Execution ---
if __name__ == '__main__':
    root = tk.Tk()
    app = MathsQuizApp(root)
    root.mainloop()