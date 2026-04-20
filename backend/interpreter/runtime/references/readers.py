from __future__ import annotations

from backend.ast.ast_nodes import IndexRef, MemberRef, NameRef
from backend.errors import (
    IndexOutOfBoundsRuntimeError,
    InvalidMemberAccessRuntimeError,
    RuntimeErrorBase,
    RuntimeTypeError,
)

def _read_lvalue(self, reference_node, current_environment):
    if isinstance(reference_node, NameRef):
        return current_environment.get(reference_node.name, node=reference_node)

    if isinstance(reference_node, IndexRef):
        base_value = self._read_lvalue(reference_node.base, current_environment)
        index_value = self._eval_expr(reference_node.index, current_environment)

        if not isinstance(index_value, int) or isinstance(index_value, bool):
            raise RuntimeTypeError(reference_node, "Array index must be a tally value.")

        if not isinstance(base_value, list):
            raise RuntimeTypeError(
                reference_node,
                "Indexed access requires an array value.",
            )

        if index_value < 0 or index_value >= len(base_value):
            raise IndexOutOfBoundsRuntimeError(
                reference_node,
                f"Index {index_value} is out of bounds.",
            )

        return base_value[index_value]

    if isinstance(reference_node, MemberRef):
        base_value = self._read_lvalue(reference_node.base, current_environment)

        if not isinstance(base_value, dict):
            raise InvalidMemberAccessRuntimeError(
                reference_node,
                "Member access requires an order instance.",
            )

        if reference_node.member not in base_value:
            raise InvalidMemberAccessRuntimeError(
                reference_node,
                f"Unknown member '{reference_node.member}'.",
            )

        return base_value[reference_node.member]

    raise RuntimeErrorBase(
        reference_node,
        "This reference is not yet supported during execution.",
    )

def _read_lvalue_from_value(self, access_reference, base_value, node=None):
    from backend.interpreter.environment import Environment

    temporary_environment = Environment()
    temporary_environment.declare("__temp__", base_value)

    if isinstance(access_reference, NameRef):
        if access_reference.name == "__temp__":
            return base_value
        raise RuntimeErrorBase(
            node or access_reference,
            "Direct name access on a call result is invalid.",
        )

    synthetic_reference = access_reference

    if isinstance(access_reference, MemberRef):
        synthetic_reference = MemberRef(
            base=NameRef(name="__temp__", pos=getattr(access_reference, "pos", None)),
            member=access_reference.member,
            pos=getattr(access_reference, "pos", None),
        )

    elif isinstance(access_reference, IndexRef):
        synthetic_reference = IndexRef(
            base=NameRef(name="__temp__", pos=getattr(access_reference, "pos", None)),
            index=access_reference.index,
            pos=getattr(access_reference, "pos", None),
        )

    return self._read_lvalue(synthetic_reference, temporary_environment)
