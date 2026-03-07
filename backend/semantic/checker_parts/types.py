from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type

class TypeBuildersMixin:
    def _type_from_return_type(self, return_type_value: Any) -> Type:
        if return_type_value is None:
            return Type.unknown()

        if isinstance(return_type_value, str):
            type_name = return_type_value
        else:
            type_name = str(return_type_value)

        resolved_type = Type.base_t(type_name)

        if resolved_type.base == BaseType.UNKNOWN and type_name:
            return Type.order(type_name)

        return resolved_type

    def _type_from_decl(self, declaration_node: Any) -> Type:
        declared_type_name = getattr(declaration_node, "type_name", None)

        if isinstance(declared_type_name, str):
            base_type = Type.base_t(declared_type_name)
        else:
            base_type = Type.base_t(str(declared_type_name))

        if base_type.base == BaseType.UNKNOWN and isinstance(declared_type_name, str) and declared_type_name:
            base_type = Type.order(declared_type_name)

        dimension_nodes = getattr(declaration_node, "dims", None)

        if isinstance(dimension_nodes, list):
            dimension_count = len(dimension_nodes)
        else:
            dimension_count = int(getattr(declaration_node, "array_dims", 0) or 0)

        if dimension_count > 0:
            return Type.array(base_type, dimension_count)

        return base_type