from __future__ import annotations

from backend.ast.ast_nodes import (
    AbsolveStatement,
    DismissStatement,
    FallStatement,
    ProceedStatement,
)
from backend.interpreter.control import (
    AbsolveSignal,
    DismissSignal,
    FallSignal,
    ProceedSignal,
)


def handleControlStatement(self, statementNode, currentEnvironment):
    if isinstance(statementNode, ProceedStatement):
        raise ProceedSignal()

    if isinstance(statementNode, FallStatement):
        raise FallSignal()

    if isinstance(statementNode, AbsolveStatement):
        raise AbsolveSignal()

    if isinstance(statementNode, DismissStatement):
        dismissValueNode = getattr(statementNode, "value", None)

        if dismissValueNode is not None:
            dismissValue = self.evaluateExpression(
                dismissValueNode,
                currentEnvironment
            )
        else:
            dismissValue = None

        raise DismissSignal(dismissValue)

    return False