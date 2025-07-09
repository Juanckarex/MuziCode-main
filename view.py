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
        fig, ax = plt.subplots(figsize=(6, 2), facecolor="#181818")
        ax.set_facecolor("#181818")
        ax.plot(audio, color='#2ecc40')  # verde para la onda
        ax.set_title("Forma de onda", color="#fff")
        ax.set_xlabel("Muestras", color="#fff")
        ax.set_ylabel("Amplitud", color="#fff")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor('#fff')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    root = tk.Tk()
    root.title("Music DSL Compiler")
    root.configure(bg="#181818")

    # Estilos generales
    style_args = {"bg": "#181818", "fg": "#fff", "insertbackground": "#fff", "highlightbackground": "#fff", "highlightcolor": "#fff"}
    code_input = scrolledtext.ScrolledText(root, width=80, height=12, **style_args, borderwidth=2, relief="solid")
    code_input.pack(padx=10, pady=(10, 0))
    # No insertar texto por defecto para evitar errores de compilación

    console_output = scrolledtext.ScrolledText(root, height=6, state="disabled", bg="#181818", fg="#fff", insertbackground="#fff", borderwidth=2, relief="solid", highlightbackground="#fff", highlightcolor="#fff")
    console_output.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)
    console_output.configure(font=("Consolas", 10))
    console_output.configure(state="normal")
    console_output.insert(tk.END, "Console\n")
    console_output.configure(state="disabled")

    bottom_frame = tk.Frame(root, bg="#181818")
    bottom_frame.pack(fill=tk.X, padx=10, pady=5)

    test_button = tk.Button(bottom_frame, text="Prueba", command=insertar_texto_prueba, bg="#181818", fg="#fff", activebackground="#222", activeforeground="#fff", borderwidth=1, relief="solid", highlightbackground="#fff")
    test_button.pack(side=tk.LEFT, padx=5)

    compile_button = tk.Button(bottom_frame, text="Compilar y Guardar", command=run_compile, bg="#181818", fg="#fff", activebackground="#222", activeforeground="#fff", borderwidth=1, relief="solid", highlightbackground="#fff")
    compile_button.pack(side=tk.RIGHT, padx=5)

    play_button = tk.Button(bottom_frame, text="▶", command=run_play, bg="#2ecc40", fg="#fff", font=("Arial", 14, "bold"), activebackground="#27ae60", activeforeground="#fff", borderwidth=1, relief="solid", highlightbackground="#fff")
    play_button.pack(side=tk.RIGHT, padx=5)

    waveform_frame = tk.Frame(root, height=120, bg="#181818", highlightbackground="#fff", highlightcolor="#fff", highlightthickness=1, bd=0)
    waveform_frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)

    # Etiqueta de Wavelength
    label_wave = tk.Label(root, text="Wavelengh", bg="#181818", fg="#fff", font=("Arial", 10))
    label_wave.pack(pady=(0, 5))

    # Cambia los bordes de los cuadros principales
    code_input.config(borderwidth=2, relief="solid", highlightthickness=2, highlightbackground="#fff")
    console_output.config(borderwidth=2, relief="solid", highlightthickness=2, highlightbackground="#fff")
    waveform_frame.config(borderwidth=2, relief="solid", highlightthickness=2, highlightbackground="#fff")

    root.mainloop()