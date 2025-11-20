import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox  # <-- NEW: Fixes the messagebox error
from PIL import Image, ImageTk, ImageDraw 
import re # For email validation
import subprocess # For running external ML scripts

# --- Configuration & Styling ---
PRIMARY_COLOR = "#19F1F5"     # Blue for the button and links
SECONDARY_COLOR = "#B9F3A6"   # Green for success/sign up button
ERROR_COLOR = "#FBA9A9"       # Red for error messages
BG_CONTENT_COLOR = "#FFFFFF"  # Base color for content frame background
LIGHT_BLUE_BG = "#D0E0F0"     # Lighter blue for sidebar/main background
DASHBOARD_BLUE = "#B0E0E6"    # Background color used in the dashboard/practice screenshot
PRACTICE_BG = DASHBOARD_BLUE  # Background color for main content areas

# Dictionary Card Colors 
AZ_COLOR = "#21E8F6"          # Light Blue
NUMBERS_COLOR = "#A5D6A7"     # Greenish
INTRO_COLOR = "#F2E67A"       # Yellow
TALKS_COLOR = "#F4A9BC"       # Pinkish

# Settings Page Styling
SETTINGS_CONTAINER_BG = "#FFFFFF" # White background for the central settings panel
SETTINGS_ITEM_BG = "#E0F7FA"      # Very light cyan/blue for the buttons (similar to Picture.png)
SETTINGS_BORDER_COLOR = "#B0E0E6" # Light blue border color
SETTINGS_TEXT_COLOR = "#333333" # Dark text


# Global variables for images, must be declared outside classes for Tkinter to keep a reference
signify_logo = None
welcome_full_bg_img = None 
welcome_full_bg_pil = None # Holds the original PIL image for resizing


# --- Utility Functions ---
def is_valid_email_or_phone(text):
    """Simple check for email or 10-digit number."""
    # Phone number (10 digits)
    if re.fullmatch(r'\d{10}', text):
        return True
    # Basic email format
    if re.fullmatch(r'[^@]+@[^@]+\.[^@]+', text):
        return True
    return False


# --- Main Application Class ---
class SignifyApp(tk.Tk):
    """
    Main application window managing different pages (frames).
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.subtitle_font = tkfont.Font(family='Helvetica', size=14, weight="bold")
        self.text_font = tkfont.Font(family='Helvetica', size=10)
        
        self.title("Signify: ISL Translator & Learner")
        self.geometry("1000x600") 
        self.minsize(800, 500)
        
        # 1. Load Assets & Icons
        self.load_assets()
        # Load specific icons for navigation and pages
        self.home_icon = self.load_icon("home.png", size=(20, 20))
        self.practice_icon = self.load_icon("jjj.png", size=(20, 20))
        self.dictionary_icon = self.load_icon("jj.png", size=(20, 20))
        self.setting_icon = self.load_icon("settings.jpg", size=(20, 20))
        
        # Practice Page Icons (Placeholders, assume the user provides these)
        self.game_icon = self.load_icon("game.png", size=(50, 50))
        self.quiz_icon = self.load_icon("quiz.jpeg", size=(50, 50))
        # self.color_sign_icon = self.load_icon("colors.png", size=(30, 30)) # REMOVED
        self.flashcard_icon = self.load_icon("flashcard.png", size=(30, 30))
        self.sign_race_icon = self.load_icon("race.jpeg", size=(30, 30))
        self.alphabets_icon = self.load_icon("abc.png", size=(30, 30))
        self.words_icon = self.load_icon("word.png", size=(30, 30))
        self.sentences_icon = self.load_icon("sentence.png", size=(30, 30))
        
        # Dictionary Page Icons (Placeholders, based on dict.jpeg)
        self.az_icon = self.load_icon("alphabet.png", size=(50, 50))
        self.numbers_icon = self.load_icon("numbers.png", size=(50, 50))
        self.intro_icon = self.load_icon("intro.png", size=(50, 50))
        # self.talks_icon = self.load_icon("talk.png", size=(50, 50)) # REMOVED
        
        # Settings Page Icons (Placeholders, based on Picture.png)
        # Using icons that visually represent the content (Alert, Lock, Help, Info)
        self.notif_icon = self.load_icon("notification.jpg", size=(30, 30))
        self.privacy_icon = self.load_icon("security.jpg", size=(30, 30))
        self.support_icon = self.load_icon("help_icon.png", size=(30, 30))
        self.about_icon = self.load_icon("about.jpg", size=(30, 30))


        # 2. Container setup
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # 3. Initialize all pages (frames)
        for F in (WelcomePage, LoginPage, SignupPage, HomePage, PracticePage, DictionaryPage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") 
        
        self.show_frame("WelcomePage") 
        
    def load_icon(self, filename, size):
        """Helper function to load and resize icons."""
        try:
            pil_img = Image.open(filename)
            pil_img = pil_img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(pil_img)
        except FileNotFoundError:
            # Create a simple placeholder image (e.g., a colored square)
            placeholder_img = Image.new('RGB', size, color = '#cccccc')
            d = ImageDraw.Draw(placeholder_img)
            d.text((5, 5), '?', fill=(0,0,0))
            return ImageTk.PhotoImage(placeholder_img)
        except Exception as e:
            return None

    def load_assets(self):
        """Loads all general assets (logo, background)."""
        global welcome_full_bg_pil, welcome_full_bg_img, signify_logo
        
        # Load background image
        try:
            welcome_full_bg_pil = Image.open("fir.jpg")
            welcome_full_bg_img = ImageTk.PhotoImage(welcome_full_bg_pil) 
        except FileNotFoundError:
            try:
                welcome_full_bg_pil = Image.open("fir.jpeg")
                welcome_full_bg_img = ImageTk.PhotoImage(welcome_full_bg_pil) 
            except FileNotFoundError:
                pass
            except Exception:
                pass
        except Exception:
            pass

        # Load logo
        try:
            logo_pil_img = Image.open("logo.png") 
            logo_pil_img = logo_pil_img.resize((150, 150), Image.Resampling.LANCZOS)
            signify_logo = ImageTk.PhotoImage(logo_pil_img)
        except FileNotFoundError:
            pass
        except Exception:
            pass
            
    def launch_ml_script(self, script_name):
        """Launches an external Python script using subprocess."""
        try:
            # NOTE: If running on a different environment, 'python' may need to be 'python3' 
            # or the full path to your environment's python executable.
            subprocess.Popen(['python', script_name]) 
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not launch {script_name}.\n\nEnsure:\n1. The file '{script_name}' exists in the current directory.\n2. The 'python' command is accessible in your system's PATH.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while trying to launch {script_name}.\nDetails: {e}")


    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
        # Trigger background update/centering when the frame is shown
        if page_name == "WelcomePage" and hasattr(frame, 'update_background'):
             frame.update_background() 


# ------------------- Page 1: Welcome Page -------------------
class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg_image_id = None
        self.canvas_window = None 
        
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        if welcome_full_bg_img:
            self.bg_image_id = self.canvas.create_image(0, 0, anchor="center", image=welcome_full_bg_img)
        else:
            self.canvas.config(bg="#DCBC99") 
        
        self.content_frame = tk.Frame(self.canvas, bg=BG_CONTENT_COLOR, 
                                      padx=30, pady=30, relief=tk.RAISED, bd=1, highlightthickness=0)
        
        if signify_logo:
            logo_label = tk.Label(self.content_frame, image=signify_logo, bg=BG_CONTENT_COLOR) 
            logo_label.pack(pady=(10, 10))
        else:
            logo_label = tk.Label(self.content_frame, text="SIGNIFY LOGO", 
                                  font=controller.title_font, fg=PRIMARY_COLOR, bg=BG_CONTENT_COLOR)
            logo_label.pack(pady=(10, 10))
            
        description_label = tk.Label(self.content_frame, 
                                     text="Connect through ISL: Sign-to-Text and Text-to-Sign", 
                                     font=('Helvetica', 12), fg="#333333", bg=BG_CONTENT_COLOR)
        description_label.pack(pady=(0, 20))

        get_started_button = tk.Button(self.content_frame, text="Get Started", 
                                       command=lambda: controller.show_frame("LoginPage"),
                                       bg=PRIMARY_COLOR, fg="white",
                                       font=('Helvetica', 16, 'bold'), 
                                       activebackground=PRIMARY_COLOR, activeforeground="white",
                                       relief=tk.FLAT, bd=0, padx=30, pady=15, highlightthickness=0)
        get_started_button.pack(pady=20)
        
        self.canvas_window = self.canvas.create_window(0, 0, window=self.content_frame, anchor="nw")
        
        self.content_frame.bind("<Configure>", self.center_content)
        self.bind("<Configure>", self.update_background)

    def center_content(self, event=None):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        content_width = self.content_frame.winfo_reqwidth()
        content_height = self.content_frame.winfo_reqheight()

        x = (canvas_width - content_width) / 2
        y = (canvas_height - content_height) / 2
        
        x = max(0, x)
        y = max(0, y)

        self.canvas.coords(self.canvas_window, x, y)

    def update_background(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        
        if welcome_full_bg_pil and self.bg_image_id is not None:
            img_width, img_height = welcome_full_bg_pil.size
            ratio_w = width / img_width
            ratio_h = height / img_height
            scale_factor = max(ratio_w, ratio_h)
            
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            
            if new_width > 0 and new_height > 0:
                try:
                    resized_pil = welcome_full_bg_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    global welcome_full_bg_img
                    welcome_full_bg_img = ImageTk.PhotoImage(resized_pil)
                    self.canvas.itemconfig(self.bg_image_id, image=welcome_full_bg_img)
                    self.canvas.coords(self.bg_image_id, width/2, height/2)
                except Exception as e:
                    pass

        if self.canvas_window is not None:
             self.canvas.tag_raise(self.canvas_window)
        
        self.center_content(None) 

# ------------------- Page 2: Login Page -------------------
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=DASHBOARD_BLUE)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- LEFT SIDE: IMAGE AREA ----------------
        illustration_frame = tk.Frame(self, bg=DASHBOARD_BLUE)
        illustration_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=50)

        # --- ADD LOGIN PNG DIRECTLY ---
        try:
            login_img = Image.open("login.png")   # add your image here
            login_img = login_img.resize((350, 350), Image.Resampling.LANCZOS)
            self.login_photo = ImageTk.PhotoImage(login_img)

            illustration_image_label = tk.Label(
                illustration_frame,
                image=self.login_photo,
                bg=DASHBOARD_BLUE
            )
            illustration_image_label.pack(expand=True, fill="both", padx=20, pady=20)

        except Exception as e:
            illustration_label = tk.Label(
                illustration_frame,
                text="[Login Image Missing]",
                font=('Helvetica', 14, 'italic'),
                fg="#555555",
                bg=DASHBOARD_BLUE,
                width=40,
                height=20
            )
            illustration_label.pack(expand=True, fill="both", padx=20, pady=20)

        # ---------------- RIGHT SIDE: LOGIN FORM ----------------
        form_container = tk.Frame(self, bg="#FFFFFF", padx=40, pady=50, relief=tk.RAISED, bd=1)
        form_container.grid(row=0, column=1, sticky="nsew", padx=(0, 50), pady=50)
        form_container.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(
            form_container,
            text="LOGIN",
            font=controller.title_font,
            fg="#333333",
            bg="#FFFFFF"
        )
        title_label.pack(pady=(0, 30))

        # Email / Phone
        email_label = tk.Label(
            form_container,
            text="Email / Phone no",
            anchor='w',
            font=controller.text_font,
            bg="#FFFFFF",
            fg="#333333"
        )
        email_label.pack(fill='x', pady=(10, 0))

        self.email_entry = tk.Entry(
            form_container,
            font=controller.text_font,
            relief=tk.RIDGE,
            bd=2,
            width=30
        )
        self.email_entry.pack(fill='x', ipady=5)

        # Password
        password_label = tk.Label(
            form_container,
            text="Password",
            anchor='w',
            font=controller.text_font,
            bg="#FFFFFF",
            fg="#333333"
        )
        password_label.pack(fill='x', pady=(10, 0))

        self.password_entry = tk.Entry(
            form_container,
            font=controller.text_font,
            relief=tk.RIDGE,
            bd=2,
            show='*',
            width=30
        )
        self.password_entry.pack(fill='x', ipady=5)

        # Error message
        self.error_message = tk.StringVar()
        error_label = tk.Label(
            form_container,
            textvariable=self.error_message,
            fg=ERROR_COLOR,
            bg="#FFFFFF",
            font=controller.text_font
        )
        error_label.pack(pady=(5, 10))

        # Login Button
        login_button = tk.Button(
            form_container,
            text="Login",
            command=self.handle_login,
            bg=PRIMARY_COLOR,
            fg="white",
            font=controller.subtitle_font,
            activebackground=PRIMARY_COLOR,
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            highlightthickness=0
        )
        login_button.pack(fill='x', pady=(10, 20))

        # Forgot Password
        forgot_password_link = tk.Label(
            form_container,
            text="Forgot Password?",
            fg=PRIMARY_COLOR,
            bg="#FFFFFF",
            cursor="hand2"
        )
        forgot_password_link.bind("<Button-1>", lambda e: self.error_message.set("Forgot Password functionality TBD."))
        forgot_password_link.pack(pady=(0, 10))

        # Signup Prompt
        signup_prompt = tk.Label(
            form_container,
            text="Don't have an account?",
            bg="#FFFFFF",
            fg="#333333"
        )
        signup_prompt.pack()

        signup_link = tk.Label(
            form_container,
            text="Sign Up Here",
            fg=PRIMARY_COLOR,
            bg="#FFFFFF",
            cursor="hand2",
            font=controller.text_font
        )
        signup_link.bind("<Button-1>", lambda e: controller.show_frame("SignupPage"))
        signup_link.pack(pady=(0, 10))

    # ---------------- HANDLE LOGIN ----------------
    def handle_login(self):
        email_phone = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email_phone or not password:
            self.error_message.set("Please enter both email/phone and password.")
            return

        if not is_valid_email_or_phone(email_phone):
            self.error_message.set("Invalid email or 10-digit phone number format.")
            return

        if password == "1234":
            self.error_message.set("")
            self.controller.show_frame("HomePage")
        else:
            self.error_message.set("Invalid credentials. Try password '1234'.")


# ------------------- Page 3: Signup Page -------------------
class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=DASHBOARD_BLUE) 
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)
        
        illustration_frame = tk.Frame(self, bg=DASHBOARD_BLUE)
        illustration_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=50)
        illustration_label = tk.Label(illustration_frame, text="[Signup Illustration]", 
                                      font=('Helvetica', 14, 'italic'), fg="#555555", bg=DASHBOARD_BLUE, width=40, height=20)
        illustration_label.pack(expand=True, fill="both", padx=20, pady=20)

        form_container = tk.Frame(self, bg="#FFFFFF", padx=40, pady=50, relief=tk.RAISED, bd=1)
        form_container.grid(row=0, column=1, sticky="nsew", padx=(0, 50), pady=50)
        form_container.grid_columnconfigure(0, weight=1)
        
        title_label = tk.Label(form_container, text="SIGN UP", font=controller.title_font, fg="#333333", bg="#FFFFFF")
        title_label.pack(pady=(0, 30))

        name_label = tk.Label(form_container, text="Full Name", anchor='w', font=controller.text_font, bg="#FFFFFF", fg="#333333")
        name_label.pack(fill='x', pady=(10, 0))
        self.name_entry = tk.Entry(form_container, font=controller.text_font, relief=tk.RIDGE, bd=2, width=30)
        self.name_entry.pack(fill='x', ipady=5)
        
        email_label = tk.Label(form_container, text="Email / Phone no", anchor='w', font=controller.text_font, bg="#FFFFFF", fg="#333333")
        email_label.pack(fill='x', pady=(10, 0))
        self.email_entry = tk.Entry(form_container, font=controller.text_font, relief=tk.RIDGE, bd=2, width=30)
        self.email_entry.pack(fill='x', ipady=5)
        
        password_label = tk.Label(form_container, text="Password", anchor='w', font=controller.text_font, bg="#FFFFFF", fg="#333333")
        password_label.pack(fill='x', pady=(10, 0))
        self.password_entry = tk.Entry(form_container, font=controller.text_font, relief=tk.RIDGE, bd=2, show='*', width=30)
        self.password_entry.pack(fill='x', ipady=5)

        self.error_message = tk.StringVar()
        error_label = tk.Label(form_container, textvariable=self.error_message, fg=ERROR_COLOR, bg="#FFFFFF", font=controller.text_font)
        error_label.pack(pady=(5, 10))

        signup_button = tk.Button(form_container, text="Sign Up", command=self.handle_signup, bg=PRIMARY_COLOR, fg="white",
                                 font=controller.subtitle_font, activebackground=PRIMARY_COLOR, activeforeground="white",
                                 relief=tk.FLAT, bd=0, padx=20, pady=10, highlightthickness=0)
        signup_button.pack(fill='x', pady=(10, 10))

        or_label = tk.Label(form_container, text="OR", bg="#FFFFFF", fg="#888888")
        or_label.pack(pady=10)

        login_button = tk.Button(form_container, text="Login", command=lambda: controller.show_frame("LoginPage"),
                                 bg="#FFFFFF", fg=PRIMARY_COLOR, font=controller.subtitle_font, 
                                 activebackground="#EEEEEE", activeforeground=PRIMARY_COLOR,
                                 relief=tk.SOLID, bd=1, padx=20, pady=10, highlightthickness=0)
        login_button.pack(fill='x', pady=(0, 20))

    def handle_signup(self):
        full_name = self.name_entry.get().strip()
        email_phone = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not full_name or not email_phone or not password:
            self.error_message.set("All fields are required.")
            return

        if not is_valid_email_or_phone(email_phone):
            self.error_message.set("Invalid email or 10-digit phone number format.")
            return

        self.error_message.set("Sign Up successful! Redirecting to login...")
        self.controller.after(1500, lambda: self.controller.show_frame("LoginPage"))


# ------------------- Common: Navigation Bar Class -------------------
class NavigationBar(tk.Frame):
    def __init__(self, parent, controller, active_page):
        tk.Frame.__init__(self, parent, width=150, bg=LIGHT_BLUE_BG, relief=tk.FLAT)
        self.controller = controller
        self.active_page = active_page
        self.pack_propagate(False)
        
        # Signify Logo/Title at the top
        logo_label = tk.Label(self, text="Signify", font=('Helvetica', 16, 'bold'), 
                              fg=PRIMARY_COLOR, bg=LIGHT_BLUE_BG)
        logo_label.pack(pady=(20, 30))

        # Navigation Buttons
        self.create_nav_button("Home", "HomePage", controller.home_icon)
        self.create_nav_button("Practice", "PracticePage", controller.practice_icon)
        self.create_nav_button("Dictionary", "DictionaryPage", controller.dictionary_icon)
        self.create_nav_button("Setting", "SettingsPage", controller.setting_icon)
        
        # Logout at the bottom
        logout_button = tk.Button(self, text="Logout", 
                                 command=lambda: controller.show_frame("LoginPage"),
                                 bg="#FF6347", fg="white", relief=tk.FLAT)
        logout_button.pack(side=tk.BOTTOM, pady=20, padx=10, fill='x')


    def create_nav_button(self, text, page_name, icon):
        is_active = (page_name == self.active_page) 
        
        btn = tk.Button(self, 
                        text=text, 
                        image=icon, 
                        compound=tk.LEFT,
                        command=lambda: self.controller.show_frame(page_name),
                        font=('Helvetica', 12, 'bold' if is_active else 'normal'),
                        bg=PRIMARY_COLOR if is_active else LIGHT_BLUE_BG,
                        fg="white" if is_active else "#333333",
                        activebackground=PRIMARY_COLOR if is_active else "#C0D0E0",
                        activeforeground="white" if is_active else "#333333",
                        relief=tk.FLAT, 
                        bd=0, 
                        padx=10, 
                        pady=10, 
                        anchor='w')
        btn.image = icon 
        btn.pack(fill='x', pady=5, padx=10)


# ------------------- Page 4: Home Page (UPDATED COMMANDS) -------------------
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=LIGHT_BLUE_BG) 
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        nav_bar = NavigationBar(self, controller, active_page="HomePage")
        nav_bar.grid(row=0, column=0, sticky="nsew")

        main_content = tk.Frame(self, bg=DASHBOARD_BLUE, padx=20, pady=20)
        main_content.grid(row=0, column=1, sticky="nsew")
        main_content.grid_rowconfigure(0, weight=0)
        main_content.grid_rowconfigure(1, weight=1)
        main_content.grid_columnconfigure(0, weight=1)

        # --- Top Section: Header ---
        header_frame = tk.Frame(main_content, bg=DASHBOARD_BLUE)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        # --- Small Frame for Image + Text (Left to Right) ---
        title_row = tk.Frame(header_frame, bg=DASHBOARD_BLUE)
        title_row.pack(anchor='w', padx=(100, 0))

        # --- Load image to appear before "नमस्ते" ---
        try:
            hello_img = Image.open("namesta.png")     # <-- your image file name
            hello_img = hello_img.resize((50, 50), Image.Resampling.LANCZOS)
            self.hello_icon = ImageTk.PhotoImage(hello_img)

            icon_label = tk.Label(title_row, image=self.hello_icon, bg=DASHBOARD_BLUE)
            icon_label.pack(side="left", padx=(0, 10))

        except:
            icon_label = tk.Label(title_row, text="🖼️", bg=DASHBOARD_BLUE, fg="white", font=("Arial", 20))
            icon_label.pack(side="left", padx=(0, 10))

        # --- नमस्ते text ---
        title_label = tk.Label(
            title_row,
            text="नमस्ते",
            font=('Arial', 30, 'bold'),
            fg=PRIMARY_COLOR,
            bg=DASHBOARD_BLUE
        )
        title_label.pack(side="left")

        # --- Subtitle below it ---
        subtitle_label = tk.Label(
            header_frame,
            text="\"बातचीत सबके लिये - Signify\"",
            font=('Arial', 12),
            fg="#555555",
            bg=DASHBOARD_BLUE
        )
        subtitle_label.pack(anchor='w', padx=(100, 0))


        # --- Middle Section: Feature Cards ---
        card_container = tk.Frame(main_content, bg=DASHBOARD_BLUE, padx=50, pady=30)
        card_container.grid(row=1, column=0, sticky="nsew")
        card_container.grid_columnconfigure(0, weight=1)
        card_container.grid_columnconfigure(1, weight=1)
        card_container.grid_rowconfigure(0, weight=1)
        card_container.grid_rowconfigure(1, weight=1)

        # 1. Start Recognition (Sign-to-Text) - GREEN
        # CONNECTED TO: sign_to_text.py
        self.create_feature_card(card_container, "Start Recognition", "Sign-to-Text", "#A5D6A7", 
                                 lambda: controller.launch_ml_script("sign_to_text.py"), 
                                 controller.load_icon("camera.png", size=(40,40)), 0, 0)
        
        # 2. Text-to-Sign - YELLOW
        # CONNECTED TO: text_to_sign.py
        self.create_feature_card(card_container, "Text to Sign", "Text-to-Sign", "#FFF176", 
                                 lambda: controller.launch_ml_script("text_to_sign.py"), 
                                 controller.load_icon("text-sign.png", size=(40,40)), 0, 1)
                                 
        # 3. Sign-to-Voice (Sign to Voice) - RED/PINK
        # CONNECTED TO: sign_to_voice.py
        self.create_feature_card(card_container, "Sign to Voice", "Sign-to-Speech", "#EF9A9A", 
                                 lambda: controller.launch_ml_script("sign_to_voice.py"), 
                                 controller.load_icon("volume.png", size=(40,40)), 1, 0, columnspan=2)


    def create_feature_card(self, parent_frame, button_text, feature_name, color, command, icon, row, col, columnspan=1):
        card_frame = tk.Frame(parent_frame, bg=color, relief=tk.RAISED, bd=1)
        card_frame.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=20, pady=20)
        card_frame.grid_columnconfigure(0, weight=1)
        
        icon_label = tk.Label(card_frame, image=icon, text="[Icon]" if not icon else "", compound=tk.TOP, font=('Arial', 24), bg=color)
        icon_label.image = icon
        icon_label.pack(pady=(10, 5))
        
        button = tk.Button(card_frame, text=button_text, command=command,
                           font=('Helvetica', 14, 'bold'), bg=color, fg="#333333", relief=tk.FLAT, bd=0)
        button.pack(pady=10)

        
# ------------------- Page 5: Practice Page (UPDATED COMMANDS) -------------------
class PracticePage(tk.Frame):
    """
    Implements the layout for Games and Quizzes.
    - Removed 'Color Sign' button.
    - Updated commands for Flashcard and Sign Race.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=LIGHT_BLUE_BG) 
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left: Navigation Bar
        nav_bar = NavigationBar(self, controller, active_page="PracticePage")
        nav_bar.grid(row=0, column=0, sticky="nsew")

        # Right: Main Content Area (Practice Dashboard)
        main_content = tk.Frame(self, bg=PRACTICE_BG, padx=30, pady=30)
        main_content.grid(row=0, column=1, sticky="nsew")
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)
        main_content.grid_rowconfigure(0, weight=0) # Header row
        main_content.grid_rowconfigure(1, weight=1) # Main content row

        # --- Top Section: Header and Profile ---
        header_frame = tk.Frame(main_content, bg=PRACTICE_BG)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 30))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        
        # --- USER ICON + TITLE ---
        title_frame = tk.Frame(header_frame, bg=PRACTICE_BG)
        title_frame.grid(row=0, column=0, sticky="w", padx=20)

        # --- USER ICON IMAGE ---
        try:
            user_icon_img = Image.open("learning.png")     # replace with your image file
            user_icon_img = user_icon_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.user_icon_photo = ImageTk.PhotoImage(user_icon_img)

            tk.Label(title_frame, image=self.user_icon_photo, bg=PRACTICE_BG).pack(side=tk.LEFT, padx=(0, 10))

        except:
            tk.Label(title_frame, text="[User Icon Missing]", bg=PRACTICE_BG).pack(side=tk.LEFT, padx=(0, 10))

        # --- TITLE TEXT ---
        tk.Label(
            title_frame,
            text="Where Learning Meets Play",
            font=('Helvetica', 18, 'bold'),
            fg="#333333",
            bg=PRACTICE_BG
        ).pack(side=tk.LEFT)



        # --- PROFILE IMAGE + PROFILE LINK ---
        # Image first
        try:
            profile_img = Image.open("support.jpg")    # replace with your image file
            profile_img = profile_img.resize((35, 35), Image.Resampling.LANCZOS)
            self.profile_photo = ImageTk.PhotoImage(profile_img)

            tk.Label(header_frame, image=self.profile_photo, bg=PRACTICE_BG).grid(row=0, column=1, sticky="e", padx=(0, 10))

        except:
            tk.Label(header_frame, text="[Profile Image Missing]", bg=PRACTICE_BG, fg="#555555").grid(row=0, column=1, sticky="e")


        # Profile Label (clickable)
        profile_label = tk.Label(
            header_frame, text="Profile",
            font=('Helvetica', 12),
            fg=PRIMARY_COLOR,
            bg=PRACTICE_BG,
            cursor="hand2"
        )
        profile_label.bind("<Button-1>", lambda e: controller.show_frame("SettingsPage"))
        profile_label.grid(row=0, column=2, sticky="e", padx=(0, 20))


        # --- Main Content: Games and Quizzes Grid ---
        content_grid = tk.Frame(main_content, bg=PRACTICE_BG, padx=50, pady=20)
        content_grid.grid(row=1, column=0, columnspan=2, sticky="nsew")
        content_grid.grid_columnconfigure(0, weight=1)
        content_grid.grid_columnconfigure(1, weight=1)
        content_grid.grid_rowconfigure(0, weight=0) # Header
        content_grid.grid_rowconfigure(1, weight=0) # Flashcard/Alphabets
        content_grid.grid_rowconfigure(2, weight=0) # Sign Race/Words
        content_grid.grid_rowconfigure(3, weight=0) # Sentences
        
        # Define Colors
        FLASHCARD_COLOR = "#8CB1E3"     # Light Blue
        SIGN_RACE_COLOR = "#A5D6A7"     # Greenish
        ALPHABETS_COLOR = "#FFF176"     # Yellow
        WORDS_COLOR = "#FFF176"         # Yellow
        SENTENCES_COLOR = "#A5D6A7"      # Greenish

        # Game Title and Icon
        self.create_title_box(content_grid, "game icon", 0, 0, controller.game_icon)
        
        # Quiz Title and Icon
        self.create_title_box(content_grid, "quiz icon", 0, 1, controller.quiz_icon)

        # --- Game Cards (Column 0) ---
        # 1. Flashcard 
        # CONNECTED TO: flashcard.py
        self.create_practice_card(content_grid, "Flashcard", FLASHCARD_COLOR, 
                                  lambda: controller.launch_ml_script("flashcard.py"), controller.flashcard_icon, 1, 0)

        # 2. Sign Race
        # CONNECTED TO: sign_race.py
        self.create_practice_card(content_grid, "Sign Race", SIGN_RACE_COLOR, 
                                  lambda: controller.launch_ml_script("sign_race.py"), controller.sign_race_icon, 2, 0)


        # --- Quiz Cards (Column 1) ---
        self.create_practice_card(content_grid, "Alphabets", ALPHABETS_COLOR, 
                                  lambda: self.launch_activity("Alphabets Quiz"), controller.alphabets_icon, 1, 1)
        self.create_practice_card(content_grid, "Words", WORDS_COLOR, 
                                  lambda: self.launch_activity("Words Quiz"), controller.words_icon, 2, 1)
        self.create_practice_card(content_grid, "Sentences", SENTENCES_COLOR, 
                                  lambda: self.launch_activity("Sentences Quiz"), controller.sentences_icon, 3, 1)
        
        # Add empty row to push content up and center it more naturally
        content_grid.grid_rowconfigure(4, weight=1)


    def create_title_box(self, parent_frame, title_text, row, col, icon):
        """Creates the small rounded box for 'game' or 'quiz' title and icon."""
        title_box = tk.Frame(parent_frame, bg="#FFFFFF", padx=15, pady=5, relief=tk.RIDGE, bd=1)
        title_box.grid(row=row, column=col, sticky="n", pady=(0, 20), padx=20)
        
        box_icon = tk.Label(title_box, image=icon, text=title_text, compound=tk.TOP, font=('Arial', 8), bg="#FFFFFF", fg=PRIMARY_COLOR)
        box_icon.image = icon # Keep reference
        box_icon.pack()


    def create_practice_card(self, parent_frame, text, color, command, icon, row, col):
        """Creates a colored card button for a specific game/quiz."""
        card = tk.Button(parent_frame, 
                         text=text, 
                         image=icon,
                         compound=tk.RIGHT,
                         command=command,
                         font=('Helvetica', 14, 'bold'),
                         bg=color, 
                         fg="#333333", 
                         activebackground=color,
                         activeforeground="#333333",
                         relief=tk.FLAT, 
                         bd=0, 
                         padx=20, 
                         pady=15,
                         anchor='w')
        card.image = icon # Keep reference
        card.grid(row=row, column=col, sticky="ew", padx=20, pady=10)


    def launch_activity(self, activity_name):
        """Placeholder for launching quiz windows (non-ML scripts)."""
        messagebox.showinfo("Activity Launch", f"Launching: {activity_name}. This is for TBD Quiz logic.")


# ------------------- Page 6: Dictionary Page (UPDATED COMMANDS) -------------------
class DictionaryPage(tk.Frame):
    """
    Implements the dictionary layout.
    - Removed 'Talks' button.
    - Updated commands for remaining dictionary sections.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=PRACTICE_BG) 
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left: Navigation Bar
        nav_bar = NavigationBar(self, controller, active_page="DictionaryPage")
        nav_bar.grid(row=0, column=0, sticky="nsew")

        # Right: Main Content Area (Dictionary Library)
        main_content = tk.Frame(self, bg=PRACTICE_BG, padx=30, pady=30)
        main_content.grid(row=0, column=1, sticky="nsew")
        main_content.grid_columnconfigure(0, weight=1)
        main_row_frame = tk.Frame(main_content, bg=PRACTICE_BG)
        main_row_frame.pack(fill='both', expand=True)
        main_row_frame.grid_columnconfigure(0, weight=1)
        main_row_frame.grid_columnconfigure(1, weight=1)
        
        # --- Top Section: Header ---
        header_frame = tk.Frame(main_row_frame, bg=PRACTICE_BG)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="nw", pady=(0, 50), padx=50)

        tk.Label(header_frame, text="[User Icon]", font=('Arial', 30), bg=PRACTICE_BG, fg="#555555").pack(side=tk.LEFT, padx=(0, 15))
        title_label = tk.Label(header_frame, text="Your Sign Language ", font=('Helvetica', 20, 'bold'), fg="#333333", bg=PRACTICE_BG)
        title_label.pack(side=tk.LEFT)
        title_label_2 = tk.Label(header_frame, text="Library", font=('Helvetica', 20, 'bold'), fg="#FF8C00", bg=PRACTICE_BG)
        title_label_2.pack(side=tk.LEFT)


        # --- Main Content: Card Grid ---
        card_grid = tk.Frame(main_row_frame, bg=PRACTICE_BG, padx=50, pady=20)
        card_grid.grid(row=1, column=0, columnspan=2, sticky="nsew")
        # Configure grid for 3 items (2x2 layout with 1 removed item)
        card_grid.grid_columnconfigure(0, weight=1)
        card_grid.grid_columnconfigure(1, weight=1)
        card_grid.grid_rowconfigure(0, weight=1)
        card_grid.grid_rowconfigure(1, weight=1) # This row will only hold 1 item spanning 2 columns

        # 1. A to Z (Top Left)
        # CONNECTED TO: dict_a_to_z.py
        self.create_dictionary_card(card_grid, "A to Z", AZ_COLOR, controller.az_icon, 0, 0,
                                    lambda: controller.launch_ml_script("dict_a_to_z.py"))

        # 2. 1 to 20 (Top Right)
        # CONNECTED TO: dict_num.py
        self.create_dictionary_card(card_grid, "1 to 20", NUMBERS_COLOR, controller.numbers_icon, 0, 1,
                                    lambda: controller.launch_ml_script("dict_num.py"))

        # 3. Introduction (Bottom Center - Spanning both columns)
        # CONNECTED TO: dict_intro.py
        self.create_dictionary_card(card_grid, "Introduction", INTRO_COLOR, controller.intro_icon, 1, 0,
                                    lambda: controller.launch_ml_script("dict_intro.py"), columnspan=2)


    def create_dictionary_card(self, parent_frame, text, color, icon, row, col, command, columnspan=1):
        """Creates a large card for dictionary categories."""
        card_frame = tk.Frame(parent_frame, bg=color, relief=tk.RAISED, bd=1)
        card_frame.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=20, pady=20)
        
        # The button covers the entire card area
        button = tk.Button(card_frame, 
                           text=text, 
                           image=icon,
                           compound=tk.TOP,
                           command=command,
                           font=('Helvetica', 16, 'bold'),
                           bg=color, 
                           fg="#333333", 
                           activebackground=color,
                           activeforeground="#333333",
                           relief=tk.FLAT, 
                           bd=0, 
                           padx=30, 
                           pady=30)
        button.image = icon # Keep reference
        button.pack(expand=True, fill='both')

# ------------------- Page 7: Settings Page -------------------
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg=PRACTICE_BG) 
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left: Navigation Bar
        nav_bar = NavigationBar(self, controller, active_page="SettingsPage")
        nav_bar.grid(row=0, column=0, sticky="nsew")

        # Right: Main Content Area (Settings Panel)
        main_content = tk.Frame(self, bg=PRACTICE_BG, padx=30, pady=30)
        main_content.grid(row=0, column=1, sticky="nsew")
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_rowconfigure(0, weight=1)
        
        # Center the settings box
        settings_container = tk.Frame(main_content, bg=SETTINGS_CONTAINER_BG, bd=1, relief=tk.SOLID)
        settings_container.grid(row=0, column=0, padx=100, pady=50, sticky="nsew")
        settings_container.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = tk.Label(settings_container, text="SETTINGS", font=controller.title_font, 
                               fg="#333333", bg=SETTINGS_CONTAINER_BG, pady=20)
        title_label.pack(fill='x', padx=50, pady=(20, 30))
        
        # Settings Menu Items
        menu_frame = tk.Frame(settings_container, bg=SETTINGS_CONTAINER_BG, padx=50, pady=20)
        menu_frame.pack(fill='both', expand=True, pady=(0, 40))
        menu_frame.grid_columnconfigure(0, weight=1)

        self.create_setting_button(menu_frame, "Notification", controller.notif_icon, 
                                   lambda: self.setting_action("Notification Settings"), row=0)
        self.create_setting_button(menu_frame, "Privacy & Security", controller.privacy_icon, 
                                   lambda: self.setting_action("Privacy & Security"), row=1)
        self.create_setting_button(menu_frame, "Help & Support", controller.support_icon, 
                                   lambda: self.setting_action("Help & Support Center"), row=2)
        self.create_setting_button(menu_frame, "About", controller.about_icon, 
                                   lambda: self.setting_action("About App Information"), row=3)

    def create_setting_button(self, parent_frame, text, icon, command, row):
        """Creates a wide button for a settings option."""
        button = tk.Button(parent_frame, 
                           text=text, 
                           image=icon,
                           compound=tk.LEFT,
                           command=command,
                           font=('Helvetica', 14, 'bold'),
                           bg=SETTINGS_ITEM_BG, 
                           fg=SETTINGS_TEXT_COLOR, 
                           activebackground="#D3EBF0",
                           activeforeground=SETTINGS_TEXT_COLOR,
                           relief=tk.FLAT, 
                           bd=1, 
                           highlightthickness=1,
                           highlightbackground=SETTINGS_BORDER_COLOR,
                           padx=20, 
                           pady=15,
                           anchor='w')
        button.image = icon # Keep reference
        button.grid(row=row, column=0, sticky="ew", pady=5, ipady=5)

    def setting_action(self, action_name):
        """Placeholder for navigating to a specific setting."""
        messagebox.showinfo("Settings Action", f"Navigating to: {action_name}. Implementation of sub-pages is needed here.")


if __name__ == "__main__":
    app = SignifyApp()
    app.mainloop()