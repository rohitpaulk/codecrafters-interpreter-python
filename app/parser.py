from app.token import Token, TokenType


class Expression:
    def accept(self, visitor):
        return visitor.visit(self)


class LiteralExpression(Expression):
    value: str | float | bool | None

    def __init__(self, value: str | float | bool | None):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpression(self)


class GroupingExpression(Expression):
    expression: Expression

    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpression(self)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_index = 0
        self.has_errors = False

    def parse(self) -> Expression:
        return self._parse_expression()

    def _parse_expression(self) -> Expression:
        return self._parse_primary()

    def _parse_primary(self) -> Expression:
        if self._match(TokenType.FALSE):
            return LiteralExpression(False)

        if self._match(TokenType.TRUE):
            return LiteralExpression(True)

        if self._match(TokenType.NIL):
            return LiteralExpression(None)

        if self._match(TokenType.NUMBER):
            return LiteralExpression(self.tokens[self.current_index].literal)

        if self._match(TokenType.STRING):
            return LiteralExpression(self.tokens[self.current_index].literal)

        if self._match(TokenType.LEFT_PAREN):
            expression = self._parse_expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected )")
            return GroupingExpression(expression)

        raise Exception("Expected expression")

    def _match(self, type: TokenType) -> bool:
        if self.tokens[self.current_index].type == type:
            self.current_index += 1
            return True

        return False

    def _consume(self, type: TokenType, error_message: str) -> Token:
        if self.tokens[self.current_index].type == type:
            self.current_index += 1
            return self.tokens[self.current_index - 1]

        raise Exception(error_message)
