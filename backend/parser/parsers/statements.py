from __future__ import annotations
from typing import Any, List, Optional, Tuple, Union

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# STATEMENTS
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
        TK_DTYPE_VERITY
    ):
        declaration_node = VarDecl(
            pos=_tok_pos(self.peek(0)),
            type_name=self.parse_data_type(),
            items=self.parse_var_decl_group()
        )
        self.expect(TK_SYM_SEMICOL)
        return VarDeclStmt(pos=declaration_node.pos, decl=declaration_node)

    if lookahead_type == TK_OTHERS_ORDAIN:
        ordain_token = self.expect(TK_OTHERS_ORDAIN)
        declaration_name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        declaration_items = self.parse_ordain_dec_list()
        self.expect(TK_SYM_SEMICOL)

        return OrdainStmt(
            pos=_tok_pos(ordain_token),
            decl=OrdainDecl(
                pos=_tok_pos(ordain_token),
                name=declaration_name,
                items=declaration_items
            )
        )

    if lookahead_type == TK_OTHERS_ORDER:
        order_token = self.expect(TK_OTHERS_ORDER)
        declaration_name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        self.expect(TK_SYM_OPBRACE)
        member_list = self.parse_member_list_opt()
        self.expect(TK_SYM_CLSBRACE)
        self.expect(TK_SYM_SEMICOL)

        return OrderStmt(
            pos=_tok_pos(order_token),
            decl=OrderDecl(
                pos=_tok_pos(order_token),
                name=declaration_name,
                members=member_list
            )
        )

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

# IO
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

# CONDITIONS
def parse_cond_stmt(self: Parser) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<cond_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<cond_stmt>"].keys())
        )

    if lookahead_type == TK_CF_DECREE:
        return self.parse_decree_chain()

    return self.parse_discern_stmt()

def parse_decree_chain(self: Parser) -> DecreeStmt:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<decree_chain>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<decree_chain>"].keys())
        )

    decree_token = self.expect(TK_CF_DECREE)
    self.expect(TK_SYM_OPPAREN)
    condition_expression = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    body_statements = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)

    edict_clauses = self.parse_edict_list_opt()
    absolution_clause = self.parse_absolution_opt()

    return DecreeStmt(
        pos=_tok_pos(decree_token),
        expr=condition_expression,
        body=body_statements,
        edicts=edict_clauses,
        absolution=absolution_clause
    )

def parse_edict_list_opt(self: Parser) -> List[EdictClause]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<edict_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<edict_list_opt>"].keys())
        )

    if PREDICT["<edict_list_opt>"][lookahead_type] == [EPSILON]:
        return []

    edict_clauses: List[EdictClause] = []
    while self.current_type(0) == TK_CF_EDICT:
        edict_clauses.append(self.parse_edict())

    return edict_clauses

def parse_edict(self: Parser) -> EdictClause:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<edict>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<edict>"].keys())
        )

    edict_token = self.expect(TK_CF_EDICT)
    self.expect(TK_SYM_OPPAREN)
    condition_expression = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    body_statements = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)

    return EdictClause(
        pos=_tok_pos(edict_token),
        expr=condition_expression,
        body=body_statements
    )

def parse_absolution_opt(self: Parser) -> Optional[AbsolutionClause]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<absolution_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<absolution_opt>"].keys())
        )

    if PREDICT["<absolution_opt>"][lookahead_type] == [EPSILON]:
        return None

    absolution_token = self.expect(TK_CF_ABSOLUTION)
    self.expect(TK_SYM_OPBRACE)
    body_statements = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)

    return AbsolutionClause(
        pos=_tok_pos(absolution_token),
        body=body_statements
    )

def parse_discern_stmt(self: Parser) -> DiscernStmt:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<discern_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<discern_stmt>"].keys())
        )

    discern_token = self.expect(TK_CF_DISCERN)
    self.expect(TK_SYM_OPPAREN)
    condition_expression = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    verse_cases = self.parse_verse_list()
    grace_clause = self.parse_grace_opt()
    self.expect(TK_SYM_CLSBRACE)

    return DiscernStmt(
        pos=_tok_pos(discern_token),
        expr=condition_expression,
        verses=verse_cases,
        grace=grace_clause
    )

def parse_verse_list(self: Parser) -> List[VerseCase]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<verse_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<verse_list>"].keys())
        )

    if PREDICT["<verse_list>"][lookahead_type] == [EPSILON]:
        return []

    verse_cases: List[VerseCase] = []

    while self.current_type(0) == TK_CF_VERSE:
        verse_token = self.expect(TK_CF_VERSE)
        match_value = self.parse_literal_or_identifier()
        self.expect(TK_SYM_COLON)
        body_statements = self.parse_case_statement_list()
        verse_end = self.parse_verse_end_opt()

        verse_cases.append(
            VerseCase(
                pos=_tok_pos(verse_token),
                match=match_value,
                body=body_statements,
                end=verse_end
            )
        )

    return verse_cases

def parse_case_statement_list(self: Parser) -> List[Statement]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<case_statement_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<case_statement_list>"].keys())
        )

    if PREDICT["<case_statement_list>"][lookahead_type] == [EPSILON]:
        return []

    statement_list: List[Statement] = []

    while True:
        lookahead_type = self.current_type(0)

        if lookahead_type in (TK_CF_ABSOLVE, TK_CF_FALL, TK_CF_VERSE, TK_CF_GRACE, TK_SYM_CLSBRACE):
            break

        if lookahead_type in PREDICT["<case_statement_list>"] and PREDICT["<case_statement_list>"][lookahead_type] == [EPSILON]:
            break

        statement_list.append(self.parse_statement())

    return statement_list

def parse_literal_or_identifier(self: Parser) -> Union[Expr, IdentifierRef]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<literal_or_identifier>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<literal_or_identifier>"].keys())
        )

    if lookahead_type == TK_IDENTIFIER:
        identifier_token = self.expect(TK_IDENTIFIER)
        return IdentifierRef(
            pos=_tok_pos(identifier_token),
            name=_tok_lexeme(identifier_token)
        )

    return self.parse_literal_expr()

def parse_verse_end_opt(self: Parser) -> Optional[VerseEnd]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<verse_end_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<verse_end_opt>"].keys())
        )

    if PREDICT["<verse_end_opt>"][lookahead_type] == [EPSILON]:
        return None

    return self.parse_verse_end()

def parse_verse_end(self: Parser) -> VerseEnd:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<verse_end>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<verse_end>"].keys())
        )

    if lookahead_type == TK_CF_ABSOLVE:
        absolve_token = self.expect(TK_CF_ABSOLVE)
        self.expect(TK_SYM_SEMICOL)
        return VerseEnd(pos=_tok_pos(absolve_token), kind="absolve")

    fall_token = self.expect(TK_CF_FALL)
    self.expect(TK_SYM_SEMICOL)
    return VerseEnd(pos=_tok_pos(fall_token), kind="fall")

def parse_grace_opt(self: Parser) -> Optional[GraceDefault]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<grace_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<grace_opt>"].keys())
        )

    if PREDICT["<grace_opt>"][lookahead_type] == [EPSILON]:
        return None

    grace_token = self.expect(TK_CF_GRACE)
    self.expect(TK_SYM_COLON)
    body_statements = self.parse_case_statement_list()
    verse_end = self.parse_verse_end_opt()

    return GraceDefault(
        pos=_tok_pos(grace_token),
        body=body_statements,
        end=verse_end
    )

# LOOPS
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

# JUMPS + DISMISS OPT
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

Parser.parse_statement_list = parse_statement_list
Parser.parse_statement = parse_statement
Parser.parse_prefix_incdec_stmt = parse_prefix_incdec_stmt
Parser.parse_paren_postfix_incdec_stmt = parse_paren_postfix_incdec_stmt
Parser.parse_stmt_id_tail = parse_stmt_id_tail
Parser._assign_op_string = _assign_op_string

Parser.parse_io_stmt = parse_io_stmt
Parser.parse_output_list_opt = parse_output_list_opt
Parser.parse_output_list = parse_output_list
Parser.parse_output_tail = parse_output_tail

Parser.parse_cond_stmt = parse_cond_stmt
Parser.parse_decree_chain = parse_decree_chain
Parser.parse_edict_list_opt = parse_edict_list_opt
Parser.parse_edict = parse_edict
Parser.parse_absolution_opt = parse_absolution_opt
Parser.parse_discern_stmt = parse_discern_stmt
Parser.parse_verse_list = parse_verse_list
Parser.parse_case_statement_list = parse_case_statement_list
Parser.parse_literal_or_identifier = parse_literal_or_identifier
Parser.parse_verse_end_opt = parse_verse_end_opt
Parser.parse_verse_end = parse_verse_end
Parser.parse_grace_opt = parse_grace_opt

Parser.parse_loop_stmt = parse_loop_stmt
Parser.parse_procession_stmt = parse_procession_stmt
Parser.parse_init_opt = parse_init_opt
Parser.parse_expr_opt = parse_expr_opt
Parser.parse_update_opt = parse_update_opt
Parser.parse_update_expr = parse_update_expr
Parser.parse_update_tail = parse_update_tail
Parser.parse_endure_stmt = parse_endure_stmt
Parser.parse_ritual_stmt = parse_ritual_stmt

Parser.parse_jump_stmt = parse_jump_stmt
Parser.parse_dismiss_opt = parse_dismiss_opt
Parser.parse_dismiss_tail = parse_dismiss_tail