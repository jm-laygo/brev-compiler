from __future__ import annotations

from backend.ast.ast_nodes import (
    AbsolutionClause,
    DecreeStatement,
    DiscernStatement,
    EdictClause,
    IdentifierReference,
)
from backend.errors import RuntimeTypeError
from backend.interpreter.control import AbsolveSignal, FallSignal


def handleConditionalStatement(self, statementNode, currentEnvironment):
    if isinstance(statementNode, DecreeStatement):
        decreeConditionValue = self.evaluateExpression(
            statementNode.condition,
            currentEnvironment
        )

        if self.isTruthy(decreeConditionValue, statementNode.condition):
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

            if self.isTruthy(edictConditionValue, edictClause.condition):
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

                    # no fall means stop after matched verse
                    break

                except FallSignal:
                    # fall means continue to the next verse
                    continue

                except AbsolveSignal:
                    # absolve exits the discern completely
                    break

        graceDefault = getattr(statementNode, "graceDefault", None)

        if not hasMatchedCase and graceDefault is not None:
            try:
                self.executeBlock(
                    graceDefault.bodyStatements,
                    currentEnvironment
                )

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

        if self.isTruthy(edictConditionValue, statementNode.condition):
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


def isTruthy(self, value, node=None) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, int) and not isinstance(value, bool):
        return value != 0

    raise RuntimeTypeError(
        node,
        f"Condition value must be verity or tally, got {self.getRuntimeTypeName(value)}."
    )


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