from .token import Token, TokenType
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
                if self._consume_char_if("="):
                    self._add_token(TokenType.EQUAL_EQUAL)
                else:
                    self._add_token(TokenType.EQUAL)
            case "!":
                if self._consume_char_if("="):
                    self._add_token(TokenType.BANG_EQUAL)
                else:
                    self._add_token(TokenType.BANG)
            case "<":
                if self._consume_char_if("="):
                    self._add_token(TokenType.LESS_EQUAL)
                else:
                    self._add_token(TokenType.LESS)
            case ">":
                if self._consume_char_if("="):
                    self._add_token(TokenType.GREATER_EQUAL)
                else:
                    self._add_token(TokenType.GREATER)
            case "/":
                if self._consume_char_if("/"):
                    self._consume_chars_until("\n")
                else:
                    self._add_token(TokenType.SLASH)
            case char:
                self.has_errors = True

                print(
                    f"[line {self.current_line}] Error: Unexpected character: {char}",
                    file=sys.stderr,
                )

    def _add_token(self, type: TokenType, literal: str | int | None = None):
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

    def _consume_char_if(self, char: str) -> bool:
        if self._is_at_end():
            return False

        if self.source[self.current_index] != char:
            return False

        self.current_index += 1
        return True

    def _consume_char_unless(self, char: str) -> bool:
        if self._is_at_end():
            return False

        if self.source[self.current_index] == char:
            return False

        self.current_index += 1
        return True

    def _consume_chars_until(self, char: str):
        while self._consume_char_unless(char):
            pass

    def _is_at_end(self) -> bool:
        return self.current_index >= len(self.source)
