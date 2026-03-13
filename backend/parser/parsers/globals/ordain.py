from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_ordain_dec_list(self: Parser) -> List[OrdainItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ordain_dec_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ordain_dec_list>"].keys()),
        )

    ordain_items = [self.parse_ordain_dec()]
    ordain_items.extend(self.parse_ordain_dec_tail())
    return ordain_items


def parse_ordain_dec_tail(self: Parser) -> List[OrdainItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ordain_dec_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ordain_dec_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_ordain_items = [self.parse_ordain_dec()]
    remaining_ordain_items.extend(self.parse_ordain_dec_tail())
    return remaining_ordain_items


def parse_ordain_dec(self: Parser) -> OrdainItem:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ordain_dec>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ordain_dec>"].keys()),
        )

    identifier_token = self.expect(TK_IDENTIFIER)
    array_dimensions = self.parse_array_dims_tail()
    initializer = self.parse_ordain_init_opt()

    return OrdainItem(
        pos=_tok_pos(identifier_token),
        name=_tok_lexeme(identifier_token),
        dims=array_dimensions,
        init=initializer
    )


def parse_ordain_init_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ordain_init_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ordain_init_opt>"].keys()),
        )

    if lookahead_type in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)
    return self.parse_expr()


Parser.parse_ordain_dec_list = parse_ordain_dec_list
Parser.parse_ordain_dec_tail = parse_ordain_dec_tail
Parser.parse_ordain_dec = parse_ordain_dec
Parser.parse_ordain_init_opt = parse_ordain_init_opt
