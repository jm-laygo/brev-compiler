from __future__ import annotations
from typing import Any

from backend.semantic.symbols import VarSymbol
from backend.semantic.typesys import BaseType, can_assign

class StatementActionsMixin:
    def _check_callstmt(self, statement_node: Any) -> None:
        function_name = getattr(statement_node, "callee", None)
        argument_nodes = getattr(statement_node, "args", []) or []
        self._check_call(function_name, argument_nodes, statement_node)

    def _check_receivestmt(self, statement_node: Any) -> None:
        target_reference = getattr(statement_node, "target", None)

        root_symbol = self._lvalue_root_symbol(target_reference)
        if isinstance(root_symbol, VarSymbol) and getattr(root_symbol, "is_const", False):
            self._error(statement_node, f"Cannot store input into sacred constant '{root_symbol.name}'.")
            return

        self._lvalue_type(target_reference)

    def _check_proclaimstmt(self, statement_node: Any) -> None:
        argument_nodes = getattr(statement_node, "args", []) or []
        for argument_node in argument_nodes:
            self._expr_type(argument_node)

    def _check_dismissstmt(self, statement_node: Any) -> None:
        if self.current_func is None:
            return

        return_type = self.current_func.return_type
        return_value = getattr(statement_node, "value", None)

        if return_type.is_base(BaseType.HOLLOW):
            if return_value is not None:
                self._error(statement_node, "hollow function cannot dismiss a value.")
            return

        if return_value is None:
            self._error(statement_node, f"Function must dismiss a value of type {return_type}.")
            return

        value_type = self._expr_type(return_value)
        if not can_assign(return_type, value_type):
            self._error(statement_node, f"Cannot dismiss {value_type} from function returning {return_type}.")