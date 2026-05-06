from __future__ import annotations
import difflib
from typing import List


class SuggestionsMixin:
    def getAllVisibleNames(self) -> List[str]:
        visibleNames = set()

        currentScope = self.currentScope

        while currentScope is not None:
            scopeSymbols = getattr(currentScope, "symbolTable", {})
            visibleNames.update(scopeSymbols.keys())
            currentScope = getattr(currentScope, "parentScope", None)

        functionNames = getattr(self, "functions", {}).keys()
        orderNames = getattr(self, "orders", {}).keys()

        visibleNames.update(functionNames)
        visibleNames.update(orderNames)

        return sorted(visibleNames)

    def getSuggestionMessage(self, enteredName: str, cutoff: float = 0.72) -> str:
        if not enteredName:
            return ""

        visibleNames = self.getAllVisibleNames()

        closestMatches = difflib.get_close_matches(
            enteredName,
            visibleNames,
            n=1,
            cutoff=cutoff
        )

        if closestMatches:
            return f" Did you mean '{closestMatches[0]}'?"

        return ""

    def getSuggestionFromCandidates(
        self,
        enteredName: str,
        candidateNames: List[str],
        cutoff: float = 0.72
    ) -> str:
        if not enteredName:
            return ""

        closestMatches = difflib.get_close_matches(
            enteredName,
            candidateNames or [],
            n=1,
            cutoff=cutoff
        )

        if closestMatches:
            return f" Did you mean '{closestMatches[0]}'?"

        return ""