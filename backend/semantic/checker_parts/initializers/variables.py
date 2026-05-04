from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type, canAssign
from ..helpers import getClassName


class VariableInitializerMixin:
    def checkVariableDeclarationInitialValues(self, declarationNode: Any) -> None:
        declaredTypeName = getattr(declarationNode, "typeName", "")
        declaredType = Type.fromBaseType(declaredTypeName)

        if (
            declaredType.baseType == BaseType.UNKNOWN
            and isinstance(getattr(declarationNode, "typeName", None), str)
        ):
            declaredType = Type.fromOrder(getattr(declarationNode, "typeName"))

        declaredItems = getattr(declarationNode, "items", []) or []

        for declaredItem in declaredItems:
            initialValue = getattr(declaredItem, "initialValue", None)

            if initialValue is None:
                continue

            dimensionNodes = getattr(declaredItem, "dimensions", []) or []

            if len(dimensionNodes) > 0:
                targetType = Type.fromArray(declaredType, len(dimensionNodes))
            else:
                targetType = declaredType

            if (
                len(dimensionNodes) > 0
                and getClassName(initialValue) == "ArrayInitializationExpression"
            ):
                dimensionSizes = self.convertDimensionsToSizes(
                    dimensionNodes,
                    ownerNode=declaredItem
                )

                if dimensionSizes is None:
                    continue

                self.checkArrayInitializationShape(
                    initialValue,
                    dimensionSizes,
                    level=0,
                    ownerNode=declaredItem
                )

                self.checkArrayInitializationTypes(
                    initialValue,
                    targetType,
                    level=0,
                    sizes=dimensionSizes,
                    ownerNode=declaredItem
                )

                continue

            initialValueType = self.getExpressionType(initialValue)

            if not canAssign(targetType, initialValueType):
                self.addError(
                    declaredItem,
                    f"Cannot assign {initialValueType} to {targetType} in '{getattr(declaredItem, 'name', '?')}'."
                )