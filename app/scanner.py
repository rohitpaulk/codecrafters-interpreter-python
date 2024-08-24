from typing import Callable
from .token import Token, TokenType, RESERVED_KEYWORDS_TO_TOKEN_TYPE_MAP
import sys


class Scanner:
    current_token_start_index: int
    current_index: int
    current_line: int
    has_errors: bool
    source: str
    tokens: list[Token]

    def __init__(self, source: str):
        self.source = source
        self.current_token_start_index = 0
        self.current_index = 0
        self.current_line = 1
        self.has_errors = False
        self.tokens = []

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.scan_token()
            self.current_token_start_index = self.current_index

        self._add_token(TokenType.EOF)

        return self.tokens

    def scan_token(self):
        match self._consume_char():
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "=":
                if self._consume_char_if_char_is("="):
                    self._add_token(TokenType.EQUAL_EQUAL)
                else:
                    self._add_token(TokenType.EQUAL)
            case "!":
                if self._consume_char_if_char_is("="):
                    self._add_token(TokenType.BANG_EQUAL)
                else:
                    self._add_token(TokenType.BANG)
            case "<":
                if self._consume_char_if_char_is("="):
                    self._add_token(TokenType.LESS_EQUAL)
                else:
                    self._add_token(TokenType.LESS)
            case ">":
                if self._consume_char_if_char_is("="):
                    self._add_token(TokenType.GREATER_EQUAL)
                else:
                    self._add_token(TokenType.GREATER)
            case "/":
                if self._consume_char_if_char_is("/"):
                    self._consume_chars_until_char("\n")
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\t":
                pass
            case "\n":
                self.current_line += 1
            case '"':
                self._scan_string()
            case initial_char if initial_char.isdigit():
                self._scan_number(initial_char)
            case initial_char if initial_char.isalpha() or initial_char == "_":
                self._scan_identifier_or_reserved_keyword()
            case unexpected_char:
                self._report_error(f"Unexpected character: {unexpected_char}")

    def _add_token(self, type: TokenType, literal: str | float | None = None):
        self.tokens.append(
            Token(
                type,
                self.source[self.current_token_start_index : self.current_index],
                literal,
                self.current_line,
            )
        )

    def _consume_char(self) -> str:
        self.current_index += 1
        return self.source[self.current_index - 1]

    def _consume_char_if(self, predicate: Callable[[str], bool]) -> bool:
        if self._is_at_end():
            return False

        if not predicate(self.source[self.current_index]):
            return False

        self.current_index += 1
        return True

    def _consume_char_if_char_is(self, char: str) -> bool:
        return self._consume_char_if(lambda c: c == char)

    def _consume_char_unless(self, predicate: Callable[[str], bool]) -> bool:
        if self._is_at_end():
            return False

        if predicate(self.source[self.current_index]):
            return False

        self.current_index += 1
        return True

    def _consume_chars_until_char(self, char: str) -> str:
        return self._consume_chars_until(lambda c: c == char)

    def _consume_chars_until(self, predicate: Callable[[str], bool]) -> str:
        start_index = self.current_index

        while self._consume_char_unless(predicate):
            pass

        return self.source[start_index : self.current_index]

    def _consume_chars_while(self, predicate: Callable[[str], bool]) -> str:
        return self._consume_chars_until(lambda c: not predicate(c))

    def _scan_identifier_or_reserved_keyword(self):
        self._consume_chars_while(lambda c: c.isalnum() or c == "_")
        identifier = self.source[self.current_token_start_index : self.current_index]

        if identifier in RESERVED_KEYWORDS_TO_TOKEN_TYPE_MAP:
            self._add_token(RESERVED_KEYWORDS_TO_TOKEN_TYPE_MAP[identifier])
        else:
            self._add_token(TokenType.IDENTIFIER)

    def _scan_number(self, initial_char: str):
        initial_digit_chars = initial_char + self._consume_chars_while(
            lambda c: c.isdigit()
        )

        if self._consume_char_if_char_is("."):
            decimal_digit_chars = self._consume_chars_while(lambda c: c.isdigit())
            number = float(f"{initial_digit_chars}.{decimal_digit_chars}")
        else:
            number = float(initial_digit_chars)

        self._add_token(TokenType.NUMBER, number)

    def _scan_string(self):
        string_contents = self._consume_chars_until_char('"')

        if not self._consume_char_if_char_is('"'):
            self._report_error("Unterminated string.")
        else:
            self._add_token(TokenType.STRING, string_contents)

    def _is_at_end(self) -> bool:
        return self.current_index >= len(self.source)

    def _report_error(self, message: str):
        print(
            f"[line {self.current_line}] Error: {message}",
            file=sys.stderr,
        )
        self.has_errors = True
