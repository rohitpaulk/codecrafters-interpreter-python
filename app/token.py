from enum import StrEnum
from typing import Optional


class TokenType(StrEnum):
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    COMMA = "COMMA"
    DOT = "DOT"
    EOF = "EOF"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LEFT_BRACE = "LEFT_BRACE"
    LEFT_PAREN = "LEFT_PAREN"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    MINUS = "MINUS"
    PLUS = "PLUS"
    RIGHT_BRACE = "RIGHT_BRACE"
    RIGHT_PAREN = "RIGHT_PAREN"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"
    STRING = "STRING"


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
