import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os, random

# === DATASET PATHS ===
ALPHABET_PATH = "/Users/ritesh/Downloads/isl-project(college)/main/Dataset/a_to_z"
NUMBER_PATH = "/Users/ritesh/Downloads/isl-project(college)/main/Dataset/numbers"

# === LOAD DATASET IMAGES ===
def load_dataset(path):
    data = {}
    for folder in os.listdir(path):
        if folder == ".DS_Store":
            continue
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path):
            imgs = [os.path.join(folder_path, img) for img in os.listdir(folder_path)
                    if img.lower().endswith(('.jpg', '.png', '.jpeg'))]
            data[folder] = imgs
    return data

alphabet_data = load_dataset(ALPHABET_PATH)
number_data = load_dataset(NUMBER_PATH)

# Combine both datasets
DATASET = {**alphabet_data, **number_data}
CLASSES = list(DATASET.keys())

# === QUIZ VARIABLES ===
score = 0
question_no = 0
total_questions = 20
timer = 10
running = False
current_answer = ""

# === MAIN WINDOW ===
root = tk.Tk()
root.title("Sign Guess Game")
root.geometry("700x600")
root.config(bg="#b3e5fc")

# === HEADING ===
heading = tk.Label(root, text="Sign Guess Game", font=("Arial", 28, "bold"), bg="#b3e5fc", fg="#01579b")
heading.pack(pady=15)

# === SCORE LABEL ===
score_label = tk.Label(root, text=f"Score: {score} | Question: {question_no}/{total_questions}", 
                       font=("Arial", 16), bg="#b3e5fc", fg="#01579b")
score_label.pack()

# === TIMER LABEL ===
timer_label = tk.Label(root, text=f"Time left: {timer}s", font=("Arial", 16, "bold"), bg="#b3e5fc", fg="red")
timer_label.pack(pady=10)

# === IMAGE DISPLAY ===
image_label = tk.Label(root, bg="#b3e5fc")
image_label.pack(pady=20)

# === OPTIONS FRAME ===
option_frame = tk.Frame(root, bg="#b3e5fc")
option_frame.pack(pady=20)

# Create option buttons (4)
option_buttons = []
for i in range(4):
    btn = tk.Button(option_frame, text="", font=("Arial", 16), width=15, height=2, 
                    bg="#0288d1", fg="white", command=lambda i=i: check_answer(i))
    btn.grid(row=i//2, column=i%2, padx=20, pady=15)
    option_buttons.append(btn)

# === FUNCTION DEFINITIONS ===

def update_timer():
    global timer, running
    if running:
        if timer > 0:
            timer_label.config(text=f"Time left: {timer}s")
            timer -= 1
            root.after(1000, update_timer)
        else:
            messagebox.showinfo("Time Up!", f"Time's up! The correct answer was '{current_answer}'.")
            next_question()

def check_answer(selected):
    global score
    if option_buttons[selected]['text'] == current_answer:
        score += 1
        messagebox.showinfo("Correct!", "✅ Well done!")
    else:
        messagebox.showinfo("Incorrect!", f"❌ Correct answer: {current_answer}")
    next_question()

def next_question():
    global question_no, score, timer, current_answer, running

    if question_no >= total_questions:
        end_game()
        return

    question_no += 1
    timer = 10
    running = True
    timer_label.config(text=f"Time left: {timer}s")

    # Pick random class and image
    current_answer = random.choice(CLASSES)
    img_path = random.choice(DATASET[current_answer])

    # Load image with larger size
    img = Image.open(img_path)
    img = img.resize((400, 400))
    photo = ImageTk.PhotoImage(img)

    image_label.config(image=photo)
    image_label.image = photo

    # Generate 4 options
    options = random.sample(CLASSES, 3)
    if current_answer not in options:
        options.append(current_answer)
    random.shuffle(options)

    # Update buttons
    for i, btn in enumerate(option_buttons):
        btn.config(text=options[i], state="normal")

    # Update score label
    score_label.config(text=f"Score: {score} | Question: {question_no}/{total_questions}")

    # Start timer
    update_timer()

def end_game():
    global running
    running = False
    for btn in option_buttons:
        btn.config(state="disabled")
    messagebox.showinfo("Game Over", f"🎉 Your final score is {score}/{total_questions}!")
    play_again_button.pack(pady=20)

def restart_game():
    global score, question_no
    score = 0
    question_no = 0
    play_again_button.pack_forget()
    next_question()

# === RESTART BUTTON ===
play_again_button = tk.Button(root, text="Play Again", font=("Arial", 16), bg="#0288d1", fg="white",
                              command=restart_game)

# === START THE GAME ===
next_question()

root.mainloop()
