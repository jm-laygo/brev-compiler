from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any

# Symbols + Scopes
@dataclass
class Symbol:
    name: str
    sym_kind: str
    type_name: str | None = None
    meta: dict = field(default_factory=dict)

@dataclass
class VarSymbol(Symbol):
    is_const: bool = False
    dims: int = 0
    def __init__(self, name: str, type_name: str, *, is_const: bool = False, dims: int = 0, meta: dict | None = None):
        super().__init__(name=name, sym_kind="var", type_name=type_name, meta=meta or {})
        self.is_const = is_const
        self.dims = dims

@dataclass
class FuncSymbol(Symbol):
    return_type: str = "hollow"
    params: list[VarSymbol] = field(default_factory=list)

    def __init__(self, name: str, return_type: str, params: List[VarSymbol], meta: dict | None = None):
        super().__init__(name=name, sym_kind="func", type_name=None, meta=meta or {})
        self.return_type = return_type
        self.params = params

@dataclass
class TypeSymbol(Symbol):
    members: Dict[str, VarSymbol] = field(default_factory=dict)

    def __init__(self, name: str, members: Dict[str, VarSymbol] | None = None, meta: dict | None = None):
        super().__init__(name=name, sym_kind="type", type_name=name, meta=meta or {})
        self.members = members or {}


class Scope:
    def __init__(self, parent: Optional["Scope"] = None, name: str = "scope"):
        self.parent = parent
        self.name = name
        self.symbols: Dict[str, Symbol] = {}

    def define(self, sym: Symbol) -> None:
        self.symbols[sym.name] = sym

    def lookup_local(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    def resolve(self, name: str) -> Optional[Symbol]:
        s = self.symbols.get(name)
        if s is not None:
            return s
        if self.parent is not None:
            return self.parent.resolve(name)
        return None

    def __repr__(self) -> str:
        return f"<Scope {self.name} symbols={list(self.symbols.keys())}>"