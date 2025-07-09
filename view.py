# view.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
from compiler import Compiler

TEXTO_PRUEBA = """tempo 80
pattern kick = [1,0,1,0]
pattern snare = [1,0,1,0]
pattern hat = [1,0,1,1]
melody main = [E4, G4, C4, C4, G4, E4, C4]
repeat 2
save salida.wav (kick, snare, hat, main)
"""



def show_gui():

    def log_to_console(msg):
        console_output.configure(state="normal")
        console_output.insert(tk.END, msg + "\n")
        console_output.see(tk.END)
        console_output.configure(state="disabled")

    def run_compile():
        code = code_input.get("1.0", tk.END)
        try:
            compiler = Compiler(log_callback=log_to_console)
            compiler.compile(code)
            log_to_console("Compilación completada exitosamente.")
        except Exception as e:
            log_to_console(f"[ERROR] {str(e)}")

    def insertar_texto_prueba():
        code_input.delete("1.0", tk.END)
        code_input.insert(tk.END, TEXTO_PRUEBA)        

    root = tk.Tk()
    root.title("Music DSL Compiler")

    
    # Cuadro de texto principal para el código
    code_input = scrolledtext.ScrolledText(root, width=80, height=20)
    code_input.pack(padx=10, pady=(10, 0))

    # Frame inferior para botones
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(fill=tk.X, padx=10, pady=5)

    test_button = tk.Button(bottom_frame, text="Prueba", command=insertar_texto_prueba)
    test_button.pack(side=tk.LEFT)

    compile_button = tk.Button(bottom_frame, text="Play", command=run_compile)
    compile_button.pack(side=tk.RIGHT)

    # Consola de salida (solo lectura)
    console_output = scrolledtext.ScrolledText(root, height=10, state="disabled", bg="#111", fg="#0f0")
    console_output.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)

    root.mainloop()