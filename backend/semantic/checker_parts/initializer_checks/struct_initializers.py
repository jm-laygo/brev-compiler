from __future__ import annotations
from typing import Any


class OrdainInitializerMixin:
    def checkOrdainDeclarationInitialValues(self, declarationNode: Any) -> None:
        declaredItems = getattr(declarationNode, "items", []) or []

        for declaredItem in declaredItems:
            initialValue = getattr(declaredItem, "initialValue", None)

            if initialValue is None:
                continue

            self.getExpressionType(initialValue)