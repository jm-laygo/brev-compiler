from __future__ import annotations
from typing import Any
from backend.semantic.symbols import Scope
from .helpers import _class
from backend.semantic.typesys import BaseType

class ProgramFlowMixin:
    def _check_program(self, program: Any) -> None:
        for g in getattr(program, "globals", []) or []:
            if _class(g) == "VarDecl":
                self._check_var_decl_init(g)
            elif _class(g) == "SacredDecl":
                self._check_sacred_decl_init(g)
            elif _class(g) == "OrdainDecl":
                self._check_ordain_decl_init(g)

        entry = getattr(program, "entry", None)
        if entry is not None:
            self._check_function(entry)

        for f in getattr(program, "functions", []) or []:
            self._check_function(f)

    def _check_function(self, f: Any) -> None:
        if _class(f) != "RiteDecl":
            return

        fname = getattr(f, "name", "")
        fs = self.funcs.get(fname)
        self.current_func = fs

        old_scope = self.scope
        self.scope = Scope(self.global_scope)

        if fs:
            seen = set()
            for p in fs.params:
                if p.name in seen:
                    self._error(p.pos, f"Duplicate parameter '{p.name}' in function '{fname}'.")
                seen.add(p.name)
                self.scope.define(p)

        for d in getattr(f, "local_decls", []) or []:
            if _class(d) == "VarDecl":
                self._declare_var_decl(d, is_global=False)
                self._check_var_decl_init(d)
            elif _class(d) == "SacredDecl":
                self._declare_var_decl(d, is_global=False, force_const=True)
                self._check_sacred_decl_init(d)
            elif _class(d) == "OrdainDecl":
                self._declare_ordain_decl(d, is_global=False)
                self._check_ordain_decl_init(d)
            elif _class(d) == "OrderDecl":
                self._error(d, "Order declarations are not allowed inside functions (if intended, implement it).")

        body = getattr(f, "body", []) or []
        for s in body:
            self._check_stmt(s)

        dismiss_stmt = getattr(f, "dismiss", None)
        if dismiss_stmt is not None:
            self._check_stmt(dismiss_stmt)

        has_dismiss_in_body = any(_class(st) == "DismissStmt" for st in body)
        has_any_dismiss = (dismiss_stmt is not None) or has_dismiss_in_body

        if fs is not None and not fs.return_type.is_base(BaseType.HOLLOW):
            if not has_any_dismiss:
                self._error(f, f"Function '{fname}' must dismiss a value of type {fs.return_type}.")

        self.scope = old_scope
        self.current_func = None