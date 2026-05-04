from __future__ import annotations

from backend.ast.ast_nodes import IndexReference, MemberReference, NameReference
from backend.errors import (
    IndexOutOfBoundsRuntimeError,
    InvalidMemberAccessRuntimeError,
    RuntimeErrorBase,
    RuntimeTypeError,
)


def readLeftHandValue(self, referenceNode, currentEnvironment):
    if isinstance(referenceNode, NameReference):
        return currentEnvironment.get(
            referenceNode.name,
            node=referenceNode
        )

    if isinstance(referenceNode, IndexReference):
        baseValue = self.readLeftHandValue(
            referenceNode.baseReference,
            currentEnvironment
        )

        indexValue = self.evaluateExpression(
            referenceNode.indexExpression,
            currentEnvironment
        )

        if not isinstance(indexValue, int):
            raise RuntimeTypeError(
                referenceNode,
                "Array index must be a tally value."
            )

        try:
            return baseValue[indexValue]

        except IndexError:
            raise IndexOutOfBoundsRuntimeError(
                referenceNode,
                f"Index {indexValue} is out of bounds."
            )

        except TypeError:
            raise RuntimeTypeError(
                referenceNode,
                "Indexed access requires an array-like value."
            )

    if isinstance(referenceNode, MemberReference):
        baseValue = self.readLeftHandValue(
            referenceNode.baseReference,
            currentEnvironment
        )

        if not isinstance(baseValue, dict):
            raise InvalidMemberAccessRuntimeError(
                referenceNode,
                "Member access requires an order instance."
            )

        if referenceNode.memberName not in baseValue:
            raise InvalidMemberAccessRuntimeError(
                referenceNode,
                f"Unknown member '{referenceNode.memberName}'."
            )

        return baseValue[referenceNode.memberName]

    raise RuntimeErrorBase(
        referenceNode,
        "This reference is not yet supported during execution."
    )

def readLeftHandValueFromValue(self, accessReference, baseValue, node=None):
    from backend.interpreter.environment import Environment

    temporaryEnvironment = Environment()
    temporaryEnvironment.declare("__temp__", baseValue)

    if isinstance(accessReference, NameReference):
        if accessReference.name == "__temp__":
            return baseValue

        raise RuntimeErrorBase(
            node or accessReference,
            "Direct name access on a call result is invalid."
        )

    syntheticReference = accessReference

    if isinstance(accessReference, MemberReference):
        syntheticReference = MemberReference(
            baseReference=NameReference(
                name="__temp__",
                position=getattr(accessReference, "position", None)
            ),
            memberName=accessReference.memberName,
            position=getattr(accessReference, "position", None)
        )

    elif isinstance(accessReference, IndexReference):
        syntheticReference = IndexReference(
            baseReference=NameReference(
                name="__temp__",
                position=getattr(accessReference, "position", None)
            ),
            indexExpression=accessReference.indexExpression,
            position=getattr(accessReference, "position", None)
        )

    return self.readLeftHandValue(
        syntheticReference,
        temporaryEnvironment
    )