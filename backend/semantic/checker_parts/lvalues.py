from __future__ import annotations
from typing import Any
from backend.semantic.typesys import (
    BaseType,
    Type,
    is_numeric,
)
from .helpers import _class

class LValuesMixin:
    def _lvalue_root_symbol(self, lv: Any):
        if lv is None:
            return None

        k = _class(lv)

        if k == "NameRef":
            name = getattr(lv, "name", None)
            return self.scope.resolve(name) if name else None

        if k == "IndexRef":
            base = getattr(lv, "base", None)
            return self._lvalue_root_symbol(base)

        if k == "MemberRef":
            base = getattr(lv, "base", None)
            return self._lvalue_root_symbol(base)

        return None

    def _lvalue_type(self, lv: Any) -> Type:
        if lv is None:
            return Type.unknown()

        k = _class(lv)

        if k == "NameRef":
            name = getattr(lv, "name", None)
            sym = self.scope.resolve(name) if name else None
            from backend.semantic.symbols import VarSymbol

            if isinstance(sym, VarSymbol):
                return sym.typ

            hint = self._did_you_mean(name)
            self._error(lv, f"Undeclared identifier '{name}'.{hint}")
            return Type.error()

        if k == "IndexRef":
            base = getattr(lv, "base", None)
            idx = getattr(lv, "index", None)

            bt = self._lvalue_type(base)
            it = self._expr_type(idx)

            if self._has_type_error(bt) or self._has_type_error(it):
                return Type.error()

            if not is_numeric(it):
                self._error(
                    idx if idx is not None else lv,
                    f"Type error: array index must be numeric, got {self._tname(it)}.",
                )

            # scripture indexing rule
            if bt.is_base(BaseType.SCRIPTURE):
                return Type.base_t(BaseType.SIGIL)

            if not bt.is_array():
                self._error(lv, f"Cannot index non-array type {self._tname(bt)}.")
                return Type.error()

            return bt.array_of or Type.error()

        if k == "MemberRef":
            base = getattr(lv, "base", None)
            mem = getattr(lv, "member", None)

            bt = self._lvalue_type(base)
            if self._has_type_error(bt):
                return Type.error()

            if not bt.is_order():
                self._error(lv, f"Member access '.{mem}' on non-order type {self._tname(bt)}.")
                return Type.error()

            order = self.orders.get(bt.order_name or "")
            if order is None:
                self._error(lv, f"Unknown order type '{bt.order_name}'.")
                return Type.error()

            ms = order.members.get(mem)
            if ms is None:
                hint = self._did_you_mean_from(mem, list(order.members.keys()))
                self._error(lv, f"Order '{order.name}' has no member '{mem}'.{hint}")
                return Type.error()

            return ms.typ

        return self._expr_type(lv)