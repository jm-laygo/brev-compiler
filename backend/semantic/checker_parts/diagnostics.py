from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type

def _fmt_type(t: Type) -> str:
    if t is None:
        return "<unknown>"
    if getattr(t, "base", None) == BaseType.ERROR:
        return "<invalid>"
    if getattr(t, "base", None) == BaseType.UNKNOWN:
        return "<unknown>"
    return str(t)

def _is_bad(t: Type) -> bool:
    if t is None:
        return True
    return t.base in (BaseType.ERROR,)

def _fmt_type_for_msg(t: Type) -> str:
    if t is None:
        return "unknown"
    if getattr(t, "base", None) == BaseType.ERROR:
        return "an invalid expression"
    if getattr(t, "base", None) == BaseType.UNKNOWN:
        return "unknown"
    return str(t)

def _binop_error_msg(op: str, lt: Type, rt: Type) -> str:
    l = _fmt_type_for_msg(lt)
    r = _fmt_type_for_msg(rt)

    if lt.base == BaseType.ERROR and rt.base != BaseType.ERROR:
        return f"Invalid '{op}' because the left operand is an invalid expression and the right operand is {r}."
    if rt.base == BaseType.ERROR and lt.base != BaseType.ERROR:
        return f"Invalid '{op}' because the left operand is {l} and the right operand is an invalid expression."
    if lt.base == BaseType.ERROR and rt.base == BaseType.ERROR:
        return f"Invalid '{op}' because both operands are invalid expressions."

    return f"Invalid binary op '{op}' for operands {l} and {r}."

def _has_type_error(t: Type) -> bool:
    return getattr(t, "base", None) == BaseType.ERROR

def _tname(t: Type) -> str:
    if _has_type_error(t):
        return "<previous type error>"
    return str(t)