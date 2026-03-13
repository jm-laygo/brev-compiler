from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<expr>"].keys())
        )

    return self.parse_logic_or()


def parse_logic_or(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<logic_or>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<logic_or>"].keys())
        )

    left_expr = self.parse_logic_and()

    while self.current_type(0) == TK_OP_OR:
        operator_token = self.advance()
        right_expr = self.parse_logic_and()
        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=_tok_lexeme(operator_token) or "or",
            right=right_expr
        )

    return left_expr


def parse_logic_and(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<logic_and>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<logic_and>"].keys())
        )

    left_expr = self.parse_equality()

    while self.current_type(0) == TK_OP_AND:
        operator_token = self.advance()
        right_expr = self.parse_equality()
        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=_tok_lexeme(operator_token) or "and",
            right=right_expr
        )

    return left_expr


def parse_equality(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<equality>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<equality>"].keys())
        )

    left_expr = self.parse_relational()

    while self.current_type(0) in (TK_OP_EQ, TK_OP_NOT_EQ):
        operator_token = self.advance()
        right_expr = self.parse_relational()
        operator_lexeme = _tok_lexeme(operator_token) or (
            "==" if operator_token.type == TK_OP_EQ else "!="
        )
        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=operator_lexeme,
            right=right_expr
        )

    return left_expr


def parse_relational(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<relational>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<relational>"].keys())
        )

    left_expr = self.parse_arith_expr()

    while self.current_type(0) in (TK_OP_GT, TK_OP_LT, TK_OP_GTE, TK_OP_LTE):
        operator_token = self.advance()
        right_expr = self.parse_arith_expr()
        operator_lexeme = _tok_lexeme(operator_token) or {
            TK_OP_GT: ">",
            TK_OP_LT: "<",
            TK_OP_GTE: ">=",
            TK_OP_LTE: "<=",
        }.get(operator_token.type, str(operator_token.type))

        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=operator_lexeme,
            right=right_expr
        )

    return left_expr


def parse_arith_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<arith_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<arith_expr>"].keys())
        )

    left_expr = self.parse_mul_expr()

    while self.current_type(0) in (TK_OP_PLUS, TK_OP_MINUS, TK_OP_CONCAT):
        operator_token = self.advance()
        right_expr = self.parse_mul_expr()
        operator_lexeme = _tok_lexeme(operator_token) or {
            TK_OP_PLUS: "+",
            TK_OP_MINUS: "-",
            TK_OP_CONCAT: "&",
        }.get(operator_token.type, str(operator_token.type))

        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=operator_lexeme,
            right=right_expr
        )

    return left_expr


def parse_mul_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<mul_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<mul_expr>"].keys())
        )

    left_expr = self.parse_pow_expr()

    while self.current_type(0) in (TK_OP_MUL, TK_OP_DIV, TK_OP_MOD):
        operator_token = self.advance()
        right_expr = self.parse_pow_expr()
        operator_lexeme = _tok_lexeme(operator_token) or {
            TK_OP_MUL: "*",
            TK_OP_DIV: "/",
            TK_OP_MOD: "%",
        }.get(operator_token.type, str(operator_token.type))

        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=operator_lexeme,
            right=right_expr
        )

    return left_expr


def parse_pow_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<pow_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<pow_expr>"].keys())
        )

    left_expr = self.parse_unary_expr()

    if self.current_type(0) == TK_OP_POW:
        operator_token = self.advance()
        right_expr = self.parse_pow_expr()
        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=_tok_lexeme(operator_token) or "^",
            right=right_expr
        )

    return left_expr


Parser.parse_expr = parse_expr
Parser.parse_logic_or = parse_logic_or
Parser.parse_logic_and = parse_logic_and
Parser.parse_equality = parse_equality
Parser.parse_relational = parse_relational
Parser.parse_arith_expr = parse_arith_expr
Parser.parse_mul_expr = parse_mul_expr
Parser.parse_pow_expr = parse_pow_expr
