from __future__ import annotations
from backend.errors import InputConversionRuntimeError

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
        try:
            return int(raw_input_value)
        except Exception:
            raise InputConversionRuntimeError(
                target_reference,
                f"'{raw_input_value}' cannot be converted to tally.",
            )

    if isinstance(current_runtime_value, float):
        try:
            return float(raw_input_value)
        except Exception:
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

        return input_text

    return raw_input_value

def bind_input_conversion_methods(cls):
    cls._convert_input_for_target = _convert_input_for_target