from __future__ import annotations

from backend.interpreter.control import (
    AbsolveSignal,
    DismissSignal,
    FallSignal,
    ProceedSignal,
)
from backend.interpreter.environment import Environment
from backend.errors import RuntimeErrorBase, RuntimeNameError


# calling rites
def callRite(self, riteName: str, argumentValues, *, callNode=None):
    riteNode = self.riteDeclarations.get(riteName)

    if riteNode is None:
        raise RuntimeNameError(
            callNode,
            f"Undefined rite '{riteName}'."
        )

    riteEnvironment = Environment(parentEnvironment=self.globalEnvironment)

    parameterNodes = getattr(riteNode, "parameters", []) or []

    if len(argumentValues) != len(parameterNodes):
        raise RuntimeErrorBase(
            callNode,
            f"Rite '{riteName}' expected {len(parameterNodes)} argument(s), but received {len(argumentValues)}."
        )

    for parameterNode, argumentValue in zip(parameterNodes, argumentValues):
        riteEnvironment.declare(
            parameterNode.name,
            argumentValue,
            isConstant=False
        )

    self.executeLocalDeclarations(
        getattr(riteNode, "localDeclarations", []) or [],
        riteEnvironment
    )

    try:
        riteBodyStatements = getattr(riteNode, "bodyStatements", []) or []

        self.executeBlock(
            riteBodyStatements,
            riteEnvironment,
            createScope=False
        )

        finalDismissStatement = getattr(riteNode, "dismissStatement", None)

        if finalDismissStatement is not None:
            self.executeStatement(
                finalDismissStatement,
                riteEnvironment
            )

    except DismissSignal as dismissSignal:
        return dismissSignal.value

    except ProceedSignal:
        raise RuntimeErrorBase(
            callNode or riteNode,
            "'proceed' may only be used inside loops."
        )

    except FallSignal:
        raise RuntimeErrorBase(
            callNode or riteNode,
            "'fall' may only be used inside loops or valid discern flow."
        )

    except AbsolveSignal:
        raise RuntimeErrorBase(
            callNode or riteNode,
            "'absolve' may only be used inside discern statements."
        )

    return None