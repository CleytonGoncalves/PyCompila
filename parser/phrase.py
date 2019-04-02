from typing import Sequence, Callable

from lexer.token import Token
from parser.parser import Parser


class Phrase(Parser):
    def __init__(self, parser_func: Callable[..., Parser]) -> None:
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens: Sequence[Token], pos: int) -> Parser:
        if not self.parser:
            self.parser = self.parser_func
        return self.parser(tokens, pos)
