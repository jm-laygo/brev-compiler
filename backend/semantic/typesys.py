from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


class BaseType(str, Enum):
    TALLY = "tally"
    DIVINE = "divine"
    SIGIL = "sigil"
    SCRIPTURE = "scripture"
    VERITY = "verity"
    HOLLOW = "hollow"
    UNKNOWN = "unknown"
    ERROR = "error"


@dataclass(frozen=True)
class Type:
    baseType: BaseType = BaseType.UNKNOWN
    arrayElementType: Optional["Type"] = None
    orderName: Optional[str] = None

    @staticmethod
    def fromBaseType(typeName: Union[str, BaseType]) -> "Type":
        if isinstance(typeName, BaseType):
            return Type(baseType=typeName)

        normalizedTypeName = (typeName or "").lower()

        typeMapping = {
            "tally": BaseType.TALLY,
            "divine": BaseType.DIVINE,
            "sigil": BaseType.SIGIL,
            "scripture": BaseType.SCRIPTURE,
            "verity": BaseType.VERITY,
            "hollow": BaseType.HOLLOW,
        }

        return Type(
            baseType=typeMapping.get(normalizedTypeName, BaseType.UNKNOWN)
        )

    @staticmethod
    def fromArray(elementType: "Type", dimensionCount: int = 1) -> "Type":
        arrayType = elementType

        for _ in range(max(0, dimensionCount)):
            arrayType = Type(
                baseType=BaseType.UNKNOWN,
                arrayElementType=arrayType
            )

        return arrayType

    @staticmethod
    def fromOrder(orderName: str) -> "Type":
        return Type(
            baseType=BaseType.UNKNOWN,
            orderName=orderName
        )

    @staticmethod
    def unknown() -> "Type":
        return Type(baseType=BaseType.UNKNOWN)

    @staticmethod
    def error() -> "Type":
        return Type(baseType=BaseType.ERROR)

    def isArray(self) -> bool:
        return self.arrayElementType is not None

    def isOrder(self) -> bool:
        return self.orderName is not None

    def isBaseType(self, baseType: BaseType) -> bool:
        return (
            self.arrayElementType is None
            and self.orderName is None
            and self.baseType == baseType
        )

    def __str__(self) -> str:
        if self.baseType == BaseType.ERROR:
            return "type-error"

        if self.isArray():
            dimensionCount = 0
            currentType = self

            while currentType.arrayElementType is not None:
                dimensionCount += 1
                currentType = currentType.arrayElementType

            return f"{currentType}[{dimensionCount}]"

        if self.isOrder():
            return f"order {self.orderName}"

        return self.baseType.value


def isNumericType(typeValue: Type) -> bool:
    if typeValue is None:
        return False

    return (
        typeValue.isBaseType(BaseType.TALLY)
        or typeValue.isBaseType(BaseType.DIVINE)
    )


def isTallyType(typeValue: Type) -> bool:
    if typeValue is None:
        return False

    return typeValue.isBaseType(BaseType.TALLY)


def isBooleanType(typeValue: Type) -> bool:
    if typeValue is None:
        return False

    return typeValue.isBaseType(BaseType.VERITY)


def isStringType(typeValue: Type) -> bool:
    if typeValue is None:
        return False

    return typeValue.isBaseType(BaseType.SCRIPTURE)


def isCharacterType(typeValue: Type) -> bool:
    if typeValue is None:
        return False

    return typeValue.isBaseType(BaseType.SIGIL)


def isErrorType(typeValue: Type) -> bool:
    if typeValue is None:
        return True

    return typeValue.baseType == BaseType.ERROR


def promoteNumericType(leftType: Type, rightType: Type) -> Type:
    if leftType.isBaseType(BaseType.DIVINE) or rightType.isBaseType(BaseType.DIVINE):
        return Type.fromBaseType(BaseType.DIVINE)

    return Type.fromBaseType(BaseType.TALLY)


def isSameType(leftType: Type, rightType: Type) -> bool:
    if leftType is None or rightType is None:
        return False

    return str(leftType) == str(rightType)


def canAssign(destinationType: Type, sourceType: Type) -> bool:
    if destinationType is None or sourceType is None:
        return False

    if destinationType.baseType == BaseType.ERROR or sourceType.baseType == BaseType.ERROR:
        return True

    if isSameType(destinationType, sourceType):
        return True

    if isNumericType(destinationType) and isNumericType(sourceType):
        return True

    if destinationType.isBaseType(BaseType.SCRIPTURE) and sourceType.isBaseType(BaseType.SIGIL):
        return True

    if destinationType.isArray() and sourceType.isArray():
        destinationElementType = destinationType
        sourceElementType = sourceType

        while destinationElementType.isArray() and sourceElementType.isArray():
            destinationElementType = destinationElementType.arrayElementType
            sourceElementType = sourceElementType.arrayElementType

        if destinationElementType.isArray() or sourceElementType.isArray():
            return False

        return canAssign(destinationElementType, sourceElementType)

    return False


def canConcatenate(leftType: Type, rightType: Type, allowCoercion: bool = False) -> bool:
    if leftType is None or rightType is None:
        return False

    if leftType.baseType == BaseType.ERROR or rightType.baseType == BaseType.ERROR:
        return True

    if isStringType(leftType) and isStringType(rightType):
        return True

    if isStringType(leftType) and isCharacterType(rightType):
        return True

    if isCharacterType(leftType) and isStringType(rightType):
        return True

    if isCharacterType(leftType) and isCharacterType(rightType):
        return True

    if allowCoercion and (isStringType(leftType) or isStringType(rightType)):
        return True

    return False


def getBinaryOperationResult(operator: str, leftType: Type, rightType: Type) -> Type:
    if leftType is None or rightType is None:
        return Type.error()

    if leftType.baseType == BaseType.ERROR or rightType.baseType == BaseType.ERROR:
        return Type.error()

    operator = operator or ""

    if operator == "&":
        if canConcatenate(leftType, rightType, allowCoercion=False):
            return Type.fromBaseType(BaseType.SCRIPTURE)

        return Type.error()

    if operator in ("+", "-", "*", "/", "**", "^"):
        if isNumericType(leftType) and isNumericType(rightType):
            return promoteNumericType(leftType, rightType)

        return Type.error()

    if operator == "%":
        if leftType.isBaseType(BaseType.TALLY) and rightType.isBaseType(BaseType.TALLY):
            return Type.fromBaseType(BaseType.TALLY)

        return Type.error()

    if operator in ("==", "!="):
        if isSameType(leftType, rightType):
            return Type.fromBaseType(BaseType.VERITY)

        if isNumericType(leftType) and isNumericType(rightType):
            return Type.fromBaseType(BaseType.VERITY)

        return Type.error()

    if operator in (">", "<", ">=", "<="):
        if isNumericType(leftType) and isNumericType(rightType):
            return Type.fromBaseType(BaseType.VERITY)

        if leftType.isBaseType(BaseType.SIGIL) and rightType.isBaseType(BaseType.SIGIL):
            return Type.fromBaseType(BaseType.VERITY)

        return Type.error()

    if operator == "&&":
        if isBooleanType(leftType) and isBooleanType(rightType):
            return Type.fromBaseType(BaseType.VERITY)

        return Type.error()

    if operator == "||":
        if isBooleanType(leftType) and isBooleanType(rightType):
            return Type.fromBaseType(BaseType.VERITY)

        return Type.error()

    return Type.error()


def getUnaryOperationResult(operator: str, operandType: Type) -> Type:
    if operandType is None:
        return Type.error()

    if operandType.baseType == BaseType.ERROR:
        return Type.error()

    operator = operator or ""

    if operator == "!!":
        if isBooleanType(operandType):
            return Type.fromBaseType(BaseType.VERITY)

        return Type.error()

    if operator == "-":
        if isNumericType(operandType):
            return operandType

        return Type.error()

    if operator in ("++", "--"):
        if isNumericType(operandType):
            return operandType

        return Type.error()

    return Type.error()


def isNumeric(typeValue: Type) -> bool:
    return isNumericType(typeValue)


def isTally(typeValue: Type) -> bool:
    return isTallyType(typeValue)


def isBool(typeValue: Type) -> bool:
    return isBooleanType(typeValue)


def isString(typeValue: Type) -> bool:
    return isStringType(typeValue)


def isCharacter(typeValue: Type) -> bool:
    return isCharacterType(typeValue)


def isError(typeValue: Type) -> bool:
    return isErrorType(typeValue)