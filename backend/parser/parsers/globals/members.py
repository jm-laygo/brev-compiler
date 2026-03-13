from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_member_list_opt(self: Parser) -> List[OrderMember]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_list_opt>"].keys()),
        )

    if PREDICT["<member_list_opt>"][lookahead_type] == [EPSILON]:
        return []

    return self.parse_member_list()


def parse_member_list(self: Parser) -> List[OrderMember]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_list>"].keys()),
        )

    member_list = [self.parse_member()]
    member_list.extend(self.parse_member_list_tail())
    return member_list


def parse_member_list_tail(self: Parser) -> List[OrderMember]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_list_tail>"].keys()),
        )

    if PREDICT["<member_list_tail>"][lookahead_type] == [EPSILON]:
        return []

    remaining_members = [self.parse_member()]
    remaining_members.extend(self.parse_member_list_tail())
    return remaining_members


def parse_member(self: Parser) -> OrderMember:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member>"].keys()),
        )

    type_name = self.parse_data_type_id()
    member_name_token = self.expect(TK_IDENTIFIER)
    array_dimensions = self.parse_array_dims_tail()
    initializer = self.parse_member_init_opt()
    self.expect(TK_SYM_SEMICOL)

    return OrderMember(
        pos=_tok_pos(member_name_token),
        type_name=type_name,
        name=_tok_lexeme(member_name_token),
        dims=array_dimensions,
        init=initializer
    )


def parse_member_init_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_init_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_init_opt>"].keys()),
        )

    if lookahead_type == TK_SYM_SEMICOL:
        return None

    self.expect(TK_OP_ASSIGN)
    return self.parse_member_init_val()


def parse_member_init_val(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_init_val>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_init_val>"].keys()),
        )

    if lookahead_type == TK_SYM_OPBRACE:
        return self.parse_array_init()

    return self.parse_expr()


Parser.parse_member_list_opt = parse_member_list_opt
Parser.parse_member_list = parse_member_list
Parser.parse_member_list_tail = parse_member_list_tail
Parser.parse_member = parse_member
Parser.parse_member_init_opt = parse_member_init_opt
Parser.parse_member_init_val = parse_member_init_val
