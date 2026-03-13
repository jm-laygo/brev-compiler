from __future__ import annotations

from backend.ast.ast_nodes import AssignStmt, IncDecStmt
from backend.errors import DivisionByZeroRuntimeError, RuntimeErrorBase, RuntimeTypeError


def _run_assignment_operation(statement_node, operator_text, operation):
    try:
        return operation()
    except TypeError as exc:
        raise RuntimeTypeError(
            statement_node,
            f"Operator '{operator_text}' cannot be applied to the given operands.",
        ) from exc


def _handle_assign_incdec_stmt(self, statement_node, current_environment):
    if isinstance(statement_node, AssignStmt):
        assigned_value = self._eval_expr(statement_node.value, current_environment)
        assignment_operator = getattr(statement_node, "op", "=")

        if assignment_operator == "=":
            self._assign_lvalue(statement_node.target, assigned_value, current_environment, statement_node)
            return True

        current_target_value = self._read_lvalue(statement_node.target, current_environment)

        if assignment_operator == "+=":
            computed_result = _run_assignment_operation(
                statement_node,
                assignment_operator,
                lambda: current_target_value + assigned_value,
            )
        elif assignment_operator == "-=":
            computed_result = _run_assignment_operation(
                statement_node,
                assignment_operator,
                lambda: current_target_value - assigned_value,
            )
        elif assignment_operator == "*=":
            computed_result = _run_assignment_operation(
                statement_node,
                assignment_operator,
                lambda: current_target_value * assigned_value,
            )
        elif assignment_operator == "/=":
            if assigned_value == 0:
                raise DivisionByZeroRuntimeError(statement_node, "Division by zero.")
            if isinstance(current_target_value, int) and isinstance(assigned_value, int):
                computed_result = _run_assignment_operation(
                    statement_node,
                    assignment_operator,
                    lambda: current_target_value // assigned_value,
                )
            else:
                computed_result = _run_assignment_operation(
                    statement_node,
                    assignment_operator,
                    lambda: current_target_value / assigned_value,
                )
        elif assignment_operator == "%=":
            if assigned_value == 0:
                raise DivisionByZeroRuntimeError(statement_node, "Modulo by zero.")
            computed_result = _run_assignment_operation(
                statement_node,
                assignment_operator,
                lambda: current_target_value % assigned_value,
            )
        elif assignment_operator == "**=":
            computed_result = _run_assignment_operation(
                statement_node,
                assignment_operator,
                lambda: current_target_value ** assigned_value,
            )
        else:
            raise RuntimeErrorBase(
                statement_node,
                f"Assignment operator '{assignment_operator}' is not supported during execution.",
            )

        self._assign_lvalue(statement_node.target, computed_result, current_environment, statement_node)
        return True

    if isinstance(statement_node, IncDecStmt):
        current_target_value = self._read_lvalue(statement_node.target, current_environment)

        if not isinstance(current_target_value, (int, float)):
            raise RuntimeTypeError(statement_node, "Increment and decrement require a numeric variable.")

        if statement_node.op == "++":
            self._assign_lvalue(statement_node.target, current_target_value + 1, current_environment, statement_node)
            return True

        if statement_node.op == "--":
            self._assign_lvalue(statement_node.target, current_target_value - 1, current_environment, statement_node)
            return True

        raise RuntimeErrorBase(statement_node, "Unsupported increment/decrement operator.")

    return False
