from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_var_decl_group(self: Parser) -> List[VarItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_decl_group>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_decl_group>"].keys()),
        )

    variable_items = [self.parse_var_decl_item()]
    variable_items.extend(self.parse_var_decl_tail())
    return variable_items


def parse_var_decl_tail(self: Parser) -> List[VarItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_decl_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_decl_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_variable_items = [self.parse_var_decl_item()]
    remaining_variable_items.extend(self.parse_var_decl_tail())
    return remaining_variable_items


def parse_var_decl_item(self: Parser) -> VarItem:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_decl_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_decl_item>"].keys()),
        )

    variable_name_token = self.expect(TK_IDENTIFIER)
    array_dimensions = self.parse_array_dims_tail()
    initializer = self.parse_var_decl_item_tail()

    return VarItem(
        pos=_tok_pos(variable_name_token),
        name=_tok_lexeme(variable_name_token),
        dims=array_dimensions,
        init=initializer
    )


def parse_var_decl_item_tail(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_decl_item_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_decl_item_tail>"].keys()),
        )

    if lookahead_type in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)
    return self.parse_var_after_eq()


def parse_var_after_eq(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_after_eq>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_after_eq>"].keys()),
        )

    if lookahead_type == TK_SYM_OPBRACE:
        return self.parse_array_init()

    return self.parse_expr()


Parser.parse_var_decl_group = parse_var_decl_group
Parser.parse_var_decl_tail = parse_var_decl_tail
Parser.parse_var_decl_item = parse_var_decl_item
Parser.parse_var_decl_item_tail = parse_var_decl_item_tail
Parser.parse_var_after_eq = parse_var_after_eq
