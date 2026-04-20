from __future__ import annotations
from typing import Any

from backend.semantic.typesys import is_bool, is_numeric
from backend.semantic.typesys import is_bool


class LoopStatementsMixin:
    def _check_processionstmt(self, statement_node: Any) -> None:
        self.in_loop += 1
        try:
            init_statement = getattr(statement_node, "init", None)
            if init_statement:
                self._check_stmt(init_statement)

            condition_expression = getattr(statement_node, "condition", None)
            if condition_expression:
                condition_type = self._expr_type(condition_expression)
                if not is_bool(condition_type):
                    self._error(statement_node, f"procession condition must be verity, got {condition_type}.")

            update_statement = getattr(statement_node, "update", None)
            if update_statement:
                self._check_stmt(update_statement)

            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)
        finally:
            self.in_loop -= 1

    def _check_endurestmt(self, statement_node: Any) -> None:
        self.in_loop += 1
        try:
            condition_expression = getattr(statement_node, "condition", None)
            condition_type = self._expr_type(condition_expression)

            if not (is_bool(condition_type) or is_numeric(condition_type)):
                self._error(statement_node, f"endure condition must be verity or numeric, got {condition_type}.")

            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)
        finally:
            self.in_loop -= 1

    def _check_ritualstmt(self, statement_node: Any) -> None:
        self.in_loop += 1
        try:
            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)

            condition_expression = getattr(statement_node, "condition", None)
            condition_type = self._expr_type(condition_expression)

            if not is_bool(condition_type):
                self._error(statement_node, f"ritual endure condition must be verity, got {condition_type}.")
        finally:
            self.in_loop -= 1