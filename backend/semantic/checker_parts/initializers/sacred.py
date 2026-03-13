from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type, can_assign

class SacredInitializerMixin:
    def _check_sacred_decl_init(self, declaration_node: Any) -> None:
        declared_type_name = getattr(declaration_node, "type_name", "")
        declared_type = Type.base_t(declared_type_name)

        if declared_type.base == BaseType.UNKNOWN and isinstance(getattr(declaration_node, "type_name", None), str):
            declared_type = Type.order(getattr(declaration_node, "type_name"))

        declared_items = getattr(declaration_node, "items", []) or []

        for declared_item in declared_items:
            initializer_value = getattr(declared_item, "value", None)

            if initializer_value is None:
                self._error(
                    declared_item,
                    f"Sacred '{getattr(declared_item, 'name', '?')}' must be initialized."
                )
                continue

            initializer_type = self._expr_type(initializer_value)

            if not can_assign(declared_type, initializer_type):
                self._error(
                    declared_item,
                    f"Cannot assign {initializer_type} to {declared_type} in sacred '{getattr(declared_item, 'name', '?')}'."
                )