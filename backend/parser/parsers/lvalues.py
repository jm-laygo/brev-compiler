from __future__ import annotations
from typing import Optional
from backend.tokens import *
from backend.parser.predict_set import EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# LVALUES / ACCESS
def parse_lvalue(self: Parser) -> LValue:
    self.choose_prod("<lvalue>")
    id_tok = self.expect(TK_IDENTIFIER)
    base: LValue = NameRef(pos=_tok_pos(id_tok), name=_tok_lexeme(id_tok))
    lv = self.parse_access_chain_opt(base=base)
    return lv if lv is not None else base

def parse_lvalue_core(self: Parser) -> LValue:
    self.choose_prod("<lvalue_core>")
    if self.la(0) == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        inner = self.parse_lvalue_core()
        self.expect(TK_SYM_CLSPAREN)
        return inner
    id_tok = self.expect(TK_IDENTIFIER)
    base: LValue = NameRef(pos=_tok_pos(id_tok), name=_tok_lexeme(id_tok))
    lv = self.parse_access_chain_opt(base=base)
    return lv if lv is not None else base

def parse_access_chain_opt(self: Parser, base: LValue) -> Optional[LValue]:
    prod = self.choose_prod("<access_chain_opt>")
    if prod == [EPSILON]:
        return None
    return self.parse_access_chain(base)

def parse_access_chain(self: Parser, base: LValue) -> LValue:
    self.choose_prod("<access_chain>")
    lv = base
    while self.la(0) in (TK_SYM_OPBRACK, TK_SYM_DOT):
        lv = self.parse_access_step(lv)
    return lv

def parse_access_step(self: Parser, base: LValue) -> LValue:
    self.choose_prod("<access_step>")
    if self.la(0) == TK_SYM_OPBRACK:
        lb = self.expect(TK_SYM_OPBRACK)
        idx = self.parse_expr()
        self.expect(TK_SYM_CLSBRACK)
        return IndexRef(pos=_tok_pos(lb), base=base, index=idx)
    dot = self.expect(TK_SYM_DOT)
    mem_tok = self.expect(TK_IDENTIFIER)
    return MemberRef(pos=_tok_pos(dot), base=base, member=_tok_lexeme(mem_tok))

Parser.parse_lvalue = parse_lvalue
Parser.parse_lvalue_core = parse_lvalue_core
Parser.parse_access_chain_opt = parse_access_chain_opt
Parser.parse_access_chain = parse_access_chain
Parser.parse_access_step = parse_access_step