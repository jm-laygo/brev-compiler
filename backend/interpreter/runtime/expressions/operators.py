from __future__ import annotations

import math

from backend.ast.ast_nodes import BinaryExpr, UnaryExpr, VarExpr
from backend.errors import DivisionByZeroRuntimeError, RuntimeErrorBase, RuntimeTypeError

# UNARY EXPRESSIONS
def _runtime_type_name(value):
    if isinstance(value, bool):
        return "verity"
    if isinstance(value, int):
        return "tally"
    if isinstance(value, float):
        return "divine"
    if isinstance(value, str):
        return "sigil" if len(value) == 1 else "scripture"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        order_name = value.get("__order__")
        if order_name:
            return f"order {order_name}"
        return "order"
    if value is None:
        return "hollow"
    return type(value).__name__

# BINARY EXPRESSIONS
def _is_numeric_runtime(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)

# SIGIL CHECK
def _is_sigil_runtime(value):
    return isinstance(value, str) and len(value) == 1

# OPERAND CHECKS
def _require_bool_operand(expression_node, operator_text, operand_value):
    if not isinstance(operand_value, bool):
        raise RuntimeTypeError(
            expression_node,
            f"Unary operator '{operator_text}' requires a verity operand, got {_runtime_type_name(operand_value)}.",
        )

def _require_logical_operands(expression_node, operator_text, left_value, right_value):
    if not isinstance(left_value, bool) or not isinstance(right_value, bool):
        raise RuntimeTypeError(
            expression_node,
            f"Logical operator '{operator_text}' requires verity operands, got {_runtime_type_name(left_value)} and {_runtime_type_name(right_value)}.",
        )

def _require_numeric_operands(expression_node, operator_text, left_value, right_value):
    if _is_numeric_runtime(left_value) and _is_numeric_runtime(right_value):
        return
    raise RuntimeTypeError(
        expression_node,
        f"Operator '{operator_text}' requires numeric operands, got {_runtime_type_name(left_value)} and {_runtime_type_name(right_value)}.",
    )
    
def _require_relational_operands(expression_node, operator_text, left_value, right_value):
    if _is_numeric_runtime(left_value) and _is_numeric_runtime(right_value):
        return
    if _is_sigil_runtime(left_value) and _is_sigil_runtime(right_value):
        return
    raise RuntimeTypeError(
        expression_node,
        f"Relational operator '{operator_text}' requires two numeric operands or two sigils, got {_runtime_type_name(left_value)} and {_runtime_type_name(right_value)}.",
    )

def _require_equality_operands(expression_node, operator_text, left_value, right_value):
    if _is_numeric_runtime(left_value) and _is_numeric_runtime(right_value):
        return
    if _runtime_type_name(left_value) == _runtime_type_name(right_value):
        return
    raise RuntimeTypeError(
        expression_node,
        f"Equality operator '{operator_text}' requires matching operand types or numeric operands, got {_runtime_type_name(left_value)} and {_runtime_type_name(right_value)}.",
    )

# ORDERS 
def _run_binary_operation(expression_node, operator_text, operation):
    try:
        return operation()
    except OverflowError as exc:
        raise RuntimeErrorBase(
            expression_node,
            f"Operator '{operator_text}' overflowed during execution.",
        ) from exc
    except TypeError as exc:
        raise RuntimeTypeError(
            expression_node,
            f"Operator '{operator_text}' cannot be applied to the given operands.",
        ) from exc

# TYPE CHECKS
def _handle_unary_expr(self, expression_node, current_environment):
    if not isinstance(expression_node, UnaryExpr):
        return None

    operator_text = expression_node.op
    operand_value = self._eval_expr(expression_node.operand, current_environment)

    if operator_text in ("!", "!!", "not"):
        _require_bool_operand(expression_node, operator_text, operand_value)
        return not operand_value

    if operator_text == "~":
        if not _is_numeric_runtime(operand_value):
            raise RuntimeTypeError(expression_node, "Unary negation requires a numeric operand.")
        return _run_binary_operation(expression_node, operator_text, lambda: -operand_value)

    if operator_text == "++":
        if not isinstance(expression_node.operand, VarExpr):
            raise RuntimeTypeError(expression_node, "Increment requires a variable target.")

        target_reference = expression_node.operand.ref
        current_value = self._read_lvalue(target_reference, current_environment)

        if not _is_numeric_runtime(current_value):
            raise RuntimeTypeError(expression_node, "Increment requires a numeric variable.")

        incremented_value = current_value + 1
        self._assign_lvalue(target_reference, incremented_value, current_environment, expression_node)
        return incremented_value

    if operator_text == "--":
        if not isinstance(expression_node.operand, VarExpr):
            raise RuntimeTypeError(expression_node, "Decrement requires a variable target.")

        target_reference = expression_node.operand.ref
        current_value = self._read_lvalue(target_reference, current_environment)

        if not _is_numeric_runtime(current_value):
            raise RuntimeTypeError(expression_node, "Decrement requires a numeric variable.")

        decremented_value = current_value - 1
        self._assign_lvalue(target_reference, decremented_value, current_environment, expression_node)
        return decremented_value

    raise RuntimeErrorBase(expression_node, "This unary expression is not yet supported during execution.")

# BINARY EXPRESSIONS
def _handle_binary_expr(self, expression_node, current_environment):
    if not isinstance(expression_node, BinaryExpr):
        return None

    left_value = self._eval_expr(expression_node.left, current_environment)
    right_value = self._eval_expr(expression_node.right, current_environment)
    operator_text = expression_node.op

    if operator_text == "+":
        _require_numeric_operands(expression_node, operator_text, left_value, right_value)
        return _run_binary_operation(expression_node, operator_text, lambda: left_value + right_value)

    if operator_text == "-":
        _require_numeric_operands(expression_node, operator_text, left_value, right_value)
        return _run_binary_operation(expression_node, operator_text, lambda: left_value - right_value)

    if operator_text == "*":
        _require_numeric_operands(expression_node, operator_text, left_value, right_value)
        return _run_binary_operation(expression_node, operator_text, lambda: left_value * right_value)

    if operator_text == "/":
        _require_numeric_operands(expression_node, operator_text, left_value, right_value)
        if right_value == 0:
            raise DivisionByZeroRuntimeError(expression_node, "Division by zero.")
        if isinstance(left_value, int) and isinstance(right_value, int):
            return _run_binary_operation(expression_node, operator_text, lambda: left_value // right_value)
        return _run_binary_operation(expression_node, operator_text, lambda: left_value / right_value)

    if operator_text == "%":
        _require_numeric_operands(expression_node, operator_text, left_value, right_value)
        if right_value == 0:
            raise DivisionByZeroRuntimeError(expression_node, "Modulo by zero.")
        return _run_binary_operation(expression_node, operator_text, lambda: left_value % right_value)

    if operator_text in ("^", "**"):
        _require_numeric_operands(expression_node, operator_text, left_value, right_value)
        result = _run_binary_operation(expression_node, operator_text, lambda: left_value ** right_value)
        if isinstance(result, float) and (math.isnan(result) or math.isinf(result)):
            raise RuntimeErrorBase(expression_node, "Power operation overflowed during execution.")
        return result

    if operator_text == "==":
        _require_equality_operands(expression_node, operator_text, left_value, right_value)
        return left_value == right_value

    if operator_text == "!=":
        _require_equality_operands(expression_node, operator_text, left_value, right_value)
        return left_value != right_value

    if operator_text == ">":
        _require_relational_operands(expression_node, operator_text, left_value, right_value)
        return _run_binary_operation(expression_node, operator_text, lambda: left_value > right_value)

    if operator_text == "<":
        _require_relational_operands(expression_node, operator_text, left_value, right_value)
        return _run_binary_operation(expression_node, operator_text, lambda: left_value < right_value)

    if operator_text == ">=":
        _require_relational_operands(expression_node, operator_text, left_value, right_value)
        return _run_binary_operation(expression_node, operator_text, lambda: left_value >= right_value)

    if operator_text == "<=":
        _require_relational_operands(expression_node, operator_text, left_value, right_value)
        return _run_binary_operation(expression_node, operator_text, lambda: left_value <= right_value)

    if operator_text in ("&&", "and"):
        _require_logical_operands(expression_node, operator_text, left_value, right_value)
        return left_value and right_value

    if operator_text in ("||", "or"):
        _require_logical_operands(expression_node, operator_text, left_value, right_value)
        return left_value or right_value

    if operator_text in ("&", "concat"):
        try:
            return self.stringify(left_value) + self.stringify(right_value)
        except RecursionError as exc:
            raise RuntimeErrorBase(
                expression_node,
                "String concatenation failed due to nested/circular values.",
            ) from exc

    raise RuntimeErrorBase(expression_node, "This binary expression is not yet supported during execution.")
