from __future__ import annotations
from typing import Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_loop_stmt(self: Parser) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<loop_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<loop_stmt>"].keys())
        )

    if lookahead_type == TK_CF_PROCESSION:
        return self.parse_procession_stmt()

    if lookahead_type == TK_CF_ENDURE:
        return self.parse_endure_stmt()

    return self.parse_ritual_stmt()


def parse_procession_stmt(self: Parser) -> ProcessionStmt:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<procession_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<procession_stmt>"].keys())
        )

    procession_token = self.expect(TK_CF_PROCESSION)
    self.expect(TK_SYM_OPPAREN)

    init_statement = self.parse_init_opt()
    self.expect(TK_SYM_SEMICOL)
    condition_expression = self.parse_expr_opt()
    self.expect(TK_SYM_SEMICOL)
    update_statement = self.parse_update_opt()
    self.expect(TK_SYM_CLSPAREN)

    self.expect(TK_SYM_OPBRACE)
    body_statements = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)

    return ProcessionStmt(
        pos=_tok_pos(procession_token),
        init=init_statement,
        condition=condition_expression,
        update=update_statement,
        body=body_statements
    )


def parse_init_opt(self: Parser) -> Optional[Statement]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<init_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<init_opt>"].keys())
        )

    if PREDICT["<init_opt>"][lookahead_type] == [EPSILON]:
        return None

    if lookahead_type in (
        TK_DTYPE_TALLY,
        TK_DTYPE_DIVINE,
        TK_DTYPE_SIGIL,
        TK_DTYPE_SCRIPTURE,
        TK_DTYPE_VERITY
    ):
        type_name = self.parse_data_type()
        identifier_token = self.expect(TK_IDENTIFIER)
        self.expect(TK_OP_ASSIGN)
        value_expression = self.parse_expr()

        declaration_node = VarDecl(
            pos=_tok_pos(identifier_token),
            type_name=type_name,
            items=[
                VarItem(
                    pos=_tok_pos(identifier_token),
                    name=_tok_lexeme(identifier_token),
                    dims=[],
                    init=value_expression
                )
            ],
        )

        return VarDeclStmt(pos=declaration_node.pos, decl=declaration_node)

    target_reference = self.parse_lvalue()
    self.expect(TK_OP_ASSIGN)
    value_expression = self.parse_expr()

    return AssignStmt(
        pos=_tok_pos(self.peek(-1)),
        target=target_reference,
        op="=",
        value=value_expression
    )


def parse_expr_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<expr_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<expr_opt>"].keys())
        )

    if PREDICT["<expr_opt>"][lookahead_type] == [EPSILON]:
        return None

    return self.parse_expr()


def parse_update_opt(self: Parser) -> Optional[Statement]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<update_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<update_opt>"].keys())
        )

    if PREDICT["<update_opt>"][lookahead_type] == [EPSILON]:
        return None

    return self.parse_update_expr()


def parse_update_expr(self: Parser) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<update_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<update_expr>"].keys())
        )

    if lookahead_type == TK_OP_INC:
        operator_token = self.expect(TK_OP_INC)
        target_reference = self.parse_lvalue_core()
        return IncDecStmt(pos=_tok_pos(operator_token), target=target_reference, op="++", prefix=True)

    if lookahead_type == TK_OP_DEC:
        operator_token = self.expect(TK_OP_DEC)
        target_reference = self.parse_lvalue_core()
        return IncDecStmt(pos=_tok_pos(operator_token), target=target_reference, op="--", prefix=True)

    if lookahead_type == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        inner_statement = self.parse_update_expr()
        self.expect(TK_SYM_CLSPAREN)
        return inner_statement

    target_reference = self.parse_lvalue()
    return self.parse_update_tail(target_reference)


def parse_update_tail(self: Parser, target_reference: LValue) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<update_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<update_tail>"].keys())
        )

    if lookahead_type == TK_OP_INC:
        operator_token = self.expect(TK_OP_INC)
        return IncDecStmt(pos=_tok_pos(operator_token), target=target_reference, op="++", prefix=False)

    if lookahead_type == TK_OP_DEC:
        operator_token = self.expect(TK_OP_DEC)
        return IncDecStmt(pos=_tok_pos(operator_token), target=target_reference, op="--", prefix=False)

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

        return AssignStmt(
            pos=_tok_pos(operator_token),
            target=target_reference,
            op=operator_lexeme,
            value=value_expression
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=[
            TK_OP_INC,
            TK_OP_DEC,
            TK_OP_ASSIGN,
            TK_OP_PLUS_EQ,
            TK_OP_MINUS_EQ,
            TK_OP_MUL_EQ,
            TK_OP_DIV_EQ,
            TK_OP_MOD_EQ,
            TK_OP_POW_EQ
        ]
    )


def parse_endure_stmt(self: Parser) -> EndureStmt:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<endure_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<endure_stmt>"].keys())
        )

    endure_token = self.expect(TK_CF_ENDURE)
    self.expect(TK_SYM_OPPAREN)
    condition_expression = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    body_statements = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)

    return EndureStmt(
        pos=_tok_pos(endure_token),
        condition=condition_expression,
        body=body_statements
    )


def parse_ritual_stmt(self: Parser) -> RitualStmt:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ritual_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ritual_stmt>"].keys())
        )

    ritual_token = self.expect(TK_CF_RITUAL)
    self.expect(TK_SYM_OPBRACE)
    body_statements = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)
    self.expect(TK_CF_ENDURE)
    self.expect(TK_SYM_OPPAREN)
    condition_expression = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_SEMICOL)

    return RitualStmt(
        pos=_tok_pos(ritual_token),
        body=body_statements,
        condition=condition_expression
    )


Parser.parse_loop_stmt = parse_loop_stmt
Parser.parse_procession_stmt = parse_procession_stmt
Parser.parse_init_opt = parse_init_opt
Parser.parse_expr_opt = parse_expr_opt
Parser.parse_update_opt = parse_update_opt
Parser.parse_update_expr = parse_update_expr
Parser.parse_update_tail = parse_update_tail
Parser.parse_endure_stmt = parse_endure_stmt
Parser.parse_ritual_stmt = parse_ritual_stmt
