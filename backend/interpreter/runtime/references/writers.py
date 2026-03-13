from __future__ import annotations

from backend.ast.ast_nodes import IndexRef, MemberRef, NameRef
from backend.errors import (
    IndexOutOfBoundsRuntimeError,
    InvalidMemberAccessRuntimeError,
    RuntimeErrorBase,
    RuntimeTypeError,
)

def _assign_lvalue(self, reference_node, assigned_value, current_environment, node=None):
    if isinstance(reference_node, NameRef):
        current_environment.assign(
            reference_node.name,
            assigned_value,
            node=node or reference_node,
        )
        return

    if isinstance(reference_node, IndexRef):
        target_container, target_index = self._resolve_index_target(
            reference_node,
            current_environment,
        )
        target_container[target_index] = assigned_value
        return

    if isinstance(reference_node, MemberRef):
        base_object = self._read_lvalue(reference_node.base, current_environment)

        if not isinstance(base_object, dict):
            raise InvalidMemberAccessRuntimeError(
                reference_node,
                "Member assignment requires an order instance.",
            )

        if reference_node.member not in base_object:
            raise InvalidMemberAccessRuntimeError(
                reference_node,
                f"Unknown member '{reference_node.member}'.",
            )

        base_object[reference_node.member] = assigned_value
        return

    raise RuntimeErrorBase(
        reference_node,
        "This assignment target is not valid during execution.",
    )

def _resolve_index_target(self, index_reference, current_environment):
    target_container = self._read_lvalue(index_reference.base, current_environment)
    index_value = self._eval_expr(index_reference.index, current_environment)

    if not isinstance(index_value, int):
        raise RuntimeTypeError(index_reference, "Array index must be a tally value.")

    if not isinstance(target_container, list):
        raise RuntimeTypeError(index_reference, "Indexed assignment requires an array value.")

    if index_value < 0 or index_value >= len(target_container):
        raise IndexOutOfBoundsRuntimeError(
            index_reference,
            f"Index {index_value} is out of bounds.",
        )

    return target_container, index_value
