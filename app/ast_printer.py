from app.parser import Expression, GroupingExpression, LiteralExpression


class AstPrinter:
    def print(self, expression: Expression):
        return expression.accept(self)

    def visitGroupingExpression(self, expression: GroupingExpression):
        return f"(group {self.print(expression.expression)})"

    def visitLiteralExpression(self, expression: LiteralExpression):
        if isinstance(expression.value, str):
            return f"{expression.value}"
        elif isinstance(expression.value, float):
            return f"{expression.value}"
        elif isinstance(expression.value, bool):
            return "true" if expression.value else "false"
        else:
            return "nil"
