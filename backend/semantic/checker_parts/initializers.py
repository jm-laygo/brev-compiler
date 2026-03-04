from __future__ import annotations
from typing import Any
from backend.semantic.typesys import Type, BaseType, can_assign

class InitializersMixin:
    def _check_var_decl_init(self, decl: Any) -> None:
        decl_type = Type.base_t(getattr(decl, "type_name", ""))
        if decl_type.base == BaseType.UNKNOWN and isinstance(getattr(decl, "type_name", None), str):
            decl_type = Type.order(getattr(decl, "type_name"))

        for it in getattr(decl, "items", []) or []:
            init = getattr(it, "init", None)
            if init is None:
                continue
            t = self._expr_type(init)
            dims = getattr(it, "dims", []) or []
            target_t = Type.array(decl_type, len(dims)) if len(dims) > 0 else decl_type
            if not can_assign(target_t, t):
                self._error(it, f"Cannot assign {t} to {target_t} in initialization of '{getattr(it,'name','?')}'.")

    def _check_sacred_decl_init(self, decl: Any) -> None:
        decl_type = Type.base_t(getattr(decl, "type_name", ""))
        for it in getattr(decl, "items", []) or []:
            val = getattr(it, "value", None)
            if val is None:
                continue
            t = self._expr_type(val)
            if not can_assign(decl_type, t):
                self._error(it, f"Cannot assign {t} to {decl_type} in sacred '{getattr(it,'name','?')}'.")

    def _check_ordain_decl_init(self, decl: Any) -> None:
        for it in getattr(decl, "items", []) or []:
            init = getattr(it, "init", None)
            if init is None:
                continue
            _ = self._expr_type(init)