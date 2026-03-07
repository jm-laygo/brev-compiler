from __future__ import annotations

from backend.ast.ast_nodes import (
    ArrayInit,
    BinaryExpr,
    CallExpr,
    GroupExpr,
    LiteralExpr,
    UnaryExpr,
    VarExpr,
    VerseOfExpr,
)
from backend.errors import (
    DivisionByZeroRuntimeError,
    RuntimeErrorBase,
    RuntimeTypeError,
)

def _eval_expr(self, expression_node, current_environment):
    if expression_node is None:
        return None

    if isinstance(expression_node, LiteralExpr):
        return expression_node.value

    if isinstance(expression_node, GroupExpr):
        return self._eval_expr(expression_node.expr, current_environment)

    if isinstance(expression_node, VarExpr):
        return self._read_lvalue(expression_node.ref, current_environment)

    if isinstance(expression_node, ArrayInit):
        evaluated_items = []
        for item_node in expression_node.items:
            evaluated_items.append(self._eval_expr(item_node, current_environment))
        return evaluated_items

    if isinstance(expression_node, VerseOfExpr):
        inner_value = self._eval_expr(expression_node.expr, current_environment)

        if isinstance(inner_value, list):
            return len(inner_value)

        if isinstance(inner_value, str):
            return len(inner_value)

        raise RuntimeTypeError(expression_node, "The verseof operator requires an array or scripture value.")

    if isinstance(expression_node, CallExpr):
        evaluated_argument_values = []
        for argument_node in expression_node.args:
            evaluated_argument_values.append(self._eval_expr(argument_node, current_environment))

        call_result = self._call_rite(expression_node.callee, evaluated_argument_values, call_node=expression_node)

        call_access_chain = getattr(expression_node, "access", None)
        if call_access_chain is not None:
            return self._read_lvalue_from_value(call_access_chain, call_result, expression_node)

        return call_result

    if isinstance(expression_node, UnaryExpr):
        operator_text = expression_node.op
        operand_value = self._eval_expr(expression_node.operand, current_environment)

        if operator_text in ("!", "!!", "not"):
            return not self._truthy(operand_value)

        if operator_text == "~":
            if not isinstance(operand_value, (int, float)):
                raise RuntimeTypeError(expression_node, "Unary negation requires a numeric operand.")
            return -operand_value

        if operator_text == "++":
            if not isinstance(expression_node.operand, VarExpr):
                raise RuntimeTypeError(expression_node, "Increment requires a variable target.")

            target_reference = expression_node.operand.ref
            current_value = self._read_lvalue(target_reference, current_environment)

            if not isinstance(current_value, (int, float)):
                raise RuntimeTypeError(expression_node, "Increment requires a numeric variable.")

            incremented_value = current_value + 1
            self._assign_lvalue(target_reference, incremented_value, current_environment, expression_node)
            return incremented_value

        if operator_text == "--":
            if not isinstance(expression_node.operand, VarExpr):
                raise RuntimeTypeError(expression_node, "Decrement requires a variable target.")

            target_reference = expression_node.operand.ref
            current_value = self._read_lvalue(target_reference, current_environment)

            if not isinstance(current_value, (int, float)):
                raise RuntimeTypeError(expression_node, "Decrement requires a numeric variable.")

            decremented_value = current_value - 1
            self._assign_lvalue(target_reference, decremented_value, current_environment, expression_node)
            return decremented_value

        raise RuntimeErrorBase(expression_node, "This unary expression is not yet supported during execution.")

    if isinstance(expression_node, BinaryExpr):
        left_value = self._eval_expr(expression_node.left, current_environment)
        right_value = self._eval_expr(expression_node.right, current_environment)
        operator_text = expression_node.op

        if operator_text == "+":
            return left_value + right_value

        if operator_text == "-":
            return left_value - right_value

        if operator_text == "*":
            return left_value * right_value

        if operator_text == "/":
            if right_value == 0:
                raise DivisionByZeroRuntimeError(expression_node, "Division by zero.")
            return left_value / right_value

        if operator_text == "%":
            if right_value == 0:
                raise DivisionByZeroRuntimeError(expression_node, "Modulo by zero.")
            return left_value % right_value

        if operator_text in ("^", "**"):
            return left_value ** right_value

        if operator_text == "==":
            return left_value == right_value

        if operator_text == "!=":
            return left_value != right_value

        if operator_text == ">":
            return left_value > right_value

        if operator_text == "<":
            return left_value < right_value

        if operator_text == ">=":
            return left_value >= right_value

        if operator_text == "<=":
            return left_value <= right_value

        if operator_text in ("&&", "and"):
            return self._truthy(left_value) and self._truthy(right_value)

        if operator_text in ("||", "or"):
            return self._truthy(left_value) or self._truthy(right_value)

        if operator_text in ("&", "concat"):
            return self.stringify(left_value) + self.stringify(right_value)

        raise RuntimeErrorBase(expression_node, "This binary expression is not yet supported during execution.")

    raise RuntimeErrorBase(expression_node, "This expression is not yet supported during execution.")

def bind_expression_methods(cls):
    cls._eval_expr = _eval_expr