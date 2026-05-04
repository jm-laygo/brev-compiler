from __future__ import annotations

from backend.errors import InputConversionRuntimeError


def convertInputForTarget(self, targetReference, rawInputValue, currentEnvironment):
    currentRuntimeValue = self.readLeftHandValue(
        targetReference,
        currentEnvironment
    )

    if isinstance(currentRuntimeValue, bool):
        normalizedInputText = str(rawInputValue).strip().lower()

        if normalizedInputText in ("holy", "true", "1"):
            return True

        if normalizedInputText in ("unholy", "false", "0"):
            return False

        raise InputConversionRuntimeError(
            targetReference,
            f"'{rawInputValue}' cannot be converted to verity."
        )

    if isinstance(currentRuntimeValue, int) and not isinstance(currentRuntimeValue, bool):
        inputText = str(rawInputValue).strip()

        # allow ~ as negative sign
        if inputText.startswith("~"):
            inputText = "-" + inputText[1:]

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
        try:
            return float(rawInputValue)

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