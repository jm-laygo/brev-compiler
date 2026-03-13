from __future__ import annotations
from typing import Any


class OrdainInitializerMixin:
    def _check_ordain_decl_init(self, declaration_node: Any) -> None:
        declared_items = getattr(declaration_node, "items", []) or []

        for declared_item in declared_items:
            initializer_value = getattr(declared_item, "init", None)

            if initializer_value is None:
                continue

            self._expr_type(initializer_value)