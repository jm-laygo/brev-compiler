from __future__ import annotations
from typing import Any, List
from backend.semantic.typesys import BaseType, Type
from backend.semantic.symbols import VarSymbol, FuncSymbol, OrderSymbol, MemberSymbol
from .helpers import _class, _pos

class DeclarationsMixin:
    def _declare_globals(self, program: Any) -> None:
        for g in getattr(program, "globals", []) or []:
            k = _class(g)
            if k in ("VarDecl", "SacredDecl"):
                self._declare_var_decl(g, is_global=True)
            elif k == "OrdainDecl":
                self._declare_ordain_decl(g, is_global=True)
            elif k == "OrderDecl":
                continue
            else:
                continue

    def _declare_orders(self, program: Any) -> None:
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

            sym = OrderSymbol(name=order_name, typ=Type.order(order_name), pos=_pos(g))

            for m in getattr(g, "members", []) or []:
                mem_name = getattr(m, "name", None)
                if not mem_name:
                    self._error(m, f"Order '{order_name}' member missing name.")
                    continue
                if mem_name in sym.members:
                    self._error(m, f"Duplicate member '{mem_name}' in order '{order_name}'.")
                    continue

                mem_type = self._type_from_decl(m)  # from TypeBuildersMixin
                sym.members[mem_name] = MemberSymbol(name=mem_name, typ=mem_type, pos=_pos(m))

            self.orders[order_name] = sym

    def _declare_functions(self, program: Any) -> None:
        all_funcs: List[Any] = []
        entry = getattr(program, "entry", None)
        if entry is not None:
            all_funcs.append(entry)
        all_funcs.extend(getattr(program, "functions", []) or [])

        for f in all_funcs:
            if f is None or _class(f) != "RiteDecl":
                continue

            fname = getattr(f, "name", None)
            if not fname:
                self._error(f, "Function missing name.")
                continue
            if fname in self.funcs:
                self._error(f, f"Function '{fname}' already declared.")
                continue

            ret_t = self._type_from_return_type(getattr(f, "return_type", None))
            fs = FuncSymbol(name=fname, typ=Type.unknown(), return_type=ret_t, pos=_pos(f))

            params: List[VarSymbol] = []
            for p in getattr(f, "params", []) or []:
                pname = getattr(p, "name", None)
                pt = self._type_from_decl(p)
                params.append(VarSymbol(name=pname, typ=pt, pos=_pos(p), is_const=False))

            fs.params = params
            self.funcs[fname] = fs
            self.global_scope.define(fs)

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

            self.scope.define(
                VarSymbol(name=name, typ=var_type, pos=_pos(it), is_const=is_const)
            )

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

            self.scope.define(
                VarSymbol(name=vname, typ=vtype, pos=_pos(it), is_const=False)
            )