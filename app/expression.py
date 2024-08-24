from app.token import Token


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


class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression

    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpression(self)
