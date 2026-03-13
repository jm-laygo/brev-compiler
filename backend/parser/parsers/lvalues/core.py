from __future__ import annotations

from backend.tokens import *
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


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


Parser.parse_lvalue = parse_lvalue
Parser.parse_lvalue_core = parse_lvalue_core