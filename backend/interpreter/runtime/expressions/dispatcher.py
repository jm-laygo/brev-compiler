from __future__ import annotations

from backend.ast.ast_nodes import (
    ArrayInitializationExpression,
    BinaryExpression,
    FunctionCallExpression,
    GroupExpression,
    LiteralExpression,
    UnaryExpression,
    VariableExpression,
    VerseOfExpression,
)
from backend.errors import RuntimeErrorBase

from .calls import handleFunctionCallExpression
from .operators import handleUnaryExpression, handleBinaryExpression
from .primitives import handlePrimitiveExpression


def evaluateExpression(self, expressionNode, currentEnvironment):
    if expressionNode is None:
        return None

    if isinstance(
        expressionNode,
        (
            LiteralExpression,
            GroupExpression,
            VariableExpression,
            ArrayInitializationExpression,
            VerseOfExpression,
        )
    ):
        return handlePrimitiveExpression(
            self,
            expressionNode,
            currentEnvironment
        )

    if isinstance(expressionNode, FunctionCallExpression):
        return handleFunctionCallExpression(
            self,
            expressionNode,
            currentEnvironment
        )

    if isinstance(expressionNode, UnaryExpression):
        return handleUnaryExpression(
            self,
            expressionNode,
            currentEnvironment
        )

    if isinstance(expressionNode, BinaryExpression):
        return handleBinaryExpression(
            self,
            expressionNode,
            currentEnvironment
        )

    raise RuntimeErrorBase(
        expressionNode,
        "This expression is not yet supported during execution."
    )

def bindExpressionMethods(interpreterClass):
    interpreterClass.evaluateExpression = evaluateExpression