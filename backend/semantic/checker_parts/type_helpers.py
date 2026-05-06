from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type


class TypeBuildersMixin:
    def getTypeFromReturnType(self, returnTypeValue: Any) -> Type:
        if returnTypeValue is None:
            return Type.unknown()

        if isinstance(returnTypeValue, str):
            typeName = returnTypeValue
        else:
            typeName = str(returnTypeValue)

        resolvedType = Type.fromBaseType(typeName)

        if resolvedType.baseType == BaseType.UNKNOWN and typeName:
            return Type.fromOrder(typeName)

        return resolvedType

    def getTypeFromDeclaration(self, declarationNode: Any) -> Type:
        declaredTypeName = getattr(declarationNode, "typeName", None)

        if isinstance(declaredTypeName, str):
            baseType = Type.fromBaseType(declaredTypeName)
        else:
            baseType = Type.fromBaseType(str(declaredTypeName))

        if (
            baseType.baseType == BaseType.UNKNOWN
            and isinstance(declaredTypeName, str)
            and declaredTypeName
        ):
            baseType = Type.fromOrder(declaredTypeName)

        dimensionNodes = getattr(declarationNode, "dimensions", None)

        if isinstance(dimensionNodes, list):
            dimensionCount = len(dimensionNodes)
        else:
            dimensionCount = int(getattr(declarationNode, "arrayDimensions", 0) or 0)

        if dimensionCount > 0:
            return Type.fromArray(baseType, dimensionCount)

        return baseType