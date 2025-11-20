import tkinter as tk
from PIL import Image, ImageTk
import os
import random

# === PATH TO DATASET ===
DATASET_PATH = "/Users/ritesh/Downloads/isl-project(college)/main/Dataset/numbers"  # change if needed

# === LOAD DATASET INTO A DICTIONARY ===
numbers = [folder for folder in os.listdir(DATASET_PATH)
           if os.path.isdir(os.path.join(DATASET_PATH, folder)) and not folder.startswith('.')]
numbers.sort(key=lambda x: int(x))  # ensure numeric order

number_images = {}
for num in numbers:
    folder_path = os.path.join(DATASET_PATH, num)
    imgs = [os.path.join(folder_path, img)
            for img in os.listdir(folder_path)
            if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if imgs:
        number_images[num] = imgs

# === MAIN WINDOW ===
root = tk.Tk()
root.title("ISL Number Viewer")
root.configure(bg="#b3e5fc")

current_frame = None

# === FUNCTION TO CLEAR CURRENT FRAME ===
def clear_frame():
    global current_frame
    if current_frame is not None:
        current_frame.destroy()

# === SHOW NUMBER GRID ===
def show_number_grid():
    clear_frame()
    global current_frame
    current_frame = tk.Frame(root, bg="#b3e5fc")
    current_frame.pack(fill="both", expand=True)

    tk.Label(current_frame, text="Select a Number", font=("Arial", 24, "bold"), bg="#b3e5fc").pack(pady=20)

    grid_frame = tk.Frame(current_frame, bg="#b3e5fc")
    grid_frame.pack()

    # Create 0-9 buttons
    for i, num in enumerate(number_images.keys()):
        btn = tk.Button(grid_frame, text=num, font=("Arial", 16, "bold"), width=5, height=2,
                        bg="white", fg="black",
                        command=lambda n=num: show_images(n))
        btn.grid(row=i//5, column=i%5, padx=10, pady=10)

# === SHOW 10 RANDOM IMAGES FOR SELECTED NUMBER ===
def show_images(num):
    clear_frame()
    global current_frame
    current_frame = tk.Frame(root, bg="#b3e5fc")
    current_frame.pack(fill="both", expand=True)

    tk.Label(current_frame, text=f"Number: {num}", font=("Arial", 24, "bold"), bg="#b3e5fc").pack(pady=20)

    images_frame = tk.Frame(current_frame, bg="#b3e5fc")
    images_frame.pack()

    # Pick up to 10 random images
    imgs = random.sample(number_images[num], min(10, len(number_images[num])))

    for i, img_path in enumerate(imgs):
        img = Image.open(img_path).resize((120, 120))
        img = ImageTk.PhotoImage(img)
        lbl = tk.Label(images_frame, image=img, bg="#b3e5fc")
        lbl.image = img
        lbl.grid(row=i//5, column=i%5, padx=10, pady=10)

    # Back button
    back_btn = tk.Button(current_frame, text="Back", font=("Arial", 14, "bold"),
                         bg="red", fg="white", command=show_number_grid)
    back_btn.pack(pady=20)

# === START APP ===
show_number_grid()
root.mainloop()
