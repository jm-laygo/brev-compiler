from __future__ import annotations
from typing import Any

class StatementDeclarationsMixin:
    def _check_vardeclstmt(self, statement_node: Any) -> None:
        declaration_node = getattr(statement_node, "decl", None)
        if declaration_node:
            self._declare_var_decl(declaration_node, is_global=False)
            self._check_var_decl_init(declaration_node)

    def _check_ordainstmt(self, statement_node: Any) -> None:
        declaration_node = getattr(statement_node, "decl", None)
        if declaration_node:
            self._declare_ordain_decl(declaration_node, is_global=False)
            self._check_ordain_decl_init(declaration_node)

    def _check_orderstmt(self, statement_node: Any) -> None:
        self._error(statement_node, "order statement inside function is not supported in semantics yet.")