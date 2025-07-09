# view.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
from compiler import Compiler

def show_gui():
    def run_compile():
        code = code_input.get("1.0", tk.END)
        try:
            Compiler().compile(code)
            messagebox.showinfo("Éxito", "El código fue compilado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error:\n{str(e)}")

    root = tk.Tk()
    root.title("Music DSL Compiler")

    # Editor de texto
    code_input = scrolledtext.ScrolledText(root, width=80, height=20)
    code_input.pack(padx=10, pady=10)

    # Frame inferior para los botones
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    # Botón de prueba (no hace nada)
    test_button = tk.Button(bottom_frame, text="Prueba", command=lambda: print("Botón de prueba presionado"))
    test_button.pack(side=tk.LEFT)

    # Botón de compilar
    compile_button = tk.Button(bottom_frame, text="Play", command=run_compile)
    compile_button.pack(side=tk.RIGHT)

    root.mainloop()