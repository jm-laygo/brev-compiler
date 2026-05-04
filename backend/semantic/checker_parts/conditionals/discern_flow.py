from __future__ import annotations
from typing import Any


class DiscernFlowMixin:
    def checkDiscernStatement(self, statementNode: Any) -> None:
        self.discernDepth += 1

        try:
            switchExpression = getattr(statementNode, "expression", None)
            self.getExpressionType(switchExpression)

            verseCases = getattr(statementNode, "verseCases", []) or []

            for verseCase in verseCases:
                self.checkStatement(verseCase)

            graceDefault = getattr(statementNode, "graceDefault", None)

            if graceDefault:
                self.checkStatement(graceDefault)

        finally:
            self.discernDepth -= 1

    def checkVerseCase(self, statementNode: Any) -> None:
        matchValue = getattr(statementNode, "matchValue", None)
        self.getExpressionType(matchValue)

        bodyStatements = getattr(statementNode, "bodyStatements", []) or []

        for bodyStatement in bodyStatements:
            self.checkStatement(bodyStatement)

        verseEnd = getattr(statementNode, "verseEnd", None)

        if verseEnd:
            self.checkStatement(verseEnd)

    def checkVerseEnd(self, statementNode: Any) -> None:
        if self.discernDepth <= 0:
            self.addError(
                statementNode,
                "absolve/fall verse-end used outside discern."
            )

    def checkGraceDefault(self, statementNode: Any) -> None:
        bodyStatements = getattr(statementNode, "bodyStatements", []) or []

        for bodyStatement in bodyStatements:
            self.checkStatement(bodyStatement)

    def checkFallStatement(self, statementNode: Any) -> None:
        if self.loopDepth <= 0 and self.discernDepth <= 0:
            self.addError(
                statementNode,
                "fall used outside loop/discern."
            )

    def checkAbsolveStatement(self, statementNode: Any) -> None:
        if self.loopDepth <= 0 and self.discernDepth <= 0:
            self.addError(
                statementNode,
                "absolve used outside loop/discern."
            )

    def checkProceedStatement(self, statementNode: Any) -> None:
        if self.loopDepth <= 0:
            self.addError(
                statementNode,
                "proceed used outside a loop."
            )