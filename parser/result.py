from typing import Any


class Result:
    def __init__(self, value: Any, pos: int) -> None:
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f"Result({self.value!r}, {self.pos})"
