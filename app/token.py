from enum import StrEnum
from typing import Optional


class TokenType(StrEnum):
    EOF = "EOF"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


class Token:
    type: TokenType
    lexeme: Optional[str]
    literal: str | int | None
    line_number: int

    def __init__(
        self,
        type: TokenType,
        lexeme: Optional[str],
        literal: str | int | None,
        line_number: int,
    ):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line_number = line_number

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal or 'null'}"
