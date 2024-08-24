from app.expression import (
    Expression,
    LiteralExpression,
    GroupingExpression,
    UnaryExpression,
    BinaryExpression,
)
from app.token import Token, TokenType


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_index = 0
        self.has_errors = False

    def parse(self) -> Expression:
        return self._parse_expression()

    def _parse_expression(self) -> Expression:
        return self._parse_equality()

    def _parse_equality(self) -> Expression:
        expression = self._parse_comparison()

        while self._match(TokenType.BANG_EQUAL) or self._match(TokenType.EQUAL_EQUAL):
            operator = self._previous_token()
            right = self._parse_comparison()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _parse_comparison(self) -> Expression:
        expression = self._parse_term()

        while self._match(TokenType.GREATER) or self._match(TokenType.GREATER_EQUAL) or self._match(TokenType.LESS) or self._match(TokenType.LESS_EQUAL):
            operator = self._previous_token()
            right = self._parse_term()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _parse_term(self) -> Expression:
        expression = self._parse_factor()

        while self._match(TokenType.MINUS) or self._match(TokenType.PLUS):
            operator = self._previous_token()
            right = self._parse_factor()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _parse_factor(self) -> Expression:
        expression = self._parse_unary()

        while self._match(TokenType.SLASH) or self._match(TokenType.STAR):
            operator = self._previous_token()
            right = self._parse_unary()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _parse_unary(self) -> Expression:
        if self._match(TokenType.BANG) or self._match(TokenType.MINUS):
            operator = self._previous_token()
            operand = self._parse_unary()
            return UnaryExpression(operator, operand)

        return self._parse_primary()

    def _parse_primary(self) -> Expression:
        if self._match(TokenType.FALSE):
            return LiteralExpression(False)

        if self._match(TokenType.TRUE):
            return LiteralExpression(True)

        if self._match(TokenType.NIL):
            return LiteralExpression(None)

        if self._match(TokenType.NUMBER):
            return LiteralExpression(self._previous_token().literal)

        if self._match(TokenType.STRING):
            return LiteralExpression(self._previous_token().literal)

        if self._match(TokenType.LEFT_PAREN):
            expression = self._parse_expression()
            self._match_or_raise_error(TokenType.RIGHT_PAREN, "Expected )")
            return GroupingExpression(expression)

        raise Exception("Expected expression")

    def _match(self, type: TokenType) -> bool:
        if self.tokens[self.current_index].type == type:
            self.current_index += 1
            return True

        return False

    def _match_or_raise_error(self, type: TokenType, error_message: str):
        if self.tokens[self.current_index].type == type:
            self.current_index += 1
            return self.tokens[self.current_index - 1]
        else:
            raise ParseError(error_message)

    def _previous_token(self) -> Token:
        return self.tokens[self.current_index - 1]
