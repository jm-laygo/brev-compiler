from __future__ import annotations
from typing import Any, Optional, List

from backend.semantic.typesys import Type, BaseType, can_assign
from .helpers import _class


class InitializersMixin:
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

    def _check_ordain_decl_init(self, declaration_node: Any) -> None:
        declared_items = getattr(declaration_node, "items", []) or []

        for declared_item in declared_items:
            initializer_value = getattr(declared_item, "init", None)

            if initializer_value is None:
                continue

            self._expr_type(initializer_value)

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

    def _dims_to_sizes(self, dimension_nodes: List[Any], owner_node: Any) -> Optional[List[int]]:
        dimension_sizes: List[int] = []

        for dimension_node in dimension_nodes:
            if _class(dimension_node) != "LiteralExpr" or (getattr(dimension_node, "literal_type", "") or "").lower() != "int":
                self._error(owner_node, "Array dimensions must be constant integer literals.")
                return None

            try:
                dimension_value = int(getattr(dimension_node, "value"))
            except Exception:
                self._error(owner_node, "Array dimensions must be valid integer literals.")
                return None

            if dimension_value <= 0:
                self._error(owner_node, f"Array dimension must be > 0, got {dimension_value}.")
                return None

            dimension_sizes.append(dimension_value)

        return dimension_sizes

    def _check_array_init_shape(self, initializer_node: Any, dimension_sizes: List[int], level: int, owner_node: Any) -> None:
        initializer_items = getattr(initializer_node, "items", []) or []
        expected_count = dimension_sizes[level]

        if len(initializer_items) > expected_count:
            self._error(
                initializer_node,
                f"Too many initializer elements at dimension {level + 1}: max {expected_count}, got {len(initializer_items)}."
            )

        is_last_dimension = (level == len(dimension_sizes) - 1)

        if is_last_dimension:
            for initializer_item in initializer_items[:expected_count]:
                if _class(initializer_item) == "ArrayInit":
                    self._error(
                        initializer_item,
                        f"Too many nested braces: array is {len(dimension_sizes)}D but initializer nests deeper."
                    )
            return

        for item_index, initializer_item in enumerate(initializer_items[:expected_count]):
            if _class(initializer_item) != "ArrayInit":
                self._error(
                    initializer_item,
                    f"Missing nested braces at dimension {level + 1}: element {item_index + 1} must be a brace group."
                )
                continue

            self._check_array_init_shape(initializer_item, dimension_sizes, level + 1, owner_node)

    def _check_array_init_types(
        self,
        initializer_node: Any,
        target_type: Type,
        level: int,
        sizes: List[int],
        owner_node: Any
    ) -> None:
        initializer_items = getattr(initializer_node, "items", []) or []
        expected_count = sizes[level]

        if not initializer_items:
            return

        is_last_dimension = (level == len(sizes) - 1)

        if is_last_dimension:
            element_type = target_type
            while element_type.array_of is not None:
                element_type = element_type.array_of

            for initializer_item in initializer_items[:expected_count]:
                if _class(initializer_item) == "ArrayInit":
                    self._error(initializer_item, "Unexpected nested brace at last dimension.")
                    continue

                initializer_item_type = self._expr_type(initializer_item)
                if not can_assign(element_type, initializer_item_type):
                    self._error(
                        initializer_item,
                        f"Cannot assign {initializer_item_type} to {element_type} in array initializer."
                    )
            return

        child_target_type = target_type.array_of if target_type.array_of is not None else target_type

        for initializer_item in initializer_items[:expected_count]:
            if _class(initializer_item) != "ArrayInit":
                continue

            self._check_array_init_types(
                initializer_item,
                child_target_type,
                level + 1,
                sizes,
                owner_node
            )