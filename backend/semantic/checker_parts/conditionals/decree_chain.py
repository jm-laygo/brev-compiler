from __future__ import annotations
from typing import Any

from backend.semantic.typesys import isBooleanType


class DecreeChainMixin:
    def checkDecreeStatement(self, statementNode: Any) -> None:
        conditionExpression = getattr(statementNode, "condition", None)
        conditionType = self.getExpressionType(conditionExpression)

        if not isBooleanType(conditionType):
            self.addError(
                conditionExpression,
                f"Type error: decree condition must be verity, got {conditionType}."
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

        if not isBooleanType(conditionType):
            self.addError(
                statementNode,
                f"edict condition must be verity, got {conditionType}."
            )

        bodyStatements = getattr(statementNode, "bodyStatements", []) or []

        for bodyStatement in bodyStatements:
            self.checkStatement(bodyStatement)

    def checkAbsolutionClause(self, statementNode: Any) -> None:
        bodyStatements = getattr(statementNode, "bodyStatements", []) or []

        for bodyStatement in bodyStatements:
            self.checkStatement(bodyStatement)