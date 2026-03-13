from __future__ import annotations
from typing import List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser


def parse_arg_list_opt(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<arg_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<arg_list_opt>"].keys())
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    return self.parse_arg_list()


def parse_arg_list(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<arg_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<arg_list>"].keys())
        )

    argument_list = [self.parse_expr()]
    argument_list.extend(self.parse_arg_list_tail())
    return argument_list


def parse_arg_list_tail(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<arg_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<arg_list_tail>"].keys())
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_arguments = [self.parse_expr()]
    remaining_arguments.extend(self.parse_arg_list_tail())
    return remaining_arguments


Parser.parse_arg_list_opt = parse_arg_list_opt
Parser.parse_arg_list = parse_arg_list
Parser.parse_arg_list_tail = parse_arg_list_tail
