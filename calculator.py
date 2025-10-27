import tkinter as tk
from tkinter import ttk
import math

class FuturisticCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 CALCULADORA CYBER 2024 🚀")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        
        # Futuristic color scheme - cyber neon theme
        self.bg_color = "#0a0a0a"  # Deep black
        self.panel_bg = "#1a1a2e"  # Dark blue-purple
        self.display_bg = "#16213e"  # Darker blue
        self.button_bg = "#0f3460"  # Dark cyber blue
        self.button_hover = "#1e5f8c"  # Bright cyber blue
        self.operator_bg = "#00ffff"  # Neon cyan
        self.operator_hover = "#00e6e6"  # Bright cyan
        self.special_bg = "#ff00ff"  # Neon magenta
        self.special_hover = "#e600e6"  # Bright magenta
        self.text_color = "#00ffff"  # Neon cyan text
        self.display_text = "#ffffff"  # White display text
        self.glow_color = "#00ffff"  # Cyan glow
        
        self.root.configure(bg=self.bg_color)
        
        # Variables for calculation
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with cyber border
        main_container = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title with futuristic styling
        title_frame = tk.Frame(main_container, bg=self.bg_color, height=50)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="◢ CYBER CALC ◤",
            font=("Orbitron", 20, "bold"),
            bg=self.bg_color,
            fg=self.glow_color,
            pady=10
        )
        title_label.pack()
        
        # Outer panel with neon border effect
        outer_panel = tk.Frame(main_container, bg=self.glow_color, padx=3, pady=3)
        outer_panel.pack(fill=tk.BOTH, expand=True)
        
        inner_panel = tk.Frame(outer_panel, bg=self.panel_bg, padx=20, pady=20)
        inner_panel.pack(fill=tk.BOTH, expand=True)
        
        # Display frame with multiple layers for glow effect
        display_outer = tk.Frame(inner_panel, bg=self.glow_color, padx=2, pady=2)
        display_outer.pack(fill=tk.X, pady=(0, 25))
        
        display_frame = tk.Frame(display_outer, bg=self.display_bg, height=140, relief=tk.FLAT)
        display_frame.pack(fill=tk.X)
        display_frame.pack_propagate(False)
        
        # Status indicator
        status_frame = tk.Frame(display_frame, bg=self.display_bg, height=20)
        status_frame.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        status_dots = tk.Label(
            status_frame,
            text="● ● ● ONLINE ● ● ●",
            font=("Courier", 8, "bold"),
            bg=self.display_bg,
            fg=self.glow_color
        )
        status_dots.pack()
        
        # Previous operation display with cyber styling
        self.prev_label = tk.Label(
            display_frame, 
            text="", 
            font=("Courier New", 12, "bold"), 
            bg=self.display_bg, 
            fg="#888888",
            anchor="e"
        )
        self.prev_label.pack(fill=tk.X, padx=15, pady=(5, 0))
        
        # Current display with futuristic font
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            font=("Orbitron", 32, "bold"), 
            bg=self.display_bg, 
            fg=self.display_text,
            anchor="e"
        )
        self.display.pack(fill=tk.BOTH, padx=15, pady=(0, 15))
        
        # Buttons frame
        buttons_frame = tk.Frame(inner_panel, bg=self.panel_bg)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button configuration
        button_config = {
            'font': ('Orbitron', 16, 'bold'),
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': 'hand2',
            'fg': self.text_color,
            'activeforeground': '#ffffff'
        }
        
        # Create buttons with futuristic symbols
        buttons = [
            ['CLR', '⟸', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['±', '0', '•', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                # Determine button style based on type
                if text in ['÷', '×', '−', '+', '=']:
                    btn_bg = self.operator_bg
                    btn_hover = self.operator_hover
                    text_color = '#000000'  # Black text on bright buttons
                elif text in ['CLR', '⟸', '%', '±']:
                    btn_bg = self.special_bg
                    btn_hover = self.special_hover
                    text_color = '#000000'  # Black text on bright buttons
                else:
                    btn_bg = self.button_bg
                    btn_hover = self.button_hover
                    text_color = self.text_color
                
                # Create button with border for glow effect
                btn_frame = tk.Frame(buttons_frame, bg=btn_bg, padx=1, pady=1)
                btn_frame.grid(row=i, column=j, columnspan=2 if text == '0' else 1, 
                              sticky="nsew", padx=3, pady=3)
                
                btn = tk.Button(
                    btn_frame,
                    text=text,
                    bg=btn_bg,
                    fg=text_color,
                    activebackground=btn_hover,
                    activeforeground='#ffffff',
                    command=lambda t=text: self.button_click(t),
                    **{k: v for k, v in button_config.items() if k not in ['fg']}
                )
                btn.pack(fill=tk.BOTH, expand=True)
                
                # Enhanced hover effects with color transitions
                def on_enter(e, button=btn, frame=btn_frame, hover_color=btn_hover):
                    button.configure(bg=hover_color)
                    frame.configure(bg=hover_color)
                    
                def on_leave(e, button=btn, frame=btn_frame, normal_color=btn_bg):
                    button.configure(bg=normal_color)
                    frame.configure(bg=normal_color)
                
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
                btn_frame.bind("<Enter>", on_enter)
                btn_frame.bind("<Leave>", on_leave)
        
        # Configure grid weights for responsive design
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
        
        # Footer with cyber branding
        footer_frame = tk.Frame(inner_panel, bg=self.panel_bg, height=30)
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="▼▲▼ QUANTUM COMPUTING DIVISION ▼▲▼",
            font=("Courier", 8),
            bg=self.panel_bg,
            fg="#555555"
        )
        footer_label.pack()
            
        # Keyboard bindings
        self.root.bind('<Key>', self.key_press)
        self.root.focus_set()
        
        # Add pulsing effect to the display
        self.pulse_display()
    
    def pulse_display(self):
        """Create a subtle pulsing effect on the display border"""
        colors = ["#00ffff", "#00e6e6", "#00cccc", "#00e6e6"]
        current_color = colors[0]
        
        def pulse():
            nonlocal current_color
            idx = colors.index(current_color)
            current_color = colors[(idx + 1) % len(colors)]
            
            # Find display outer frame and update color
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Frame) and str(grandchild).endswith('!frame2'):
                                    grandchild.configure(bg=current_color)
                                    break
            
            self.root.after(1500, pulse)  # Pulse every 1.5 seconds
        
        self.root.after(1500, pulse)
    
    def button_click(self, value):
        # Map display symbols to calculation symbols
        symbol_map = {
            '•': '.',
            '−': '-',
            'CLR': 'C',
            '⟸': '⌫'
        }
        
        mapped_value = symbol_map.get(value, value)
        
        if mapped_value.isdigit() or mapped_value == '.':
            self.input_number(mapped_value)
        elif mapped_value in ['÷', '×', '-', '+']:
            self.input_operator(mapped_value)
        elif mapped_value == '=':
            self.calculate()
        elif mapped_value == 'C':
            self.clear()
        elif mapped_value == '⌫':
            self.backspace()
        elif mapped_value == '±':
            self.toggle_sign()
        elif mapped_value == '%':
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
                    self.current = "ERROR"
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
            self.current = "ERROR"
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
        if self.current != "0" and self.current != "ERROR":
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
        # Limit display length and format for futuristic look
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
            self.prev_label.config(text=f">> {self.previous} {self.operator}")
    
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
    calculator = FuturisticCalculator()
    calculator.run()