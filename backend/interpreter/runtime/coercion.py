from __future__ import annotations
from backend.errors import RuntimeTypeError

def _runtime_type_name(value):
    if isinstance(value, bool):
        return "verity"
    if isinstance(value, int):
        return "tally"
    if isinstance(value, float):
        return "divine"
    if isinstance(value, str):
        return "sigil" if len(value) == 1 else "scripture"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        order_name = value.get("__order__")
        if order_name:
            return f"order {order_name}"
        return "order"
    if value is None:
        return "hollow"
    return type(value).__name__

def _coerce_value_to_type(self, declared_type_name: str, value, node=None):
    lowered_type_name = (declared_type_name or "").lower()

    if lowered_type_name == "tally":
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        raise RuntimeTypeError(node, f"Cannot convert {_runtime_type_name(value)} to tally.")

    if lowered_type_name == "divine":
        if isinstance(value, bool):
            return float(value)
        if isinstance(value, int):
            return float(value)
        if isinstance(value, float):
            return value
        raise RuntimeTypeError(node, f"Cannot convert {_runtime_type_name(value)} to divine.")

    if lowered_type_name == "scripture":
        return self.stringify(value)

    if lowered_type_name == "verity":
        if isinstance(value, bool):
            return value
        raise RuntimeTypeError(node, f"Cannot convert {_runtime_type_name(value)} to verity.")

    if lowered_type_name == "sigil":
        string_form = str(value)

        if len(string_form) == 1:
            return string_form

        if len(string_form) == 3 and string_form[0] == "'" and string_form[2] == "'":
            return string_form[1]

        raise RuntimeTypeError(node, f"Cannot convert {_runtime_type_name(value)} to sigil.")

    return value

def bind_coercion_methods(cls):
    cls._coerce_value_to_type = _coerce_value_to_type