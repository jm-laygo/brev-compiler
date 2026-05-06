from __future__ import annotations
from typing import Any

from backend.semantic.symbols import VariableSymbol
from backend.semantic.typesys import BaseType, canAssign


class StatementActionsMixin:
    def checkFunctionCallStatement(self, statementNode: Any) -> None:
        functionName = getattr(statementNode, "calleeName", None)
        argumentNodes = getattr(statementNode, "arguments", []) or []

        self.checkFunctionCall(
            functionName,
            argumentNodes,
            statementNode
        )

    def checkReceiveStatement(self, statementNode: Any) -> None:
        targetReference = getattr(statementNode, "target", None)

        rootSymbol = self.getLeftHandValueRootSymbol(targetReference)

        if isinstance(rootSymbol, VariableSymbol) and getattr(rootSymbol, "isConstant", False):
            self.addError(
                statementNode,
                f"Cannot store input into sacred constant '{rootSymbol.name}'."
            )

            return

        self.getLeftHandValueType(targetReference)

    def checkProclaimStatement(self, statementNode: Any) -> None:
        argumentNodes = getattr(statementNode, "arguments", []) or []

        for argumentNode in argumentNodes:
            self.getExpressionType(argumentNode)

    def checkDismissStatement(self, statementNode: Any) -> None:
        if self.currentFunction is None:
            return

        returnType = self.currentFunction.returnType
        returnValue = getattr(statementNode, "value", None)

        if returnType.isBaseType(BaseType.HOLLOW):
            if returnValue is not None:
                self.addError(
                    statementNode,
                    "hollow rite cannot dismiss a value."
                )

            return

        if returnValue is None:
            self.addError(
                statementNode,
                f"Rite must dismiss a value of type {returnType}."
            )

            return

        valueType = self.getExpressionType(returnValue)

        if not canAssign(returnType, valueType):
            self.addError(
                statementNode,
                f"Cannot dismiss {valueType} from rite returning {returnType}."
            )