from __future__ import annotations
from typing import Any


class DiscernFlowMixin:
    def _check_discernstmt(self, statement_node: Any) -> None:
        self.in_discern += 1
        try:
            switch_expression = getattr(statement_node, "expr", None)
            self._expr_type(switch_expression)

            verse_nodes = getattr(statement_node, "verses", []) or []
            for verse_node in verse_nodes:
                self._check_stmt(verse_node)

            grace_node = getattr(statement_node, "grace", None)
            if grace_node:
                self._check_stmt(grace_node)
        finally:
            self.in_discern -= 1

    def _check_versecase(self, statement_node: Any) -> None:
        match_expression = getattr(statement_node, "match", None)
        self._expr_type(match_expression)

        body_statements = getattr(statement_node, "body", []) or []
        for body_statement in body_statements:
            self._check_stmt(body_statement)

        end_node = getattr(statement_node, "end", None)
        if end_node:
            self._check_stmt(end_node)

    def _check_verseend(self, statement_node: Any) -> None:
        if self.in_discern <= 0:
            self._error(statement_node, "absolve/fall verse-end used outside discern.")

    def _check_gracedefault(self, statement_node: Any) -> None:
        body_statements = getattr(statement_node, "body", []) or []
        for body_statement in body_statements:
            self._check_stmt(body_statement)

    def _check_fallstmt(self, statement_node: Any) -> None:
        if self.in_loop <= 0 and self.in_discern <= 0:
            self._error(statement_node, "fall used outside loop/discern.")

    def _check_absolvestmt(self, statement_node: Any) -> None:
        if self.in_loop <= 0 and self.in_discern <= 0:
            self._error(statement_node, "absolve used outside loop/discern.")

    def _check_proceedstmt(self, statement_node: Any) -> None:
        if self.in_loop <= 0:
            self._error(statement_node, "proceed used outside a loop.")