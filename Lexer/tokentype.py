from enum import Enum


# var, : , id, , , integer, real, ; , :=, if, then, +
class TokenType(Enum):
    ADD_OPERATOR = (r"\+", 1)
    ASSIGNMENT = (r"(:=)", 1)
    SEMI_COLON = (r";", 1)
    COMMA = (r",", 1)
    COLON = (r":", 2)

    KEYWORD = (r"(var)|(integer)|(real)|(if)|(then)", 9)
    IDENTIFIER = (r"[a-zA-Z][a-zA-Z0-9]*", 10)

    NEWLINE = (r"\n", 997)
    WHITESPACE = (r"[ \t]+", 998)
    MISMATCH = (r".", 999)  # Any leftover character

    def __init__(self, regex: str, precedence: int) -> None:
        self.regex = regex
        self.precedence = precedence

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
