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

    def compile(self, code: str):
        # 1. Lexical analysis: convierte el código en tokens
        tokens = LexicalAnalyzer.lex(code)
        # 2. Sintactic analysis: valida y estructura los comandos
        commands = SintacticAnalyzer(tokens).parse()
        # 3. Semantic analysis: ejecuta la lógica musical
        SemanticAnalyzer(commands).analyze()


if __name__ == "__main__":
    # Ejemplo de uso: puedes reemplazar este código por lectura de archivo o entrada de usuario
    code = """
    tempo 120
    pattern kick = [1,0,0,0]
    pattern snare = [0,0,1,0]
    pattern hat = [1,1,1,1]
    melody main = [C4, E4, G4, C5]
    mix(kick, snare, hat, main)
    """
    Compiler().compile(code)