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
    IDENTIFIER = "IDENTIFIER"
    LEFT_BRACE = "LEFT_BRACE"
    LEFT_PAREN = "LEFT_PAREN"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    MINUS = "MINUS"
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    RIGHT_BRACE = "RIGHT_BRACE"
    RIGHT_PAREN = "RIGHT_PAREN"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"
    STRING = "STRING"

    # Reserved keywords
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FOR = "FOR"
    FUN = "FUN"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"


RESERVED_KEYWORDS_TO_TOKEN_TYPE_MAP = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Token:
    type: TokenType
    lexeme: Optional[str]
    literal: str | float | None
    line_number: int

    def __init__(
        self,
        type: TokenType,
        lexeme: Optional[str],
        literal: str | float | None,
        line_number: int,
    ):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line_number = line_number

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal if self.literal is not None else 'null'}"
