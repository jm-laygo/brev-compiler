from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

from backend.semantic.typesys import Type


@dataclass
class Symbol:
    name: str
    symbolType: Type
    position: Optional[object] = None


@dataclass
class VariableSymbol(Symbol):
    arraySizes: Optional[List[int]] = None
    isConstant: bool = False
    constantValue: Any = None


@dataclass
class FunctionSymbol(Symbol):
    returnType: Type = field(default_factory=Type.unknown)
    parameters: List[VariableSymbol] = field(default_factory=list)


@dataclass
class MemberSymbol(Symbol):
    pass


@dataclass
class OrderSymbol(Symbol):
    members: Dict[str, MemberSymbol] = field(default_factory=dict)


class Scope:
    def __init__(self, parentScope: Optional["Scope"] = None):
        self.parentScope = parentScope
        self.symbolTable: Dict[str, Symbol] = {}

    def define(self, symbol: Symbol) -> None:
        self.symbolTable[symbol.name] = symbol

    def resolveLocal(self, name: str) -> Optional[Symbol]:
        return self.symbolTable.get(name)

    def resolve(self, name: str) -> Optional[Symbol]:
        resolvedSymbol = self.resolveLocal(name)

        if resolvedSymbol is not None:
            return resolvedSymbol

        if self.parentScope is not None:
            return self.parentScope.resolve(name)

        return None