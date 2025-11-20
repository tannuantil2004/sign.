import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# -------------------------
# Paths to datasets
# -------------------------
alphabet_dir = r"/Users/ritesh/Downloads/isl-project(college)/main/Dataset/a_to_z"
number_dir   = r"/Users/ritesh/Downloads/isl-project(college)/main/Dataset/numbers"

# -------------------------
# Main App
# -------------------------
class TextToSignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to ISL Sign")
        self.root.configure(bg="#b3e5fc")

        # Input frame
        self.input_frame = tk.Frame(root, bg="#b3e5fc")
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Enter Text:", font=("Arial", 14), bg="#b3e5fc").pack(side=tk.LEFT, padx=5)
        self.text_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=50)
        self.text_entry.pack(side=tk.LEFT, padx=5)

        self.display_btn = tk.Button(self.input_frame, text="Display", font=("Arial", 12), command=self.display_signs)
        self.display_btn.pack(side=tk.LEFT, padx=5)

        # Scrollable frame for images
        self.canvas = tk.Canvas(root, bg="#b3e5fc", width=800, height=400)
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#b3e5fc")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.canvas.pack(side="top", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        # Refresh button (hidden initially)
        self.refresh_btn = tk.Button(root, text="Refresh", font=("Arial", 12), command=self.refresh)
        self.refresh_btn.pack(pady=5)
        self.refresh_btn.pack_forget()  # hide initially

        self.image_refs = []  # Keep persistent references to images

    def display_signs(self):
        text = self.text_entry.get().strip().upper()
        if not text:
            return

        self.refresh_btn.pack()  # show refresh button

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()

        row_frame = tk.Frame(self.scrollable_frame, bg="#b3e5fc")
        row_frame.pack(anchor="w", pady=5)

        for char in text:
            if char == " ":
                spacer = tk.Label(row_frame, width=2, bg="#b3e5fc")
                spacer.pack(side=tk.LEFT)
                continue

            # Determine folder path
            if char.isalpha():
                folder = alphabet_dir
            elif char.isdigit():
                folder = number_dir
            else:
                continue

            char_folder = os.path.join(folder, char)
            if not os.path.exists(char_folder):
                continue

            # Pick first image from folder
            img_name = os.listdir(char_folder)[0]
            img_path = os.path.join(char_folder, img_name)
            pil_img = Image.open(img_path)
            pil_img = pil_img.resize((300,300))
            tk_img = ImageTk.PhotoImage(pil_img)
            self.image_refs.append(tk_img)  # keep reference!

            label = tk.Label(row_frame, image=tk_img, bg="#b3e5fc")
            label.pack(side=tk.LEFT, padx=2)

    def refresh(self):
        self.text_entry.delete(0, tk.END)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()
        self.refresh_btn.pack_forget()

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSignApp(root)
    root.mainloop()
