from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List

from backend.ast.ast_nodes import *
from backend.tokens import *
from backend.errors import SemanticError 

from backend.semantic.symbols import Scope, VarSymbol, FuncSymbol, TypeSymbol
from backend.semantic.types import (
    token_dtype_to_type,
    literal_token_to_type,
    can_assign,
    unary_result,
    binary_result,
    T_HOLLOW,
    T_VERITY,
    T_TALLY,
    is_bool,
    is_numeric,
)

@dataclass
class Context:
    current_function: Optional[FuncSymbol] = None
    in_loop: int = 0
    in_discern: int = 0
    in_case: int = 0

class SemanticChecker:
    def __init__(self):
        self.global_scope = Scope(None, "global")
        self.scope = self.global_scope
        self.errors: List[SemanticError] = []
        self.ctx = Context()

    def error(self, node, msg: str):
        self.errors.append(SemanticError(node, msg))

    def push_scope(self, name: str):
        self.scope = Scope(self.scope, name)

    def pop_scope(self):
        assert self.scope.parent is not None
        self.scope = self.scope.parent

    # Entry
    def check(self, program: Program) -> List[SemanticError]:
        # register types (order)
        for g in program.globals:
            if isinstance(g, OrderDecl):
                self._define_order_type(g)

        # register globals (vars/sacred/ordain)
        for g in program.globals:
            if isinstance(g, (VarDecl, SacredDecl, OrdainDecl)):
                self._define_global_decl(g)
            # OrderDecl already handled

        # register function signatures
        for fn in program.functions + ([program.entry] if program.entry else []):
            if fn is None:
                continue
            self._define_function_sig(fn)

        # check function bodies
        for fn in program.functions + ([program.entry] if program.entry else []):
            if fn is None:
                continue
            self._check_function_body(fn)

        return self.errors

    # Definitions
    def _define_order_type(self, order: OrderDecl):
        name = order.name
        if self.global_scope.lookup_local(name):
            self.error(order, f"Duplicate type '{name}'.")
            return

        members: dict[str, VarSymbol] = {}
        for m in order.members:
            mtype = token_dtype_to_type(m.type_name)
            if m.name in members:
                self.error(m, f"Duplicate member '{m.name}' in order '{name}'.")
                continue
            members[m.name] = VarSymbol(m.name, mtype, is_const=False, dims=len(m.dims), meta={"pos": m.pos})

            if m.init is not None:
                it = self._infer_expr(m.init)
                if it is not None and not can_assign(mtype, it):
                    self.error(m, f"Cannot assign '{it}' to member '{m.name}' of type '{mtype}'.")

        self.global_scope.define(TypeSymbol(name, members))

    def _define_global_decl(self, decl: Node):
        if isinstance(decl, VarDecl):
            dtype = token_dtype_to_type(decl.type_name)
            for item in decl.items:
                self._define_var(item.name, dtype, is_const=False, dims=len(item.dims), init=item.init, where=item)
        elif isinstance(decl, SacredDecl):
            dtype = token_dtype_to_type(decl.type_name)
            for item in decl.items:
                self._define_var(item.name, dtype, is_const=True, dims=0, init=item.value, where=item)
        elif isinstance(decl, OrdainDecl):
            order_type_name = decl.name

            ts = self.global_scope.resolve(order_type_name)
            if not isinstance(ts, TypeSymbol):
                self.error(decl, f"Cannot ordain '{order_type_name}': type is not an order (or not declared).")
                return

            for item in decl.items:
                self._define_var(
                    name=item.name,
                    dtype=order_type_name,
                    is_const=False,
                    dims=len(item.dims),
                    init=item.init,
                    where=item
                )

    def _define_var(self, name: str, dtype: str, *, is_const: bool, dims: int, init: Optional[Expr], where: Node):
        if self.scope.lookup_local(name):
            self.error(where, f"Duplicate declaration of '{name}' in scope '{self.scope.name}'.")
            return
        self.scope.define(VarSymbol(name, dtype, is_const=is_const, dims=dims, meta={"pos": where.pos}))

        if init is not None:
            it = self._infer_expr(init)
            if it is not None and not can_assign(dtype, it):
                self.error(where, f"Cannot assign '{it}' to '{name}' of type '{dtype}'.")

    def _define_function_sig(self, fn: RiteDecl):
        fname = fn.name
        if self.global_scope.lookup_local(fname):
            self.error(fn, f"Duplicate function '{fname}'.")
            return

        rtype = token_dtype_to_type(fn.return_type)
        params: list[VarSymbol] = []
        seen = set()
        for p in fn.params:
            ptype = token_dtype_to_type(p.type_name)
            if p.name in seen:
                self.error(p, f"Duplicate parameter '{p.name}' in function '{fname}'.")
                continue
            seen.add(p.name)
            params.append(VarSymbol(p.name, ptype, is_const=False, dims=p.array_dims, meta={"pos": p.pos}))

        self.global_scope.define(FuncSymbol(fname, rtype, params, meta={"pos": fn.pos}))

    # Function body
    def _check_function_body(self, fn: RiteDecl):
        fsym = self.global_scope.resolve(fn.name)
        if not isinstance(fsym, FuncSymbol):
            return

        self.ctx.current_function = fsym
        self.push_scope(f"Function:{fn.name}")

        # define parameters
        for ps in fsym.params:
            if self.scope.lookup_local(ps.name):
                self.error(fn, f"Parameter name conflicts: '{ps.name}'.")
            else:
                self.scope.define(ps)

        # local decls
        for d in fn.local_decls:
            if isinstance(d, OrderDecl):
                self.error(d, "Order declarations are not allowed inside functions (if that's your rule).")
            elif isinstance(d, (VarDecl, SacredDecl, OrdainDecl)):
                self._define_global_decl(d)

        # statements
        for s in fn.body:
            self._check_stmt(s)

        # function dismiss check
        if fn.dismiss is not None:
            self._check_stmt(fn.dismiss)

        self.pop_scope()
        self.ctx.current_function = None

    # Statement checking
    def _check_stmt(self, s: Statement):
        if isinstance(s, VarDeclStmt):
            self._define_global_decl(s.decl)
            return
        if isinstance(s, OrderStmt):
            self.error(s, "Order statement not allowed here (if local order is disallowed).")
            return
        if isinstance(s, OrdainStmt):
            self._define_global_decl(s.decl)
            return

        if isinstance(s, ReceiveStmt):
            lvt = self._infer_lvalue(s.target)
            if lvt is None:
                return
            return

        if isinstance(s, ProclaimStmt):
            for a in s.args:
                self._infer_expr(a)
            return

        if isinstance(s, CallStmt):
            self._check_call_like(s.callee, s.args, s)
            if s.access is not None:
                self._infer_lvalue(s.access)
            return

        if isinstance(s, AssignStmt):
            if isinstance(s.target, NameRef):
                sym = self.scope.resolve(s.target.name)
                if isinstance(sym, VarSymbol) and sym.is_const:
                    self.error(s, f"Cannot assign to sacred constant '{sym.name}'.")
                    return

            lt = self._infer_lvalue(s.target)
            rt = self._infer_expr(s.value)
            if lt and rt and not can_assign(lt, rt):
                self.error(s, f"Cannot assign '{rt}' to '{lt}'.")
            return

        if isinstance(s, IncDecStmt):
            lt = self._infer_lvalue(s.target)
            if lt and not is_numeric(lt):
                self.error(s, f"Inc/Dec requires numeric type, got '{lt}'.")
            return

        if isinstance(s, DismissStmt):
            self._check_dismiss(s)
            return

        if isinstance(s, ProceedStmt):
            # treat as break
            if self.ctx.in_loop == 0 and self.ctx.in_discern == 0:
                self.error(s, "'proceed' can only be used inside loops or discern.")
            return

        if isinstance(s, AbsolveStmt):
            # treat as "break discern"
            if self.ctx.in_discern == 0:
                self.error(s, "'absolve' can only be used inside discern.")
            return

        # FallStmt: continue in loops OR fallthrough in discern cases
        if FallStmt is not None and isinstance(s, FallStmt):
            if self.ctx.in_loop == 0 and self.ctx.in_discern == 0:
                self.error(s, "'fall' can only be used inside loops or discern.")
            return

        if isinstance(s, DecreeStmt):
            ct = self._infer_expr(s.expr)
            if ct and ct != T_VERITY:
                self.error(s, f"'decree' condition must be verity, got '{ct}'.")
            self.push_scope("decree")
            for st in s.body:
                self._check_stmt(st)
            self.pop_scope()

            # edicts
            for e in s.edicts:
                ect = self._infer_expr(e.expr)
                if ect and ect != T_VERITY:
                    self.error(e, f"'edict' condition must be verity, got '{ect}'.")
                self.push_scope("edict")
                for st in e.body:
                    self._check_stmt(st)
                self.pop_scope()

            # absolution
            if s.absolution is not None:
                self.push_scope("absolution")
                for st in s.absolution.body:
                    self._check_stmt(st)
                self.pop_scope()
            return

        if isinstance(s, DiscernStmt):
            self.ctx.in_discern += 1
            disc_t = self._infer_expr(s.expr)

            # verses
            for v in s.verses:
                self.ctx.in_case += 1

                mt = None
                if isinstance(v.match, IdentifierRef):
                    sym = self.scope.resolve(v.match.name)
                    if not isinstance(sym, VarSymbol):
                        self.error(v.match, f"Undeclared identifier '{v.match.name}' in verse match.")
                    else:
                        mt = sym.type_name
                else:
                    mt = self._infer_expr(v.match)

                if disc_t and mt and disc_t != mt:
                    if not (is_numeric(disc_t) and is_numeric(mt)):
                        self.error(v, f"Verse match type '{mt}' does not match discern type '{disc_t}'.")

                self.push_scope("verse")
                for st in v.body:
                    self._check_stmt(st)
                self.pop_scope()

                # verse end keyword rules
                if v.end is not None:
                    pass

                self.ctx.in_case -= 1

            # grace
            if s.grace is not None:
                self.ctx.in_case += 1
                self.push_scope("grace")
                for st in s.grace.body:
                    self._check_stmt(st)
                self.pop_scope()
                self.ctx.in_case -= 1

            self.ctx.in_discern -= 1
            return

        if isinstance(s, EndureStmt):
            self.ctx.in_loop += 1
            ct = self._infer_expr(s.condition)
            if ct and ct != T_VERITY:
                self.error(s, f"'endure' condition must be verity, got '{ct}'.")
            self.push_scope("endure")
            for st in s.body:
                self._check_stmt(st)
            self.pop_scope()
            self.ctx.in_loop -= 1
            return

        if isinstance(s, ProcessionStmt):
            self.ctx.in_loop += 1
            self.push_scope("procession")

            if s.init is not None:
                self._check_stmt(s.init)

            if s.condition is not None:
                ct = self._infer_expr(s.condition)
                if ct and ct != T_VERITY:
                    self.error(s, f"'procession' condition must be verity, got '{ct}'.")

            if s.update is not None:
                self._check_stmt(s.update)

            for st in s.body:
                self._check_stmt(st)

            self.pop_scope()
            self.ctx.in_loop -= 1
            return

        if isinstance(s, RitualStmt):
            self.ctx.in_loop += 1
            self.push_scope("ritual")
            for st in s.body:
                self._check_stmt(st)
            self.pop_scope()

            ct = self._infer_expr(s.condition)
            if ct and ct != T_VERITY:
                self.error(s, f"'ritual ... endure(...)' condition must be verity, got '{ct}'.")

            self.ctx.in_loop -= 1
            return

        self.error(s, f"Unhandled statement node: {type(s).__name__}")

    def _check_dismiss(self, s: DismissStmt):
        fn = self.ctx.current_function
        if fn is None:
            self.error(s, "'dismiss' used outside of function.")
            return

        if fn.return_type == T_HOLLOW:
            if s.value is not None:
                self.error(s, "Cannot return a value from a hollow function.")
            return

        # non-hollow
        if s.value is None:
            self.error(s, f"Function must return '{fn.return_type}' but dismiss has no value.")
            return

        vt = self._infer_expr(s.value)
        if vt and not can_assign(fn.return_type, vt):
            self.error(s, f"Return type mismatch: expected '{fn.return_type}', got '{vt}'.")

    # Expression inference
    def _infer_expr(self, e: Expr | None) -> Optional[str]:
        if e is None:
            return None

        # Literal
        if isinstance(e, LiteralExpr):
            e.inferred_type = e.literal_type
            return e.inferred_type

        if isinstance(e, GroupExpr):
            t = self._infer_expr(e.expr)
            e.inferred_type = t
            return t

        if isinstance(e, VarExpr):
            t = self._infer_lvalue(e.ref)
            e.inferred_type = t
            return t

        if isinstance(e, VerseOfExpr):
            t = self._infer_expr(e.expr)
            e.inferred_type = t
            return t

        if isinstance(e, CallExpr):
            self._check_call_like(e.callee, e.args, e)
            sym = self.global_scope.resolve(e.callee)
            if isinstance(sym, FuncSymbol):
                e.inferred_type = sym.return_type
                return sym.return_type
            e.inferred_type = None
            return None

        if isinstance(e, UnaryExpr):
            ot = self._infer_expr(e.operand)
            if ot is None:
                return None
            rt = unary_result(e.op, ot)
            if rt is None:
                self.error(e, f"Invalid unary op '{e.op}' for type '{ot}'.")
                return None
            e.inferred_type = rt
            return rt

        if isinstance(e, BinaryExpr):
            lt = self._infer_expr(e.left)
            rt = self._infer_expr(e.right)
            if lt is None or rt is None:
                return None
            out = binary_result(e.op, lt, rt)
            if out is None:
                self.error(e, f"Invalid binary op '{e.op}' for types '{lt}' and '{rt}'.")
                return None
            e.inferred_type = out
            return out

        if isinstance(e, TernaryExpr):
            ct = self._infer_expr(e.condition)
            tt = self._infer_expr(e.true_expr)
            ft = self._infer_expr(e.false_expr)
            if ct and ct != T_VERITY:
                self.error(e, f"Ternary condition must be verity, got '{ct}'.")
            if tt and ft:
                if tt == ft:
                    e.inferred_type = tt
                    return tt
                if is_numeric(tt) and is_numeric(ft):
                    e.inferred_type = "divine" if ("divine" in (tt, ft)) else "tally"
                    return e.inferred_type
                self.error(e, f"Ternary branches mismatch: '{tt}' vs '{ft}'.")
            return None

        if isinstance(e, ArrayInit):
            e.inferred_type = None
            return None

        self.error(e, f"Unhandled expression node: {type(e).__name__}")
        return None

    def _infer_lvalue(self, lv: LValue | None) -> Optional[str]:
        if lv is None:
            return None

        if isinstance(lv, NameRef):
            sym = self.scope.resolve(lv.name)
            if not isinstance(sym, VarSymbol):
                self.error(lv, f"Undeclared identifier '{lv.name}'.")
                return None
            return sym.type_name

        if isinstance(lv, IndexRef):
            bt = self._infer_lvalue(lv.base)
            it = self._infer_expr(lv.index)
            if it and it != T_TALLY:
                self.error(lv, f"Array index must be tally, got '{it}'.")
            return bt

        if isinstance(lv, MemberRef):
            bt = self._infer_lvalue(lv.base)
            if bt is None:
                return None
            ts = self.global_scope.resolve(bt)
            if not isinstance(ts, TypeSymbol):
                self.error(lv, f"Type '{bt}' has no members (not an order).")
                return None
            mem = ts.members.get(lv.member)
            if mem is None:
                self.error(lv, f"Order '{bt}' has no member '{lv.member}'.")
                return None
            return mem.type_name

        self.error(lv, f"Unhandled lvalue node: {type(lv).__name__}")
        return None

    def _check_call_like(self, callee: str, args: list[Expr], node):
        sym = self.global_scope.resolve(callee)
        if not isinstance(sym, FuncSymbol):
            # not a function
            self.error(node, f"Call to undefined function '{callee}'.")
            for a in args:
                self._infer_expr(a)
            return

        if len(args) != len(sym.params):
            self.error(node, f"Function '{callee}' expects {len(sym.params)} args, got {len(args)}.")
        for i, a in enumerate(args):
            at = self._infer_expr(a)
            if i < len(sym.params) and at is not None:
                pt = sym.params[i].type_name
                if not can_assign(pt, at):
                    self.error(node, f"Arg {i+1} of '{callee}' expects '{pt}', got '{at}'.")