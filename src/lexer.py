import re
from enum import Enum
from typing import Sequence, List


class TokenType(Enum):
    COMMENT = r"(\/\*(.*?)\*\/)|(\{(.*?)\})"

    LITERAL_FLOAT = r"([0-9]+\.[0-9]+)"
    LITERAL_INTEGER = r"([0-9]+)"

    KEYWORD_VAR = r"(var)"
    KEYWORD_INTEGER = r"(integer)"
    KEYWORD_REAL = r"(real)"
    KEYWORD_IF = r"(if)"
    KEYWORD_THEN = r"(then)"
    KEYWORD_ELSE = r"(else)"
    KEYWORD_BEGIN = r"(begin)"
    KEYWORD_END = r"(end)"
    KEYWORD_WHILE = r"(while)"
    KEYWORD_DO = r"(do)"
    KEYWORD_WRITE = r"(write)"
    KEYWORD_READ = r"(read)"
    KEYWORD_PROGRAM = r"(program)"
    KEYWORD_PROCEDURE = r"(procedure)"

    SYMBOL_DIFFERENT = r"(<>)"
    SYMBOL_GREATER_EQUAL = r"(>=)"
    SYMBOL_LESS_EQUAL = r"(<=)"
    SYMBOL_ASSIGNMENT = r"(:=)"
    SYMBOL_DOLLAR = r"\$"
    SYMBOL_OPEN_PARENS = r"\("
    SYMBOL_CLOSE_PARENS = r"\)"
    SYMBOL_MULTIPLICATION = r"\*"
    SYMBOL_DIVISION = r"\/"
    SYMBOL_ADD = r"\+"
    SYMBOL_SUBTRACT = r"\-"
    SYMBOL_GREATER = r"\>"
    SYMBOL_LESS = r"\<"
    SYMBOL_COLON = r"\:"
    SYMBOL_SEMICOLON = r"\;"
    SYMBOL_EQUALS = r"\="
    SYMBOL_COMMA = r"\,"
    SYMBOL_FULL_STOP = r"\."

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
    should_end = False

    tokens = []
    for match in re.finditer(tokens_regex, code, re.DOTALL):
        token_type = TokenType[f'{match.lastgroup}']
        value = match.group()
        column_num = match.start() - line_start

        if token_type == TokenType.COMMENT:
            line_num += value.count("\n")  # Conta quebras de linha dos comentários
            continue
        elif token_type == TokenType.NEWLINE:
            line_start = match.end()
            line_num += 1
            continue
        elif token_type == TokenType.WHITESPACE:
            continue
        elif should_end:
            raise Exception(f"Unexpected {value!r} after program end")
        elif token_type == TokenType.MISMATCH:
            raise Exception(f"Character {value!r} unexpected on line {line_num}:\n>\t{code.splitlines()[line_num - 1]}")

        tokens.append(Token(token_type, value, line_num, column_num))

        should_end = is_end_of_program(tokens)

    return tokens


def is_end_of_program(tokens: List[Token]):
    return len(tokens) >= 2 and tokens[-2].token_type == TokenType.KEYWORD_END \
           and tokens[-1].token_type == TokenType.SYMBOL_FULL_STOP
