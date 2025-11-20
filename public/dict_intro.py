import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Path to your introduction dataset
base_path = "/Users/ritesh/Downloads/isl-project(college)/main/Dataset/intro"

# Create main window
root = tk.Tk()
root.title("Signify - Introduction")
root.geometry("1000x700")
root.configure(bg="#b3e5fc")

# Frame for displaying buttons and images
frame = ttk.Frame(root)
frame.pack(expand=True, fill="both", padx=20, pady=20)

# Create dictionary dynamically
intro_words = [
    "again", "agree", "careful", "change", "chat", "congratulations", 
    "good morning", "Hello", "home", "how are you", "hungry", "I",
    "i need help", "keepsmile", "Namaste", "Name", "Please", "questions", 
    "remember", "seat", "Sorry", "Thank-you", "thirsty", "this", 
    "together", "understand", "wait", "where"
]

intro_dict = {}

# Automatically map each word to its image folder
for word in intro_words:
    folder_path = os.path.join(base_path, word)
    if os.path.exists(folder_path):
        images = [os.path.join(folder_path, img) for img in os.listdir(folder_path)[:10]]
        intro_dict[word] = images

# Function to show introduction words
def show_intro_words():
    for widget in frame.winfo_children():
        widget.destroy()

    title = tk.Label(frame, text="Sign Language Introduction ✋", font=("Helvetica", 22, "bold"), bg="#f3f4f6")
    title.pack(pady=15)

    # Grid layout for words
    button_frame = tk.Frame(frame, bg="#f3f4f6")
    button_frame.pack()

    for i, word in enumerate(intro_dict.keys()):
        btn = tk.Button(
            button_frame,
            text=word.capitalize(),
            width=18,
            height=2,
            bg="#2563eb",
            fg="white",
            font=("Helvetica", 13, "bold"),
            command=lambda w=word: show_images(w)
        )
        btn.grid(row=i // 4, column=i % 4, padx=12, pady=12)

# Function to show 10 images for a selected word
def show_images(word):
    for widget in frame.winfo_children():
        widget.destroy()

    title = tk.Label(frame, text=f"Sign for '{word.capitalize()}'", font=("Helvetica", 20, "bold"), bg="#f3f4f6")
    title.pack(pady=10)

    images_frame = tk.Frame(frame, bg="#FFE5B4")
    images_frame.pack()

    # Load and display up to 10 images
    img_refs = []
    for i, img_path in enumerate(intro_dict[word][:10]):
        try:
            img = Image.open(img_path)
            img = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            img_refs.append(img_tk)
            lbl = tk.Label(images_frame, image=img_tk, bg="#f3f4f6")
            lbl.image = img_tk
            lbl.grid(row=i // 5, column=i % 5, padx=10, pady=10)
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")

    # Back button
    back_btn = tk.Button(
        frame, text="⬅ Back", command=show_intro_words,
        bg="#ef4444", fg="white", font=("Helvetica", 13, "bold"),
        width=10, height=1
    )
    back_btn.pack(pady=15)

# Start with intro words view
show_intro_words()

root.mainloop()
