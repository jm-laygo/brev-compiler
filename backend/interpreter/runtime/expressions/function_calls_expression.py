from __future__ import annotations

from backend.ast.ast_nodes import FunctionCallExpression


def handleFunctionCallExpression(self, expressionNode, currentEnvironment):
    if not isinstance(expressionNode, FunctionCallExpression):
        return None

    evaluatedArgumentValues = []

    for argumentNode in expressionNode.arguments:
        evaluatedArgumentValues.extend([
            self.evaluateExpression(argumentNode, currentEnvironment)
        ])

    callResult = self.callRite(
        expressionNode.calleeName,
        evaluatedArgumentValues,
        callNode=expressionNode
    )

    callAccessChain = getattr(expressionNode, "accessChain", None)

    if callAccessChain is not None:
        return self.readLeftHandValueFromValue(
            callAccessChain,
            callResult,
            expressionNode
        )

    return callResult