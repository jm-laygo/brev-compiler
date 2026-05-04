from __future__ import annotations
from typing import Any

from backend.semantic.symbols import VariableSymbol
from backend.semantic.typesys import BaseType, Type

from ..helpers import getClassName, getNodePosition


class VariableDeclarationsMixin:
    def declareVariableDeclaration(
        self,
        declarationNode: Any,
        isGlobal: bool,
        forceConstant: bool = False
    ) -> None:
        declaredTypeName = getattr(declarationNode, "typeName", "")
        declaredType = Type.fromBaseType(declaredTypeName)

        if (
            declaredType.baseType == BaseType.UNKNOWN
            and isinstance(getattr(declarationNode, "typeName", None), str)
        ):
            declaredType = Type.fromOrder(getattr(declarationNode, "typeName"))

        isConstant = forceConstant or getClassName(declarationNode) == "SacredDeclaration"
        declaredItems = getattr(declarationNode, "items", []) or []

        for declaredItem in declaredItems:
            variableName = getattr(declaredItem, "name", None)

            if not variableName:
                self.addError(
                    declaredItem,
                    "Variable item missing name."
                )

                continue

            dimensionNodes = getattr(declaredItem, "dimensions", []) or []

            if len(dimensionNodes) > 0:
                arraySizes = self.extractArraySizes(dimensionNodes, declaredItem)
                variableType = Type.fromArray(declaredType, len(dimensionNodes))
            else:
                arraySizes = None
                variableType = declaredType

            if self.currentScope.resolveLocal(variableName):
                self.addError(
                    declaredItem,
                    f"Redeclaration of '{variableName}' in the same scope."
                )

                continue

            self.currentScope.define(
                VariableSymbol(
                    name=variableName,
                    symbolType=variableType,
                    position=getNodePosition(declaredItem),
                    isConstant=isConstant,
                    arraySizes=arraySizes
                )
            )
            # If this is a sacred constant with an initializer, try to store
            # its literal value on the symbol so later declarations (like
            # arrays) can use it when extracting sizes.
            if isConstant:
                try:
                    # declaredItem may use 'value' (SacredItem) or
                    # 'initialValue' (VariableItem/OrdainItem).
                    initExpr = getattr(declaredItem, "value", None) or getattr(declaredItem, "initialValue", None)

                    # Prefer integer constant extraction when available.
                    if initExpr is not None and hasattr(self, "getConstantIntegerValue"):
                        constInt = self.getConstantIntegerValue(initExpr)
                        if constInt is not None:
                            sym = self.currentScope.resolveLocal(variableName) or self.currentScope.resolve(variableName)
                            if sym is not None and hasattr(sym, "constantValue"):
                                sym.constantValue = constInt
                    else:
                        # Fallback: if initializer is a literal expression, store its raw value.
                        if initExpr is not None and getattr(initExpr, "literalType", None) is not None:
                            sym = self.currentScope.resolveLocal(variableName) or self.currentScope.resolve(variableName)
                            if sym is not None and hasattr(sym, "constantValue"):
                                sym.constantValue = getattr(initExpr, "value", None)
                except Exception:
                    pass

    def declareOrdainDeclaration(self, declarationNode: Any, isGlobal: bool) -> None:
        orderName = getattr(declarationNode, "name", None)

        if not orderName:
            self.addError(
                declarationNode,
                "ordain declaration missing order name."
            )

            return

        if orderName not in self.orders:
            self.addError(
                declarationNode,
                f"Unknown order type '{orderName}'."
            )

        orderType = Type.fromOrder(orderName)
        declaredItems = getattr(declarationNode, "items", []) or []

        for declaredItem in declaredItems:
            variableName = getattr(declaredItem, "name", None)

            if not variableName:
                self.addError(
                    declaredItem,
                    "ordain item missing name."
                )

                continue

            dimensionNodes = getattr(declaredItem, "dimensions", []) or []

            if len(dimensionNodes) > 0:
                arraySizes = self.extractArraySizes(dimensionNodes, declaredItem)
                variableType = Type.fromArray(orderType, len(dimensionNodes))
            else:
                arraySizes = None
                variableType = orderType

            if self.currentScope.resolveLocal(variableName):
                self.addError(
                    declaredItem,
                    f"Redeclaration of '{variableName}' in the same scope."
                )

                continue

            self.currentScope.define(
                VariableSymbol(
                    name=variableName,
                    symbolType=variableType,
                    position=getNodePosition(declaredItem),
                    isConstant=False,
                    arraySizes=arraySizes
                )
            )