import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# === DATASET PATH ===
DATASET_PATH = "/Users/ritesh/Downloads/isl-project(college)/Dataset/words"

# === LOAD DATA SAFELY (skip .DS_Store and hidden files) ===
word_classes = [w for w in os.listdir(DATASET_PATH) 
                if not w.startswith('.') and os.path.isdir(os.path.join(DATASET_PATH, w))]
word_classes.sort()

# === LOAD IMAGES DICTIONARY ===
word_images = {}
for word in word_classes:
    folder_path = os.path.join(DATASET_PATH, word)
    imgs = [os.path.join(folder_path, img)
            for img in os.listdir(folder_path)
            if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if imgs:  # only keep words that have images
        word_images[word] = imgs

# === QUIZ VARIABLES ===
score = 0
total_questions = 20
question_count = 0
current_word = None

# === FUNCTIONS ===
def load_new_question():
    global current_word, question_count
    
    if question_count >= total_questions:
        messagebox.showinfo("Quiz Finished", f"🎯 Your final score: {score}/{total_questions}")
        root.destroy()
        return
    
    question_count += 1
    
    # Choose a valid word
    current_word = random.choice(list(word_images.keys()))
    
    # Load a random image of that word
    img_path = random.choice(word_images[current_word])
    img = Image.open(img_path).resize((250, 250))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img
    
    # Update score label
    score_label.config(text=f"Score: {score} | Question: {question_count}/{total_questions}")
    
    # === Generate 4 options ===
    options = [current_word]
    # Pick 3 random other words
    others = random.sample([w for w in word_images.keys() if w != current_word], 3)
    options.extend(others)
    random.shuffle(options)
    
    # === Update buttons ===
    for i in range(4):
        buttons[i].config(text=options[i], command=lambda w=options[i]: check_answer(w))

def check_answer(selected_word):
    global score
    if selected_word == current_word:
        score += 1
    load_new_question()

def exit_quiz():
    root.destroy()

# === GUI SETUP ===
root = tk.Tk()
root.title("Quiz")
root.configure(bg="#b3e5fc")
root.geometry("800x31000") 
heading = tk.Label(root, text="Quiz", font=("Arial", 28, "bold"), bg="#b3e5fc")
heading.pack(pady=10)

score_label = tk.Label(root, text=f"Score: {score} | Question: {question_count}/{total_questions}",
                       font=("Arial", 16), bg="#b3e5fc")
score_label.pack(pady=5)

image_label = tk.Label(root, bg="#b3e5fc")
image_label.pack(pady=20)

frame = tk.Frame(root, bg="#b3e5fc")
frame.pack(pady=10)

# === CREATE 4 OPTION BUTTONS (a,b,c,d layout) ===
buttons = []
for i in range(4):
    btn = tk.Button(frame, text="", font=("Arial", 14), width=15, bg="white", fg="black")
    btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    buttons.append(btn)

exit_button = tk.Button(root, text="Exit", command=exit_quiz, font=("Arial", 14), bg="red", fg="white")
exit_button.pack(pady=20)

# === START QUIZ ===
load_new_question()
root.mainloop()
