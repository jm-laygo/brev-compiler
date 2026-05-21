from __future__ import annotations

from backend.errors import InputConversionRuntimeError
from backend.ast.ast_nodes import NameReference


def getTargetDeclaredTypeName(self, targetReference, currentEnvironment):
    if isinstance(targetReference, NameReference):
        return currentEnvironment.getDeclaredType(targetReference.name)

    return None


def convertInputForTarget(self, targetReference, rawInputValue, currentEnvironment):
    declaredTypeName = getTargetDeclaredTypeName(
        self,
        targetReference,
        currentEnvironment
    )

    if declaredTypeName is not None:
        loweredTypeName = declaredTypeName.lower() if isinstance(declaredTypeName, str) else str(declaredTypeName).lower()

        if loweredTypeName == "verity":
            normalizedInputText = str(rawInputValue).strip().lower()

            if normalizedInputText == "holy":
                return True

            if normalizedInputText == "unholy":
                return False

            raise InputConversionRuntimeError(
                targetReference,
                f"'{rawInputValue}' cannot be converted to verity. Use only holy or unholy."
            )

        if loweredTypeName == "tally":
            inputText = str(rawInputValue).strip()

            try:
                convertedValue = int(inputText)

            except (TypeError, ValueError):
                raise InputConversionRuntimeError(
                    targetReference,
                    f"'{rawInputValue}' cannot be converted to tally."
                )

            digitCount = len(inputText.lstrip("-"))

            if digitCount > 9:
                raise InputConversionRuntimeError(
                    targetReference,
                    f"Tally input '{rawInputValue}' exceeds the 9-digit limit."
                )

            return convertedValue

        if loweredTypeName == "divine":
            inputText = str(rawInputValue).strip()

            try:
                return float(inputText)

            except (TypeError, ValueError):
                raise InputConversionRuntimeError(
                    targetReference,
                    f"'{rawInputValue}' cannot be converted to divine."
                )

        if loweredTypeName == "sigil":
            inputText = str(rawInputValue)

            if len(inputText) != 1:
                raise InputConversionRuntimeError(
                    targetReference,
                    f"'{rawInputValue}' cannot be converted to sigil."
                )

            return inputText

        if loweredTypeName == "scripture":
            return str(rawInputValue)

    currentRuntimeValue = self.readLeftHandValue(
        targetReference,
        currentEnvironment
    )

    if isinstance(currentRuntimeValue, bool):
        normalizedInputText = str(rawInputValue).strip().lower()

        if normalizedInputText == "holy":
            return True

        if normalizedInputText == "unholy":
            return False

        raise InputConversionRuntimeError(
            targetReference,
            f"'{rawInputValue}' cannot be converted to verity. Use only holy or unholy."
        )

    if isinstance(currentRuntimeValue, int) and not isinstance(currentRuntimeValue, bool):
        inputText = str(rawInputValue).strip()

        try:
            convertedValue = int(inputText)

        except (TypeError, ValueError):
            raise InputConversionRuntimeError(
                targetReference,
                f"'{rawInputValue}' cannot be converted to tally."
            )

        digitCount = len(inputText.lstrip("-"))

        if digitCount > 9:
            raise InputConversionRuntimeError(
                targetReference,
                f"Tally input '{rawInputValue}' exceeds the 9-digit limit."
            )

        return convertedValue

    if isinstance(currentRuntimeValue, float):
        inputText = str(rawInputValue).strip()

        try:
            return float(inputText)

        except (TypeError, ValueError):
            raise InputConversionRuntimeError(
                targetReference,
                f"'{rawInputValue}' cannot be converted to divine."
            )

    if isinstance(currentRuntimeValue, str):
        inputText = str(rawInputValue)

        if len(currentRuntimeValue) == 1:
            if len(inputText) != 1:
                raise InputConversionRuntimeError(
                    targetReference,
                    f"'{rawInputValue}' cannot be converted to sigil."
                )

            return inputText

        return inputText

    return rawInputValue


def bindInputConversionMethods(interpreterClass):
    interpreterClass.convertInputForTarget = convertInputForTarget