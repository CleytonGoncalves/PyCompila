import re
from enum import Enum
from typing import Sequence


class TokenType(Enum):
    # A ordem da declaração define a prioridade de cada tipo
    ADD_OPERATOR = r"\+"
    ASSIGNMENT = r"(:=)"
    SEMI_COLON = r";"
    COMMA = r","
    COLON = r":"

    KEYWORD_VAR = r"(var)"
    KEYWORD_INTEGER = r"(integer)"
    KEYWORD_REAL = r"(real)"
    KEYWORD_IF = r"(if)"
    KEYWORD_THEN = r"(then)"

    IDENTIFIER = r"[a-zA-Z][a-zA-Z0-9]*"

    NEWLINE = r"\n"
    WHITESPACE = r"[ \t]+"
    MISMATCH = r"."  # Any leftover character

    def __init__(self, regex: str) -> None:
        self.regex = regex

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}: {self.regex!r}"


class Token:
    printLineColumnNumber = False

    def __init__(self, token_type: TokenType, value: str, line: int = None, column: int = None) -> None:
        self.token_type = token_type
        self.value = value
        self.column = column
        self.line = line

    def __eq__(self, o: object) -> bool:
        return isinstance(o, self.__class__) and self.token_type == o.token_type and self.value == o.value

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        line_column = ""
        if self.line is not None:
            line_column = f" at {self.line}"
            if self.column is not None:
                line_column += f":{self.column}"

        return f"{self.token_type.name:>15}:{'':>2}{self.value!r}{line_column if Token.printLineColumnNumber else ''}"


def tokenize(code: str) -> Sequence[Token]:
    tokens_regex: str = '|'.join(f'(?P<{token_type.name}>{token_type.regex})' for token_type in TokenType)
    line_num: int = 1
    line_start: int = 0

    tokens = []
    for match in re.finditer(tokens_regex, code):
        token_type = TokenType[f'{match.lastgroup}']
        value = match.group()
        column_num = match.start() - line_start

        if token_type == TokenType.NEWLINE:
            line_start = match.end()
            line_num += 1
            continue
        elif token_type == TokenType.WHITESPACE:
            continue
        elif token_type == TokenType.MISMATCH:
            raise Exception(f"Character {value!r} unexpected on line {line_num}:\n>\t{code.splitlines()[line_num - 1]}")

        tokens.append(Token(token_type, value, line_num, column_num))

    return tokens
