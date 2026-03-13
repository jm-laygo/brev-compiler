from __future__ import annotations

from backend.ast.ast_nodes import AbsolveStmt, DismissStmt, FallStmt, ProceedStmt
from backend.interpreter.control import AbsolveSignal, DismissSignal, FallSignal, ProceedSignal


def _handle_control_stmt(self, statement_node, current_environment):
    if isinstance(statement_node, ProceedStmt):
        raise ProceedSignal()

    if isinstance(statement_node, FallStmt):
        raise FallSignal()

    if isinstance(statement_node, AbsolveStmt):
        raise AbsolveSignal()

    if isinstance(statement_node, DismissStmt):
        dismiss_value_node = getattr(statement_node, "value", None)
        if dismiss_value_node is not None:
            dismiss_value = self._eval_expr(dismiss_value_node, current_environment)
        else:
            dismiss_value = None

        raise DismissSignal(dismiss_value)

    return False
