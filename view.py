# view.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
from compiler import Compiler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import wave
import os
import threading
import time
from lexical import LexicalAnalyzer
from sintactic import SintacticAnalyzer

TEXTO_PRUEBA = """tempo 80
pattern kick = [1,0,1,0]
pattern snare = [1,0,1,0]
pattern hat = [1,0,1,1]
melody main = [E4, G4, C4, C4, G4, E4, C4]
repeat 2
save salida.wav (kick, snare, hat, main)
mix (kick, snare, hat, main)
"""


def show_gui():
    def log_to_console(msg):
        console_output.configure(state="normal")
        console_output.insert(tk.END, msg + "\n")
        console_output.see(tk.END)
        console_output.configure(state="disabled")
        # Si el mensaje indica que se guardó un wav, graficar
        if msg.startswith("Mezcla guardada como "):
            wav_path = msg.split("Mezcla guardada como ")[-1].strip()
            if os.path.exists(wav_path):
                plot_waveform(wav_path, waveform_frame)

    def run_compile():
        code = code_input.get("1.0", tk.END)
        try:
            compiler = Compiler(log_callback=log_to_console)
            compiler.compile(code)
            log_to_console("Compilación completada exitosamente.")
            # Mostrar la forma de onda de salida.wav si existe
            if os.path.exists("salida.wav"):
                plot_waveform("salida.wav", waveform_frame)
        except Exception as e:
            log_to_console(f"[ERROR] {str(e)}")

    def run_play():
        try:
            import simpleaudio
            if not os.path.exists("salida.wav"):
                log_to_console("[ERROR] No existe salida.wav. Compila primero.")
                return
            wave_obj = simpleaudio.WaveObject.from_wave_file("salida.wav")
            play_obj = wave_obj.play()
        except Exception as e:
            log_to_console(f"[ERROR reproducción]: {str(e)}")

    def insertar_texto_prueba():
        code_input.delete("1.0", tk.END)
        code_input.insert(tk.END, TEXTO_PRUEBA)

    def plot_waveform(wav_path, parent_frame, show_bar=False, bar_pos=0.0):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        with wave.open(wav_path, 'rb') as wf:
            n_frames = wf.getnframes()
            audio = wf.readframes(n_frames)
            audio = np.frombuffer(audio, dtype=np.int16)
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.plot(audio, color='blue')
        ax.set_title("Forma de onda")
        ax.set_xlabel("Muestras")
        ax.set_ylabel("Amplitud")
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    root = tk.Tk()
    root.title("Music DSL Compiler")

    code_input = scrolledtext.ScrolledText(root, width=80, height=20)
    code_input.pack(padx=10, pady=(10, 0))

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(fill=tk.X, padx=10, pady=5)

    test_button = tk.Button(bottom_frame, text="Prueba", command=insertar_texto_prueba)
    test_button.pack(side=tk.LEFT)

    compile_button = tk.Button(bottom_frame, text="Compilar y Guardar", command=run_compile)
    compile_button.pack(side=tk.RIGHT)

    play_button = tk.Button(bottom_frame, text="Play", command=run_play)
    play_button.pack(side=tk.RIGHT, padx=5)

    console_output = scrolledtext.ScrolledText(root, height=10, state="disabled", bg="#111", fg="#0f0")
    console_output.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)

    waveform_frame = tk.Frame(root, height=120)
    waveform_frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)

    root.mainloop()