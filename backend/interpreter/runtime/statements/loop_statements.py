from __future__ import annotations

from backend.ast.ast_nodes import EndureStatement, ProcessionStatement, RitualStatement
from backend.interpreter.control import AbsolveSignal, ProceedSignal
from backend.interpreter.environment import Environment


def handleLoopStatement(self, statementNode, currentEnvironment):
    if isinstance(statementNode, ProcessionStatement):
        loopEnvironment = Environment(parentEnvironment=currentEnvironment)

        initializerStatement = getattr(statementNode, "initializerStatement", None)
        loopConditionExpression = getattr(statementNode, "condition", None)
        updateStatement = getattr(statementNode, "updateStatement", None)
        bodyStatements = getattr(statementNode, "bodyStatements", []) or []

        if initializerStatement is not None:
            self.executeStatement(initializerStatement, loopEnvironment)

        while True:
            if loopConditionExpression is not None:
                loopConditionValue = self.evaluateExpression(
                    loopConditionExpression,
                    loopEnvironment
                )

                if not self.isTruthy(loopConditionValue, loopConditionExpression):
                    break

            try:
                self.executeBlock(
                    bodyStatements,
                    loopEnvironment,
                    createScope=True
                )

            except ProceedSignal:
                pass

            except AbsolveSignal:
                break

            if updateStatement is not None:
                self.executeStatement(updateStatement, loopEnvironment)

        return True

    if isinstance(statementNode, EndureStatement):
        while self.isTruthy(
            self.evaluateExpression(
                statementNode.condition,
                currentEnvironment
            ),
            statementNode.condition
        ):
            try:
                self.executeBlock(
                    statementNode.bodyStatements,
                    currentEnvironment
                )

            except ProceedSignal:
                continue

            except AbsolveSignal:
                break

        return True

    if isinstance(statementNode, RitualStatement):
        while True:
            try:
                self.executeBlock(
                    statementNode.bodyStatements,
                    currentEnvironment
                )

            except ProceedSignal:
                pass

            except AbsolveSignal:
                break

            ritualConditionValue = self.evaluateExpression(
                statementNode.condition,
                currentEnvironment
            )

            if not self.isTruthy(ritualConditionValue, statementNode.condition):
                break

        return True

    return False