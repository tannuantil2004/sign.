import tkinter as tk
from tkinter import PhotoImage
import subprocess
import os

# ---------------------------
# App constants / colors
# ---------------------------
BG = "#92dff3"
SIDEBAR_WIDTH = 200
ACTIVE_BTN_BG = "#BBDEFB"
SIDEBAR_BTN_BG = BG
WHITE = "white"

# ---------------------------
# PATH HANDLING
# ---------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

# ---------------------------
# Helper functions
# ---------------------------
def show_frame(name):
    for key, frame in pages.items():
        if key == name:
            frame.tkraise()
            set_active_sidebar(name)

def set_active_sidebar(active_name):
    for name, btn in sidebar_buttons.items():
        if name == active_name:
            btn.config(bg=ACTIVE_BTN_BG)
        else:
            btn.config(bg=SIDEBAR_BTN_BG)

def open_module(file_name):
    """Open external .py files from /main folder"""
    path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(path):
        subprocess.Popen(["python", path])
    else:
        print(f"❌ File not found: {file_name}")

# ---------------------------
# Root window
# ---------------------------
root = tk.Tk()
root.title("Signify - Multi Page App")
root.geometry("1400x1400")
root.configure(bg=BG)

# ---------------------------
# Sidebar
# ---------------------------
sidebar = tk.Frame(root, bg=SIDEBAR_BTN_BG, width=SIDEBAR_WIDTH)
sidebar.pack(side="left", fill="y")

lbl_title = tk.Label(sidebar, text="Signify", font=("Helvetica", 20, "bold"), fg="#ff7f50", bg=SIDEBAR_BTN_BG)
lbl_title.pack(pady=(20, 30))

sidebar_buttons = {}

def make_sidebar_button(text, page_name):
    btn = tk.Button(sidebar,
                    text=text,
                    font=("Helvetica", 14),
                    bg=SIDEBAR_BTN_BG,
                    fg="black",
                    bd=0,
                    relief="flat",
                    anchor="w",
                    padx=20,
                    activebackground=ACTIVE_BTN_BG,
                    command=lambda: show_frame(page_name))
    btn.pack(fill="x", pady=10, padx=10)
    sidebar_buttons[page_name] = btn
    return btn

make_sidebar_button("🏠  Home", "home")
make_sidebar_button("🎵  Practice", "practice")
make_sidebar_button("📖  Dictionary", "dictionary")
make_sidebar_button("⚙️  Setting", "setting")

# ---------------------------
# Divider line
# ---------------------------
divider = tk.Frame(root, bg=WHITE, width=2)
divider.pack(side="left", fill="y")

# ---------------------------
# Content Container
# ---------------------------
container = tk.Frame(root, bg=BG)
container.pack(side="left", fill="both", expand=True)

pages = {}
for name in ("home", "practice", "dictionary", "setting"):
    frame = tk.Frame(container, bg=BG)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    pages[name] = frame

# ============================================================
# ====================== HOME PAGE ===========================
# ============================================================
home = pages["home"]

header_frame = tk.Frame(home, bg=BG)
header_frame.pack(pady=40)

# Add your image here ↓↓↓ (replace with actual path)
# logo_img = PhotoImage(file="path/to/namaste_image.png")
# logo_lbl = tk.Label(header_frame, image=logo_img, bg=BG); logo_lbl.image = logo_img
logo_lbl = tk.Label(header_frame, text="🙏", font=("Arial", 48), bg=BG)
logo_lbl.pack(side="left", padx=20)

text_frame = tk.Frame(header_frame, bg=BG)
text_frame.pack(side="left")

app_title = tk.Label(text_frame, text="नमस्ते", fg="#1f51ff", bg=BG, font=("Noto Sans Devanagari", 40, "bold"))
app_title.pack(anchor="w")
subtitle = tk.Label(text_frame, text='“बातचीत Sabke Liye – Signify”', fg="#ff4d4d", bg=BG, font=("Helvetica", 18, "italic"))
subtitle.pack(anchor="w")

button_frame = tk.Frame(home, bg=BG)
button_frame.pack(pady=60)

def create_colored_button(parent, text, color, file_to_open=None, width=280, height=160):
    border = tk.Frame(parent, bg=WHITE, bd=0)
    border.pack_propagate(False)
    border.config(width=width, height=height)
    inner = tk.Frame(border, bg=color)
    inner.pack(expand=True, fill="both", padx=6, pady=6)

    def click_action():
        if file_to_open:
            open_module(file_to_open)

    lbl = tk.Button(inner, text=text, bg=color, fg="black", font=("Helvetica", 16, "bold"),
                    justify="center", bd=0, activebackground=color, command=click_action)
    lbl.pack(expand=True, fill="both")
    return border

# Top row
top_row = tk.Frame(button_frame, bg=BG)
top_row.pack()
b1 = create_colored_button(top_row, "📷\nStart Recognition", "#D1FFBD", "sign_to_text.py", width=420, height=170)
b1.pack(side="left", padx=30, pady=10)
b2 = create_colored_button(top_row, "📝\nText to Sign", "#FFF59E", "text_to_sign.py", width=420, height=170)
b2.pack(side="left", padx=30, pady=10)

# Bottom single
bottom_row = tk.Frame(button_frame, bg=BG)
bottom_row.pack()
b3 = create_colored_button(bottom_row, "🔊\nSign to Voice", "#fbd9d3", "sign_to_voice.py", width=900, height=140)
b3.pack(padx=10, pady=20)

# ============================================================
# ===================== PRACTICE PAGE ========================
# ============================================================
practice = pages["practice"]

title_frame = tk.Frame(practice, bg=BG)
title_frame.pack(pady=40)
lbl1 = tk.Label(title_frame, text="Where ", font=("Arial Rounded MT Bold", 36), bg=BG)
lbl1.pack(side="left")
lbl2 = tk.Label(title_frame, text="Learning", font=("Arial Rounded MT Bold", 36), fg="orange", bg=BG)
lbl2.pack(side="left")
lbl3 = tk.Label(title_frame, text=" Meets Play", font=("Arial Rounded MT Bold", 36), bg=BG)
lbl3.pack(side="left")

# Placeholders for images
tk.Label(practice, text="[Game Image Here]", bg=BG, font=("Arial", 12)).pack(pady=(20,10))
tk.Label(practice, text="[Quiz Image Here]", bg=BG, font=("Arial", 12)).pack(pady=(0,20))

frame_buttons = tk.Frame(practice, bg=BG)
frame_buttons.pack(pady=20)

def create_activity_card(parent, text, color, file_to_open=None, w=420, h=110):
    outer = tk.Frame(parent, bg=WHITE)
    outer.pack_propagate(False)
    outer.config(width=w, height=h)
    inner = tk.Frame(outer, bg=color)
    inner.pack(expand=True, fill="both", padx=6, pady=6)

    def click_action():
        if file_to_open:
            open_module(file_to_open)

    lbl = tk.Button(inner, text=text, bg=color, font=("Helvetica", 16, "bold"),
                    bd=0, activebackground=color, command=click_action)
    lbl.pack(expand=True, fill="both")
    return outer

# Layout (3x2 style)
left_col = tk.Frame(frame_buttons, bg=BG)
left_col.grid(row=0, column=0, padx=40)
right_col = tk.Frame(frame_buttons, bg=BG)
right_col.grid(row=0, column=1, padx=40)

create_activity_card(left_col, "Alphabets", "#A2FF9C", "dict_a_to_z.py").pack(pady=10)
create_activity_card(left_col, "Flashcard", "#a3c5ff", "flashcard.py").pack(pady=10)
create_activity_card(right_col, "Words", "#FFF59E", "dict_intro.py").pack(pady=10)
create_activity_card(right_col, "Sign Race", "#A2FF9C", "sign_race.py").pack(pady=10)

r2 = tk.Frame(frame_buttons, bg=BG)
r2.grid(row=1, column=0, columnspan=2, pady=10)
create_activity_card(r2, "Numbers (0–9)", "#a3c5ff", "dict_num.py", w=900).pack()

# ============================================================
# ===================== DICTIONARY PAGE ======================
# ============================================================
dictionary = pages["dictionary"]

tframe = tk.Frame(dictionary, bg=BG)
tframe.pack(pady=40)
tk.Label(tframe, text="Your Sign Language ", font=("Arial Rounded MT Bold", 36), bg=BG).pack(side="left")
tk.Label(tframe, text="Library", font=("Arial Rounded MT Bold", 36), fg="orange", bg=BG).pack(side="left")

tk.Label(dictionary, text="[Top Image Here]", bg=BG, font=("Arial", 12)).pack(pady=(10,20))

cards_frame = tk.Frame(dictionary, bg=BG)
cards_frame.pack(pady=10)

create_activity_card(cards_frame, "A to Z", "#D1FFBD", "dict_a_to_z.py").grid(row=0, column=0, padx=60, pady=20)
create_activity_card(cards_frame, "0 to 9", "#FFF59E", "dict_num.py").grid(row=0, column=1, padx=60, pady=20)
create_activity_card(cards_frame, "Introduction", "#fbd9d3", "dict_intro.py").grid(row=1, column=0, columnspan=2, pady=20)

# ============================================================
# ===================== SETTINGS PAGE ========================
# ============================================================
setting = pages["setting"]

main_box = tk.Frame(setting, bg="#b3e5fc", width=700, height=700, highlightbackground=WHITE, highlightthickness=4)
main_box.place(relx=0.5, rely=0.5, anchor="center")
tk.Label(main_box, text="Settings", font=("Arial Rounded MT Bold", 20, "bold"), bg="#b3e5fc").place(x=290, y=20)

def create_setting_row(parent, text, icon_text, y):
    row_frame = tk.Frame(parent, bg="#E3F2FD", width=600, height=70, highlightbackground="black", highlightthickness=1)
    row_frame.place(x=50, y=y)
    tk.Label(row_frame, text=icon_text, bg="#E3F2FD", font=("Arial", 18)).place(x=15, y=12)
    tk.Label(row_frame, text=text, bg="#E3F2FD", font=("Arial Rounded MT Bold", 14)).place(x=70, y=18)

create_setting_row(main_box, "Notification", "🔔", 100)
create_setting_row(main_box, "Privacy & Security", "🛡️", 190)
create_setting_row(main_box, "Help & Support", "🧑‍💼", 280)
create_setting_row(main_box, "About", "ℹ️", 370)

# ============================================================
# Default Page
# ============================================================
set_active_sidebar("home")
show_frame("home")

root.mainloop()
