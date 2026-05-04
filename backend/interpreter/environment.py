from __future__ import annotations

from backend.errors import RuntimeNameError, ConstAssignmentRuntimeError


UNSET_VALUE = object()


class Environment:
    def __init__(self, parentEnvironment=None):
        self.parentEnvironment = parentEnvironment
        self.storedValues = {}
        self.constantNames = set()

    def declare(self, name, value=None, *, isConstant=False, node=None):
        if name in self.storedValues:
            raise RuntimeNameError(
                node,
                f"Runtime redeclaration of '{name}'."
            )

        self.storedValues[name] = value

        if isConstant:
            self.constantNames.add(name)

    def containsLocal(self, name: str) -> bool:
        return name in self.storedValues

    def assign(self, name, value, *, node=None):
        if name in self.storedValues:
            if name in self.constantNames:
                raise ConstAssignmentRuntimeError(
                    node,
                    f"Cannot modify sacred constant '{name}'."
                )

            self.storedValues[name] = value
            return

        if self.parentEnvironment is not None:
            self.parentEnvironment.assign(name, value, node=node)
            return

        raise RuntimeNameError(
            node,
            f"Undefined variable '{name}'."
        )

    def get(self, name, *, node=None):
        if name in self.storedValues:
            return self.storedValues[name]

        if self.parentEnvironment is not None:
            return self.parentEnvironment.get(name, node=node)

        raise RuntimeNameError(
            node,
            f"Undefined variable '{name}'."
        )

    def isConstant(self, name: str) -> bool:
        if name in self.storedValues:
            return name in self.constantNames

        if self.parentEnvironment is not None:
            return self.parentEnvironment.isConstant(name)

        return False