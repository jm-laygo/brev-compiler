from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union
from backend.semantic.typesys import *
from backend.semantic.symbols import Scope, Symbol, VarSymbol, FuncSymbol, OrderSymbol, MemberSymbol
from backend.ast.ast_nodes import *

try:
    from backend.errors import SemanticError
except Exception:
    class SemanticError(Exception):
        def __init__(self, pos: Any, message: str):
            self.pos = pos
            self.message = message
            super().__init__(message)

def _pos(node: Any) -> Any:
    return getattr(node, "pos", None)

def _name(node: Any, fallback: str = "") -> str:
    return getattr(node, "name", fallback)

def _class(node: Any) -> str:
    return node.__class__.__name__ if node is not None else "None"

@dataclass
class CheckerConfig:
    allow_concat_coercion: bool = True
    allow_numeric_to_string_in_concat: bool = True

class SemanticChecker:
    def __init__(self, config: Optional[CheckerConfig] = None):
        self.cfg = config or CheckerConfig()

        self.global_scope = Scope(None)
        self.orders: Dict[str, OrderSymbol] = {}
        self.funcs: Dict[str, FuncSymbol] = {}

        self.scope: Scope = self.global_scope
        self.current_func: Optional[FuncSymbol] = None
        self.in_loop: int = 0
        self.in_discern: int = 0

        self.errors: List[SemanticError] = []

    def check(self, program: Program) -> Tuple[Program, List[SemanticError]]:
        self._declare_globals(program)
        self._declare_orders(program)
        self._declare_functions(program)
        self._check_program(program)

        return program, self.errors

    def _error(self, node_or_token: Any, msg: str) -> None:
        self.errors.append(SemanticError(node_or_token, msg))

    def _declare_globals(self, program: Program) -> None:
        for g in getattr(program, "globals", []) or []:
            k = _class(g)
            if k in ("VarDecl", "SacredDecl"):
                self._declare_var_decl(g, is_global = True)
            elif k == "OrdainDecl":
                self._declare_ordain_decl(g, is_global = True)
            elif k == "OrderDecl":
                continue
            else:
                continue

    def _declare_orders(self, program: Program) -> None:
        for g in getattr(program, "globals", []) or []:
            if _class(g) != "OrderDecl":
                continue
            order_name = getattr(g, "name", None)
            if not order_name:
                self._error(g, "Order declaration missing name.")
                continue
            if order_name in self.orders:
                self._error(g, f"Order '{order_name}' already declared.")
                continue
            sym = OrderSymbol(name = order_name, typ = Type.order(order_name), pos = _pos(g))
            for m in getattr(g, "members", []) or []:
                mem_name = getattr(m, "name", None)
                if not mem_name:
                    self._error(m, f"Order '{order_name}' member missing name.")
                    continue
                if mem_name in sym.members:
                    self._error(m, f"Duplicate member '{mem_name}' in order '{order_name}'.")
                    continue
                mem_type = self._type_from_decl(m)
                sym.members[mem_name] = MemberSymbol(name = mem_name, typ = mem_type, pos = _pos(m))
            self.orders[order_name] = sym

    def _declare_functions(self, program: Program) -> None:
        all_funcs: List[Any] = []
        entry = getattr(program, "entry", None)
        if entry is not None:
            all_funcs.append(entry)
        all_funcs.extend(getattr(program, "functions", []) or [])

        for f in all_funcs:
            if f is None:
                continue
            if _class(f) != "RiteDecl":
                continue
            fname = getattr(f, "name", None)
            if not fname:
                self._error(f, "Function missing name.")
                continue
            if fname in self.funcs:
                self._error(f, f"Function '{fname}' already declared.")
                continue

            ret_t = self._type_from_return_type(getattr(f, "return_type", None))
            fs = FuncSymbol(name = fname, typ = Type.unknown(), return_type = ret_t, pos = _pos(f))

            params: List[VarSymbol] = []
            for p in getattr(f, "params", []) or []:
                pname = getattr(p, "name", None)
                pt = self._type_from_decl(p)
                params.append(VarSymbol(name = pname, typ = pt, pos = _pos(p), is_const = False))
            fs.params = params
            self.funcs[fname] = fs

            self.global_scope.define(fs)

    def _check_program(self, program: Program) -> None:
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
                self._declare_var_decl(d, is_global = False)
                self._check_var_decl_init(d)
            elif _class(d) == "SacredDecl":
                self._declare_var_decl(d, is_global = False, force_const = True)
                self._check_sacred_decl_init(d)
            elif _class(d) == "OrdainDecl":
                self._declare_ordain_decl(d, is_global = False)
                self._check_ordain_decl_init(d)
            elif _class(d) == "OrderDecl":
                self._error(d, "Order declarations are not allowed inside functions (if intended, implement it).")

        for s in getattr(f, "body", []) or []:
            self._check_stmt(s)

        dismiss_stmt = getattr(f, "dismiss", None)
        if dismiss_stmt is not None:
            self._check_stmt(dismiss_stmt)

        self.scope = old_scope
        self.current_func = None

    def _type_from_return_type(self, rt: Any) -> Type:
        if rt is None:
            return Type.unknown()
        if isinstance(rt, str):
            return Type.base_t(rt)
        return Type.base_t(str(rt))

    def _type_from_decl(self, node: Any) -> Type:
        tname = getattr(node, "type_name", None)
        base = Type.base_t(tname) if isinstance(tname, str) else Type.base_t(str(tname))

        if base.base == BaseType.UNKNOWN and isinstance(tname, str) and tname:
            base = Type.order(tname)

        dims_list = getattr(node, "dims", None)
        if isinstance(dims_list, list):
            dims = len(dims_list)
        else:
            dims = int(getattr(node, "array_dims", 0) or 0)

        if dims > 0:
            return Type.array(base, dims)
        return base

    def _declare_var_decl(self, decl: Any, is_global: bool, force_const: bool = False) -> None:
        decl_type = Type.base_t(getattr(decl, "type_name", ""))
        if decl_type.base == BaseType.UNKNOWN and isinstance(getattr(decl, "type_name", None), str):
            decl_type = Type.order(getattr(decl, "type_name"))

        is_const = force_const or (_class(decl) == "SacredDecl")
        items = getattr(decl, "items", []) or []

        for it in items:
            name = getattr(it, "name", None)
            if not name:
                self._error(it, "Variable item missing name.")
                continue

            dims = getattr(it, "dims", []) or []
            var_type = Type.array(decl_type, len(dims)) if len(dims) > 0 else decl_type

            if self.scope.resolve_local(name):
                self._error(it, f"Redeclaration of '{name}' in the same scope.")
                continue

            self.scope.define(VarSymbol(name = name, typ = var_type, pos = _pos(it), is_const = is_const))

    def _declare_ordain_decl(self, decl: Any, is_global: bool) -> None:
        order_name = getattr(decl, "name", None)
        if not order_name:
            self._error(decl, "ordain declaration missing order name.")
            return

        order_type = Type.order(order_name)

        items = getattr(decl, "items", []) or []
        for it in items:
            vname = getattr(it, "name", None)
            if not vname:
                self._error(it, "ordain item missing name.")
                continue

            dims = getattr(it, "dims", []) or []
            vtype = Type.array(order_type, len(dims)) if len(dims) > 0 else order_type

            if self.scope.resolve_local(vname):
                self._error(it, f"Redeclaration of '{vname}' in the same scope.")
                continue

            self.scope.define(VarSymbol(name = vname, typ = vtype, pos = _pos(it), is_const = False))

    def _check_var_decl_init(self, decl: Any) -> None:
        decl_type = Type.base_t(getattr(decl, "type_name", ""))
        if decl_type.base == BaseType.UNKNOWN and isinstance(getattr(decl, "type_name", None), str):
            decl_type = Type.order(getattr(decl, "type_name"))

        for it in getattr(decl, "items", []) or []:
            init = getattr(it, "init", None)
            if init is None:
                continue
            t = self._expr_type(init)
            dims = getattr(it, "dims", []) or []
            target_t = Type.array(decl_type, len(dims)) if len(dims) > 0 else decl_type
            if not can_assign(target_t, t):
                self._error(it, f"Cannot assign {t} to {target_t} in initialization of '{getattr(it,'name','?')}'.")

    def _check_sacred_decl_init(self, decl: Any) -> None:
        decl_type = Type.base_t(getattr(decl, "type_name", ""))
        for it in getattr(decl, "items", []) or []:
            val = getattr(it, "value", None)
            if val is None:
                continue
            t = self._expr_type(val)
            if not can_assign(decl_type, t):
                self._error(it, f"Cannot assign {t} to {decl_type} in sacred '{getattr(it,'name','?')}'.")

    def _check_ordain_decl_init(self, decl: Any) -> None:
        for it in getattr(decl, "items", []) or []:
            init = getattr(it, "init", None)
            if init is None:
                continue
            _ = self._expr_type(init)

    def _check_stmt(self, s: Any) -> None:
        k = _class(s)

        if k == "VarDeclStmt":
            decl = getattr(s, "decl", None)
            if decl:
                self._declare_var_decl(decl, is_global = False)
                self._check_var_decl_init(decl)
            return

        if k == "OrdainStmt":
            decl = getattr(s, "decl", None)
            if decl:
                self._declare_ordain_decl(decl, is_global = False)
                self._check_ordain_decl_init(decl)
            return

        if k == "OrderStmt":
            self._error(s, "order statement inside function is not supported in semantics yet.")
            return

        if k == "AssignStmt":
            target = getattr(s, "target", None)
            value = getattr(s, "value", None)
            op = getattr(s, "op", "=")
            t_target = self._lvalue_type(target)
            t_val = self._expr_type(value)

            if op != "=" and not is_numeric(t_target):
                self._error(s, f"Compound assignment '{op}' requires numeric target, got {t_target}.")
            if not can_assign(t_target, t_val):
                self._error(s, f"Cannot assign {t_val} to {t_target}.")
            return

        if k == "IncDecStmt":
            target = getattr(s, "target", None)
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
                self._error(s, f"decree condition must be verity, got {t}.")
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

    def _expr_type(self, e: Any) -> Type:
        if e is None:
            return Type.unknown()

        k = _class(e)

        if k == "LiteralExpr":
            lit_t = (getattr(e, "literal_type", None) or "").lower()

            if lit_t == "int":
                return Type.base_t(BaseType.TALLY)
            if lit_t == "decimal":
                return Type.base_t(BaseType.DIVINE)
            if lit_t == "char":
                return Type.base_t(BaseType.SIGIL)
            if lit_t == "string":
                return Type.base_t(BaseType.SCRIPTURE)
            if lit_t == "bool":
                return Type.base_t(BaseType.VERITY)

            return Type.unknown()

        if k == "ArrayInit":
            items = getattr(e, "items", []) or []
            if not items:
                return Type.unknown()

            elem_types = [self._expr_type(x) for x in items]

            if any(t.base == BaseType.ERROR for t in elem_types):
                return Type.error()

            first = elem_types[0]

            if all(is_numeric(t) for t in elem_types):
                out = Type.base_t(BaseType.TALLY)
                for t in elem_types:
                    if t.is_base(BaseType.DIVINE):
                        out = Type.base_t(BaseType.DIVINE)
                        break
                return Type.array(out, 1)

            if all(str(t) == str(first) for t in elem_types):
                return Type.array(first, 1)

            self._error(e, f"Inconsistent array initializer types: {', '.join(str(t) for t in elem_types)}")
            return Type.error()

        if k == "GroupExpr":
            inner = getattr(e, "expr", None)
            return self._expr_type(inner)

        if k == "VarExpr":
            ref = getattr(e, "ref", None)
            return self._lvalue_type(ref)

        if k == "CallExpr":
            callee = getattr(e, "callee", None)
            args = getattr(e, "args", []) or []
            return self._check_call(callee, args, e)

        if k == "VerseOfExpr":
            inner = getattr(e, "expr", None)
            _ = self._expr_type(inner)
            return Type.base_t(BaseType.SCRIPTURE)

        if k == "UnaryExpr":
            op = getattr(e, "op", "") or ""
            operand = getattr(e, "operand", None)
            t = self._expr_type(operand)
            r = result_of_unary(op, t)
            if r.base == BaseType.ERROR:
                self._error(e, f"Invalid unary op '{op}' for type {t}.")
            return r

        if k == "BinaryExpr":
            op = getattr(e, "op", "") or ""
            left = getattr(e, "left", None)
            right = getattr(e, "right", None)
            lt = self._expr_type(left)
            rt = self._expr_type(right)
            r = result_of_binary(op, lt, rt)
            if r.base == BaseType.ERROR:
                self._error(e, f"Invalid binary op '{op}' for types {lt} and {rt}.")
                return Type.error()
            return r

        if k == "IdentifierRef":
            name = getattr(e, "name", None)
            sym = self.scope.resolve(name) if name else None
            if isinstance(sym, VarSymbol):
                return sym.typ
            self._error(e, f"Undeclared identifier '{name}'.")
            return Type.error()

        return Type.unknown()

    def _lvalue_type(self, lv: Any) -> Type:
        if lv is None:
            return Type.unknown()

        k = _class(lv)

        if k == "NameRef":
            name = getattr(lv, "name", None)
            sym = self.scope.resolve(name) if name else None
            if isinstance(sym, VarSymbol):
                return sym.typ
            self._error(lv, f"Undeclared identifier '{name}'.")
            return Type.error()

        if k == "IndexRef":
            base = getattr(lv, "base", None)
            idx = getattr(lv, "index", None)

            bt = self._lvalue_type(base)
            it = self._expr_type(idx)

            if not is_numeric(it):
                self._error(lv, f"Array index must be numeric, got {it}.")

            if bt.is_base(BaseType.SCRIPTURE):
                return Type.base_t(BaseType.SIGIL)

            if not bt.is_array():
                self._error(lv, f"Cannot index non-array type {bt}.")
                return Type.error()
            return bt.array_of or Type.error()

        if k == "MemberRef":
            base = getattr(lv, "base", None)
            mem = getattr(lv, "member", None)
            bt = self._lvalue_type(base)
            if not bt.is_order():
                self._error(lv, f"Member access '.{mem}' on non-order type {bt}.")
                return Type.error()
            order = self.orders.get(bt.order_name or "")
            if order is None:
                self._error(lv, f"Unknown order type '{bt.order_name}'.")
                return Type.error()
            ms = order.members.get(mem)
            if ms is None:
                self._error(lv, f"Order '{order.name}' has no member '{mem}'.")
                return Type.error()
            return ms.typ

        return self._expr_type(lv)

    def _check_call(self, callee: str, args: List[Any], node: Any) -> Type:
        if not callee:
            self._error(node, "Call missing callee.")
            return Type.error()

        fs = self.funcs.get(callee)
        if fs is None:
            self._error(node, f"Call to undeclared function '{callee}'.")
            return Type.error()

        if len(args) != len(fs.params):
            self._error(node, f"Function '{callee}' expects {len(fs.params)} args, got {len(args)}.")

        n = min(len(args), len(fs.params))
        for i in range(n):
            at = self._expr_type(args[i])
            pt = fs.params[i].typ
            if not can_assign(pt, at):
                self._error(node, f"Arg {i + 1} of '{callee}': cannot pass {at} to {pt}.")

        return fs.return_type