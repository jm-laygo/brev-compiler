from __future__ import annotations

from backend.semantic.typesys import BaseType, Type


def formatType(typeValue: Type) -> str:
    if typeValue is None:
        return "<unknown>"

    if getattr(typeValue, "baseType", None) == BaseType.ERROR:
        return "<invalid>"

    if getattr(typeValue, "baseType", None) == BaseType.UNKNOWN:
        return "<unknown>"

    return str(typeValue)

def isBadType(typeValue: Type) -> bool:
    if typeValue is None:
        return True

    return typeValue.baseType in (BaseType.ERROR,)

def formatTypeForMessage(typeValue: Type) -> str:
    if typeValue is None:
        return "unknown"

    if getattr(typeValue, "baseType", None) == BaseType.ERROR:
        return "an invalid expression"

    if getattr(typeValue, "baseType", None) == BaseType.UNKNOWN:
        return "unknown"

    return str(typeValue)

def getBinaryOperationErrorMessage(operatorText: str, leftType: Type, rightType: Type) -> str:
    leftTypeName = formatTypeForMessage(leftType)
    rightTypeName = formatTypeForMessage(rightType)

    if leftType.baseType == BaseType.ERROR and rightType.baseType != BaseType.ERROR:
        return f"Invalid '{operatorText}' because the left operand is an invalid expression and the right operand is {rightTypeName}."

    if rightType.baseType == BaseType.ERROR and leftType.baseType != BaseType.ERROR:
        return f"Invalid '{operatorText}' because the left operand is {leftTypeName} and the right operand is an invalid expression."

    if leftType.baseType == BaseType.ERROR and rightType.baseType == BaseType.ERROR:
        return f"Invalid '{operatorText}' because both operands are invalid expressions."

    return f"Invalid binary op '{operatorText}' for operands {leftTypeName} and {rightTypeName}."

def hasTypeError(typeValue: Type) -> bool:
    return getattr(typeValue, "baseType", None) == BaseType.ERROR

def getTypeName(typeValue: Type) -> str:
    if hasTypeError(typeValue):
        return "<previous type error>"

    return str(typeValue)