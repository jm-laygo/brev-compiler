from __future__ import annotations

from backend.ast.ast_nodes import IndexRef, MemberRef, NameRef
from backend.interpreter.environment import Environment
from backend.errors import (
    IndexOutOfBoundsRuntimeError,
    InvalidMemberAccessRuntimeError,
    RuntimeErrorBase,
    RuntimeTypeError,
)

def _read_lvalue(self, reference_node, current_environment: Environment):
    if isinstance(reference_node, NameRef):
        return current_environment.get(reference_node.name, node=reference_node)

    if isinstance(reference_node, IndexRef):
        base_value = self._read_lvalue(reference_node.base, current_environment)
        index_value = self._eval_expr(reference_node.index, current_environment)

        if not isinstance(index_value, int):
            raise RuntimeTypeError(reference_node, "Array index must be a tally value.")

        try:
            return base_value[index_value]
        except IndexError:
            raise IndexOutOfBoundsRuntimeError(
                reference_node,
                f"Index {index_value} is out of bounds.",
            )
        except TypeError:
            raise RuntimeTypeError(
                reference_node,
                "Indexed access requires an array-like value.",
            )

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

def _assign_lvalue(self, reference_node, assigned_value, current_environment: Environment, node=None):
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

def _resolve_index_target(self, index_reference: IndexRef, current_environment: Environment):
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

def _read_lvalue_from_value(self, access_reference, base_value, node=None):
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

def bind_reference_methods(cls):
    cls._read_lvalue = _read_lvalue
    cls._assign_lvalue = _assign_lvalue
    cls._resolve_index_target = _resolve_index_target
    cls._read_lvalue_from_value = _read_lvalue_from_value