from __future__ import annotations
from typing import Any

from backend.semantic.typesys import (
    BaseType,
    can_assign,
    is_numeric,
    is_bool,
)

from .helpers import _class

class StatementsMixin:
    def _check_stmt(self, s: Any) -> None:
        k = _class(s)

        if k == "VarDeclStmt":
            decl = getattr(s, "decl", None)
            if decl:
                self._declare_var_decl(decl, is_global=False)
                self._check_var_decl_init(decl)
            return

        if k == "OrdainStmt":
            decl = getattr(s, "decl", None)
            if decl:
                self._declare_ordain_decl(decl, is_global=False)
                self._check_ordain_decl_init(decl)
            return

        if k == "OrderStmt":
            self._error(s, "order statement inside function is not supported in semantics yet.")
            return

        if k == "AssignStmt":
            target = getattr(s, "target", None)
            value  = getattr(s, "value", None)
            op     = getattr(s, "op", "=")

            from backend.semantic.symbols import VarSymbol
            sym = self._lvalue_root_symbol(target)
            if isinstance(sym, VarSymbol) and getattr(sym, "is_const", False):
                self._error(target if target is not None else s, f"Cannot modify sacred constant '{sym.name}'.")                
                return

            t_target = self._lvalue_type(target)
            t_val    = self._expr_type(value)

            if self._has_type_error(t_target) or self._has_type_error(t_val):
                return

            if op != "=" and not is_numeric(t_target):
                self._error(
                    target if target is not None else s,
                    f"Type error: '{op}' requires numeric target, got {self._tname(t_target)}."
                )
                return

            if not can_assign(t_target, t_val):
                self._error(
                    value if value is not None else s,
                    f"Type mismatch: cannot assign {self._tname(t_val)} to {self._tname(t_target)}."
                )
            return

        if k == "IncDecStmt":
            target = getattr(s, "target", None)

            from backend.semantic.symbols import VarSymbol
            sym = self._lvalue_root_symbol(target)
            if isinstance(sym, VarSymbol) and getattr(sym, "is_const", False):
                self._error(s, f"Cannot increment/decrement sacred constant '{sym.name}'.")
                return

            t = self._lvalue_type(target)
            if not is_numeric(t):
                self._error(s, f"++/-- requires numeric lvalue, got {t}.")
            return

        if k == "CallStmt":
            callee = getattr(s, "callee", None)
            args = getattr(s, "args", []) or []
            self._check_call(callee, args, s)
            return

        if k == "ReceiveStmt":
            target = getattr(s, "target", None)

            from backend.semantic.symbols import VarSymbol
            sym = self._lvalue_root_symbol(target)
            if isinstance(sym, VarSymbol) and getattr(sym, "is_const", False):
                self._error(s, f"Cannot store input into sacred constant '{sym.name}'.")
                return

            _ = self._lvalue_type(target)
            return

        if k == "ProclaimStmt":
            for e in getattr(s, "args", []) or []:
                _ = self._expr_type(e)
            return

        if k == "DecreeStmt":
            cond = getattr(s, "expr", None)
            t = self._expr_type(cond)
            if not is_bool(t):
                self._error(cond, f"Type error: decree condition must be verity, got {t}.")
            for st in getattr(s, "body", []) or []:
                self._check_stmt(st)
            for ed in getattr(s, "edicts", []) or []:
                self._check_stmt(ed)
            ab = getattr(s, "absolution", None)
            if ab:
                self._check_stmt(ab)
            return

        if k == "EdictClause":
            cond = getattr(s, "expr", None)
            t = self._expr_type(cond)
            if not is_bool(t):
                self._error(s, f"edict condition must be verity, got {t}.")
            for st in getattr(s, "body", []) or []:
                self._check_stmt(st)
            return

        if k == "AbsolutionClause":
            for st in getattr(s, "body", []) or []:
                self._check_stmt(st)
            return

        if k == "DiscernStmt":
            self.in_discern += 1
            expr = getattr(s, "expr", None)
            _ = self._expr_type(expr)
            for v in getattr(s, "verses", []) or []:
                self._check_stmt(v)
            g = getattr(s, "grace", None)
            if g:
                self._check_stmt(g)
            self.in_discern -= 1
            return

        if k == "VerseCase":
            match = getattr(s, "match", None)
            _ = self._expr_type(match)
            for st in getattr(s, "body", []) or []:
                self._check_stmt(st)
            end = getattr(s, "end", None)
            if end:
                self._check_stmt(end)
            return

        if k == "VerseEnd":
            if self.in_discern <= 0:
                self._error(s, "absolve/fall verse-end used outside discern.")
            return

        if k == "GraceDefault":
            for st in getattr(s, "body", []) or []:
                self._check_stmt(st)
            return

        if k == "ProcessionStmt":
            self.in_loop += 1
            init = getattr(s, "init", None)
            if init:
                self._check_stmt(init)
            cond = getattr(s, "condition", None)
            if cond:
                t = self._expr_type(cond)
                if not is_bool(t):
                    self._error(s, f"procession condition must be verity, got {t}.")
            upd = getattr(s, "update", None)
            if upd:
                self._check_stmt(upd)
            for st in getattr(s, "body", []) or []:
                self._check_stmt(st)
            self.in_loop -= 1
            return

        if k == "EndureStmt":
            self.in_loop += 1
            cond = getattr(s, "condition", None)
            t = self._expr_type(cond)
            if not is_bool(t):
                self._error(s, f"endure condition must be verity, got {t}.")
            for st in getattr(s, "body", []) or []:
                self._check_stmt(st)
            self.in_loop -= 1
            return

        if k == "RitualStmt":
            self.in_loop += 1
            for st in getattr(s, "body", []) or []:
                self._check_stmt(st)
            cond = getattr(s, "condition", None)
            t = self._expr_type(cond)
            if not is_bool(t):
                self._error(s, f"ritual endure condition must be verity, got {t}.")
            self.in_loop -= 1
            return

        if k == "ProceedStmt":
            if self.in_loop <= 0:
                self._error(s, "proceed used outside a loop.")
            return

        if k == "FallStmt":
            if self.in_loop <= 0 and self.in_discern <= 0:
                self._error(s, "fall used outside loop/discern.")
            return

        if k == "AbsolveStmt":
            if self.in_loop <= 0 and self.in_discern <= 0:
                self._error(s, "absolve used outside loop/discern.")
            return

        if k == "DismissStmt":
            if self.current_func is None:
                return

            ret_t = self.current_func.return_type
            val = getattr(s, "value", None)

            if ret_t.is_base(BaseType.HOLLOW):
                if val is not None:
                    self._error(s, "hollow function cannot dismiss a value.")
            else:
                if val is None:
                    self._error(s, f"Function must dismiss a value of type {ret_t}.")
                else:
                    vt = self._expr_type(val)
                    if not can_assign(ret_t, vt):
                        self._error(s, f"Cannot dismiss {vt} from function returning {ret_t}.")
            return