import tkinter as tk
from tkinter import ttk
import math

class ElegantCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora Elegante")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Color scheme - modern dark theme
        self.bg_color = "#1e1e1e"
        self.display_bg = "#2d2d2d"
        self.button_bg = "#3c3c3c"
        self.button_hover = "#4c4c4c"
        self.operator_bg = "#ff9500"
        self.operator_hover = "#ffad33"
        self.text_color = "#ffffff"
        self.display_text = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
        
        # Variables for calculation
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display frame
        display_frame = tk.Frame(main_frame, bg=self.display_bg, height=120, relief=tk.FLAT, bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 20))
        display_frame.pack_propagate(False)
        
        # Previous operation display
        self.prev_label = tk.Label(
            display_frame, 
            text="", 
            font=("Segoe UI", 12), 
            bg=self.display_bg, 
            fg="#888888",
            anchor="e"
        )
        self.prev_label.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # Current display
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            font=("Segoe UI", 28, "bold"), 
            bg=self.display_bg, 
            fg=self.display_text,
            anchor="e"
        )
        self.display.pack(fill=tk.BOTH, padx=15, pady=(0, 15))
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button configuration
        button_config = {
            'font': ('Segoe UI', 16, 'bold'),
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': 'hand2',
            'fg': self.text_color
        }
        
        # Create buttons
        buttons = [
            ['C', '⌫', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                btn_bg = self.operator_bg if text in ['÷', '×', '-', '+', '='] else self.button_bg
                btn_hover = self.operator_hover if text in ['÷', '×', '-', '+', '='] else self.button_hover
                
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    bg=btn_bg,
                    activebackground=btn_hover,
                    command=lambda t=text: self.button_click(t),
                    **button_config
                )
                
                # Special width for 0 button
                colspan = 2 if text == '0' else 1
                btn.grid(row=i, column=j, columnspan=colspan, sticky="nsew", padx=2, pady=2)
                
                # Hover effects
                btn.bind("<Enter>", lambda e, b=btn, color=btn_hover: b.configure(bg=color))
                btn.bind("<Leave>", lambda e, b=btn, color=btn_bg: b.configure(bg=color))
        
        # Configure grid weights
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
            
        # Keyboard bindings
        self.root.bind('<Key>', self.key_press)
        self.root.focus_set()
    
    def button_click(self, value):
        if value.isdigit() or value == '.':
            self.input_number(value)
        elif value in ['÷', '×', '-', '+']:
            self.input_operator(value)
        elif value == '=':
            self.calculate()
        elif value == 'C':
            self.clear()
        elif value == '⌫':
            self.backspace()
        elif value == '±':
            self.toggle_sign()
        elif value == '%':
            self.percentage()
    
    def input_number(self, num):
        if self.should_reset:
            self.current = "0"
            self.should_reset = False
            
        if num == '.' and '.' in self.current:
            return
            
        if self.current == "0" and num != '.':
            self.current = num
        else:
            self.current += num
            
        self.update_display()
    
    def input_operator(self, op):
        if self.previous and self.operator and not self.should_reset:
            self.calculate()
        
        self.previous = self.current
        self.operator = op
        self.should_reset = True
        self.update_prev_display()
    
    def calculate(self):
        if not self.previous or not self.operator:
            return
            
        try:
            prev_num = float(self.previous)
            current_num = float(self.current)
            
            if self.operator == '+':
                result = prev_num + current_num
            elif self.operator == '-':
                result = prev_num - current_num
            elif self.operator == '×':
                result = prev_num * current_num
            elif self.operator == '÷':
                if current_num == 0:
                    self.current = "Error"
                    self.update_display()
                    return
                result = prev_num / current_num
            
            # Format result
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = f"{result:.10g}"
                
            self.previous = ""
            self.operator = ""
            self.should_reset = True
            self.update_display()
            self.prev_label.config(text="")
            
        except (ValueError, ZeroDivisionError):
            self.current = "Error"
            self.update_display()
    
    def clear(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        self.update_display()
        self.prev_label.config(text="")
    
    def backspace(self):
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()
    
    def toggle_sign(self):
        if self.current != "0" and self.current != "Error":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.update_display()
    
    def percentage(self):
        try:
            num = float(self.current)
            self.current = str(num / 100)
            self.update_display()
            self.should_reset = True
        except ValueError:
            pass
    
    def update_display(self):
        # Limit display length
        display_text = self.current
        if len(display_text) > 12:
            try:
                num = float(display_text)
                display_text = f"{num:.6e}"
            except ValueError:
                display_text = display_text[:12]
        
        self.display_var.set(display_text)
    
    def update_prev_display(self):
        if self.previous and self.operator:
            self.prev_label.config(text=f"{self.previous} {self.operator}")
    
    def key_press(self, event):
        key = event.char
        
        if key.isdigit() or key == '.':
            self.input_number(key)
        elif key in ['+', '-']:
            self.input_operator(key)
        elif key == '*':
            self.input_operator('×')
        elif key == '/':
            self.input_operator('÷')
            event.char = ''  # Prevent default behavior
        elif key in ['\r', '\n', '=']:  # Enter or equals
            self.calculate()
        elif key in ['\x08', '\x7f']:  # Backspace or Delete
            self.backspace()
        elif key.lower() == 'c':
            self.clear()
        elif key == '%':
            self.percentage()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    calculator = ElegantCalculator()
    calculator.run()