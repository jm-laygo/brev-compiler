from __future__ import annotations
from backend.errors import RuntimeTypeError

def _coerce_value_to_type(self, declared_type_name: str, value, node=None):
    lowered_type_name = (declared_type_name or "").lower()

    if lowered_type_name == "tally":
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        raise RuntimeTypeError(node, "Value cannot be converted to tally.")

    if lowered_type_name == "divine":
        if isinstance(value, bool):
            return float(value)
        if isinstance(value, int):
            return float(value)
        if isinstance(value, float):
            return value
        raise RuntimeTypeError(node, "Value cannot be converted to divine.")

    if lowered_type_name == "scripture":
        return self.stringify(value)

    if lowered_type_name == "verity":
        if isinstance(value, bool):
            return value
        raise RuntimeTypeError(node, "Value cannot be converted to verity.")

    if lowered_type_name == "sigil":
        string_form = str(value)
        if len(string_form) == 1:
            return string_form
        raise RuntimeTypeError(node, "Value cannot be converted to sigil.")

    return value

def bind_coercion_methods(cls):
    cls._coerce_value_to_type = _coerce_value_to_type