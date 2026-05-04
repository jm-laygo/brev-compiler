from __future__ import annotations
from typing import Any

from backend.semantic.symbols import VariableSymbol
from backend.semantic.typesys import canAssign, isNumericType


class StatementMutationsMixin:
    def checkAssignmentStatement(self, statementNode: Any) -> None:
        targetReference = getattr(statementNode, "target", None)
        valueExpression = getattr(statementNode, "value", None)
        operatorText = getattr(statementNode, "operator", "=")

        rootSymbol = self.getLeftHandValueRootSymbol(targetReference)

        if isinstance(rootSymbol, VariableSymbol) and getattr(rootSymbol, "isConstant", False):
            self.addError(
                targetReference if targetReference is not None else statementNode,
                f"Cannot modify sacred constant '{rootSymbol.name}'."
            )

            return

        targetType = self.getLeftHandValueType(targetReference)
        valueType = self.getExpressionType(valueExpression)

        if self.hasTypeError(targetType) or self.hasTypeError(valueType):
            return

        if operatorText != "=" and not isNumericType(targetType):
            self.addError(
                targetReference if targetReference is not None else statementNode,
                f"Type error: '{operatorText}' requires numeric target, got {self.getTypeName(targetType)}."
            )

            return

        if not canAssign(targetType, valueType):
            self.addError(
                valueExpression if valueExpression is not None else statementNode,
                f"Type mismatch: cannot assign {self.getTypeName(valueType)} to {self.getTypeName(targetType)}."
            )

    def checkIncrementDecrementStatement(self, statementNode: Any) -> None:
        targetReference = getattr(statementNode, "target", None)

        rootSymbol = self.getLeftHandValueRootSymbol(targetReference)

        if isinstance(rootSymbol, VariableSymbol) and getattr(rootSymbol, "isConstant", False):
            self.addError(
                statementNode,
                f"Cannot increment/decrement sacred constant '{rootSymbol.name}'."
            )

            return

        targetType = self.getLeftHandValueType(targetReference)

        if not isNumericType(targetType):
            self.addError(
                statementNode,
                f"++/-- requires numeric lvalue, got {targetType}."
            )