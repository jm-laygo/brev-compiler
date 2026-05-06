from __future__ import annotations
from typing import Any, List

from backend.semantic.typesys import (
    BaseType,
    Type,
    isNumericType,
    getUnaryOperationResult,
    getBinaryOperationResult,
)
from .helper_functions import getClassName


class ExpressionsMixin:
    def getExpressionType(self, expressionNode: Any) -> Type:
        if expressionNode is None:
            return Type.unknown()

        expressionKind = getClassName(expressionNode)

        if expressionKind == "LiteralExpression":
            literalTypeName = (getattr(expressionNode, "literalType", None) or "").lower()

            if literalTypeName == "int":
                return Type.fromBaseType(BaseType.TALLY)

            if literalTypeName == "decimal":
                return Type.fromBaseType(BaseType.DIVINE)

            if literalTypeName == "char":
                return Type.fromBaseType(BaseType.SIGIL)

            if literalTypeName == "string":
                return Type.fromBaseType(BaseType.SCRIPTURE)

            if literalTypeName == "bool":
                return Type.fromBaseType(BaseType.VERITY)

            return Type.unknown()

        if expressionKind == "ArrayInitializationExpression":
            itemNodes = getattr(expressionNode, "items", []) or []

            if not itemNodes:
                return Type.unknown()

            itemTypes: List[Type] = []

            for itemNode in itemNodes:
                itemTypes.extend([self.getExpressionType(itemNode)])

            for itemType in itemTypes:
                if itemType.baseType == BaseType.ERROR:
                    return Type.error()

            firstItemType = itemTypes[0]

            if all(isNumericType(itemType) for itemType in itemTypes):
                resultingNumericType = Type.fromBaseType(BaseType.TALLY)

                for itemType in itemTypes:
                    if itemType.isBaseType(BaseType.DIVINE):
                        resultingNumericType = Type.fromBaseType(BaseType.DIVINE)
                        break

                return Type.fromArray(resultingNumericType, 1)

            if all(str(itemType) == str(firstItemType) for itemType in itemTypes):
                return Type.fromArray(firstItemType, 1)

            self.addError(
                expressionNode,
                f"Inconsistent array initializer types: {', '.join(str(itemType) for itemType in itemTypes)}"
            )

            return Type.error()

        if expressionKind == "GroupExpression":
            innerExpression = getattr(expressionNode, "expression", None)

            return self.getExpressionType(innerExpression)

        if expressionKind == "VariableExpression":
            referenceNode = getattr(expressionNode, "reference", None)

            return self.getLeftHandValueType(referenceNode)

        if expressionKind == "FunctionCallExpression":
            functionName = getattr(expressionNode, "calleeName", None)
            argumentNodes = getattr(expressionNode, "arguments", []) or []

            return self.checkFunctionCall(functionName, argumentNodes, expressionNode)

        if expressionKind == "VerseOfExpression":
            innerExpression = getattr(expressionNode, "expression", None)
            innerType = self.getExpressionType(innerExpression)

            if self.hasTypeError(innerType):
                return Type.error()

            if not innerType.isBaseType(BaseType.SCRIPTURE):
                self.addError(
                    expressionNode,
                    f"verseof() expects scripture, got {self.getTypeName(innerType)}."
                )
                return Type.error()

            return Type.fromBaseType(BaseType.TALLY)

        if expressionKind == "UnaryExpression":
            operatorText = getattr(expressionNode, "operator", "") or ""
            operandNode = getattr(expressionNode, "operand", None)
            operandType = self.getExpressionType(operandNode)

            if self.hasTypeError(operandType):
                return Type.error()

            resultType = getUnaryOperationResult(operatorText, operandType)

            if self.hasTypeError(resultType):
                self.addError(
                    expressionNode,
                    f"Invalid unary operator '{operatorText}' for type {self.getTypeName(operandType)}."
                )

            return resultType

        if expressionKind == "BinaryExpression":
            operatorText = getattr(expressionNode, "operator", "") or ""
            leftExpression = getattr(expressionNode, "leftExpression", None)
            rightExpression = getattr(expressionNode, "rightExpression", None)

            leftType = self.getExpressionType(leftExpression)
            rightType = self.getExpressionType(rightExpression)

            if self.hasTypeError(leftType) or self.hasTypeError(rightType):
                return Type.error()

            resultType = getBinaryOperationResult(operatorText, leftType, rightType)

            if self.hasTypeError(resultType):
                self.addError(
                    expressionNode,
                    f"Invalid binary operator '{operatorText}' for types {self.getTypeName(leftType)} and {self.getTypeName(rightType)}."
                )

                return Type.error()

            return resultType

        if expressionKind == "IdentifierReference":
            identifierName = getattr(expressionNode, "name", None)

            if identifierName:
                resolvedSymbol = self.currentScope.resolve(identifierName)
            else:
                resolvedSymbol = None

            from backend.semantic.symbols import VariableSymbol

            if isinstance(resolvedSymbol, VariableSymbol):
                return resolvedSymbol.symbolType

            suggestionText = self.getSuggestionMessage(identifierName)

            self.addError(
                expressionNode,
                f"Undeclared identifier '{identifierName}'.{suggestionText}"
            )

            return Type.error()

        return Type.unknown()