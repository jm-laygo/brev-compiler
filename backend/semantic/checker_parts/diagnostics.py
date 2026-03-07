from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type

def _fmt_type(type_value: Type) -> str:
    if type_value is None:
        return "<unknown>"
    if getattr(type_value, "base", None) == BaseType.ERROR:
        return "<invalid>"
    if getattr(type_value, "base", None) == BaseType.UNKNOWN:
        return "<unknown>"
    return str(type_value)

def _is_bad(type_value: Type) -> bool:
    if type_value is None:
        return True
    return type_value.base in (BaseType.ERROR,)

def _fmt_type_for_msg(type_value: Type) -> str:
    if type_value is None:
        return "unknown"
    if getattr(type_value, "base", None) == BaseType.ERROR:
        return "an invalid expression"
    if getattr(type_value, "base", None) == BaseType.UNKNOWN:
        return "unknown"
    return str(type_value)

def _binop_error_msg(operator_text: str, left_type: Type, right_type: Type) -> str:
    left_type_name = _fmt_type_for_msg(left_type)
    right_type_name = _fmt_type_for_msg(right_type)

    if left_type.base == BaseType.ERROR and right_type.base != BaseType.ERROR:
        return f"Invalid '{operator_text}' because the left operand is an invalid expression and the right operand is {right_type_name}."
    if right_type.base == BaseType.ERROR and left_type.base != BaseType.ERROR:
        return f"Invalid '{operator_text}' because the left operand is {left_type_name} and the right operand is an invalid expression."
    if left_type.base == BaseType.ERROR and right_type.base == BaseType.ERROR:
        return f"Invalid '{operator_text}' because both operands are invalid expressions."

    return f"Invalid binary op '{operator_text}' for operands {left_type_name} and {right_type_name}."

def _has_type_error(type_value: Type) -> bool:
    return getattr(type_value, "base", None) == BaseType.ERROR

def _tname(type_value: Type) -> str:
    if _has_type_error(type_value):
        return "<previous type error>"
    return str(type_value)