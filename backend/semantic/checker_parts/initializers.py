from __future__ import annotations
from typing import Any, Optional, List
from backend.semantic.typesys import Type, BaseType, can_assign
from .helpers import _class

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
                continue

            if len(dims) > 0 and _class(init) == "ArrayInit":
                sizes = self._dims_to_sizes(dims, owner_node=it)
                if sizes is not None:
                    self._check_array_init_shape(init, sizes, level=0, owner=it)

    def _dims_to_sizes(self, dims: List[Any], owner_node: Any) -> Optional[List[int]]:
        out: List[int] = []
        for d in dims:
            if _class(d) != "LiteralExpr" or (getattr(d, "literal_type", "") or "").lower() != "int":
                self._error(owner_node, "Array dimensions must be constant integer literals.")
                return None
            try:
                v = int(getattr(d, "value"))
            except Exception:
                self._error(owner_node, "Array dimensions must be valid integer literals.")
                return None
            if v <= 0:
                self._error(owner_node, f"Array dimension must be > 0, got {v}.")
                return None
            out.append(v)
        return out

    def _check_array_init_shape(self, init: Any, sizes: List[int], level: int, owner: Any) -> None:
        items = getattr(init, "items", []) or []
        expected = sizes[level]

        if len(items) != expected:
            self._error(
                init,
                f"Array initializer size mismatch at dimension {level+1}: expected {expected} element(s), got {len(items)}."
            )
        last_level = (level == len(sizes) - 1)

        if last_level:
            for x in items:
                if _class(x) == "ArrayInit":
                    self._error(x, f"Too many nested braces: array is {len(sizes)}D but initializer nests deeper.")
            return

        for idx, x in enumerate(items):
            if _class(x) != "ArrayInit":
                self._error(x, f"Missing nested braces at dimension {level+1}: element {idx+1} must be a brace group.")
                continue
            self._check_array_init_shape(x, sizes, level + 1, owner)

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