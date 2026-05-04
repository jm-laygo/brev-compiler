from __future__ import annotations

from backend.ast.ast_nodes import (
    ArrayInitializationExpression,
    GroupExpression,
    LiteralExpression,
    VariableExpression,
    VerseOfExpression,
)
from backend.errors import RuntimeTypeError


# primitive expressions
def handlePrimitiveExpression(self, expressionNode, currentEnvironment):
    if isinstance(expressionNode, LiteralExpression):
        return expressionNode.value

    if isinstance(expressionNode, GroupExpression):
        return self.evaluateExpression(
            expressionNode.expression,
            currentEnvironment
        )

    if isinstance(expressionNode, VariableExpression):
        return self.readLeftHandValue(
            expressionNode.reference,
            currentEnvironment
        )

    if isinstance(expressionNode, ArrayInitializationExpression):
        evaluatedItems = []

        for itemNode in expressionNode.items:
            evaluatedItems.extend([
                self.evaluateExpression(itemNode, currentEnvironment)
            ])

        return evaluatedItems

    if isinstance(expressionNode, VerseOfExpression):
        innerValue = self.evaluateExpression(
            expressionNode.expression,
            currentEnvironment
        )

        if isinstance(innerValue, list):
            return len(innerValue)

        if isinstance(innerValue, str):
            return len(innerValue)

        raise RuntimeTypeError(
            expressionNode,
            "The verseof operator requires an array or scripture value."
        )

    return None