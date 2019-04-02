from collections import Sequence
from typing import Callable, Optional

from lexer.token import Token
from parser.alternate import Alternate
from parser.concat import Concat
from parser.process import Process
from parser.result import Result


class Parser:
    def __call__(self, tokens: Sequence[Token], pos: int) -> Optional[Result]:
        return None

    def __add__(self, other: 'Parser'):
        return Concat(self, other)

    def __or__(self, other: 'Parser'):
        return Alternate(self, other)

    def __xor__(self, function: Callable):
        return Process(self, function)
