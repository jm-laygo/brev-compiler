from __future__ import annotations
from typing import Optional

from backend.tokens import *
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# LVALUES / ACCESS
def parse_lvalue(self: Parser) -> LValue:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<lvalue>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<lvalue>"].keys())
        )

    identifier_token = self.expect(TK_IDENTIFIER)
    base_reference: LValue = NameRef(
        pos=_tok_pos(identifier_token),
        name=_tok_lexeme(identifier_token)
    )

    access_reference = self.parse_access_chain_opt(base_reference=base_reference)
    return access_reference if access_reference is not None else base_reference

def parse_lvalue_core(self: Parser) -> LValue:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<lvalue_core>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<lvalue_core>"].keys())
        )

    if lookahead_type == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        inner_reference = self.parse_lvalue_core()
        self.expect(TK_SYM_CLSPAREN)
        return inner_reference

    identifier_token = self.expect(TK_IDENTIFIER)
    base_reference: LValue = NameRef(
        pos=_tok_pos(identifier_token),
        name=_tok_lexeme(identifier_token)
    )

    access_reference = self.parse_access_chain_opt(base_reference=base_reference)
    return access_reference if access_reference is not None else base_reference

def parse_access_chain_opt(self: Parser, base_reference: LValue) -> Optional[LValue]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<access_chain_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<access_chain_opt>"].keys())
        )

    if PREDICT["<access_chain_opt>"][lookahead_type] == [EPSILON]:
        return None

    return self.parse_access_chain(base_reference)

def parse_access_chain(self: Parser, base_reference: LValue) -> LValue:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<access_chain>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<access_chain>"].keys())
        )

    current_reference = base_reference

    while self.current_type(0) in (TK_SYM_OPBRACK, TK_SYM_DOT):
        current_reference = self.parse_access_step(current_reference)

    return current_reference

def parse_access_step(self: Parser, base_reference: LValue) -> LValue:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<access_step>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<access_step>"].keys())
        )

    if lookahead_type == TK_SYM_OPBRACK:
        opening_bracket_token = self.expect(TK_SYM_OPBRACK)
        index_expression = self.parse_expr()
        self.expect(TK_SYM_CLSBRACK)

        return IndexRef(
            pos=_tok_pos(opening_bracket_token),
            base=base_reference,
            index=index_expression
        )

    dot_token = self.expect(TK_SYM_DOT)
    member_token = self.expect(TK_IDENTIFIER)

    return MemberRef(
        pos=_tok_pos(dot_token),
        base=base_reference,
        member=_tok_lexeme(member_token)
    )

Parser.parse_lvalue = parse_lvalue
Parser.parse_lvalue_core = parse_lvalue_core
Parser.parse_access_chain_opt = parse_access_chain_opt
Parser.parse_access_chain = parse_access_chain
Parser.parse_access_step = parse_access_step