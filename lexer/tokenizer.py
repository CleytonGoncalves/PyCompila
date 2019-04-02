import re

from lexer.token import Token
from lexer.tokentype import TokenType


def tokenize(code):
    tokens_regex: str = '|'.join(f'(?P<{token_type.name}>{token_type.regex})' for token_type in TokenType)
    line_num: int = 1
    line_start: int = 0

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
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')

        yield Token(token_type, value, line_num, column_num)
