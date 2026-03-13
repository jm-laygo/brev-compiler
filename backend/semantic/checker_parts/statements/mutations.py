from __future__ import annotations
from typing import Any

from backend.semantic.symbols import VarSymbol
from backend.semantic.typesys import can_assign, is_numeric

class StatementMutationsMixin:
    def _check_assignstmt(self, statement_node: Any) -> None:
        target_reference = getattr(statement_node, "target", None)
        value_expression = getattr(statement_node, "value", None)
        operator_text = getattr(statement_node, "op", "=")

        root_symbol = self._lvalue_root_symbol(target_reference)
        if isinstance(root_symbol, VarSymbol) and getattr(root_symbol, "is_const", False):
            self._error(
                target_reference if target_reference is not None else statement_node,
                f"Cannot modify sacred constant '{root_symbol.name}'."
            )
            return

        target_type = self._lvalue_type(target_reference)
        value_type = self._expr_type(value_expression)

        if self._has_type_error(target_type) or self._has_type_error(value_type):
            return

        if operator_text != "=" and not is_numeric(target_type):
            self._error(
                target_reference if target_reference is not None else statement_node,
                f"Type error: '{operator_text}' requires numeric target, got {self._tname(target_type)}."
            )
            return

        if not can_assign(target_type, value_type):
            self._error(
                value_expression if value_expression is not None else statement_node,
                f"Type mismatch: cannot assign {self._tname(value_type)} to {self._tname(target_type)}."
            )

    def _check_incdecstmt(self, statement_node: Any) -> None:
        target_reference = getattr(statement_node, "target", None)

        root_symbol = self._lvalue_root_symbol(target_reference)
        if isinstance(root_symbol, VarSymbol) and getattr(root_symbol, "is_const", False):
            self._error(statement_node, f"Cannot increment/decrement sacred constant '{root_symbol.name}'.")
            return

        target_type = self._lvalue_type(target_reference)
        if not is_numeric(target_type):
            self._error(statement_node, f"++/-- requires numeric lvalue, got {target_type}.")