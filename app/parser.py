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


class UnaryExpression(Expression):
    operator: Token
    operand: Expression

    def __init__(self, operator: Token, operand: Expression):
        self.operator = operator
        self.operand = operand

    def accept(self, visitor):
        return visitor.visitUnaryExpression(self)


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
        # TODO: Change this as higher-precedence rules are added
        return self._parse_unary()

    def _parse_unary(self) -> Expression:
        if self._match(TokenType.BANG) or self._match(TokenType.MINUS):
            operator = self._previous_token()
            operand = self._parse_expression()
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
