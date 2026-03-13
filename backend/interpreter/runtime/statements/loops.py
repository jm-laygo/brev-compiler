from __future__ import annotations

from backend.ast.ast_nodes import EndureStmt, ProcessionStmt, RitualStmt
from backend.interpreter.control import FallSignal, ProceedSignal
from backend.interpreter.environment import Environment


def _handle_loop_stmt(self, statement_node, current_environment):
    if isinstance(statement_node, ProcessionStmt):
        loop_environment = Environment(parent=current_environment)

        initialization_statement = getattr(statement_node, "init", None)
        loop_condition_expression = getattr(statement_node, "condition", None)
        update_statement = getattr(statement_node, "update", None)
        body_statements = getattr(statement_node, "body", []) or []

        if initialization_statement is not None:
            self._exec_stmt(initialization_statement, loop_environment)

        while True:
            if loop_condition_expression is not None:
                loop_condition_value = self._eval_expr(loop_condition_expression, loop_environment)
                if not self._truthy(loop_condition_value):
                    break

            try:
                self._exec_block(body_statements, loop_environment, create_scope=True)
            except ProceedSignal:
                pass
            except FallSignal:
                break

            if update_statement is not None:
                self._exec_stmt(update_statement, loop_environment)

        return True

    if isinstance(statement_node, EndureStmt):
        while self._truthy(self._eval_expr(statement_node.condition, current_environment)):
            try:
                self._exec_block(statement_node.body, current_environment)
            except ProceedSignal:
                continue
            except FallSignal:
                break
        return True

    if isinstance(statement_node, RitualStmt):
        while True:
            try:
                self._exec_block(statement_node.body, current_environment)
            except ProceedSignal:
                pass
            except FallSignal:
                break

            ritual_condition_value = self._eval_expr(statement_node.condition, current_environment)
            if not self._truthy(ritual_condition_value):
                break

        return True

    return False
