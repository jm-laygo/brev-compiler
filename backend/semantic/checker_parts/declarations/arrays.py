from __future__ import annotations
from typing import Any, Optional

from ..helpers import _class


class DeclarationArrayMixin:
    def _const_int(self, expression_node: Any) -> Optional[int]:
        if expression_node is None:
            return None

        if _class(expression_node) == "LiteralExpr":
            literal_type = (getattr(expression_node, "literal_type", "") or "").lower()
            if literal_type == "int":
                try:
                    return int(getattr(expression_node, "value"))
                except Exception:
                    return None

        return None

    def _extract_array_sizes(self, dimension_nodes: list[Any], owner_node: Any) -> Optional[list[int]]:
        array_sizes: list[int] = []

        for dimension_node in dimension_nodes:
            constant_size = self._const_int(dimension_node)

            if constant_size is None:
                self._error(owner_node, "Array size must be a constant integer literal (tally).")
                return None

            if constant_size <= 0:
                self._error(owner_node, f"Array size must be > 0, got {constant_size}.")
                return None

            array_sizes.append(constant_size)

        return array_sizes