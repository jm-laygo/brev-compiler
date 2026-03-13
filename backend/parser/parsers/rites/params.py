from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_param_list_opt(self: Parser) -> List[Param]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_list_opt>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    return self.parse_param_list()


def parse_param_list(self: Parser) -> List[Param]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_list>"].keys()),
        )

    parameter_list = [self.parse_param()]
    parameter_list.extend(self.parse_param_list_tail())
    return parameter_list


def parse_param_list_tail(self: Parser) -> List[Param]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_list_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_parameters = [self.parse_param()]
    remaining_parameters.extend(self.parse_param_list_tail())
    return remaining_parameters


def parse_param(self: Parser) -> Param:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param>"].keys()),
        )

    type_name = self.parse_data_type_id()
    identifier_token = self.expect(TK_IDENTIFIER)
    dims = self.parse_param_array_tail()

    return Param(
        pos=_tok_pos(identifier_token),
        type_name=type_name,
        name=_tok_lexeme(identifier_token),
        dims=dims
    )


def parse_param_array_tail(self: Parser) -> List[Optional[Expr]]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_array_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_array_tail>"].keys()),
        )

    dims: List[Optional[Expr]] = []

    while self.current_type(0) == TK_SYM_OPBRACK:
        self.expect(TK_SYM_OPBRACK)
        dim_expr = self.parse_param_dim_expr_opt()
        self.expect(TK_SYM_CLSBRACK)
        dims.append(dim_expr)

    return dims


def parse_param_dim_expr_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_dim_expr_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_dim_expr_opt>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSBRACK:
        return None

    return self.parse_expr()


Parser.parse_param_list_opt = parse_param_list_opt
Parser.parse_param_list = parse_param_list
Parser.parse_param_list_tail = parse_param_list_tail
Parser.parse_param = parse_param
Parser.parse_param_array_tail = parse_param_array_tail
Parser.parse_param_dim_expr_opt = parse_param_dim_expr_opt
