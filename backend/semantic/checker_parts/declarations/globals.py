from __future__ import annotations
from typing import Any

from ..helpers import _class


class GlobalDeclarationsMixin:
    def _declare_globals(self, program_node: Any) -> None:
        global_declarations = getattr(program_node, "globals", []) or []

        for global_declaration in global_declarations:
            declaration_kind = _class(global_declaration)

            if declaration_kind in ("VarDecl", "SacredDecl"):
                self._declare_var_decl(global_declaration, is_global=True)
            elif declaration_kind == "OrdainDecl":
                self._declare_ordain_decl(global_declaration, is_global=True)
            elif declaration_kind == "OrderDecl":
                continue