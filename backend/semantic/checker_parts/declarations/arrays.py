from __future__ import annotations
from typing import Any, Optional

from ..helpers import getClassName


class DeclarationArrayMixin:
    def getConstantIntegerValue(self, expressionNode: Any) -> Optional[int]:
        if expressionNode is None:
            return None

        if getClassName(expressionNode) == "LiteralExpression":
            literalType = (getattr(expressionNode, "literalType", "") or "").lower()

            if literalType == "int":
                try:
                    return int(getattr(expressionNode, "value"))

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
                    "Array size must be a constant integer literal (tally)."
                )

                return None

            if constantSize <= 0:
                self.addError(
                    ownerNode,
                    f"Array size must be > 0, got {constantSize}."
                )

                return None

            arraySizes.extend([constantSize])

        return arraySizes