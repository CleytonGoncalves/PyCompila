from Lexer.tokentype import TokenType


class Token:
    printLineColumnNumber = False

    def __init__(self, token_type: TokenType, value: str, line: int = None, column: int = None) -> None:
        self.token_type = token_type
        self.value = value
        self.column = column
        self.line = line

    def __str__(self) -> str:
        line_column = ""
        if self.line is not None:
            line_column = f" at {self.line}"
            if self.column is not None:
                line_column += f":{self.column}"

        return f"{self.token_type.name:>15}:{'':>2}{self.value!r}{line_column if Token.printLineColumnNumber else ''}"
