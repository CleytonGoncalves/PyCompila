from typing import Sequence, Callable, Any

from lexer.token import Token
from parser.parser import Parser


class Process(Parser):
    def __init__(self, parser: Parser, function: Callable) -> None:
        self.parser = parser
        self.function = function

    def __call__(self, tokens: Sequence[Token], pos: int) -> Any:
        result = self.parser(tokens, pos)
        if result:
            callable(result.value)
