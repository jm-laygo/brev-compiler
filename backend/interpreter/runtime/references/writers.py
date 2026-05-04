from __future__ import annotations

from backend.ast.ast_nodes import IndexReference, MemberReference, NameReference
from backend.errors import (
    IndexOutOfBoundsRuntimeError,
    InvalidMemberAccessRuntimeError,
    RuntimeErrorBase,
    RuntimeTypeError,
)


def assignLeftHandValue(self, referenceNode, assignedValue, currentEnvironment, node=None):
    if isinstance(referenceNode, NameReference):
        currentEnvironment.assign(
            referenceNode.name,
            assignedValue,
            node=node or referenceNode
        )

        return

    if isinstance(referenceNode, IndexReference):
        targetContainer, targetIndex = self.resolveIndexTarget(
            referenceNode,
            currentEnvironment
        )

        targetContainer[targetIndex] = assignedValue
        return

    if isinstance(referenceNode, MemberReference):
        baseObject = self.readLeftHandValue(
            referenceNode.baseReference,
            currentEnvironment
        )

        if not isinstance(baseObject, dict):
            raise InvalidMemberAccessRuntimeError(
                referenceNode,
                "Member assignment requires an order instance."
            )

        if referenceNode.memberName not in baseObject:
            raise InvalidMemberAccessRuntimeError(
                referenceNode,
                f"Unknown member '{referenceNode.memberName}'."
            )

        baseObject[referenceNode.memberName] = assignedValue
        return

    raise RuntimeErrorBase(
        referenceNode,
        "This assignment target is not valid during execution."
    )

def resolveIndexTarget(self, indexReference, currentEnvironment):
    targetContainer = self.readLeftHandValue(
        indexReference.baseReference,
        currentEnvironment
    )

    indexValue = self.evaluateExpression(
        indexReference.indexExpression,
        currentEnvironment
    )

    if not isinstance(indexValue, int):
        raise RuntimeTypeError(
            indexReference,
            "Array index must be a tally value."
        )

    if not isinstance(targetContainer, list):
        raise RuntimeTypeError(
            indexReference,
            "Indexed assignment requires an array value."
        )

    if indexValue < 0 or indexValue >= len(targetContainer):
        raise IndexOutOfBoundsRuntimeError(
            indexReference,
            f"Index {indexValue} is out of bounds."
        )

    return targetContainer, indexValue