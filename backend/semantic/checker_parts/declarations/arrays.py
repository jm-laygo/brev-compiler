from __future__ import annotations
from typing import Any, Optional

from backend.semantic.typesys import BaseType

from ..helpers import getClassName


class DeclarationArrayMixin:
    def getConstantIntegerValue(self, expressionNode: Any) -> Optional[int]:
        if expressionNode is None:
            return None

        expressionKind = getClassName(expressionNode)

        # Case 1: direct integer literal
        # Example: tally numbers[5];
        if expressionKind == "LiteralExpression":
            literalType = (getattr(expressionNode, "literalType", "") or "").lower()

            if literalType == "int":
                try:
                    return int(getattr(expressionNode, "value"))
                except Exception:
                    return None

            return None

        # Case 2: sacred tally identifier
        # Example:
        # sacred tally SIZE = 5;
        # tally numbers[SIZE];
        if expressionKind == "VariableExpression":
            referenceNode = getattr(expressionNode, "reference", None)

            if getClassName(referenceNode) != "NameReference":
                return None

            constantName = getattr(referenceNode, "name", None)

            if not constantName:
                return None

            symbol = self.currentScope.resolve(constantName)

            if symbol is None:
                return None

            isConstant = getattr(symbol, "isConstant", False)
            symbolType = getattr(symbol, "symbolType", None)

            if not isConstant:
                return None

            if symbolType is None or not symbolType.isBaseType(BaseType.TALLY):
                return None

            constantValue = getattr(symbol, "constantValue", None)

            if constantValue is None:
                return None

            try:
                return int(constantValue)
            except Exception:
                return None

        return None

    def extractArraySizes(self, dimensionNodes: list[Any], ownerNode: Any) -> Optional[list[int]]:
        arraySizes: list[int] = []

        for dimensionNode in dimensionNodes:
            constantSize = self.getConstantIntegerValue(dimensionNode)

            if constantSize is None:
                self.addError(
                    ownerNode,
                    "Array size must be a positive tally literal or sacred tally constant."
                )
                return None

            if constantSize <= 0:
                self.addError(
                    ownerNode,
                    f"Array size must be > 0, got {constantSize}."
                )
                return None

            arraySizes.append(constantSize)

        return arraySizes