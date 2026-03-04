from __future__ import annotations
from typing import Any, List
from backend.semantic.typesys import (
    BaseType,
    Type,
    can_assign,
    is_numeric,
    result_of_unary,
    result_of_binary,
)
from .helpers import _class

class ExpressionsMixin:
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

            elem_types: List[Type] = [self._expr_type(x) for x in items]

            if any(t.base == BaseType.ERROR for t in elem_types):
                return Type.error()

            first = elem_types[0]

            # numeric promotion: any DIVINE => DIVINE else TALLY
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

            if self._has_type_error(t):
                return Type.error()

            r = result_of_unary(op, t)
            if self._has_type_error(r):
                self._error(e, f"Invalid unary op '{op}' for type {self._tname(t)}.")
            return r

        if k == "BinaryExpr":
            op = getattr(e, "op", "") or ""
            left = getattr(e, "left", None)
            right = getattr(e, "right", None)

            lt = self._expr_type(left)
            rt = self._expr_type(right)

            if self._has_type_error(lt) or self._has_type_error(rt):
                return Type.error()

            r = result_of_binary(op, lt, rt)
            if self._has_type_error(r):
                self._error(e, f"Invalid binary op '{op}' for types {self._tname(lt)} and {self._tname(rt)}.")
                return Type.error()
            return r

        if k == "IdentifierRef":
            name = getattr(e, "name", None)
            sym = self.scope.resolve(name) if name else None
            from backend.semantic.symbols import VarSymbol
            if isinstance(sym, VarSymbol):
                return sym.typ

            hint = self._did_you_mean(name)
            self._error(e, f"Undeclared identifier '{name}'.{hint}")
            return Type.error()

        return Type.unknown()