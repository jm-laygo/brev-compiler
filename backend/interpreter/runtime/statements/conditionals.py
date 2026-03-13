from __future__ import annotations

from backend.ast.ast_nodes import (
    AbsolutionClause,
    DecreeStmt,
    DiscernStmt,
    EdictClause,
    IdentifierRef,
    VerseEnd,
)
from backend.interpreter.control import AbsolveSignal, FallSignal


def _handle_conditional_stmt(self, statement_node, current_environment):
    if isinstance(statement_node, DecreeStmt):
        decree_condition_value = self._eval_expr(statement_node.expr, current_environment)

        if self._truthy(decree_condition_value):
            self._exec_block(statement_node.body, current_environment)
            return True

        edict_clauses = getattr(statement_node, "edicts", []) or []
        for edict_clause in edict_clauses:
            edict_condition_value = self._eval_expr(edict_clause.expr, current_environment)

            if self._truthy(edict_condition_value):
                self._exec_block(edict_clause.body, current_environment)
                return True

        absolution_clause = getattr(statement_node, "absolution", None)
        if absolution_clause is not None:
            self._exec_block(absolution_clause.body, current_environment)

        return True

    if isinstance(statement_node, DiscernStmt):
        discern_value = self._eval_expr(statement_node.expr, current_environment)
        has_matched_case = False

        verse_cases = getattr(statement_node, "verses", []) or []
        for verse_case in verse_cases:
            verse_match_value = self._eval_verse_match(verse_case.match, current_environment)

            if has_matched_case or discern_value == verse_match_value:
                has_matched_case = True

                try:
                    self._exec_block(verse_case.body, current_environment)

                    if getattr(verse_case, "end", None) is not None:
                        self._handle_verse_end(verse_case.end)

                except FallSignal:
                    break
                except AbsolveSignal:
                    break

        grace_clause = getattr(statement_node, "grace", None)
        if (not has_matched_case) and grace_clause is not None:
            try:
                self._exec_block(grace_clause.body, current_environment)

                if getattr(grace_clause, "end", None) is not None:
                    self._handle_verse_end(grace_clause.end)

            except FallSignal:
                pass
            except AbsolveSignal:
                pass

        return True

    if isinstance(statement_node, EdictClause):
        edict_condition_value = self._eval_expr(statement_node.expr, current_environment)
        if self._truthy(edict_condition_value):
            self._exec_block(statement_node.body, current_environment)
        return True

    if isinstance(statement_node, AbsolutionClause):
        self._exec_block(statement_node.body, current_environment)
        return True

    return False


def _truthy(self, value) -> bool:
    if isinstance(value, bool):
        return value
    return bool(value)


def _eval_verse_match(self, match_node, current_environment):
    if isinstance(match_node, IdentifierRef):
        return current_environment.get(match_node.name, node=match_node)
    return self._eval_expr(match_node, current_environment)


def _handle_verse_end(self, verse_end_node: VerseEnd):
    end_kind = (getattr(verse_end_node, "kind", "") or "").lower()

    if end_kind == "fall":
        raise FallSignal()

    if end_kind == "absolve":
        raise AbsolveSignal()
