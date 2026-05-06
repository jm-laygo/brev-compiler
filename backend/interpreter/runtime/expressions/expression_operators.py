from __future__ import annotations

from backend.ast.ast_nodes import BinaryExpression, UnaryExpression, VariableExpression
from backend.errors import DivisionByZeroRuntimeError, RuntimeErrorBase, RuntimeTypeError
from backend.interpreter.runtime.type_conversion import getRuntimeTypeName


def isNumericRuntimeValue(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def isSigilRuntimeValue(value):
    return isinstance(value, str) and len(value) == 1


def requireBooleanOperand(expressionNode, operatorText, operandValue):
    if not isinstance(operandValue, bool):
        raise RuntimeTypeError(
            expressionNode,
            f"Unary operator '{operatorText}' requires a verity operand, got {getRuntimeTypeName(operandValue)}."
        )


def requireLogicalOperands(expressionNode, operatorText, leftValue, rightValue):
    if not isinstance(leftValue, bool) or not isinstance(rightValue, bool):
        raise RuntimeTypeError(
            expressionNode,
            f"Logical operator '{operatorText}' requires verity operands, got {getRuntimeTypeName(leftValue)} and {getRuntimeTypeName(rightValue)}."
        )


def requireRelationalOperands(expressionNode, operatorText, leftValue, rightValue):
    if isNumericRuntimeValue(leftValue) and isNumericRuntimeValue(rightValue):
        return

    if isSigilRuntimeValue(leftValue) and isSigilRuntimeValue(rightValue):
        return

    raise RuntimeTypeError(
        expressionNode,
        f"Relational operator '{operatorText}' requires two numeric operands or two sigils, got {getRuntimeTypeName(leftValue)} and {getRuntimeTypeName(rightValue)}."
    )


def requireEqualityOperands(expressionNode, operatorText, leftValue, rightValue):
    if isNumericRuntimeValue(leftValue) and isNumericRuntimeValue(rightValue):
        return

    if getRuntimeTypeName(leftValue) == getRuntimeTypeName(rightValue):
        return

    raise RuntimeTypeError(
        expressionNode,
        f"Equality operator '{operatorText}' requires matching operand types or numeric operands, got {getRuntimeTypeName(leftValue)} and {getRuntimeTypeName(rightValue)}."
    )


def runBinaryOperation(expressionNode, operatorText, operation):
    try:
        return operation()

    except TypeError as typeError:
        raise RuntimeTypeError(
            expressionNode,
            f"Operator '{operatorText}' cannot be applied to the given operands."
        ) from typeError


def handleUnaryExpression(self, expressionNode, currentEnvironment):
    if not isinstance(expressionNode, UnaryExpression):
        return None

    operatorText = expressionNode.operator
    operandValue = self.evaluateExpression(
        expressionNode.operand,
        currentEnvironment
    )

    # boolean not
    if operatorText in ("!", "!!", "not"):
        requireBooleanOperand(
            expressionNode,
            operatorText,
            operandValue
        )

        return not operandValue

    # numeric negation
    if operatorText == "-":
        if not isNumericRuntimeValue(operandValue):
            raise RuntimeTypeError(
                expressionNode,
                f"Unary operator '-' requires a numeric operand, got {getRuntimeTypeName(operandValue)}."
            )

        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: -operandValue
        )

    # increment expression
    if operatorText == "++":
        if not isinstance(expressionNode.operand, VariableExpression):
            raise RuntimeTypeError(
                expressionNode,
                "Increment requires a variable target."
            )

        targetReference = expressionNode.operand.reference
        currentValue = self.readLeftHandValue(
            targetReference,
            currentEnvironment
        )

        if not isNumericRuntimeValue(currentValue):
            raise RuntimeTypeError(
                expressionNode,
                f"Increment requires a numeric variable, got {getRuntimeTypeName(currentValue)}."
            )

        incrementedValue = currentValue + 1

        self.assignLeftHandValue(
            targetReference,
            incrementedValue,
            currentEnvironment,
            expressionNode
        )

        return incrementedValue

    # decrement expression
    if operatorText == "--":
        if not isinstance(expressionNode.operand, VariableExpression):
            raise RuntimeTypeError(
                expressionNode,
                "Decrement requires a variable target."
            )

        targetReference = expressionNode.operand.reference
        currentValue = self.readLeftHandValue(
            targetReference,
            currentEnvironment
        )

        if not isNumericRuntimeValue(currentValue):
            raise RuntimeTypeError(
                expressionNode,
                f"Decrement requires a numeric variable, got {getRuntimeTypeName(currentValue)}."
            )

        decrementedValue = currentValue - 1

        self.assignLeftHandValue(
            targetReference,
            decrementedValue,
            currentEnvironment,
            expressionNode
        )

        return decrementedValue

    raise RuntimeErrorBase(
        expressionNode,
        "This unary expression is not yet supported during execution."
    )


def handleBinaryExpression(self, expressionNode, currentEnvironment):
    if not isinstance(expressionNode, BinaryExpression):
        return None

    leftValue = self.evaluateExpression(
        expressionNode.leftExpression,
        currentEnvironment
    )

    rightValue = self.evaluateExpression(
        expressionNode.rightExpression,
        currentEnvironment
    )

    operatorText = expressionNode.operator

    # addition
    if operatorText == "+":
        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue + rightValue
        )

    # subtraction
    if operatorText == "-":
        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue - rightValue
        )

    # multiplication
    if operatorText == "*":
        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue * rightValue
        )

    # division
    if operatorText == "/":
        if rightValue == 0:
            raise DivisionByZeroRuntimeError(
                expressionNode,
                "Division by zero."
            )

        if isinstance(leftValue, int) and not isinstance(leftValue, bool) and isinstance(rightValue, int) and not isinstance(rightValue, bool):
            return runBinaryOperation(
                expressionNode,
                operatorText,
                lambda: leftValue // rightValue
            )

        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue / rightValue
        )

    # modulo
    if operatorText == "%":
        if not (
            isinstance(leftValue, int)
            and not isinstance(leftValue, bool)
            and isinstance(rightValue, int)
            and not isinstance(rightValue, bool)
        ):
            raise RuntimeTypeError(
                expressionNode,
                "Modulo operator '%' requires tally operands."
            )

        if rightValue == 0:
            raise DivisionByZeroRuntimeError(
                expressionNode,
                "Modulo by zero."
            )

        return leftValue % rightValue

    # power
    if operatorText in ("^", "**"):
        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue ** rightValue
        )

    # equality
    if operatorText == "==":
        requireEqualityOperands(
            expressionNode,
            operatorText,
            leftValue,
            rightValue
        )

        return leftValue == rightValue

    # inequality
    if operatorText == "!=":
        requireEqualityOperands(
            expressionNode,
            operatorText,
            leftValue,
            rightValue
        )

        return leftValue != rightValue

    # greater than
    if operatorText == ">":
        requireRelationalOperands(
            expressionNode,
            operatorText,
            leftValue,
            rightValue
        )

        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue > rightValue
        )

    # less than
    if operatorText == "<":
        requireRelationalOperands(
            expressionNode,
            operatorText,
            leftValue,
            rightValue
        )

        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue < rightValue
        )

    # greater than or equal
    if operatorText == ">=":
        requireRelationalOperands(
            expressionNode,
            operatorText,
            leftValue,
            rightValue
        )

        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue >= rightValue
        )

    # less than or equal
    if operatorText == "<=":
        requireRelationalOperands(
            expressionNode,
            operatorText,
            leftValue,
            rightValue
        )

        return runBinaryOperation(
            expressionNode,
            operatorText,
            lambda: leftValue <= rightValue
        )

    # logical and
    if operatorText in ("&&", "and"):
        requireLogicalOperands(
            expressionNode,
            operatorText,
            leftValue,
            rightValue
        )

        return leftValue and rightValue

    # logical or
    if operatorText in ("||", "or"):
        requireLogicalOperands(
            expressionNode,
            operatorText,
            leftValue,
            rightValue
        )

        return leftValue or rightValue

    # concat
    if operatorText in ("&", "concat"):
        return self.stringifyRuntimeValue(leftValue) + self.stringifyRuntimeValue(rightValue)

    raise RuntimeErrorBase(
        expressionNode,
        "This binary expression is not yet supported during execution."
    )