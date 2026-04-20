from __future__ import annotations

MAX_STRINGIFY_DEPTH = 64


def stringify(value, _seen=None, _depth=0):
    if _seen is None:
        _seen = set()

    if _depth > MAX_STRINGIFY_DEPTH:
        return "..."

    if value is True:
        return "holy"
    if value is False:
        return "unholy"
    if value is None:
        return "hollow"
    if isinstance(value, list):
        object_id = id(value)
        if object_id in _seen:
            return "{...}"
        _seen.add(object_id)
        rendered = "{" + ", ".join(stringify(v, _seen, _depth + 1) for v in value) + "}"
        _seen.remove(object_id)
        return rendered
    if isinstance(value, dict):
        object_id = id(value)
        if object_id in _seen:
            return "{...}"
        _seen.add(object_id)
        inner = ", ".join(
            f"{k}: {stringify(v, _seen, _depth + 1)}" for k, v in value.items() if k != "__order__"
        )
        _seen.remove(object_id)
        return "{ " + inner + " }"
    if isinstance(value, float):
        return f"{value:.2f}"
    if isinstance(value, str):
        if value == "\0":
            return r"'\0'"
        if value == "":
            return '""'
        return value
    return str(value)