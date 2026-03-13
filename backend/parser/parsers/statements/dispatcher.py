from __future__ import annotations
from typing import List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_statement_list(self: Parser) -> List[Statement]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<statement_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<statement_list>"].keys())
        )

    if PREDICT["<statement_list>"][lookahead_type] == [EPSILON]:
        return []

    statement_list: List[Statement] = []

    while True:
        lookahead_type = self.current_type(0)

        if lookahead_type == TK_SYM_CLSBRACE:
            break

        if lookahead_type in PREDICT["<statement_list>"] and PREDICT["<statement_list>"][lookahead_type] == [EPSILON]:
            break

        statement_list.append(self.parse_statement())

    return statement_list


def parse_statement(self: Parser) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<statement>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<statement>"].keys())
        )

    if lookahead_type in (
        TK_DTYPE_TALLY,
        TK_DTYPE_DIVINE,
        TK_DTYPE_SIGIL,
        TK_DTYPE_SCRIPTURE,
        TK_DTYPE_VERITY,
        TK_OTHERS_ORDAIN,
        TK_OTHERS_ORDER,
    ):
        return self.parse_declaration_stmt()

    if lookahead_type in (TK_IO_RECEIVE, TK_IO_PROCLAIM):
        return self.parse_io_stmt()

    if lookahead_type in (TK_CF_DECREE, TK_CF_DISCERN):
        return self.parse_cond_stmt()

    if lookahead_type in (TK_CF_PROCESSION, TK_CF_ENDURE, TK_CF_RITUAL):
        return self.parse_loop_stmt()

    if lookahead_type in (TK_CF_DISMISS, TK_CF_PROCEED, TK_CF_FALL, TK_CF_ABSOLVE):
        return self.parse_jump_stmt()

    if lookahead_type in (TK_OP_INC, TK_OP_DEC):
        return self.parse_prefix_incdec_stmt()

    if lookahead_type == TK_SYM_OPPAREN:
        return self.parse_paren_postfix_incdec_stmt()

    if lookahead_type == TK_IDENTIFIER:
        identifier_token = self.expect(TK_IDENTIFIER)
        identifier_name = _tok_lexeme(identifier_token)
        return self.parse_stmt_id_tail(identifier_token, identifier_name)

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=list(PREDICT["<statement>"].keys())
    )


Parser.parse_statement_list = parse_statement_list
Parser.parse_statement = parse_statement
