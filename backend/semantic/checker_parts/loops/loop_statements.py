from __future__ import annotations
from typing import Any

from backend.semantic.typesys import isBooleanType, isNumericType


class LoopStatementsMixin:
    def checkProcessionStatement(self, statementNode: Any) -> None:
        self.loopDepth += 1

        try:
            initializerStatement = getattr(statementNode, "initializerStatement", None)

            if initializerStatement:
                self.checkStatement(initializerStatement)

            conditionExpression = getattr(statementNode, "condition", None)

            if conditionExpression:
                conditionType = self.getExpressionType(conditionExpression)

                if not isBooleanType(conditionType):
                    self.addError(
                        statementNode,
                        f"procession condition must be verity, got {conditionType}."
                    )

            updateStatement = getattr(statementNode, "updateStatement", None)

            if updateStatement:
                self.checkStatement(updateStatement)

            bodyStatements = getattr(statementNode, "bodyStatements", []) or []

            for bodyStatement in bodyStatements:
                self.checkStatement(bodyStatement)

        finally:
            self.loopDepth -= 1

    def checkEndureStatement(self, statementNode: Any) -> None:
        self.loopDepth += 1

        try:
            conditionExpression = getattr(statementNode, "condition", None)
            conditionType = self.getExpressionType(conditionExpression)

            if not (isBooleanType(conditionType) or isNumericType(conditionType)):
                self.addError(
                    statementNode,
                    f"endure condition must be verity or numeric, got {conditionType}."
                )

            bodyStatements = getattr(statementNode, "bodyStatements", []) or []

            for bodyStatement in bodyStatements:
                self.checkStatement(bodyStatement)

        finally:
            self.loopDepth -= 1

    def checkRitualStatement(self, statementNode: Any) -> None:
        self.loopDepth += 1

        try:
            bodyStatements = getattr(statementNode, "bodyStatements", []) or []

            for bodyStatement in bodyStatements:
                self.checkStatement(bodyStatement)

            conditionExpression = getattr(statementNode, "condition", None)
            conditionType = self.getExpressionType(conditionExpression)

            if not isBooleanType(conditionType):
                self.addError(
                    statementNode,
                    f"ritual endure condition must be verity, got {conditionType}."
                )

        finally:
            self.loopDepth -= 1