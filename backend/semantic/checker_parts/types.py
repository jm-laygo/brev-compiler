from __future__ import annotations
from typing import Any
from backend.semantic.typesys import BaseType, Type

class TypeBuildersMixin:
    def _type_from_return_type(self, rt: Any) -> Type:
        if rt is None:
            return Type.unknown()
        if isinstance(rt, str):
            t = Type.base_t(rt)
            if t.base == BaseType.UNKNOWN and rt:
                return Type.order(rt)
            return t
        s = str(rt)
        t = Type.base_t(s)
        if t.base == BaseType.UNKNOWN and s:
            return Type.order(s)
        return t

    def _type_from_decl(self, node: Any) -> Type:
        tname = getattr(node, "type_name", None)
        base = Type.base_t(tname) if isinstance(tname, str) else Type.base_t(str(tname))

        if base.base == BaseType.UNKNOWN and isinstance(tname, str) and tname:
            base = Type.order(tname)

        dims_list = getattr(node, "dims", None)
        if isinstance(dims_list, list):
            dims = len(dims_list)
        else:
            dims = int(getattr(node, "array_dims", 0) or 0)

        if dims > 0:
            return Type.array(base, dims)
        return base