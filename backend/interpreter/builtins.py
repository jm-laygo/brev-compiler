from __future__ import annotations

def stringify(value):
    if value is True:
        return "holy"
    if value is False:
        return "unholy"
    if value is None:
        return "hollow"
    if isinstance(value, list):
        return "{" + ", ".join(stringify(v) for v in value) + "}"
    if isinstance(value, dict):
        inner = ", ".join(f"{k}: {stringify(v)}" for k, v in value.items() if k != "__order__")
        return "{ " + inner + " }"
    return str(value)