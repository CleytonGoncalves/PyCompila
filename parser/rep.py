from typing import Sequence

from lexer.token import Token
from parser.parser import Parser
from parser.result import Result


class Phrase(Parser):
    def __init__(self, parser: Parser) -> None:
        self.parser = parser

    def __call__(self, tokens: Sequence[Token], pos: int) -> Result:
        results = Sequence[str]
        result = self.parser(tokens, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens, pos)
        return Result(results, pos)
