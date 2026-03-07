from __future__ import annotations
from typing import Any

from backend.semantic.typesys import (
    BaseType,
    Type,
    is_numeric,
)
from .helpers import _class


class LValuesMixin:
    def _lvalue_root_symbol(self, lvalue_node: Any):
        if lvalue_node is None:
            return None

        lvalue_kind = _class(lvalue_node)

        if lvalue_kind == "NameRef":
            identifier_name = getattr(lvalue_node, "name", None)
            return self.scope.resolve(identifier_name) if identifier_name else None

        if lvalue_kind == "IndexRef":
            base_reference = getattr(lvalue_node, "base", None)
            return self._lvalue_root_symbol(base_reference)

        if lvalue_kind == "MemberRef":
            base_reference = getattr(lvalue_node, "base", None)
            return self._lvalue_root_symbol(base_reference)

        return None

    def _lvalue_type(self, lvalue_node: Any) -> Type:
        if lvalue_node is None:
            return Type.unknown()

        lvalue_kind = _class(lvalue_node)

        if lvalue_kind == "NameRef":
            identifier_name = getattr(lvalue_node, "name", None)
            resolved_symbol = self.scope.resolve(identifier_name) if identifier_name else None

            from backend.semantic.symbols import VarSymbol

            if isinstance(resolved_symbol, VarSymbol):
                return resolved_symbol.typ

            suggestion_text = self._did_you_mean(identifier_name)
            self._error(lvalue_node, f"Undeclared identifier '{identifier_name}'.{suggestion_text}")
            return Type.error()

        if lvalue_kind == "IndexRef":
            base_reference = getattr(lvalue_node, "base", None)
            index_expression = getattr(lvalue_node, "index", None)

            base_type = self._lvalue_type(base_reference)
            index_type = self._expr_type(index_expression)

            if self._has_type_error(base_type) or self._has_type_error(index_type):
                return Type.error()

            if not is_numeric(index_type):
                self._error(
                    index_expression if index_expression is not None else lvalue_node,
                    f"Type error: array index must be numeric, got {self._tname(index_type)}.",
                )

            # scripture indexing rule
            if base_type.is_base(BaseType.SCRIPTURE):
                return Type.base_t(BaseType.SIGIL)

            if not base_type.is_array():
                self._error(lvalue_node, f"Cannot index non-array type {self._tname(base_type)}.")
                return Type.error()

            return base_type.array_of or Type.error()

        if lvalue_kind == "MemberRef":
            base_reference = getattr(lvalue_node, "base", None)
            member_name = getattr(lvalue_node, "member", None)

            base_type = self._lvalue_type(base_reference)
            if self._has_type_error(base_type):
                return Type.error()

            if not base_type.is_order():
                self._error(lvalue_node, f"Member access '.{member_name}' on non-order type {self._tname(base_type)}.")
                return Type.error()

            order_symbol = self.orders.get(base_type.order_name or "")
            if order_symbol is None:
                self._error(lvalue_node, f"Unknown order type '{base_type.order_name}'.")
                return Type.error()

            member_symbol = order_symbol.members.get(member_name)
            if member_symbol is None:
                suggestion_text = self._did_you_mean_from(member_name, list(order_symbol.members.keys()))
                self._error(lvalue_node, f"Order '{order_symbol.name}' has no member '{member_name}'.{suggestion_text}")
                return Type.error()

            return member_symbol.typ

        return self._expr_type(lvalue_node)