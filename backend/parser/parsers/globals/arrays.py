from __future__ import annotations
from typing import List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_pos


def parse_array_dims_tail(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_dims_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_dims_tail>"].keys()),
        )

    if PREDICT["<array_dims_tail>"][lookahead_type] == [EPSILON]:
        return []

    self.expect(TK_SYM_OPBRACK)
    dimension_expr = self.parse_expr()
    self.expect(TK_SYM_CLSBRACK)
    remaining_dimensions = self.parse_array_dims_tail()
    return [dimension_expr] + remaining_dimensions


def parse_array_init(self: Parser) -> ArrayInit:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_init>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_init>"].keys()),
        )

    opening_brace_token = self.expect(TK_SYM_OPBRACE)
    array_items = self.parse_array_vals_opt()
    self.expect(TK_SYM_CLSBRACE)

    return ArrayInit(
        pos=_tok_pos(opening_brace_token),
        items=array_items
    )


def parse_array_vals_opt(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_vals_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_vals_opt>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSBRACE:
        return []

    return self.parse_array_vals()


def parse_array_vals(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_vals>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_vals>"].keys()),
        )

    array_values = [self.parse_array_val()]
    array_values.extend(self.parse_array_vals_tail())
    return array_values


def parse_array_vals_tail(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_vals_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_vals_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSBRACE:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_array_values = [self.parse_array_val()]
    remaining_array_values.extend(self.parse_array_vals_tail())
    return remaining_array_values


def parse_array_val(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_val>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_val>"].keys()),
        )

    if lookahead_type == TK_SYM_OPBRACE:
        opening_brace_token = self.expect(TK_SYM_OPBRACE)
        nested_array_items = self.parse_array_vals_opt()
        self.expect(TK_SYM_CLSBRACE)
        return ArrayInit(
            pos=_tok_pos(opening_brace_token),
            items=nested_array_items
        )

    return self.parse_expr()


Parser.parse_array_dims_tail = parse_array_dims_tail
Parser.parse_array_init = parse_array_init
Parser.parse_array_vals_opt = parse_array_vals_opt
Parser.parse_array_vals = parse_array_vals
Parser.parse_array_vals_tail = parse_array_vals_tail
Parser.parse_array_val = parse_array_val
