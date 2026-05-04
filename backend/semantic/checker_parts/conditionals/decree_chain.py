from __future__ import annotations
from typing import Any

from backend.semantic.typesys import isBool, isTally


class DecreeChainMixin:
    def checkDecreeStatement(self, statementNode: Any) -> None:
        conditionExpression = getattr(statementNode, "condition", None)
        conditionType = self.getExpressionType(conditionExpression)

        if not (isBool(conditionType) or isTally(conditionType)):
            self.addError(
                conditionExpression if conditionExpression is not None else statementNode,
                f"decree condition must be verity or tally, got {conditionType}."
            )

        bodyStatements = getattr(statementNode, "bodyStatements", []) or []

        for bodyStatement in bodyStatements:
            self.checkStatement(bodyStatement)

        edictClauses = getattr(statementNode, "edictClauses", []) or []

        for edictClause in edictClauses:
            self.checkStatement(edictClause)

        absolutionClause = getattr(statementNode, "absolutionClause", None)

        if absolutionClause:
            self.checkStatement(absolutionClause)

    def checkEdictClause(self, statementNode: Any) -> None:
        conditionExpression = getattr(statementNode, "condition", None)
        conditionType = self.getExpressionType(conditionExpression)

        if not (isBool(conditionType) or isTally(conditionType)):
            self.addError(
                conditionExpression if conditionExpression is not None else statementNode,
                f"edict condition must be verity or tally, got {conditionType}."
            )

        bodyStatements = getattr(statementNode, "bodyStatements", []) or []

        for bodyStatement in bodyStatements:
            self.checkStatement(bodyStatement)

    def checkAbsolutionClause(self, statementNode: Any) -> None:
        bodyStatements = getattr(statementNode, "bodyStatements", []) or []

        for bodyStatement in bodyStatements:
            self.checkStatement(bodyStatement)