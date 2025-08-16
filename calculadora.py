from __future__ import annotations
import ast
import math
import re
from typing import Any, Dict, Union, Optional

try:
	import tkinter as tk
	from tkinter import ttk
	from tkinter import font as tkfont
	TK_AVAILABLE = True
except Exception:
	TK_AVAILABLE = False
	import types
	tk = types.SimpleNamespace(Tk=object)
	ttk = None
	tkfont = None


Number = Union[int, float]


class SafeEvaluator(ast.NodeVisitor):
	"""Securely evaluate a limited arithmetic expression AST."""

	allowed_bin_ops = (
		ast.Add,
		ast.Sub,
		ast.Mult,
		ast.Div,
		ast.Pow,
	)
	allowed_unary_ops = (ast.UAdd, ast.USub)

	def __init__(self, names: Optional[Dict[str, Any]] = None, funcs: Optional[Dict[str, Any]] = None) -> None:
		self.names = names or {"pi": math.pi, "e": math.e}
		self.funcs = funcs or {
			"sqrt": math.sqrt,
			"sin": math.sin,
			"cos": math.cos,
			"tan": math.tan,
			"log": math.log10,
			"ln": math.log,
		}

	def visit(self, node: ast.AST) -> Number:
		method = "visit_" + node.__class__.__name__
		visitor = getattr(self, method, self.generic_visit)
		return visitor(node)

	def visit_Expression(self, node: ast.Expression) -> Number:
		return self.visit(node.body)

	def visit_BinOp(self, node: ast.BinOp) -> Number:
		if not isinstance(node.op, self.allowed_bin_ops):
			raise ValueError("Operación no permitida")
		left = self.visit(node.left)
		right = self.visit(node.right)
		if isinstance(node.op, ast.Add):
			return left + right
		if isinstance(node.op, ast.Sub):
			return left - right
		if isinstance(node.op, ast.Mult):
			return left * right
		if isinstance(node.op, ast.Div):
			return left / right
		if isinstance(node.op, ast.Pow):
			return left ** right
		raise ValueError("Operación no permitida")

	def visit_UnaryOp(self, node: ast.UnaryOp) -> Number:
		if not isinstance(node.op, self.allowed_unary_ops):
			raise ValueError("Operación no permitida")
		operand = self.visit(node.operand)
		if isinstance(node.op, ast.UAdd):
			return +operand
		if isinstance(node.op, ast.USub):
			return -operand
		raise ValueError("Operación no permitida")

	def visit_Call(self, node: ast.Call) -> Number:
		if not isinstance(node.func, ast.Name):
			raise ValueError("Llamada no permitida")
		name = node.func.id
		if name not in self.funcs:
			raise ValueError("Función no permitida")
		args = [self.visit(arg) for arg in node.args]
		if node.keywords:
			raise ValueError("Argumentos nombrados no permitidos")
		return self.funcs[name](*args)

	def visit_Name(self, node: ast.Name) -> Number:
		if node.id not in self.names:
			raise ValueError("Nombre no permitido")
		return self.names[node.id]

	def visit_Constant(self, node: ast.Constant) -> Number:
		if isinstance(node.value, (int, float)):
			return node.value
		raise ValueError("Constante no numérica")

	# Python <3.8 compatibility if needed
	def visit_Num(self, node: ast.Num) -> Number:  # type: ignore[override]
		return node.n

	def generic_visit(self, node: ast.AST) -> Number:
		raise ValueError("Elemento no permitido en la expresión")


def evaluate_expression(expression: str) -> Number:
	"""Evaluate a user expression safely, supporting ^ for power and math names."""
	if not expression or not expression.strip():
		raise ValueError("Expresión vacía")
	# Replace unicode operators with python equivalents
	clean = (
		expression.replace("×", "*")
		.replace("÷", "/")
		.replace("−", "-")
		.replace("^", "**")
	)
	# Protect against consecutive operators like "**" already used for power is fine
		# but sequences like "//" should not occur; we do not support floor division
	if "//" in clean:
		raise ValueError("Operador no soportado: //")
	try:
		tree = ast.parse(clean, mode="eval")
		return SafeEvaluator().visit(tree)
	except ZeroDivisionError:
		raise ValueError("División por cero")
	except OverflowError:
		raise ValueError("Resultado demasiado grande")
	except Exception as exc:
		raise ValueError("Expresión inválida") from exc


def format_number(value: Number) -> str:
	"""Format result removing trailing .0 and limiting precision sensibly."""
	if isinstance(value, float) and value.is_integer():
		return str(int(value))
	# Limit to 12 significant digits for display, avoid scientific notation for small/medium numbers
	formatted = ("{:.12g}".format(value))
	return formatted


class CalculatorApp(tk.Tk):
	"""GUI Calculator with elegant styling, history panel and keyboard support."""

	def __init__(self) -> None:
		super().__init__()
		self.title("Calculadora")
		self.minsize(420, 540)
		self.geometry("520x600")
		self._current_theme = "dark"

		self._create_style()
		self._create_layout()
		self._bind_keyboard()

		# Internal state
		self.expression_var = tk.StringVar(value="")
		self.display_var = tk.StringVar(value="0")
		self.small_display_var = tk.StringVar(value="")

		# Connect variables to widgets
		self.entry.configure(textvariable=self.display_var)
		self.small_label.configure(text=self.small_display_var.get())
		self.small_display_var.trace_add("write", lambda *_: self.small_label.configure(text=self.small_display_var.get()))

	def _create_style(self) -> None:
		self.style = ttk.Style(self)
		# Use a modern base theme
		try:
			self.style.theme_use("clam")
		except tk.TclError:
			pass
		self._apply_theme_colors(self._current_theme)

	def _apply_theme_colors(self, theme: str) -> None:
		if theme == "dark":
			bg = "#0b1220"
			card = "#111827"
			muted = "#9CA3AF"
			fg = "#E5E7EB"
			digit_bg = "#1F2937"
			op_bg = "#374151"
			accent = "#2563EB"
			warn = "#EF4444"
			focus = "#3B82F6"
		else:
			bg = "#F3F4F6"
			card = "#FFFFFF"
			muted = "#6B7280"
			fg = "#111827"
			digit_bg = "#F3F4F6"
			op_bg = "#E5E7EB"
			accent = "#2563EB"
			warn = "#DC2626"
			focus = "#1D4ED8"

		self.configure(bg=bg)
		default_font = tkfont.nametofont("TkDefaultFont")
		default_font.configure(size=11)
		self.option_add("*Font", default_font)

		# Base styles
		self.style.configure("TFrame", background=bg)
		self.style.configure("Card.TFrame", background=card)
		self.style.configure("TLabel", background=card, foreground=fg)
		self.style.configure("Muted.TLabel", background=card, foreground=muted)

		entry_font = ("Inter", 26)
		small_font = ("Inter", 11)
		btn_font = ("Inter", 14)
		self.style.configure(
			"Display.TEntry",
			background=card,
			fieldbackground=card,
			foreground=fg,
			insertcolor=fg,
			padding=8,
			borderwidth=0,
			font=entry_font,
		)
		self.style.map(
			"Display.TEntry",
			fieldbackground=[("readonly", card)],
			foreground=[("readonly", fg)],
		)

		# Buttons
		common = dict(
			padding=8,
			borderwidth=0,
			font=btn_font,
		)
		self.style.configure("Btn.TButton", **common, background=digit_bg, foreground=fg)
		self.style.map(
			"Btn.TButton",
			background=[("active", focus)],
			foreground=[("active", "#ffffff")],
		)
		self.style.configure("Op.TButton", **common, background=op_bg, foreground=fg)
		self.style.map(
			"Op.TButton",
			background=[("active", focus)],
			foreground=[("active", "#ffffff")],
		)
		self.style.configure("Accent.TButton", **common, background=accent, foreground="#ffffff")
		self.style.map(
			"Accent.TButton",
			background=[("active", focus)],
		)
		self.style.configure("Warn.TButton", **common, background=warn, foreground="#ffffff")
		self.style.map(
			"Warn.TButton",
			background=[("active", focus)],
		)

		# Treeview (historial)
		self.style.configure(
			"Treeview",
			background=card,
			foreground=fg,
			fieldbackground=card,
			borderwidth=0,
		)
		self.style.map("Treeview", background=[("selected", focus)], foreground=[("selected", "#ffffff")])
		self.style.configure("Vertical.TScrollbar", background=card)

	def _create_layout(self) -> None:
		# Root layout: left content + optional right history
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		container = ttk.Frame(self, style="TFrame")
		container.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)
		container.columnconfigure(0, weight=1)
		container.rowconfigure(2, weight=1)

		# Header / toolbar
		header = ttk.Frame(container, style="TFrame")
		header.grid(row=0, column=0, sticky="ew")
		header.columnconfigure(1, weight=1)
		title_lbl = ttk.Label(header, text="Calculadora", style="TLabel", font=("Inter", 14, "bold"))
		title_lbl.grid(row=0, column=0, sticky="w")
		self.theme_btn = ttk.Button(header, text="🌙", style="Op.TButton", command=self._toggle_theme)
		self.theme_btn.grid(row=0, column=2, sticky="e", padx=(8, 0))
		self.hist_btn = ttk.Button(header, text="🕘 Historial", style="Op.TButton", command=self._toggle_history)
		self.hist_btn.grid(row=0, column=3, sticky="e", padx=(8, 0))

		# Display card
		display_card = ttk.Frame(container, padding=14, style="Card.TFrame")
		display_card.grid(row=1, column=0, sticky="ew", pady=(12, 12))
		display_card.columnconfigure(0, weight=1)

		self.small_label = ttk.Label(display_card, text="", anchor="e", style="Muted.TLabel", font=("Inter", 11))
		self.small_label.grid(row=0, column=0, sticky="ew")

		self.entry = ttk.Entry(display_card, justify="right", state="readonly", style="Display.TEntry")
		self.entry.grid(row=1, column=0, sticky="ew", pady=(6, 0))

		# Buttons grid
		keypad_card = ttk.Frame(container, padding=14, style="Card.TFrame")
		keypad_card.grid(row=2, column=0, sticky="nsew")
		for i in range(4):
			keypad_card.columnconfigure(i, weight=1, uniform="col")
		for i in range(6):
			keypad_card.rowconfigure(i, weight=1, uniform="row")

		# Row 0
		self._button(keypad_card, "C", self._on_clear, style="Warn.TButton").grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
		self._button(keypad_card, "⌫", self._on_backspace, style="Op.TButton").grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
		self._button(keypad_card, "(", lambda: self._append("("), style="Op.TButton").grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
		self._button(keypad_card, ")", lambda: self._append(")"), style="Op.TButton").grid(row=0, column=3, sticky="nsew", padx=6, pady=6)

		# Rows 1-4
		rows = [
			["7", "8", "9", "÷"],
			["4", "5", "6", "×"],
			["1", "2", "3", "−"],
			["±", "0", ".", "+"],
		]
		for r_index, row in enumerate(rows, start=1):
			for c_index, key in enumerate(row):
				if key == "±":
					cmd = self._on_toggle_sign
					style = "Op.TButton"
				elif key in {"÷", "×", "−", "+"}:
					cmd = (lambda k=key: self._append(self._op_to_symbol(k)))
					style = "Op.TButton"
				else:
					cmd = (lambda k=key: self._append(k))
					style = "Btn.TButton"
				self._button(keypad_card, key, cmd, style=style).grid(
					row=r_index, column=c_index, sticky="nsew", padx=6, pady=6
				)

		# Row 5: equals spans all columns
		self._button(keypad_card, "=", self._on_equals, style="Accent.TButton").grid(
			row=5, column=0, columnspan=4, sticky="nsew", padx=6, pady=(6, 0)
		)

		# History panel (hidden by default)
		self.history_visible = False
		self.history_frame = ttk.Frame(self, padding=(0, 14, 14, 14), style="TFrame")
		self.history_frame.grid(row=0, column=1, sticky="nsew")
		self.grid_columnconfigure(1, weight=0)
		self.history_frame.grid_remove()

		self.history_frame.rowconfigure(1, weight=1)
		self.history_frame.columnconfigure(0, weight=1)
		hdr = ttk.Label(self.history_frame, text="Historial", style="TLabel", font=("Inter", 12, "bold"))
		hdr.grid(row=0, column=0, sticky="w", pady=(0, 8))

		columns = ("exp", "res")
		self.tree = ttk.Treeview(self.history_frame, columns=columns, show="headings", height=12)
		self.tree.heading("exp", text="Expresión")
		self.tree.heading("res", text="Resultado")
		self.tree.column("exp", width=160, anchor="e")
		self.tree.column("res", width=100, anchor="e")
		self.tree.grid(row=1, column=0, sticky="nsew")
		sb = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.tree.yview)
		sb.grid(row=1, column=1, sticky="ns")
		self.tree.configure(yscrollcommand=sb.set)
		self.tree.bind("<Double-1>", self._on_history_double_click)

	def _button(self, parent: tk.Widget, text: str, command, style: str) -> ttk.Button:
		return ttk.Button(parent, text=text, command=command, style=style)

	def _bind_keyboard(self) -> None:
		self.bind("<Key>", self._on_keypress)
		self.bind("<Return>", lambda e: self._on_equals())
		self.bind("<KP_Enter>", lambda e: self._on_equals())
		self.bind("<Escape>", lambda e: self._on_clear())
		self.bind("<BackSpace>", lambda e: self._on_backspace())

	def _toggle_theme(self) -> None:
		self._current_theme = "light" if self._current_theme == "dark" else "dark"
		self._apply_theme_colors(self._current_theme)
		self.theme_btn.configure(text="🌙" if self._current_theme == "dark" else "☀️")

	def _toggle_history(self) -> None:
		self.history_visible = not self.history_visible
		if self.history_visible:
			self.history_frame.grid()
			self.grid_columnconfigure(1, weight=0, minsize=300)
		else:
			self.history_frame.grid_remove()
			self.grid_columnconfigure(1, weight=0, minsize=0)

	@staticmethod
	def _op_to_symbol(key: str) -> str:
		return {"÷": "/", "×": "*", "−": "-", "+": "+"}[key]

	def _append(self, s: str) -> None:
		current = self.display_var.get()
		if current == "0" and s not in (".", ")"):
			current = ""
		new_val = current + s
		self.display_var.set(new_val)

	def _on_clear(self) -> None:
		self.display_var.set("0")
		self.small_display_var.set("")

	def _on_backspace(self) -> None:
		current = self.display_var.get()
		if not current or current == "0":
			return
		new_val = current[:-1]
		self.display_var.set(new_val if new_val else "0")

	def _on_toggle_sign(self) -> None:
		text = self.display_var.get()
		# If the whole input is a number, just negate it
		try:
			val = float(text)
			self.display_var.set(format_number(-val))
			return
		except Exception:
			pass
		# Toggle sign of the last number token
		match = re.search(r"(^|[+\-*/(])(-?\d*\.?\d+)$", text)
		if not match:
			return
		prefix = text[: match.start(2)]
		number = match.group(2)
		if number.startswith("-"):
			number = number[1:]
		else:
			number = "-" + number
		self.display_var.set(prefix + number)

	def _on_equals(self) -> None:
		expr = self.display_var.get().strip()
		if not expr:
			return
		try:
			result = evaluate_expression(expr)
			formatted = format_number(result)
			self.small_display_var.set(expr)
			self.display_var.set(formatted)
			self._push_history(expr, formatted)
		except ValueError as err:
			self.small_display_var.set(expr)
			self.display_var.set("Error")
			self.after(1200, lambda: self.display_var.set("0"))

	def _push_history(self, expression: str, result: str) -> None:
		self.tree.insert("", index=0, values=(expression, result))

	def _on_history_double_click(self, _event) -> None:
		item = self.tree.selection()
		if not item:
			return
		values = self.tree.item(item[0], "values")
		if not values:
			return
		expression = str(values[0])
		self.small_display_var.set("")
		self.display_var.set(expression)

	def _on_keypress(self, event: object) -> None:
		char = event.char
		keysym = event.keysym
		if char in "0123456789":
			self._append(char)
			return
		if char in ".()":
			self._append(char)
			return
		if char in "+-*/^":
			self._append("**" if char == "^" else char)
			return
		if keysym in ("KP_Add", "KP_Subtract", "KP_Multiply", "KP_Divide"):
			mapping = {
				"KP_Add": "+",
				"KP_Subtract": "-",
				"KP_Multiply": "*",
				"KP_Divide": "/",
			}
			self._append(mapping[keysym])
			return
		# Allow 's' to compute sqrt(...) of the last number quickly
		if char.lower() == "s":
			self._wrap_last_number_with("sqrt")
			return

	def _wrap_last_number_with(self, func_name: str) -> None:
		text = self.display_var.get()
		match = re.search(r"(.*?)(\d*\.?\d+)$", text)
		if not match:
			return
		prefix, number = match.group(1), match.group(2)
		self.display_var.set(f"{prefix}{func_name}({number})")


def main() -> None:
	if TK_AVAILABLE:
		app = CalculatorApp()
		app.mainloop()
	else:
		print("Tkinter no está disponible. Instala python3-tk para la interfaz gráfica.")
		print("Modo consola: escribe una expresión y presiona Enter (CTRL+C para salir).")
		try:
			while True:
				line = input("> ").strip()
				if not line:
					continue
				try:
					print(format_number(evaluate_expression(line)))
				except Exception as e:
					print("Error:", e)
		except (KeyboardInterrupt, EOFError):
			print()


if __name__ == "__main__":
	main()