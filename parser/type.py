from typing import Sequence, Optional

from lexer.token import Token
from lexer.tokentype import TokenType
from parser.parser import Parser
from parser.result import Result


class Type(Parser):
    def __init__(self, token_type: TokenType) -> None:
        self.token_type = token_type

    def __call__(self, tokens: Sequence[Token], pos: int) -> Optional[Result]:
        if pos < len(tokens) and tokens[pos] == self.token_type:
            return Result(self.token_type, pos + 1)
        else:
            return None
