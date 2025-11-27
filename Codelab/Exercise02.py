import tkinter as tk
import random

# --- Data Simulation (Updated Jokes with Explanations) ---
# This big text block is basically our "database" of jokes.
# Each line is one joke and contains:
#  setup ? punchline | explanation
# We later split these lines into usable pieces.
# Joke structure: Setup?Punchline|Explanation
JOKE_DATA_WITH_EXPLANATION = """

What do you call an angry carrot?A steamed veggie.|'Steamed' means cooked with steam, but it also means angry.
Where do polar bears keep their money?In a snowbank.|A snowbank is a pile of snow, but it sounds like “bank.”
How do you make an egg roll?You push it!|The joke treats “egg roll” literally as rolling an egg.
What would bears be without bees?Ears.|Remove the letter B from “bears,” you get “ears.”
What do you call a pile of cats?A meow-ntain.|It’s a pun combining “meow” with “mountain.”
Why do cows wear bells?Because their horns don’t work.|Cows have horns, but this refers to car horns.
Why did the bicycle fall over?Because it was two tired.|“Two tired” sounds like “too tired.”
What did the triangle say to the circle?You’re pointless.|A circle has no points.
RIP, boiling water.You will be mist.|“Be mist” sounds like “be missed.”
Time flies like an arrow.Fruit flies like a banana.|Wordplay: first “flies” is a verb, second is a noun.
I ordered a chicken and an egg online.I’ll let you know what comes first.|Reference to the classic question.
Why was Cinderella bad at soccer?She kept running away from the ball.|The ball is both a dance party & a soccer ball.
What do lawyers wear to court?Lawsuits.|A pun: “lawsuit” sounds like “suit.”
What do elves learn in school?The elf-abet.|Pun on “alphabet.”
Where was King David’s temple located?Beside his ear.|“Temple” also means part of the head.
What did one toilet say to another?You look flushed.|Flushed = toilet function + turning red.
What lights up a soccer stadium?A soccer match.|“Match” = game or something that lights flame.
What does corn say when it gets a compliment?Aw, shucks!|“Shucks” means modesty and also corn husk.
What’s the difference between a poorly dressed man on a tricycle and a well-dressed man on a bicycle?Attire.|“Attire” sounds like “a tire.”
Why did the chicken cross the road?To get to the other side.|Classic anticlimax joke.
What happens if you boil a clown?You get a laughing stock.|“Laughingstock” is someone mocked; here it’s literal stock.
Why did the car get a flat tire?Because there was a fork in the road!|“Fork in the road” means a split path, not an actual fork.
How did the hipster burn his mouth?He ate his pizza before it was cool.|Hipsters like things before they’re “cool.”
What did the janitor say when he jumped out of the closet?SUPPLIES!!!!|Sounds like “surprise!”
Have you heard about the band 1023MB?They haven't got a gig yet…|You need 1024MB for a gigabyte.
Why does the golfer wear two pants?In case he gets a hole-in-one.|Hole-in-one = golf term & pant hole.
Why should you wear glasses to maths class?It helps with division.|Division = math & dividing vision.
Why does it take pirates so long to learn the alphabet?They could spend years at C.|“C” sounds like “sea.”
Why did the woman go on a date with a mushroom?He was a fun-ghi.|Fun guy.
Why do bananas never get lonely?They hang out in bunches.|Literal bunches.
What did the buffalo say when his kid went to college?Bison.|Sounds like “bye, son.”
Why shouldn't you tell secrets in a cornfield?Too many ears.|Corn has “ears.”
What do you call someone who doesn't like carbs?Lack-Toast Intolerant.|Sounds like lactose intolerant.
Why did the can crusher quit his job?It was soda pressing.|“So depressing.”
Why did the birthday boy wrap himself in paper?He wanted to live in the present.|Present = now & wrapped gift.
What does a house wear?A dress.|House address = “a dress.”
Why couldn't the toilet paper cross the road?It got stuck in a crack.|Literal crack in pavement.
Why didn't the bike want to go anywhere?It was two-tired.|Pun on “too tired.”
Want to hear a pizza joke?Nahhh, it's too cheesy!|Cheesy = corny humour & cheese in pizza.
Why are chemists great at solving problems?They have all the solutions.|Solutions = answers & chemical mixtures.
Why is it impossible to starve in the desert?Because of all the sand which is there!|Sandwich = sand which.
What did the cheese say when it looked in the mirror?Halloumi!|Sounds like “Hello me.”
Why did the developer go broke?He used up all his cache.|Cache = money stash & computer cache.
Did you know ants never get sick?They have little antibodies.|Ant bodies.
Why did the donut go to the dentist?To get a filling.|Donut filling & dental filling.
What do you call a bear with no teeth?A gummy bear!|Gummy candy & gum-only bear.
What does a vegan zombie like to eat?Graaains.|Zombies say “brains.”
What do you call a dinosaur with only one eye?Do-you-think-he-saw-us!|Sounds like “Do you think he saw us?”
Why should you never fall in love with a tennis player?Love means nothing.|In tennis, “love” = zero.
What did the full glass say to the empty glass?You look drunk.|Empty glass looks “tipsy.”
What's a potato's favorite form of transportation?The gravy train.|Gravy train = easy success + gravy.
What did one ocean say to the other?Nothing, they just waved.|Wave = sea wave & hand wave.
What did the right eye say to the left eye?Between you and me, something smells.|The nose is between the eyes.
What do you call a dog run over by a steamroller?Spot!|It becomes flat → a spot.
What's the difference between a hippo and a zippo?One's heavy, one’s a little lighter.|Lighter = light & small.
Why don't scientists trust atoms?They make up everything.|Atoms literally make everything.
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
COLOR_BTN_PUNCHLINE = "#45C4AF" # Amber - Secondary action
COLOR_BTN_EXPLAIN = "#70C2D3"   # Brown - Tertiary action
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
                               bg=COLOR_BTN_PUNCHLINE, fg="white", padx=10, pady=5,
                               state=tk.DISABLED)
show_punchline_btn.pack(side=tk.LEFT, padx=5)

# Show Explanation Button
show_explanation_btn = tk.Button(button_frame, 
                                 text=" Explain", 
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

# Keep the app running 
root.mainloop() 