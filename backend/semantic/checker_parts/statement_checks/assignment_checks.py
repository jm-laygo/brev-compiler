from __future__ import annotations
from typing import Any

from backend.semantic.symbols import VariableSymbol
from backend.semantic.typesys import canAssign, isNumericType, isTallyType


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

        # normal assignment
        if operatorText == "=":
            if not canAssign(targetType, valueType):
                self.addError(
                    valueExpression if valueExpression is not None else statementNode,
                    f"Type mismatch: cannot assign {self.getTypeName(valueType)} to {self.getTypeName(targetType)}."
                )
            return

        # modulo assignment is tally-only
        if operatorText == "%=":
            if not isTallyType(targetType) or not isTallyType(valueType):
                self.addError(
                    statementNode,
                    f"Type error: '%=' requires tally target and tally value, got {self.getTypeName(targetType)} and {self.getTypeName(valueType)}."
                )
            return

        # other compound arithmetic assignment operators
        if operatorText in ("+=", "-=", "*=", "/=", "**="):
            if not isNumericType(targetType) or not isNumericType(valueType):
                self.addError(
                    statementNode,
                    f"Type error: '{operatorText}' requires numeric target and numeric value, got {self.getTypeName(targetType)} and {self.getTypeName(valueType)}."
                )
            return

        self.addError(
            statementNode,
            f"Unknown assignment operator '{operatorText}'."
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

        if self.hasTypeError(targetType):
            return

        if not isNumericType(targetType):
            self.addError(
                statementNode,
                f"++/-- requires numeric lvalue, got {self.getTypeName(targetType)}."
            )