from __future__ import annotations

from .exec_decls import _exec_ordain_decl, _exec_sacred_decl, _exec_var_decl
from .materialize import (
    _default_value_for_type,
    _make_array_of,
    _make_order_instance,
    _materialize_var_item,
    _require_int_dim,
)

def bind_declaration_methods(cls):
    cls._exec_var_decl = _exec_var_decl
    cls._exec_sacred_decl = _exec_sacred_decl
    cls._exec_ordain_decl = _exec_ordain_decl
    cls._materialize_var_item = _materialize_var_item
    cls._make_order_instance = _make_order_instance
    cls._make_array_of = _make_array_of
    cls._require_int_dim = _require_int_dim
    cls._default_value_for_type = _default_value_for_type
