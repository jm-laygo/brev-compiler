from __future__ import annotations

from backend.errors import RuntimeNameError, ConstAssignmentRuntimeError

_UNSET = object()

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}
        self.constants = set()

    def declare(self, name, value=None, *, is_const=False):
        if name in self.values:
            raise RuntimeNameError(None, f"Runtime redeclaration of '{name}'.")
        self.values[name] = value
        if is_const:
            self.constants.add(name)

    def contains_local(self, name: str) -> bool:
        return name in self.values

    def assign(self, name, value, *, node=None):
        if name in self.values:
            if name in self.constants:
                raise ConstAssignmentRuntimeError(node, f"Cannot modify sacred constant '{name}'.")
            self.values[name] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value, node=node)
            return
        raise RuntimeNameError(node, f"Undefined variable '{name}'.")

    def get(self, name, *, node=None):
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name, node=node)
        raise RuntimeNameError(node, f"Undefined variable '{name}'.")

    def is_const(self, name: str) -> bool:
        if name in self.values:
            return name in self.constants
        if self.parent is not None:
            return self.parent.is_const(name)
        return False