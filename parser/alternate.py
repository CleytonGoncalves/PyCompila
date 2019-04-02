from typing import Sequence

from lexer.token import Token
from parser.parser import Parser
from parser.result import Result


class Alternate(Parser):
    def __init__(self, left_parser: Parser, right_parser: Parser) -> None:
        self.left_parser = left_parser
        self.right_parser = right_parser

    def __call__(self, tokens: Sequence[Token], pos: int) -> Result:
        left_result = self.left_parser(tokens, pos)
        if left_result:
            return left_result
        else:
            return self.right_parser(tokens, pos)
