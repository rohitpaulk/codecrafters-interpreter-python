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


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.expression_start_index = 0
        self.current_index = 0
        self.has_errors = False

    def parse(self) -> Expression:
        return self._parse_primary()

    def _parse_primary(self) -> Expression:
        if self.tokens[self.current_index].type == TokenType.FALSE:
            return LiteralExpression(False)
        elif self.tokens[self.current_index].type == TokenType.TRUE:
            return LiteralExpression(True)
        elif self.tokens[self.current_index].type == TokenType.NIL:
            return LiteralExpression(None)
        elif self.tokens[self.current_index].type == TokenType.NUMBER:
            return LiteralExpression(self.tokens[self.current_index].literal)
        else:
            raise Exception(f"Unexpected token: {self.tokens[self.current_index].type}")
