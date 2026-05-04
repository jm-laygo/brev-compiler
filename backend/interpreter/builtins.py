from __future__ import annotations


def stringifyValue(value):
    if value is True:
        return "holy"

    if value is False:
        return "unholy"

    if value is None:
        return "hollow"

    if isinstance(value, list):
        formattedItems = ", ".join(
            stringifyValue(itemValue)
            for itemValue in value
        )

        return "{" + formattedItems + "}"

    if isinstance(value, dict):
        formattedMembers = ", ".join(
            f"{memberName}: {stringifyValue(memberValue)}"
            for memberName, memberValue in value.items()
            if memberName != "__order__"
        )

        return "{ " + formattedMembers + " }"

    if isinstance(value, float):
        return f"{value:.2f}"

    if isinstance(value, str):
        return value

    return str(value)