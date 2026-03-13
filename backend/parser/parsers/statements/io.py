from __future__ import annotations
from typing import List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_pos


def parse_io_stmt(self: Parser) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<io_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<io_stmt>"].keys())
        )

    if lookahead_type == TK_IO_RECEIVE:
        receive_token = self.expect(TK_IO_RECEIVE)
        self.expect(TK_SYM_OPPAREN)
        target_reference = self.parse_lvalue()
        self.expect(TK_SYM_CLSPAREN)
        self.expect(TK_SYM_SEMICOL)

        return ReceiveStmt(
            pos=_tok_pos(receive_token),
            target=target_reference
        )

    proclaim_token = self.expect(TK_IO_PROCLAIM)
    self.expect(TK_SYM_OPPAREN)
    output_arguments = self.parse_output_list_opt()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_SEMICOL)

    return ProclaimStmt(
        pos=_tok_pos(proclaim_token),
        args=output_arguments
    )


def parse_output_list_opt(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<output_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<output_list_opt>"].keys())
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    return self.parse_output_list()


def parse_output_list(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<output_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<output_list>"].keys())
        )

    output_arguments = [self.parse_expr()]
    output_arguments.extend(self.parse_output_tail())
    return output_arguments


def parse_output_tail(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<output_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<output_tail>"].keys())
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_output_arguments = [self.parse_expr()]
    remaining_output_arguments.extend(self.parse_output_tail())
    return remaining_output_arguments


Parser.parse_io_stmt = parse_io_stmt
Parser.parse_output_list_opt = parse_output_list_opt
Parser.parse_output_list = parse_output_list
Parser.parse_output_tail = parse_output_tail
