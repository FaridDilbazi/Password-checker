import tkinter as tk
from tkinter import ttk
import re
from zxcvbn import zxcvbn
import string
import random

class PasswordStrengthChecker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Strength Checker")
        self.window.geometry("600x500")
        self.window.configure(bg='#2b2b2b')
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TFrame', background='#2b2b2b')
        style.configure('Custom.TLabel', background='#2b2b2b', foreground='white')
        style.configure('Custom.TCheckbutton', background='#2b2b2b', foreground='white')
        
        main_frame = ttk.Frame(self.window, padding="20", style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self._init_password_input(main_frame)
        self._init_strength_meter(main_frame)
        self._init_analysis(main_frame)
        self._init_generator(main_frame)
        
        self.password_var.trace('w', self.check_password_strength)
    
    def _init_password_input(self, parent):
        ttk.Label(parent, text="Enter Password:", style='Custom.TLabel', 
                 font=('Helvetica', 12)).pack(pady=10)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(parent, textvariable=self.password_var, 
                                      show="•", width=40)
        self.password_entry.pack()
        
        self.show_password = tk.BooleanVar()
        ttk.Checkbutton(parent, text="Show Password", variable=self.show_password,
                       command=self._toggle_password, style='Custom.TCheckbutton').pack()
    
    def _init_strength_meter(self, parent):
        self.strength_meter = ttk.Progressbar(parent, length=300, mode='determinate')
        self.strength_meter.pack(pady=15)
        
        self.strength_label = ttk.Label(parent, text="Strength: ", 
                                      style='Custom.TLabel')
        self.strength_label.pack()
    
    def _init_analysis(self, parent):
        self.analysis_text = tk.Text(parent, height=8, width=50, bg='#363636',
                                   fg='white', font=('Helvetica', 10))
        self.analysis_text.pack(pady=10)
        
        self.crack_time = ttk.Label(parent, text="", style='Custom.TLabel')
        self.crack_time.pack()
    
    def _init_generator(self, parent):
        generator_frame = ttk.Frame(parent, style='Custom.TFrame')
        generator_frame.pack(fill=tk.X, pady=10)
        
        self.length_var = tk.StringVar(value="16")
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        
        controls_frame = ttk.Frame(generator_frame, style='Custom.TFrame')
        controls_frame.pack()
        
        ttk.Button(generator_frame, text="Generate Password", 
                  command=self.generate_password).pack(pady=10)
    
    def generate_password(self):
        length = int(self.length_var.get()) if self.length_var.get().isdigit() else 16
        chars = ''
        if self.use_upper.get(): chars += string.ascii_uppercase
        if self.use_lower.get(): chars += string.ascii_lowercase
        if self.use_digits.get(): chars += string.digits
        if self.use_special.get(): chars += string.punctuation
        
        if not chars: chars = string.ascii_letters + string.digits + string.punctuation
        
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
    
    def _toggle_password(self):
        self.password_entry.configure(show="" if self.show_password.get() else "•")
    
    def check_password_strength(self, *args):
        password = self.password_var.get()
        if not password:
            self._update_ui(0, "")
            return
        
        result = zxcvbn(password)
        score = result['score'] * 25
        
        requirements = []
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        requirements = [
            f"{'✓' if len(password) >= 8 else '✗'} Length: {len(password)}",
            f"{'✓' if has_upper else '✗'} Uppercase",
            f"{'✓' if has_lower else '✗'} Lowercase",
            f"{'✓' if has_digit else '✗'} Numbers",
            f"{'✓' if has_special else '✗'} Special Chars"
        ]
        
        self._update_ui(score, "\n".join(requirements))
        self.crack_time.configure(
            text=f"Estimated crack time: {result['crack_times_display']['offline_fast_hashing_1e10_per_second']}"
        )
    
    def _update_ui(self, score, requirements):
        self.strength_meter['value'] = score
        
        strength_mapping = {
            0: ("Very Weak", "#ff4444"),
            25: ("Weak", "#ffa700"),
            50: ("Medium", "#ffe100"),
            75: ("Strong", "#a3ff00"),
            100: ("Very Strong", "#00ff00")
        }
        
        for threshold, (label, color) in strength_mapping.items():
            if score <= threshold:
                self.strength_label.configure(text=f"Strength: {label}")
                break
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, requirements)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PasswordStrengthChecker()
    app.run()