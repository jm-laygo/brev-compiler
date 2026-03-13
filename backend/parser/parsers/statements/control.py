from __future__ import annotations
from typing import Any, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_pos


def parse_jump_stmt(self: Parser) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<jump_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<jump_stmt>"].keys())
        )

    if lookahead_type == TK_CF_DISMISS:
        dismiss_token = self.expect(TK_CF_DISMISS)
        value_expression = self.parse_expr_opt()
        self.expect(TK_SYM_SEMICOL)
        return DismissStmt(pos=_tok_pos(dismiss_token), value=value_expression)

    if lookahead_type == TK_CF_PROCEED:
        proceed_token = self.expect(TK_CF_PROCEED)
        self.expect(TK_SYM_SEMICOL)
        return ProceedStmt(pos=_tok_pos(proceed_token))

    if lookahead_type == TK_CF_FALL:
        fall_token = self.expect(TK_CF_FALL)
        self.expect(TK_SYM_SEMICOL)
        return FallStmt(pos=_tok_pos(fall_token))

    absolve_token = self.expect(TK_CF_ABSOLVE)
    self.expect(TK_SYM_SEMICOL)
    return AbsolveStmt(pos=_tok_pos(absolve_token))


def parse_dismiss_opt(self: Parser) -> Optional[DismissStmt]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<dismiss_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<dismiss_opt>"].keys())
        )

    if PREDICT["<dismiss_opt>"][lookahead_type] == [EPSILON]:
        return None

    dismiss_token = self.expect(TK_CF_DISMISS)
    value_expression = self.parse_dismiss_tail(dismiss_token)

    return DismissStmt(
        pos=_tok_pos(dismiss_token),
        value=value_expression
    )


def parse_dismiss_tail(self: Parser, dismiss_token: Any) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<dismiss_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<dismiss_tail>"].keys())
        )

    if lookahead_type == TK_SYM_SEMICOL:
        self.expect(TK_SYM_SEMICOL)
        return None

    value_expression = self.parse_expr()
    self.expect(TK_SYM_SEMICOL)
    return value_expression


Parser.parse_jump_stmt = parse_jump_stmt
Parser.parse_dismiss_opt = parse_dismiss_opt
Parser.parse_dismiss_tail = parse_dismiss_tail
