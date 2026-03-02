from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.ast.ast_nodes import LValue, NameRef, IndexRef, MemberRef, Expr


class LValuesMixin:
    # ---------- lvalues ----------
    def parse_lvalue(self) -> LValue:
        """
        lvalue: IDENTIFIER access_chain_opt
        """
        id_tok = self.match(TK_IDENTIFIER)
        base: LValue = NameRef(name=id_tok.value, pos=id_tok.pos)
        return self.parse_access_chain(base)

    def parse_lvalue_core(self) -> LValue:
        """
        lvalue_core:
          - lvalue
          - '(' lvalue_core ')'
        """
        if self.at(TK_IDENTIFIER):
            return self.parse_lvalue()

        if self.accept(TK_SYM_OPPAREN):
            inner = self.parse_lvalue_core()
            self.match(TK_SYM_CLSPAREN)
            return inner

        raise ParserError(self.peek(), expected=[TK_IDENTIFIER, TK_SYM_OPPAREN], details="Expected lvalue")

    def parse_access_chain(self, base: LValue) -> LValue:
        """
        access_chain:
          ( '[' expr ']' | '.' IDENTIFIER )*
        """
        while True:
            if self.accept(TK_SYM_OPBRACK):
                idx: Expr = self.parse_expr()
                self.match(TK_SYM_CLSBRACK)
                base = IndexRef(base=base, index=idx, pos=getattr(base, "pos", None))
                continue

            if self.accept(TK_SYM_DOT):
                mem_tok = self.match(TK_IDENTIFIER)
                base = MemberRef(base=base, member=mem_tok.value, pos=mem_tok.pos)
                continue

            break

        return base