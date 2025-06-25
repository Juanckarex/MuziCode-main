"""Semantic analyzer for the music DSL."""

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import os


class SemanticAnalyzer:
    """
    This class interprets the parsed commands and executes the musical logic:
    - Stores tempo, patterns, and melodies
    - Handles mixing, playback, and saving using PyDub
    """

    def __init__(self, commands):
        self.commands = commands  # List of parsed commands (dicts)
        self.tempo = 120  # Default tempo
        self.patterns = {}  # Stores rhythm patterns
        self.melodies = {}  # Stores melodies
        self.samples_dir = "samples"  # Directory for drum samples
        self.notes_dir = "notes"      # Directory for note samples
        self.current_playback = None  # For stopping playback if needed

    def analyze(self):
        """
        Executes the list of commands, updating state and triggering audio actions.
        """
        for cmd in self.commands:
            if cmd["type"] == "TEMPO":
                self.tempo = cmd["value"]
            elif cmd["type"] == "PATTERN":
                self.patterns[cmd["name"]] = cmd["sequence"]
            elif cmd["type"] == "MELODY":
                self.melodies[cmd["name"]] = cmd["notes"]
            elif cmd["type"] == "MIX":
                self.mix_and_play(cmd["items"])
            elif cmd["type"] == "SAVE":
                self.mix_and_save(cmd["items"], cmd["filename"])

    def load_audio_file(self, file_path):
        """
        Loads an audio file (WAV) and returns an AudioSegment, or None if not found.
        """
        try:
            if not os.path.exists(file_path):
                print(f"Archivo no encontrado: {file_path}")
                return None
            return AudioSegment.from_wav(file_path)
        except Exception as e:
            print(f"Error cargando {file_path}: {str(e)}")
            return None

    def mix_and_play(self, items, loop=False):
        """
        Mixes and plays the given patterns/melodies by overlaying their audio.
        """
        if not items:
            print("Error: No hay items para mezclar")
            return
        beat_ms = 60000 // self.tempo  # Duration of a beat in ms
        final = AudioSegment.silent(duration=beat_ms * 4)  # 4 beats (1 compás)
        for name in items:
            sound = None
            if name in self.patterns:
                sound = self.create_pattern_sound(name, beat_ms)
            elif name in self.melodies:
                sound = self.create_melody_sound(name, beat_ms)
            if sound:
                final = final.overlay(sound)
        self.stop_playback()
        self.current_playback = _play_with_simpleaudio(final)
        if loop:
            pass  # Loop logic can be added here

    def mix_and_save(self, items, filename):
        """
        Mixes the given items and saves the result as a WAV file.
        """
        beat_ms = 60000 // self.tempo
        final = AudioSegment.silent(duration=beat_ms * 4)
        for name in items:
            sound = None
            if name in self.patterns:
                sound = self.create_pattern_sound(name, beat_ms)
            elif name in self.melodies:
                sound = self.create_melody_sound(name, beat_ms)
            if sound:
                final = final.overlay(sound)
        final.export(filename, format="wav")
        print(f"Mezcla guardada como {filename}")

    def create_pattern_sound(self, name, beat_ms):
        """
        Creates an AudioSegment for a rhythm pattern by sequencing hits and silences.
        """
        sound = AudioSegment.silent(duration=0)
        pattern = self.patterns[name]
        hit_sound = self.load_audio_file(f"{self.samples_dir}/{name}.wav")
        if not hit_sound:
            return None
        for val in pattern:
            if val == 1:
                sound += hit_sound + AudioSegment.silent(duration=beat_ms - len(hit_sound))
            else:
                sound += AudioSegment.silent(duration=beat_ms)
        return sound

    def create_melody_sound(self, name, beat_ms):
        """
        Creates an AudioSegment for a melody by sequencing note samples.
        """
        sound = AudioSegment.silent(duration=0)
        for note in self.melodies[name]:
            note_audio = self.load_audio_file(f"{self.notes_dir}/{note}.wav")
            if note_audio:
                sound += note_audio + AudioSegment.silent(duration=beat_ms - len(note_audio))
            else:
                sound += AudioSegment.silent(duration=beat_ms)
        return sound

    def stop_playback(self):
        """
        Stops current playback if any.
        """
        if self.current_playback:
            self.current_playback.stop()