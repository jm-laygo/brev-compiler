from __future__ import annotations
from typing import Any

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_prefix_incdec_stmt(self: Parser) -> IncDecStmt:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<prefix_incdec_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<prefix_incdec_stmt>"].keys())
        )

    operator_token = self.advance()
    operator_lexeme = _tok_lexeme(operator_token) or ("++" if operator_token.type == TK_OP_INC else "--")
    target_reference = self.parse_lvalue_core()
    self.expect(TK_SYM_SEMICOL)

    return IncDecStmt(
        pos=_tok_pos(operator_token),
        target=target_reference,
        op=operator_lexeme,
        prefix=True
    )


def parse_paren_postfix_incdec_stmt(self: Parser) -> IncDecStmt:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<paren_postfix_incdec_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<paren_postfix_incdec_stmt>"].keys())
        )

    opening_paren_token = self.expect(TK_SYM_OPPAREN)
    target_reference = self.parse_lvalue_core()
    self.expect(TK_SYM_CLSPAREN)

    if self.current_type(0) not in (TK_OP_INC, TK_OP_DEC):
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=[TK_OP_INC, TK_OP_DEC]
        )

    operator_token = self.advance()
    operator_lexeme = _tok_lexeme(operator_token) or ("++" if operator_token.type == TK_OP_INC else "--")
    self.expect(TK_SYM_SEMICOL)

    return IncDecStmt(
        pos=_tok_pos(opening_paren_token),
        target=target_reference,
        op=operator_lexeme,
        prefix=False
    )


def parse_stmt_id_tail(self: Parser, identifier_token: Any, identifier_name: str) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<stmt_id_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<stmt_id_tail>"].keys())
        )

    if lookahead_type == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        argument_list = self.parse_arg_list_opt()
        self.expect(TK_SYM_CLSPAREN)
        access_reference = self.parse_access_chain_opt(
            base_reference=NameRef(pos=_tok_pos(identifier_token), name=identifier_name)
        )
        self.expect(TK_SYM_SEMICOL)

        return CallStmt(
            pos=_tok_pos(identifier_token),
            callee=identifier_name,
            args=argument_list,
            access=access_reference
        )

    base_reference: LValue = NameRef(pos=_tok_pos(identifier_token), name=identifier_name)
    access_reference = self.parse_access_chain_opt(base_reference=base_reference)
    target_reference = access_reference if access_reference is not None else base_reference

    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<stmt_after_access>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<stmt_after_access>"].keys())
        )

    if lookahead_type in (
        TK_OP_ASSIGN,
        TK_OP_PLUS_EQ,
        TK_OP_MINUS_EQ,
        TK_OP_MUL_EQ,
        TK_OP_DIV_EQ,
        TK_OP_MOD_EQ,
        TK_OP_POW_EQ
    ):
        operator_token = self.advance()
        operator_lexeme = _tok_lexeme(operator_token) or self._assign_op_string(operator_token.type)
        value_expression = self.parse_expr()
        self.expect(TK_SYM_SEMICOL)

        return AssignStmt(
            pos=_tok_pos(operator_token),
            target=target_reference,
            op=operator_lexeme,
            value=value_expression
        )

    if lookahead_type in (TK_OP_INC, TK_OP_DEC):
        operator_token = self.advance()
        operator_lexeme = _tok_lexeme(operator_token) or ("++" if operator_token.type == TK_OP_INC else "--")
        self.expect(TK_SYM_SEMICOL)

        return IncDecStmt(
            pos=_tok_pos(operator_token),
            target=target_reference,
            op=operator_lexeme,
            prefix=False
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=list(PREDICT["<stmt_after_access>"].keys())
    )


def _assign_op_string(self: Parser, token_type: Any) -> str:
    return {
        TK_OP_ASSIGN: "=",
        TK_OP_PLUS_EQ: "+=",
        TK_OP_MINUS_EQ: "-=",
        TK_OP_MUL_EQ: "*=",
        TK_OP_DIV_EQ: "/=",
        TK_OP_MOD_EQ: "%=",
        TK_OP_POW_EQ: "^=",
    }.get(token_type, str(token_type))


Parser.parse_prefix_incdec_stmt = parse_prefix_incdec_stmt
Parser.parse_paren_postfix_incdec_stmt = parse_paren_postfix_incdec_stmt
Parser.parse_stmt_id_tail = parse_stmt_id_tail
Parser._assign_op_string = _assign_op_string
