# === ISL Memory Match Game (Bigger Images Version) ===
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random, os

# ===============================
# === SETUP DATASET PATHS ===
# ===============================
DATASET_PATHS = {
    "numbers": "/Users/ritesh/Downloads/isl-project(college)/main/Dataset/numbers",
    "alphabets": "/Users/ritesh/Downloads/isl-project(college)/main/Dataset/a_to_z",
    "words": "/Users/ritesh/Downloads/isl-project(college)/main/Dataset/words"
}

# ===============================
# === LOAD IMAGES FROM FOLDERS ===
# ===============================
def load_images_from_dataset(dataset_path, limit_per_class=3):
    images = []
    for cls in os.listdir(dataset_path):
        if cls.startswith('.'):  # skip system files
            continue
        class_dir = os.path.join(dataset_path, cls)
        if not os.path.isdir(class_dir):
            continue
        img_files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        for img in img_files[:limit_per_class]:
            images.append(os.path.join(class_dir, img))
    return images

# Load from all 3 datasets
all_images = []
for name, path in DATASET_PATHS.items():
    all_images.extend(load_images_from_dataset(path, limit_per_class=2))

# Randomly select pairs (make sure even number)
random.shuffle(all_images)
selected_images = all_images[:8]  # total of 8 pairs (16 cards)
pairs = selected_images * 2
random.shuffle(pairs)

# ===============================
# === GAME VARIABLES ===
# ===============================
flipped = []
buttons = []
score = 0
attempts = 0

# ===============================
# === FUNCTIONS ===
# ===============================
def flip_card(i):
    global flipped, score, attempts
    
    button = buttons[i]
    if button["state"] == "disabled":
        return
    
    # Show larger image (200x200)
    img = Image.open(pairs[i]).resize((100, 100))
    img_tk = ImageTk.PhotoImage(img)
    button.config(image=img_tk, text="", state="disabled", width=100, height=100)
    button.image = img_tk
    
    flipped.append(i)
    
    if len(flipped) == 2:
        root.after(900, check_match)

def check_match():
    global flipped, score, attempts
    attempts += 1
    i1, i2 = flipped
    if os.path.basename(pairs[i1]) == os.path.basename(pairs[i2]):
        score += 1
        flipped = []
        if score == len(pairs) // 2:
            messagebox.showinfo("🎉 Game Over", f"You matched all cards!\nAttempts: {attempts}")
            root.destroy()
    else:
        for i in flipped:
            buttons[i].config(image="", text="sure?", state="normal", width=10, height=5)
        flipped = []
    score_label.config(text=f"Score: {score} | Attempts: {attempts}")

def reset_game():
    global score, attempts, flipped
    score = 0
    attempts = 0
    flipped = []
    score_label.config(text=f"Score: {score} | Attempts: {attempts}")
    random.shuffle(pairs)
    for b in buttons:
        b.config(image="", text="sure?", state="normal", width=10, height=5)

# ===============================
# === GUI SETUP ===
# ===============================
root = tk.Tk()
root.title("🧩 ISL Memory Match Game")
root.configure(bg="#b3e5fc")

heading = tk.Label(root, text="🧠 ISL Memory Match Game", font=("Arial", 28, "bold"), bg="#b3e5fc")
heading.pack(pady=15)

score_label = tk.Label(root, text=f"Score: {score} | Attempts: {attempts}", font=("Arial", 18), bg="#b3e5fc")
score_label.pack(pady=10)

frame = tk.Frame(root, bg="#b3e5fc")
frame.pack(padx=25, pady=25)

# Create buttons (4x4 grid, with padding)
for i in range(16):
    btn = tk.Button(frame, text="?", font=("Arial", 20, "bold"), width=10, height=5,
                    command=lambda i=i: flip_card(i))
    btn.grid(row=i//4, column=i%4, padx=10, pady=10)
    buttons.append(btn)

# Reset & Exit buttons
bottom_frame = tk.Frame(root, bg="#b3e5fc")
bottom_frame.pack(pady=10)

reset_btn = tk.Button(bottom_frame, text="🔁 Reset", command=reset_game,
                      bg="#0288d1", fg="white", font=("Arial", 16), padx=20, pady=10)
reset_btn.grid(row=0, column=0, padx=10)

exit_btn = tk.Button(bottom_frame, text="❌ Exit", command=root.destroy,
                     bg="red", fg="white", font=("Arial", 16), padx=20, pady=10)
exit_btn.grid(row=0, column=1, padx=10)

root.mainloop()

