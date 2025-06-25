"""This module represents the behavior of a lexical analyzer.

Author: Juan Duarte <jcduartes@udistrital.edu.co>
"""

import re


class Token:
    """This class represents the data structure of a token.
    It means: a type of token and its value (lexema)."""

    def __init__(self, type_: str, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type_}, {self.value})"


class LexicalAnalyzer:
    """This class represents the behavior of a lexical analyzer."""

    @staticmethod
    def lex(code):
        """This method receives a code and returns a list of tokens."""
        tokens = []
        for line in code.splitlines():
            line = line.split("#")[0].strip()  # Remove comments
            if not line:
                continue
            # Reconoce los comandos del DSL
            if re.match(r"^tempo\s+\d+", line, re.IGNORECASE):
                tokens.append(Token("TEMPO", line))
            elif re.match(r"^pattern\s+\w+\s*=\s*\[.*\]", line, re.IGNORECASE):
                tokens.append(Token("PATTERN", line))
            elif re.match(r"^melody\s+\w+\s*=\s*\[.*\]", line, re.IGNORECASE):
                tokens.append(Token("MELODY", line))
            elif re.match(r"^mix\s*\(.*\)", line, re.IGNORECASE):
                tokens.append(Token("MIX", line))
            elif re.match(r"^save\s+\S+", line, re.IGNORECASE):
                tokens.append(Token("SAVE", line))
            else:
                tokens.append(Token("UNKNOWN", line))
        return tokens