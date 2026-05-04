from __future__ import annotations

from backend.ast.ast_nodes import FunctionCallStatement, ProclaimStatement, ReceiveStatement


def handleInputOutputStatement(self, statementNode, currentEnvironment):
    if isinstance(statementNode, FunctionCallStatement):
        evaluatedArgumentValues = []

        for argumentNode in statementNode.arguments:
            evaluatedArgumentValues.extend([
                self.evaluateExpression(argumentNode, currentEnvironment)
            ])

        self.callRite(
            statementNode.calleeName,
            evaluatedArgumentValues,
            callNode=statementNode
        )

        return True

    if isinstance(statementNode, ReceiveStatement):
        rawInputValue = self.inputProvider(statementNode.target)

        convertedInputValue = self.convertInputForTarget(
            statementNode.target,
            rawInputValue,
            currentEnvironment
        )

        self.assignLeftHandValue(
            statementNode.target,
            convertedInputValue,
            currentEnvironment,
            statementNode
        )

        return True

    if isinstance(statementNode, ProclaimStatement):
        outputParts = []

        for argumentNode in statementNode.arguments:
            evaluatedValue = self.evaluateExpression(
                argumentNode,
                currentEnvironment
            )

            outputParts.extend([
                self.stringifyRuntimeValue(evaluatedValue)
            ])

        self.writeInline("".join(outputParts))

        return True

    return False