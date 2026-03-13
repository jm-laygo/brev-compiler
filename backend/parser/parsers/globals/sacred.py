from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_sacred_init_list(self: Parser) -> List[SacredItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<sacred_init_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<sacred_init_list>"].keys()),
        )

    sacred_items = [self.parse_sacred_init()]
    sacred_items.extend(self.parse_sacred_init_tail())
    return sacred_items


def parse_sacred_init_tail(self: Parser) -> List[SacredItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<sacred_init_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<sacred_init_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_sacred_items = [self.parse_sacred_init()]
    remaining_sacred_items.extend(self.parse_sacred_init_tail())
    return remaining_sacred_items


def parse_sacred_init(self: Parser) -> SacredItem:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<sacred_init>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<sacred_init>"].keys()),
        )

    identifier_token = self.expect(TK_IDENTIFIER)
    initializer_value = self.parse_sacred_assign_opt()

    return SacredItem(
        pos=_tok_pos(identifier_token),
        name=_tok_lexeme(identifier_token),
        value=initializer_value
    )


def parse_sacred_assign_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<sacred_assign_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<sacred_assign_opt>"].keys()),
        )

    if lookahead_type in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)
    return self.parse_const_expr()


Parser.parse_sacred_init_list = parse_sacred_init_list
Parser.parse_sacred_init_tail = parse_sacred_init_tail
Parser.parse_sacred_init = parse_sacred_init
Parser.parse_sacred_assign_opt = parse_sacred_assign_opt
