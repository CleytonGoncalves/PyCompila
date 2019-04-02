from typing import Sequence, Optional

from lexer.token import Token
from parser.parser import Parser
from parser.result import Result


class Reserved(Parser):
    def __init__(self, token: Token) -> None:
        self.token = token

    def __call__(self, tokens: Sequence[Token], pos: int) -> Optional[Result]:
        if pos < len(tokens) and tokens[pos] == self.token:
            return Result(self.token.value, pos + 1)
        else:
            return None
