from __future__ import annotations

from backend.ast.ast_nodes import OrdainStmt, OrderStmt, VarDeclStmt


def _handle_decl_stmt(self, statement_node, current_environment):
    if isinstance(statement_node, VarDeclStmt):
        self._exec_var_decl(statement_node.decl, current_environment)
        return True

    if isinstance(statement_node, OrderStmt):
        self.orders[statement_node.decl.name] = statement_node.decl
        return True

    if isinstance(statement_node, OrdainStmt):
        self._exec_ordain_decl(statement_node.decl, current_environment)
        return True

    return False
