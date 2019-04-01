from Lexer.tokentype import TokenType


class Token:
    def __init__(self, token_type: TokenType, value, line: int = None, column: int = None) -> None:
        self.token_type = token_type
        self.value = value
        self.column = column
        self.line = line

    def __str__(self) -> str:
        line_column = ""
        if self.line is not None:
            line_column = f":{self.line}"
            if self.column is not None:
                line_column += f":{self.column}"

        return f"{self.token_type}: {self.value!r}{line_column}"
