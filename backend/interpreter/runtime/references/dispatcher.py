from __future__ import annotations

from .readers import _read_lvalue, _read_lvalue_from_value
from .writers import _assign_lvalue, _resolve_index_target

def bind_reference_methods(cls):
    cls._read_lvalue = _read_lvalue
    cls._assign_lvalue = _assign_lvalue
    cls._resolve_index_target = _resolve_index_target
    cls._read_lvalue_from_value = _read_lvalue_from_value
