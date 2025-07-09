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
    def run_compile():
        code = code_input.get("1.0", tk.END)
        try:
            Compiler().compile(code)
            messagebox.showinfo("Éxito", "El código fue compilado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error:\n{str(e)}")

    def insertar_texto_prueba():
        code_input.delete("1.0", tk.END)
        code_input.insert(tk.END, TEXTO_PRUEBA)        

    root = tk.Tk()
    root.title("Music DSL Compiler")

    # Editor de texto
    code_input = scrolledtext.ScrolledText(root, width=80, height=20)
    code_input.pack(padx=10, pady=10)

    # Frame inferior para los botones
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    # Botón de prueba (inserta texto en el área de texto)
    test_button = tk.Button(bottom_frame, text="Prueba", command=insertar_texto_prueba)
    test_button.pack(side=tk.LEFT)

    # Botón de compilar
    compile_button = tk.Button(bottom_frame, text="Play", command=run_compile)
    compile_button.pack(side=tk.RIGHT)

    root.mainloop()