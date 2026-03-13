from __future__ import annotations
from typing import Any

from backend.semantic.typesys import is_bool


class DecreeChainMixin:
    def _check_decreestmt(self, statement_node: Any) -> None:
        condition_expression = getattr(statement_node, "expr", None)
        condition_type = self._expr_type(condition_expression)

        if not is_bool(condition_type):
            self._error(condition_expression, f"Type error: decree condition must be verity, got {condition_type}.")

        body_statements = getattr(statement_node, "body", []) or []
        for body_statement in body_statements:
            self._check_stmt(body_statement)

        edict_nodes = getattr(statement_node, "edicts", []) or []
        for edict_node in edict_nodes:
            self._check_stmt(edict_node)

        absolution_node = getattr(statement_node, "absolution", None)
        if absolution_node:
            self._check_stmt(absolution_node)

    def _check_edictclause(self, statement_node: Any) -> None:
        condition_expression = getattr(statement_node, "expr", None)
        condition_type = self._expr_type(condition_expression)

        if not is_bool(condition_type):
            self._error(statement_node, f"edict condition must be verity, got {condition_type}.")

        body_statements = getattr(statement_node, "body", []) or []
        for body_statement in body_statements:
            self._check_stmt(body_statement)

    def _check_absolutionclause(self, statement_node: Any) -> None:
        body_statements = getattr(statement_node, "body", []) or []
        for body_statement in body_statements:
            self._check_stmt(body_statement)