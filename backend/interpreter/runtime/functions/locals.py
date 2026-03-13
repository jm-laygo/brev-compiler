from __future__ import annotations

from backend.ast.ast_nodes import OrderDecl, OrdainDecl, SacredDecl, VarDecl

# LOCAL DECLARATIONS
def _exec_local_declarations(self, local_declarations, rite_environment):
    for local_declaration in local_declarations:
        if isinstance(local_declaration, SacredDecl):
            self._exec_sacred_decl(local_declaration, rite_environment)
        elif isinstance(local_declaration, VarDecl):
            self._exec_var_decl(local_declaration, rite_environment)
        elif isinstance(local_declaration, OrdainDecl):
            self._exec_ordain_decl(local_declaration, rite_environment)
        elif isinstance(local_declaration, OrderDecl):
            self.orders[local_declaration.name] = local_declaration
