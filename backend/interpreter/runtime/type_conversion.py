from __future__ import annotations

from backend.errors import RuntimeTypeError


def getRuntimeTypeName(value):
    if isinstance(value, bool):
        return "verity"

    if isinstance(value, int):
        return "tally"

    if isinstance(value, float):
        return "divine"

    if isinstance(value, str):
        if len(value) == 1:
            return "sigil"

        return "scripture"

    if isinstance(value, list):
        return "array"

    if isinstance(value, dict):
        orderName = value.get("__order__")

        if orderName:
            return f"order {orderName}"

        return "order"

    if value is None:
        return "hollow"

    return type(value).__name__


def coerceValueToType(self, declaredTypeName: str, value, node=None):
    loweredTypeName = (declaredTypeName or "").lower()

    if loweredTypeName == "tally":
        if isinstance(value, bool):
            raise RuntimeTypeError(
                node,
                "Cannot convert verity to tally."
            )

        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        raise RuntimeTypeError(
            node,
            f"Cannot convert {getRuntimeTypeName(value)} to tally."
        )

    if loweredTypeName == "divine":
        if isinstance(value, bool):
            raise RuntimeTypeError(
                node,
                "Cannot convert verity to divine."
            )

        if isinstance(value, int):
            return float(value)

        if isinstance(value, float):
            return value

        raise RuntimeTypeError(
            node,
            f"Cannot convert {getRuntimeTypeName(value)} to divine."
        )

    if loweredTypeName == "scripture":
        if isinstance(value, str):
            return value

        raise RuntimeTypeError(
            node,
            f"Cannot convert {getRuntimeTypeName(value)} to scripture."
        )

    if loweredTypeName == "verity":
        if isinstance(value, bool):
            return value

        raise RuntimeTypeError(
            node,
            f"Cannot convert {getRuntimeTypeName(value)} to verity."
        )

    if loweredTypeName == "sigil":
        if isinstance(value, str) and len(value) == 1:
            return value

        raise RuntimeTypeError(
            node,
            f"Cannot convert {getRuntimeTypeName(value)} to sigil."
        )

    return value


def runtimeTypeName(self, value):
    return getRuntimeTypeName(value)


def bindCoercionMethods(interpreterClass):
    interpreterClass.coerceValueToType = coerceValueToType
    interpreterClass.getRuntimeTypeName = runtimeTypeName