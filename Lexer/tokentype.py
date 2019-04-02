from enum import Enum


class TokenType(Enum):
    # A ordem da declaração define a prioridade de cada tipo
    ADD_OPERATOR = r"\+"
    ASSIGNMENT = r"(:=)"
    SEMI_COLON = r";"
    COMMA = r","
    COLON = r":"

    KEYWORD = r"(var)|(integer)|(real)|(if)|(then)"
    IDENTIFIER = r"[a-zA-Z][a-zA-Z0-9]*"

    NEWLINE = r"\n"
    WHITESPACE = r"[ \t]+"
    MISMATCH = r"."  # Any leftover character

    def __init__(self, regex: str) -> None:
        self.regex = regex

    def __str__(self):
        return f"{self.name!r}: '{self.regex!r}'"

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.precedence >= other.precedence
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.precedence > other.precedence
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.precedence <= other.precedence
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.precedence < other.precedence
        return NotImplemented
