from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type, canAssign


class SacredInitializerMixin:
    def checkSacredDeclarationInitialValues(self, declarationNode: Any) -> None:
        declaredTypeName = getattr(declarationNode, "typeName", "")
        declaredType = Type.fromBaseType(declaredTypeName)

        if (
            declaredType.baseType == BaseType.UNKNOWN
            and isinstance(getattr(declarationNode, "typeName", None), str)
        ):
            declaredType = Type.fromOrder(getattr(declarationNode, "typeName"))

        declaredItems = getattr(declarationNode, "items", []) or []

        for declaredItem in declaredItems:
            initialValue = getattr(declaredItem, "value", None)

            if initialValue is None:
                self.addError(
                    declaredItem,
                    f"Sacred '{getattr(declaredItem, 'name', '?')}' must be initialized."
                )

                continue

            initialValueType = self.getExpressionType(initialValue)

            if not canAssign(declaredType, initialValueType):
                self.addError(
                    declaredItem,
                    f"Cannot assign {initialValueType} to {declaredType} in sacred '{getattr(declaredItem, 'name', '?')}'."
                )