"""This module contains the Compiler class for the music DSL."""

from lexical import LexicalAnalyzer
from sintactic import SintacticAnalyzer
from semantic import SemanticAnalyzer


class Compiler:
    """
    Main compiler/interpreter for the music DSL. Orchestrates the pipeline:
    - Lexical analysis
    - Syntactic analysis
    - Semantic analysis (execution)
    """

    def __init__(self, log_callback=None):
        self.log_callback = log_callback

    def compile(self, code: str):
        # 1. Lexical analysis: convierte el código en tokens
        tokens = LexicalAnalyzer.lex(code)
        # 2. Sintactic analysis: valida y estructura los comandos
        commands = SintacticAnalyzer(tokens).parse()
        # 3. Semantic analysis: ejecuta la lógica musical
        SemanticAnalyzer(commands, log_callback=self.log_callback).analyze()


if __name__ == "__main__":
    from view import show_gui
    show_gui()