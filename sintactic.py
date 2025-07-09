"""Syntactic analyzer for the music DSL."""

import re


class SintacticAnalyzer:
    """
    Receives a list of tokens and parses them into structured commands (dicts).
    Validates the syntax of each command.
    """

    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        commands = []
        for token in self.tokens:
            if token.type_ == "REPEAT":
                m = re.match(r"repeat\s+(\d+)", token.value, re.IGNORECASE)
                if m:
                    commands.append({"type": "REPEAT", "value": int(m.group(1))})
            elif token.type_ == "TEMPO":
                m = re.match(r"tempo\s+(\d+)", token.value, re.IGNORECASE)
                if m:
                    commands.append({"type": "TEMPO", "value": int(m.group(1))})
            elif token.type_ == "PATTERN":
                m = re.match(
                    r"pattern\s+(\w+)\s*=\s*\[(.*)\]", token.value, re.IGNORECASE
                )
                if m:
                    name = m.group(1)
                    vals = [
                        int(x.strip())
                        for x in m.group(2).split(",")
                        if x.strip()
                    ]
                    commands.append(
                        {"type": "PATTERN", "name": name, "sequence": vals}
                    )
            elif token.type_ == "MELODY":
                m = re.match(
                    r"melody\s+(\w+)\s*=\s*\[(.*)\]", token.value, re.IGNORECASE
                )
                if m:
                    name = m.group(1)
                    notes = [
                        n.strip() for n in m.group(2).split(",") if n.strip()
                    ]
                    commands.append({"type": "MELODY", "name": name, "notes": notes})
            elif token.type_ == "MIX":
                m = re.match(r"mix\s*\((.*)\)", token.value, re.IGNORECASE)
                if m:
                    items = [
                        x.strip() for x in m.group(1).split(",") if x.strip()
                    ]
                    commands.append({"type": "MIX", "items": items})
            elif token.type_ == "SAVE":
                m = re.match(
                    r"save\s+(\S+)\s*\((.*)\)", token.value, re.IGNORECASE
                )
                if m:
                    filename = m.group(1)
                    items = [
                        x.strip() for x in m.group(2).split(",") if x.strip()
                    ]
                    commands.append(
                        {"type": "SAVE", "filename": filename, "items": items}
                    )
            else:
                raise SyntaxError(f"Unknown or invalid command: {token.value}")
        return commands