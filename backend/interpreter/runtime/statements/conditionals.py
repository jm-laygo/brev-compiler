from __future__ import annotations

from backend.ast.ast_nodes import (
    AbsolutionClause,
    DecreeStatement,
    DiscernStatement,
    EdictClause,
    IdentifierReference,
    VerseEnd,
)
from backend.interpreter.control import AbsolveSignal, FallSignal


def handleConditionalStatement(self, statementNode, currentEnvironment):
    if isinstance(statementNode, DecreeStatement):
        decreeConditionValue = self.evaluateExpression(
            statementNode.condition,
            currentEnvironment
        )

        if self.isTruthy(decreeConditionValue):
            self.executeBlock(
                statementNode.bodyStatements,
                currentEnvironment
            )

            return True

        edictClauses = getattr(statementNode, "edictClauses", []) or []

        for edictClause in edictClauses:
            edictConditionValue = self.evaluateExpression(
                edictClause.condition,
                currentEnvironment
            )

            if self.isTruthy(edictConditionValue):
                self.executeBlock(
                    edictClause.bodyStatements,
                    currentEnvironment
                )

                return True

        absolutionClause = getattr(statementNode, "absolutionClause", None)

        if absolutionClause is not None:
            self.executeBlock(
                absolutionClause.bodyStatements,
                currentEnvironment
            )

        return True

    if isinstance(statementNode, DiscernStatement):
        discernValue = self.evaluateExpression(
            statementNode.expression,
            currentEnvironment
        )

        hasMatchedCase = False
        verseCases = getattr(statementNode, "verseCases", []) or []

        for verseCase in verseCases:
            verseMatchValue = self.evaluateVerseMatch(
                verseCase.matchValue,
                currentEnvironment
            )

            if hasMatchedCase or discernValue == verseMatchValue:
                hasMatchedCase = True

                try:
                    self.executeBlock(
                        verseCase.bodyStatements,
                        currentEnvironment
                    )

                    if getattr(verseCase, "verseEnd", None) is not None:
                        self.handleVerseEnd(verseCase.verseEnd)

                except FallSignal:
                    break

                except AbsolveSignal:
                    break

        graceDefault = getattr(statementNode, "graceDefault", None)

        if not hasMatchedCase and graceDefault is not None:
            try:
                self.executeBlock(
                    graceDefault.bodyStatements,
                    currentEnvironment
                )

                if getattr(graceDefault, "verseEnd", None) is not None:
                    self.handleVerseEnd(graceDefault.verseEnd)

            except FallSignal:
                pass

            except AbsolveSignal:
                pass

        return True

    if isinstance(statementNode, EdictClause):
        edictConditionValue = self.evaluateExpression(
            statementNode.condition,
            currentEnvironment
        )

        if self.isTruthy(edictConditionValue):
            self.executeBlock(
                statementNode.bodyStatements,
                currentEnvironment
            )

        return True

    if isinstance(statementNode, AbsolutionClause):
        self.executeBlock(
            statementNode.bodyStatements,
            currentEnvironment
        )

        return True

    return False

def isTruthy(self, value) -> bool:
    if isinstance(value, bool):
        return value

    return bool(value)

def evaluateVerseMatch(self, matchNode, currentEnvironment):
    if isinstance(matchNode, IdentifierReference):
        return currentEnvironment.get(
            matchNode.name,
            node=matchNode
        )

    return self.evaluateExpression(
        matchNode,
        currentEnvironment
    )

def handleVerseEnd(self, verseEndNode: VerseEnd):
    verseEndKind = (getattr(verseEndNode, "kind", "") or "").lower()

    if verseEndKind == "fall":
        raise FallSignal()

    if verseEndKind == "absolve":
        raise AbsolveSignal()