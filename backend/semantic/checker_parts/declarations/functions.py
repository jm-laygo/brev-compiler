from __future__ import annotations
from typing import Any, List

from backend.semantic.symbols import FunctionSymbol, VariableSymbol
from backend.semantic.typesys import Type

from ..helpers import getClassName, getNodePosition


class FunctionDeclarationsMixin:
    def declareFunctions(self, programNode: Any) -> None:
        functionDeclarations: List[Any] = []

        entryRite = getattr(programNode, "entryRite", None)

        if entryRite is not None:
            functionDeclarations.extend([entryRite])

        functionDeclarations.extend(getattr(programNode, "riteDeclarations", []) or [])

        for functionDeclaration in functionDeclarations:
            if functionDeclaration is None or getClassName(functionDeclaration) != "RiteDeclaration":
                continue

            functionName = getattr(functionDeclaration, "name", None)

            if not functionName:
                self.addError(
                    functionDeclaration,
                    "Function missing name."
                )

                continue

            if functionName in self.functions:
                self.addError(
                    functionDeclaration,
                    f"Function '{functionName}' already declared."
                )

                continue

            returnType = self.getTypeFromReturnType(
                getattr(functionDeclaration, "returnType", None)
            )

            functionSymbol = FunctionSymbol(
                name=functionName,
                symbolType=Type.unknown(),
                returnType=returnType,
                position=getNodePosition(functionDeclaration)
            )

            parameterSymbols: List[VariableSymbol] = []
            parameterDeclarations = getattr(functionDeclaration, "parameters", []) or []

            for parameterDeclaration in parameterDeclarations:
                parameterName = getattr(parameterDeclaration, "name", None)
                parameterType = self.getTypeFromDeclaration(parameterDeclaration)

                parameterSymbols.extend([
                    VariableSymbol(
                        name=parameterName,
                        symbolType=parameterType,
                        position=getNodePosition(parameterDeclaration),
                        isConstant=False
                    )
                ])

            functionSymbol.parameters = parameterSymbols
            self.functions[functionName] = functionSymbol
            self.globalScope.define(functionSymbol)