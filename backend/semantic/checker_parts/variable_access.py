from __future__ import annotations
from typing import Any

from backend.semantic.typesys import (
    BaseType,
    Type,
    isTallyType,
)
from .helper_functions import getClassName


class LValuesMixin:
    def getLeftHandValueRootSymbol(self, leftHandValueNode: Any):
        if leftHandValueNode is None:
            return None

        leftHandValueKind = getClassName(leftHandValueNode)

        if leftHandValueKind == "NameReference":
            identifierName = getattr(leftHandValueNode, "name", None)

            if identifierName:
                return self.currentScope.resolve(identifierName)

            return None

        if leftHandValueKind == "IndexReference":
            baseReference = getattr(leftHandValueNode, "baseReference", None)
            return self.getLeftHandValueRootSymbol(baseReference)

        if leftHandValueKind == "MemberReference":
            baseReference = getattr(leftHandValueNode, "baseReference", None)
            return self.getLeftHandValueRootSymbol(baseReference)

        return None

    def getLeftHandValueType(self, leftHandValueNode: Any) -> Type:
        if leftHandValueNode is None:
            return Type.unknown()

        leftHandValueKind = getClassName(leftHandValueNode)

        # name reference
        if leftHandValueKind == "NameReference":
            identifierName = getattr(leftHandValueNode, "name", None)

            if identifierName:
                resolvedSymbol = self.currentScope.resolve(identifierName)
            else:
                resolvedSymbol = None

            from backend.semantic.symbols import VariableSymbol

            if isinstance(resolvedSymbol, VariableSymbol):
                return resolvedSymbol.symbolType

            suggestionText = self.getSuggestionMessage(identifierName)

            self.addError(
                leftHandValueNode,
                f"Undeclared identifier '{identifierName}'.{suggestionText}"
            )

            return Type.error()

        # array index
        if leftHandValueKind == "IndexReference":
            baseReference = getattr(leftHandValueNode, "baseReference", None)
            indexExpression = getattr(leftHandValueNode, "indexExpression", None)

            baseType = self.getLeftHandValueType(baseReference)
            indexType = self.getExpressionType(indexExpression)

            if self.hasTypeError(baseType) or self.hasTypeError(indexType):
                return Type.error()

            if not isTallyType(indexType):
                self.addError(
                    indexExpression if indexExpression is not None else leftHandValueNode,
                    f"Array index must be tally, got {self.getTypeName(indexType)}."
                )

            # scripture index
            if baseType.isBaseType(BaseType.SCRIPTURE):
                return Type.fromBaseType(BaseType.SIGIL)

            if not baseType.isArray():
                self.addError(
                    leftHandValueNode,
                    f"Cannot index non-array type {self.getTypeName(baseType)}."
                )

                return Type.error()

            return baseType.arrayElementType or Type.error()

        # member access
        if leftHandValueKind == "MemberReference":
            baseReference = getattr(leftHandValueNode, "baseReference", None)
            memberName = getattr(leftHandValueNode, "memberName", None)

            baseType = self.getLeftHandValueType(baseReference)

            if self.hasTypeError(baseType):
                return Type.error()

            if not baseType.isOrder():
                self.addError(
                    leftHandValueNode,
                    f"Member access '.{memberName}' on non-order type {self.getTypeName(baseType)}."
                )

                return Type.error()

            orderSymbol = self.orders.get(baseType.orderName or "")

            if orderSymbol is None:
                self.addError(
                    leftHandValueNode,
                    f"Unknown order type '{baseType.orderName}'."
                )

                return Type.error()

            memberSymbol = orderSymbol.members.get(memberName)

            if memberSymbol is None:
                suggestionText = self.getSuggestionFromCandidates(
                    memberName,
                    list(orderSymbol.members.keys())
                )

                self.addError(
                    leftHandValueNode,
                    f"Order '{orderSymbol.name}' has no member '{memberName}'.{suggestionText}"
                )

                return Type.error()

            return memberSymbol.symbolType

        return self.getExpressionType(leftHandValueNode)