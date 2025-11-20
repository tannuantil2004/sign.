import tkinter as tk
from PIL import Image, ImageTk
import os
import random

# === PATH TO DATASET ===
DATASET_PATH = "/Users/ritesh/Downloads/isl-project(college)/main/Dataset/a_to_z"

# === LOAD DATASET INTO A DICTIONARY ===
alphabets = [folder for folder in os.listdir(DATASET_PATH)
             if os.path.isdir(os.path.join(DATASET_PATH, folder)) and not folder.startswith('.')]
alphabets.sort()

alphabet_images = {}
for letter in alphabets:
    folder_path = os.path.join(DATASET_PATH, letter)
    imgs = [os.path.join(folder_path, img)
            for img in os.listdir(folder_path)
            if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if imgs:
        alphabet_images[letter] = imgs

# === MAIN WINDOW ===
root = tk.Tk()
root.title("ISL Alphabet Viewer")
root.configure(bg="#b3e5fc")

current_frame = None

# === FUNCTION TO CLEAR CURRENT FRAME ===
def clear_frame():
    global current_frame
    if current_frame is not None:
        current_frame.destroy()

# === SHOW ALPHABET GRID ===
def show_alphabet_grid():
    clear_frame()
    global current_frame
    current_frame = tk.Frame(root, bg="#b3e5fc")
    current_frame.pack(fill="both", expand=True)

    tk.Label(current_frame, text="Select an Alphabet", font=("Arial", 24, "bold"), bg="#b3e5fc").pack(pady=20)

    grid_frame = tk.Frame(current_frame, bg="#b3e5fc")
    grid_frame.pack()

    # Create A-Z buttons in grid
    for i, letter in enumerate(alphabet_images.keys()):
        btn = tk.Button(grid_frame, text=letter, font=("Arial", 16, "bold"), width=5, height=2,
                        bg="white", fg="black",
                        command=lambda l=letter: show_images(l))
        btn.grid(row=i//6, column=i%6, padx=10, pady=10)

# === SHOW 10 RANDOM IMAGES FOR SELECTED ALPHABET ===
def show_images(letter):
    clear_frame()
    global current_frame
    current_frame = tk.Frame(root, bg="#b3e5fc")
    current_frame.pack(fill="both", expand=True)

    tk.Label(current_frame, text=f"Alphabet: {letter}", font=("Arial", 24, "bold"), bg="#b3e5fc").pack(pady=20)

    images_frame = tk.Frame(current_frame, bg="#b3e5fc")
    images_frame.pack()

    # Pick up to 10 random images
    imgs = random.sample(alphabet_images[letter], min(10, len(alphabet_images[letter])))

    for i, img_path in enumerate(imgs):
        img = Image.open(img_path).resize((120, 120))
        img = ImageTk.PhotoImage(img)
        lbl = tk.Label(images_frame, image=img, bg="#b3e5fc")
        lbl.image = img
        lbl.grid(row=i//5, column=i%5, padx=10, pady=10)

    # Back button
    back_btn = tk.Button(current_frame, text="Back", font=("Arial", 14, "bold"),
                         bg="red", fg="white", command=show_alphabet_grid)
    back_btn.pack(pady=20)

# === START APP ===
show_alphabet_grid()
root.mainloop()
