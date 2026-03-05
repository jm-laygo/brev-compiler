from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional, List
from backend.semantic.typesys import Type

@dataclass
class Symbol:
    name: str
    typ: Type
    pos: Optional[object] = None

@dataclass
class VarSymbol(Symbol):
    array_sizes: Optional[List[int]] = None
    is_const: bool = False
@dataclass
class FuncSymbol(Symbol):
    return_type: Type = field(default_factory=Type.unknown)
    params: List[VarSymbol] = field(default_factory=list)

@dataclass
class MemberSymbol(Symbol):
    pass

@dataclass
class OrderSymbol(Symbol):
    members: Dict[str, MemberSymbol] = field(default_factory=dict)

class Scope:
    def __init__(self, parent: Optional["Scope"] = None):
        self.parent = parent
        self.table: Dict[str, Symbol] = {}

    def define(self, sym: Symbol) -> None:
        self.table[sym.name] = sym

    def resolve_local(self, name: str) -> Optional[Symbol]:
        return self.table.get(name)

    def resolve(self, name: str) -> Optional[Symbol]:
        s = self.resolve_local(name)
        if s is not None:
            return s
        if self.parent is not None:
            return self.parent.resolve(name)
        return None