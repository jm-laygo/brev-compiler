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
            functionDeclarations.append(entryRite)

        functionDeclarations.extend(
            getattr(programNode, "riteDeclarations", []) or []
        )

        for functionDeclaration in functionDeclarations:
            if functionDeclaration is None:
                continue

            declarationKind = getClassName(functionDeclaration)

            if declarationKind != "RiteDeclaration":
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
            parameterDeclarations = (
                getattr(functionDeclaration, "parameters", None)
                or getattr(functionDeclaration, "params", [])
            )

            seenParameterNames = set()

            for parameterDeclaration in parameterDeclarations:
                parameterName = getattr(parameterDeclaration, "name", None)

                if not parameterName:
                    self.addError(
                        parameterDeclaration,
                        f"Parameter in function '{functionName}' missing name."
                    )
                    continue

                if parameterName in seenParameterNames:
                    self.addError(
                        parameterDeclaration,
                        f"Duplicate parameter '{parameterName}' in function '{functionName}'."
                    )
                    continue

                seenParameterNames.add(parameterName)

                parameterType = self.getTypeFromDeclaration(parameterDeclaration)

                parameterSymbols.append(
                    VariableSymbol(
                        name=parameterName,
                        symbolType=parameterType,
                        position=getNodePosition(parameterDeclaration),
                        isConstant=False
                    )
                )

            functionSymbol.parameters = parameterSymbols
            self.functions[functionName] = functionSymbol
            self.globalScope.define(functionSymbol)