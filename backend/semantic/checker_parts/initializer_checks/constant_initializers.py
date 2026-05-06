from __future__ import annotations
from typing import Any

from backend.semantic.typesys import BaseType, Type, canAssign


class SacredInitializerMixin:
    def checkSacredDeclarationInitialValues(self, declarationNode: Any) -> None:
        declaredTypeName = getattr(declarationNode, "typeName", "")
        declaredType = Type.fromBaseType(declaredTypeName)

        if (
            declaredType.baseType == BaseType.UNKNOWN
            and isinstance(getattr(declarationNode, "typeName", None), str)
        ):
            declaredType = Type.fromOrder(getattr(declarationNode, "typeName"))

        declaredItems = getattr(declarationNode, "items", []) or []

        for declaredItem in declaredItems:
            initialValue = getattr(declaredItem, "value", None)

            if initialValue is None:
                self.addError(
                    declaredItem,
                    f"Sacred '{getattr(declaredItem, 'name', '?')}' must be initialized."
                )

                continue

            initialValueType = self.getExpressionType(initialValue)

            if not canAssign(declaredType, initialValueType):
                self.addError(
                    declaredItem,
                    f"Cannot assign {initialValueType} to {declaredType} in sacred '{getattr(declaredItem, 'name', '?')}'."
                )
            else:
                # If the sacred was defined with a literal initializer, store
                # its constant value on the symbol so other checks (like
                # array-size extraction) can read it.
                try:
                    symbolName = getattr(declaredItem, "name", None)

                    if symbolName:
                        symbol = self.currentScope.resolveLocal(symbolName) or self.currentScope.resolve(symbolName)

                        if symbol is not None and hasattr(symbol, "constantValue"):
                            # Only set simple literal values here. More complex
                            # constant evaluation can be added later if needed.
                            if getattr(initialValue, "literalType", None) is not None:
                                literalVal = getattr(initialValue, "value", None)
                                symbol.constantValue = literalVal
                except Exception:
                    # Be defensive: don't crash the checker on unexpected shapes
                    pass