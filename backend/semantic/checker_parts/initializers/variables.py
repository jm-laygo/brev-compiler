from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type, can_assign

from ..helpers import _class

class VariableInitializerMixin:
    def _check_var_decl_init(self, declaration_node: Any) -> None:
        declared_type_name = getattr(declaration_node, "type_name", "")
        declared_type = Type.base_t(declared_type_name)

        if declared_type.base == BaseType.UNKNOWN and isinstance(getattr(declaration_node, "type_name", None), str):
            declared_type = Type.order(getattr(declaration_node, "type_name"))

        declared_items = getattr(declaration_node, "items", []) or []

        for declared_item in declared_items:
            initializer_value = getattr(declared_item, "init", None)

            if initializer_value is None:
                continue

            dimension_nodes = getattr(declared_item, "dims", []) or []
            target_type = Type.array(declared_type, len(dimension_nodes)) if len(dimension_nodes) > 0 else declared_type

            if len(dimension_nodes) > 0 and _class(initializer_value) == "ArrayInit":
                dimension_sizes = self._dims_to_sizes(dimension_nodes, owner_node=declared_item)
                if dimension_sizes is None:
                    continue

                self._check_array_init_shape(initializer_value, dimension_sizes, level=0, owner_node=declared_item)
                self._check_array_init_types(initializer_value, target_type, level=0, sizes=dimension_sizes, owner_node=declared_item)
                continue

            initializer_type = self._expr_type(initializer_value)

            if not can_assign(target_type, initializer_type):
                self._error(
                    declared_item,
                    f"Cannot assign {initializer_type} to {target_type} in '{getattr(declared_item, 'name', '?')}'."
                )