from typing import Sequence, Optional

from lexer.token import Token
from parser.parser import Parser
from parser.result import Result


class Concat(Parser):
    def __init__(self, left_parser: Parser, right_parser: Parser) -> None:
        self.left_parser = left_parser
        self.right_parser = right_parser

    def __call__(self, tokens: Sequence[Token], pos: int) -> Optional[Result]:
        left_result = self.left_parser(tokens, pos)
        if left_result:
            right_result = self.right_parser(tokens, left_result.pos)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None
