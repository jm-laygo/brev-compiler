from __future__ import annotations
from typing import Any, List

from backend.semantic.typesys import Type, BaseType, canAssign


class CallsMixin:
    def checkFunctionCall(
        self,
        functionName: str,
        argumentNodes: List[Any],
        callNode: Any
    ) -> Type:
        if not functionName:
            self.addError(callNode, "Rite call is missing a rite name.")
            return Type.error()

        functionSymbol = self.functions.get(functionName)

        if functionSymbol is None:
            suggestionText = self.getSuggestionFromCandidates(
                functionName,
                list(self.functions.keys())
            )

            self.addError(
                callNode,
                f"Call to undeclared rite '{functionName}'.{suggestionText}"
            )

            return Type.error()

        expectedArgumentCount = len(functionSymbol.parameters)
        actualArgumentCount = len(argumentNodes)

        if actualArgumentCount != expectedArgumentCount:
            self.addError(
                callNode,
                f"Rite '{functionName}' expects {expectedArgumentCount} argument(s), got {actualArgumentCount}."
            )

        argumentsToCheck = min(actualArgumentCount, expectedArgumentCount)

        for argumentIndex in range(argumentsToCheck):
            argumentNode = argumentNodes[argumentIndex]
            argumentType = self.getExpressionType(argumentNode)
            parameterType = functionSymbol.parameters[argumentIndex].symbolType

            if argumentType.baseType == BaseType.ERROR:
                continue

            if not canAssign(parameterType, argumentType):
                self.addError(
                    argumentNode if argumentNode is not None else callNode,
                    f"Argument {argumentIndex + 1} of rite '{functionName}' cannot pass {self.formatType(argumentType)} to {self.formatType(parameterType)}."
                )

        return functionSymbol.returnType