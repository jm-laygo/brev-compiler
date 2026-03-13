from __future__ import annotations
from typing import Any

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_unary_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<unary_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<unary_expr>"].keys())
        )

    if lookahead_type in (TK_OP_NOT, TK_OP_TILDE):
        operator_token = self.advance()
        operand_expr = self.parse_unary_expr()
        operator_lexeme = _tok_lexeme(operator_token) or (
            "!" if lookahead_type == TK_OP_NOT else "~"
        )
        return UnaryExpr(
            pos=_tok_pos(operator_token),
            op=operator_lexeme,
            operand=operand_expr,
            prefix=True
        )

    if lookahead_type in (TK_OP_INC, TK_OP_DEC):
        operator_token = self.advance()
        target_reference = self.parse_lvalue_core()
        return UnaryExpr(
            pos=_tok_pos(operator_token),
            op=_tok_lexeme(operator_token) or (
                "++" if lookahead_type == TK_OP_INC else "--"
            ),
            operand=VarExpr(pos=_tok_pos(operator_token), ref=target_reference),
            prefix=True,
        )

    return self.parse_postfix_expr()


def parse_postfix_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<postfix_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<postfix_expr>"].keys())
        )

    base_expr = self.parse_primary()

    if self.current_type(0) in (TK_OP_INC, TK_OP_DEC):
        operator_token = self.advance()
        operator_lexeme = _tok_lexeme(operator_token) or (
            "++" if operator_token.type == TK_OP_INC else "--"
        )
        return UnaryExpr(
            pos=_tok_pos(operator_token),
            op=operator_lexeme,
            operand=base_expr,
            prefix=False
        )

    return base_expr


def parse_primary(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<primary>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<primary>"].keys())
        )

    if lookahead_type in (
        TK_LIT_INT,
        TK_LIT_DECIMAL,
        TK_LIT_CHAR,
        TK_LIT_STRING,
        TK_LIT_BOOL
    ):
        return self.parse_literal_expr()

    if lookahead_type == TK_SYM_OPPAREN:
        opening_paren_token = self.expect(TK_SYM_OPPAREN)
        inner_expr = self.parse_expr()
        self.expect(TK_SYM_CLSPAREN)
        return GroupExpr(pos=_tok_pos(opening_paren_token), expr=inner_expr)

    if lookahead_type == TK_OTHERS_VERSEOF:
        verseof_token = self.expect(TK_OTHERS_VERSEOF)
        self.expect(TK_SYM_OPPAREN)
        inner_expr = self.parse_expr()
        self.expect(TK_SYM_CLSPAREN)
        return VerseOfExpr(pos=_tok_pos(verseof_token), expr=inner_expr)

    if lookahead_type == TK_IDENTIFIER:
        identifier_token = self.expect(TK_IDENTIFIER)
        identifier_name = _tok_lexeme(identifier_token)
        return self.parse_id_primary_tail(identifier_token, identifier_name)

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=list(PREDICT["<primary>"].keys())
    )


def parse_id_primary_tail(self: Parser, identifier_token: Any, identifier_name: str) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<id_primary_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<id_primary_tail>"].keys())
        )

    if lookahead_type == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        argument_list = self.parse_arg_list_opt()
        self.expect(TK_SYM_CLSPAREN)

        base_reference = NameRef(pos=_tok_pos(identifier_token), name=identifier_name)
        access_chain = self.parse_access_chain_opt(base_reference)

        return CallExpr(
            pos=_tok_pos(identifier_token),
            callee=identifier_name,
            args=argument_list,
            access=access_chain
        )

    base_reference: LValue = NameRef(pos=_tok_pos(identifier_token), name=identifier_name)
    access_chain = self.parse_access_chain_opt(base_reference)
    resolved_reference = access_chain if access_chain is not None else base_reference
    return VarExpr(pos=_tok_pos(identifier_token), ref=resolved_reference)


Parser.parse_unary_expr = parse_unary_expr
Parser.parse_postfix_expr = parse_postfix_expr
Parser.parse_primary = parse_primary
Parser.parse_id_primary_tail = parse_id_primary_tail
