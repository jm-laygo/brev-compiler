from __future__ import annotations
from backend.errors import InputConversionRuntimeError

MAX_SCRIPTURE_INPUT_LENGTH = 48


def _looks_like_numeric_literal(raw_input_value):
    normalized_text = str(raw_input_value).strip()
    if not normalized_text:
        return False

    # Brev tally input may use ~ for negative values, so mirror that here.
    if normalized_text.startswith("~"):
        normalized_text = "-" + normalized_text[1:]

    if normalized_text.startswith("-"):
        normalized_text = normalized_text[1:]

    if not normalized_text:
        return False

    if normalized_text.isdigit():
        return True

    decimal_parts = normalized_text.split(".")
    if len(decimal_parts) == 2 and decimal_parts[0].isdigit() and decimal_parts[1].isdigit():
        return True

    return False


def _preview_for_error(raw_input_value, max_len=32):
    text = str(raw_input_value)
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."

def _convert_input_for_target(self, target_reference, raw_input_value, current_environment):
    current_runtime_value = self._read_lvalue(target_reference, current_environment)

    if isinstance(current_runtime_value, bool):
        normalized_text = str(raw_input_value).strip().lower()

        if normalized_text in ("holy", "true", "1"):
            return True

        if normalized_text in ("unholy", "false", "0"):
            return False

        raise InputConversionRuntimeError(
            target_reference,
            f"'{raw_input_value}' cannot be converted to verity.",
        )

    if isinstance(current_runtime_value, int) and not isinstance(current_runtime_value, bool):
        # Accept ~ as a negative sign for tally input
        input_str = str(raw_input_value).strip()
        if input_str.startswith("~"):
            input_str = "-" + input_str[1:]
        try:
            converted_value = int(input_str)
        except (TypeError, ValueError):
            raise InputConversionRuntimeError(
                target_reference,
                f"'{raw_input_value}' cannot be converted to tally.",
            )

        digit_count = len(input_str.lstrip("-"))
        if digit_count > 9:
            raise InputConversionRuntimeError(
                target_reference,
                f"Tally input '{raw_input_value}' exceeds the 9-digit limit.",
            )

        return converted_value

    if isinstance(current_runtime_value, float):
        try:
            return float(raw_input_value)
        except (TypeError, ValueError):
            raise InputConversionRuntimeError(
                target_reference,
                f"'{raw_input_value}' cannot be converted to divine.",
            )

    if isinstance(current_runtime_value, str):
        input_text = str(raw_input_value)

        if len(current_runtime_value) == 1:
            if len(input_text) != 1:
                raise InputConversionRuntimeError(
                    target_reference,
                    f"'{raw_input_value}' cannot be converted to sigil.",
                )
            return input_text

        if _looks_like_numeric_literal(raw_input_value):
            raise InputConversionRuntimeError(
                target_reference,
                f"'{raw_input_value}' cannot be converted to scripture.",
            )

        if len(input_text) > MAX_SCRIPTURE_INPUT_LENGTH:
            preview = _preview_for_error(raw_input_value)
            raise InputConversionRuntimeError(
                target_reference,
                f"Scripture input '{preview}' exceeds {MAX_SCRIPTURE_INPUT_LENGTH} characters.",
            )

        return input_text

    return raw_input_value

def bind_input_conversion_methods(cls):
    cls._convert_input_for_target = _convert_input_for_target