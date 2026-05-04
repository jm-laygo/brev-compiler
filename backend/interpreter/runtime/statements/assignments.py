from __future__ import annotations

from backend.ast.ast_nodes import AssignmentStatement, IncrementDecrementStatement
from backend.errors import DivisionByZeroRuntimeError, RuntimeErrorBase, RuntimeTypeError


def runAssignmentOperation(statementNode, operatorText, operation):
    try:
        return operation()

    except TypeError as typeError:
        raise RuntimeTypeError(
            statementNode,
            f"Operator '{operatorText}' cannot be applied to the given operands."
        ) from typeError

def handleAssignmentIncrementDecrementStatement(self, statementNode, currentEnvironment):
    if isinstance(statementNode, AssignmentStatement):
        assignedValue = self.evaluateExpression(
            statementNode.value,
            currentEnvironment
        )

        assignmentOperator = getattr(statementNode, "operator", "=")

        # normal assignment
        if assignmentOperator == "=":
            self.assignLeftHandValue(
                statementNode.target,
                assignedValue,
                currentEnvironment,
                statementNode
            )

            return True

        currentTargetValue = self.readLeftHandValue(
            statementNode.target,
            currentEnvironment
        )

        # add assignment
        if assignmentOperator == "+=":
            computedResult = runAssignmentOperation(
                statementNode,
                assignmentOperator,
                lambda: currentTargetValue + assignedValue
            )

        # subtract assignment
        elif assignmentOperator == "-=":
            computedResult = runAssignmentOperation(
                statementNode,
                assignmentOperator,
                lambda: currentTargetValue - assignedValue
            )

        # multiply assignment
        elif assignmentOperator == "*=":
            computedResult = runAssignmentOperation(
                statementNode,
                assignmentOperator,
                lambda: currentTargetValue * assignedValue
            )

        # divide assignment
        elif assignmentOperator == "/=":
            if assignedValue == 0:
                raise DivisionByZeroRuntimeError(
                    statementNode,
                    "Division by zero."
                )

            if isinstance(currentTargetValue, int) and isinstance(assignedValue, int):
                computedResult = runAssignmentOperation(
                    statementNode,
                    assignmentOperator,
                    lambda: currentTargetValue // assignedValue
                )

            else:
                computedResult = runAssignmentOperation(
                    statementNode,
                    assignmentOperator,
                    lambda: currentTargetValue / assignedValue
                )

        # modulo assignment
        elif assignmentOperator == "%=":
            if assignedValue == 0:
                raise DivisionByZeroRuntimeError(
                    statementNode,
                    "Modulo by zero."
                )

            computedResult = runAssignmentOperation(
                statementNode,
                assignmentOperator,
                lambda: currentTargetValue % assignedValue
            )

        # power assignment
        elif assignmentOperator == "**=":
            computedResult = runAssignmentOperation(
                statementNode,
                assignmentOperator,
                lambda: currentTargetValue ** assignedValue
            )

        else:
            raise RuntimeErrorBase(
                statementNode,
                f"Assignment operator '{assignmentOperator}' is not supported during execution."
            )

        self.assignLeftHandValue(
            statementNode.target,
            computedResult,
            currentEnvironment,
            statementNode
        )

        return True

    if isinstance(statementNode, IncrementDecrementStatement):
        currentTargetValue = self.readLeftHandValue(
            statementNode.target,
            currentEnvironment
        )

        if not isinstance(currentTargetValue, (int, float)):
            raise RuntimeTypeError(
                statementNode,
                "Increment and decrement require a numeric variable."
            )

        # increment
        if statementNode.operator == "++":
            self.assignLeftHandValue(
                statementNode.target,
                currentTargetValue + 1,
                currentEnvironment,
                statementNode
            )

            return True

        # decrement
        if statementNode.operator == "--":
            self.assignLeftHandValue(
                statementNode.target,
                currentTargetValue - 1,
                currentEnvironment,
                statementNode
            )

            return True

        raise RuntimeErrorBase(
            statementNode,
            "Unsupported increment/decrement operator."
        )

    return False