import tkinter as tk
import random

# --- Data Simulation (Updated Jokes with Explanations) ---

# Joke structure: Setup?Punchline|Explanation
JOKE_DATA_WITH_EXPLANATION = """
What do you call an angry carrot?A steamed veggie.|This is a pun. 'Steamed' means cooked with steam, but it is also slang for being angry or upset.
Where do polar bears keep their money?In a snowbank.|This is a pun. A 'snowbank' is a pile of snow, but it sounds like 'bank,' a place to store money.
How do you make an egg roll?You push it!|This is literal humor. 'Egg roll' is a food item, but the joke treats it like a physical egg that needs rolling.
What would bears be without bees?Ears.|This is a wordplay joke. Removing the 'b' sounds (like the word 'bee') from 'bears' leaves the word 'ears.'
What do you call a pile of cats?A meow-ntain.|This is a pun. The sound a cat makes ('meow') replaces the 'f' in 'fountain' or the 'o' in 'mountain.'
Why do cows wear bells?Because their horns don’t work.|This is a joke based on expectations. Cows have horns (antlers) but the joke refers to horns used as car signaling devices.
Why did the bicycle fall over?Because it was two tired.|This is a homophone pun. 'Two tired' sounds exactly like 'too tired,' meaning exhausted.
What did the triangle say to the circle?You’re pointless.|This is a geometry pun. A triangle has points (vertices) while a circle is a continuous curve with no points.
RIP, boiling water.You will be mist.|This is a homophone pun. 'Be mist' sounds like 'be missed,' using the concept of steam or mist created by boiling water.
Time flies like an arrow.Fruit flies like a banana.|This is a grammatical joke. It plays on the ambiguity of "flies" as a verb (time flies) vs. "flies" as a noun (fruit flies).
I ordered a chicken and an egg online.I’ll let you know what comes first.|This is a classic paradox joke. It refers to the age-old question, "Which came first, the chicken or the egg?"
Why was Cinderella so bad at soccer?She kept running away from the ball!|This is a wordplay joke based on the fairy tale. Cinderella's story is centered on running away from the ball (the dance party).
What do lawyers wear to court?Lawsuits.|This is a pun. A 'lawsuit' is a legal action, but it sounds like 'suit,' an article of clothing.
What do elves learn in school?The elf-abet.|This is a pun. 'Elf-abet' replaces the 'alph' in 'alphabet.'
Where was King David’s temple located?Beside his ear.|This is a pun based on the temple being a part of the head, beside the ear, not a large building.
What did one toilet say to another?You look flushed.|This is a pun. 'Flushed' refers to the toilet's function, but it also describes someone looking embarrassed or red in the face.
What lights up a soccer stadium?A soccer match.|This is a pun. A 'soccer match' is a game, but a 'match' is also a small stick used to create light/fire.
What does corn say when it gets a compliment?Aw, shucks!|This is a pun. 'Shucks' is an expression of modesty, but corn grows inside a protective layer called a 'husk' or 'shuck.'
What’s the difference between a poorly dressed man on a tricycle and a well-dressed man on a bicycle?Attire.|This is a pun. 'Attire' means clothing, but it sounds like 'a tire' or 'a trier,' referring to the number of wheels.
"""

def parse_joke_line(line):
    """Parses a single line into (setup, punchline, explanation)"""
    parts = line.strip().split('?', 1)
    if len(parts) < 2:
        return None, None, None

    setup = parts[0].strip() + "?"
    punchline_explanation_str = parts[1].strip()

    # Separate Punchline and Explanation using the '|' delimiter
    pe_parts = punchline_explanation_str.split('|', 1)
    punchline = pe_parts[0].strip()
    explanation = pe_parts[1].strip() if len(pe_parts) > 1 else "No explanation available."
    
    return setup, punchline, explanation

def load_jokes_from_data(data):
    """Reads and parses the joke data."""
    jokes = []
    for line in data.strip().split('\n'):
        if line.strip():
            setup, punchline, explanation = parse_joke_line(line)
            if setup and punchline:
                jokes.append((setup, punchline, explanation))
    return jokes

# Load the joke data globally
JOKES = load_jokes_from_data(JOKE_DATA_WITH_EXPLANATION)
CURRENT_PUNCHLINE = ""      # Stores the punchline
CURRENT_EXPLANATION = ""    # Stores the explanation

# --- Color Palette ---
COLOR_BG_ROOT = "#E0FFFF"       # Light Cyan - The outer background color
COLOR_BG_MAIN = "white"         # White - The main content background color
COLOR_TEXT_SETUP = "#4A148C"    # Deep Purple - For the question
COLOR_TEXT_PUNCHLINE = "#C62828" # Deep Red - For the big reveal
COLOR_TEXT_EXPLANATION = "#1B5E20" # Dark Green - For analysis text
COLOR_BG_EXPLANATION = "#E8EAF6" # Lavender Mist - Background for the explanation box

# Button Colors
COLOR_BTN_ALEXA = "#00ACC1"  # Cyan - Primary action
COLOR_BTN_PUNCHLINE = "#FFB300" # Amber - Secondary action
COLOR_BTN_EXPLAIN = "#8D6E63"   # Brown - Tertiary action
COLOR_BTN_QUIT = "#E53935"    # Red - Danger/Exit

# --- GUI Logic Functions ---

def tell_joke():
    """Randomly selects a joke, displays the setup, and resets the punchline/explanation display."""
    global CURRENT_PUNCHLINE, CURRENT_EXPLANATION
    
    if not JOKES:
        setup_label.config(text="Sorry, no jokes loaded.", fg=COLOR_TEXT_PUNCHLINE)
        punchline_label.config(text="")
        explanation_label.config(text="")
        show_punchline_btn.config(state=tk.DISABLED)
        show_explanation_btn.config(state=tk.DISABLED)
        return
        
    # 1. Randomly select a joke (now with 3 elements)
    setup, punchline, explanation = random.choice(JOKES)
    CURRENT_PUNCHLINE = punchline
    CURRENT_EXPLANATION = explanation
    
    # 2. Display the setup
    setup_label.config(text=setup, fg=COLOR_TEXT_SETUP)
    
    # 3. Clear the previous punchline and explanation
    punchline_label.config(text="")
    explanation_label.config(text="")
    
    # Enable the punchline button
    show_punchline_btn.config(state=tk.NORMAL)
    show_explanation_btn.config(state=tk.DISABLED) # Keep disabled until punchline is shown
    next_joke_btn.config(state=tk.NORMAL)

def show_punchline():
    """Displays the punchline and enables the explanation button."""
    punchline_label.config(text=CURRENT_PUNCHLINE, fg=COLOR_TEXT_PUNCHLINE)
    show_punchline_btn.config(state=tk.DISABLED) # Disable after showing

    # Enable the explanation button
    if CURRENT_EXPLANATION:
         show_explanation_btn.config(state=tk.NORMAL)

def show_explanation():
    """Displays the explanation and disables its button."""
    explanation_label.config(text=f"*** THE HUMOR ***\n{CURRENT_EXPLANATION}", fg=COLOR_TEXT_EXPLANATION)
    show_explanation_btn.config(state=tk.DISABLED) # Disable after showing

# --- Tkinter Setup ---

# Initialize the main window
root = tk.Tk()
root.title("Alexa Joke Explainer Assistant")
root.geometry("550x480")
# Set the main window background color to Light Cyan
root.configure(bg=COLOR_BG_ROOT) 
root.resizable(False, False)

# Main container frame (set to White for contrast)
main_frame = tk.Frame(root, bg=COLOR_BG_MAIN, padx=15, pady=15, bd=5, relief=tk.RAISED) 
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# --- Title/Header ---
tk.Label(main_frame, 
         text="🎙️ JOKE EXPLAINER ASSISTANT 💡", 
         font=("Arial", 18, "bold"), 
         bg=COLOR_BG_MAIN, 
         fg="#37474F").pack(pady=(5, 15))


# 1. Joke Setup Label (Question)
setup_label = tk.Label(main_frame, 
                       text="Press 'Alexa tell me a Joke' to begin!", 
                       font=("Arial", 16, "italic"), 
                       bg=COLOR_BG_MAIN, 
                       fg=COLOR_TEXT_SETUP,
                       wraplength=500, 
                       justify=tk.CENTER)
setup_label.pack(pady=(10, 10), fill=tk.X)

# 2. Punchline Label
punchline_label = tk.Label(main_frame, 
                          text="", 
                          font=("Arial", 18, "bold"), 
                          bg=COLOR_BG_MAIN, 
                          fg=COLOR_TEXT_PUNCHLINE, 
                          wraplength=500,
                          justify=tk.CENTER)
punchline_label.pack(pady=10, fill=tk.X)

# 3. Explanation Label
explanation_label = tk.Label(main_frame, 
                             text="", 
                             font=("Arial", 10), 
                             bg=COLOR_BG_EXPLANATION, 
                             fg=COLOR_TEXT_EXPLANATION, 
                             wraplength=500,
                             justify=tk.LEFT, 
                             pady=10, padx=10, bd=2, relief=tk.GROOVE) 
explanation_label.pack(pady=15, fill=tk.X)

# --- Button Frame (uses main frame's background) ---
button_frame = tk.Frame(main_frame, bg=COLOR_BG_MAIN)
button_frame.pack(pady=10)

# Alexa Joke Button
alexa_joke_btn = tk.Button(button_frame, 
                           text="🤖 Alexa tell me a Joke", 
                           command=tell_joke, 
                           font=("Arial", 12, "bold"),
                           bg=COLOR_BTN_ALEXA, fg="white", padx=10, pady=5)
alexa_joke_btn.pack(side=tk.LEFT, padx=5)

# Show Punchline Button
show_punchline_btn = tk.Button(button_frame, 
                               text="❓ Show Punchline", 
                               command=show_punchline, 
                               font=("Arial", 12),
                               bg=COLOR_BTN_PUNCHLINE, fg="black", padx=10, pady=5,
                               state=tk.DISABLED)
show_punchline_btn.pack(side=tk.LEFT, padx=5)

# Show Explanation Button
show_explanation_btn = tk.Button(button_frame, 
                                 text="🤔 Explain the Joke", 
                                 command=show_explanation, 
                                 font=("Arial", 12),
                                 bg=COLOR_BTN_EXPLAIN, fg="white", padx=10, pady=5,
                                 state=tk.DISABLED)
show_explanation_btn.pack(side=tk.LEFT, padx=5)

# --- Control Buttons (uses main window's background) ---
control_frame = tk.Frame(root, bg=COLOR_BG_ROOT)
control_frame.pack(fill=tk.X, pady=5)

# Next Joke Button
next_joke_btn = tk.Button(control_frame, 
                          text="➡️ Next Joke", 
                          command=tell_joke, 
                          font=("Arial", 12),
                          bg="#64B5F6", fg="white", padx=10, pady=5,
                          state=tk.DISABLED)
next_joke_btn.pack(side=tk.LEFT, padx=(15, 5), pady=5)

# Quit Button
quit_btn = tk.Button(control_frame, 
                     text="❌ Quit Application", 
                     command=root.quit, 
                     font=("Arial", 12),
                     bg=COLOR_BTN_QUIT, fg="white", padx=10, pady=5)
quit_btn.pack(side=tk.RIGHT, padx=(5, 15), pady=5)

# Start the Tkinter event loop
root.mainloop()