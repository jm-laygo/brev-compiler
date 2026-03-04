from __future__ import annotations
from typing import Any, List, Optional, Tuple, Union
from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *

from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# --------------------------
# STATEMENTS
# --------------------------
def parse_statement_list(self: Parser) -> List[Statement]:
    prod = self.choose_prod("<statement_list>")
    if prod == [EPSILON]:
        return []
    stmts: List[Statement] = []
    while True:
        if self.la(0) == TK_SYM_CLSBRACE:
            break
        table = PREDICT.get("<statement_list>", {})
        if self.la(0) in table and table[self.la(0)] == [EPSILON]:
            break
        stmts.append(self.parse_statement())
    return stmts

def parse_statement(self: Parser) -> Statement:
    self.choose_prod("<statement>")
    la = self.la(0)

    if la in (TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY):
        decl = VarDecl(pos=_tok_pos(self.peek(0)), type_name=self.parse_data_type(), items=self.parse_var_decl_group())
        self.expect(TK_SYM_SEMICOL)
        return VarDeclStmt(pos=decl.pos, decl=decl)

    if la == TK_OTHERS_ORDAIN:
        tok = self.expect(TK_OTHERS_ORDAIN)
        name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        items = self.parse_ordain_dec_list()
        self.expect(TK_SYM_SEMICOL)
        return OrdainStmt(pos=_tok_pos(tok), decl=OrdainDecl(pos=_tok_pos(tok), name=name, items=items))

    if la == TK_OTHERS_ORDER:
        tok = self.expect(TK_OTHERS_ORDER)
        name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        self.expect(TK_SYM_OPBRACE)
        members = self.parse_member_list_opt()
        self.expect(TK_SYM_CLSBRACE)
        self.expect(TK_SYM_SEMICOL)
        return OrderStmt(pos=_tok_pos(tok), decl=OrderDecl(pos=_tok_pos(tok), name=name, members=members))

    if la in (TK_IO_RECEIVE, TK_IO_PROCLAIM):
        return self.parse_io_stmt()

    if la in (TK_CF_DECREE, TK_CF_DISCERN):
        return self.parse_cond_stmt()

    if la in (TK_CF_PROCESSION, TK_CF_ENDURE, TK_CF_RITUAL):
        return self.parse_loop_stmt()

    if la in (TK_CF_DISMISS, TK_CF_PROCEED, TK_CF_FALL, TK_CF_ABSOLVE):
        return self.parse_jump_stmt()

    if la in (TK_OP_INC, TK_OP_DEC):
        return self.parse_prefix_incdec_stmt()

    if la == TK_SYM_OPPAREN:
        return self.parse_paren_postfix_incdec_stmt()

    if la == TK_IDENTIFIER:
        id_tok = self.expect(TK_IDENTIFIER)
        name = _tok_lexeme(id_tok)
        return self.parse_stmt_id_tail(id_tok, name)

    tok = self.peek(0) or self.peek(-1)
    raise ParserError(tok, expected=list(PREDICT["<statement>"].keys()), details="Invalid start of <statement>")


def parse_prefix_incdec_stmt(self: Parser) -> IncDecStmt:
    self.choose_prod("<prefix_incdec_stmt>")
    op_tok = self.advance()
    op = _tok_lexeme(op_tok) or ("++" if op_tok.type == TK_OP_INC else "--")
    target = self.parse_lvalue_core()
    self.expect(TK_SYM_SEMICOL)
    return IncDecStmt(pos=_tok_pos(op_tok), target=target, op=op, prefix=True)

def parse_paren_postfix_incdec_stmt(self: Parser) -> IncDecStmt:
    self.choose_prod("<paren_postfix_incdec_stmt>")
    lpar = self.expect(TK_SYM_OPPAREN)
    target = self.parse_lvalue_core()
    self.expect(TK_SYM_CLSPAREN)
    if self.la(0) in (TK_OP_INC, TK_OP_DEC):
        op_tok = self.advance()
        op = _tok_lexeme(op_tok) or ("++" if op_tok.type == TK_OP_INC else "--")
    else:
        tok = self.peek(0) or self.peek(-1)
        raise ParserError(tok, expected=[TK_OP_INC, TK_OP_DEC], details="Expected postfix ++/-- after (lvalue)")
    self.expect(TK_SYM_SEMICOL)
    return IncDecStmt(pos=_tok_pos(lpar), target=target, op=op, prefix=False)

def parse_stmt_id_tail(self: Parser, id_tok: Any, name: str) -> Statement:
    self.choose_prod("<stmt_id_tail>")
    la = self.la(0)

    if la == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        args = self.parse_arg_list_opt()
        self.expect(TK_SYM_CLSPAREN)
        access = self.parse_access_chain_opt(base=NameRef(pos=_tok_pos(id_tok), name=name))
        self.expect(TK_SYM_SEMICOL)
        return CallStmt(pos=_tok_pos(id_tok), callee=name, args=args, access=access)

    base_lv: LValue = NameRef(pos=_tok_pos(id_tok), name=name)
    access_lv = self.parse_access_chain_opt(base=base_lv)
    target = access_lv if access_lv is not None else base_lv

    la2 = self.la(0)
    self.choose_prod("<stmt_after_access>")

    if la2 in (TK_OP_ASSIGN, TK_OP_PLUS_EQ, TK_OP_MINUS_EQ, TK_OP_MUL_EQ, TK_OP_DIV_EQ, TK_OP_MOD_EQ, TK_OP_POW_EQ):
        op_tok = self.advance()
        op = _tok_lexeme(op_tok) or self._assign_op_string(op_tok.type)
        value = self.parse_expr()
        self.expect(TK_SYM_SEMICOL)
        return AssignStmt(pos=_tok_pos(op_tok), target=target, op=op, value=value)

    if la2 in (TK_OP_INC, TK_OP_DEC):
        op_tok = self.advance()
        op = _tok_lexeme(op_tok) or ("++" if op_tok.type == TK_OP_INC else "--")
        self.expect(TK_SYM_SEMICOL)
        return IncDecStmt(pos=_tok_pos(op_tok), target=target, op=op, prefix=False)

    tok = self.peek(0) or self.peek(-1)
    raise ParserError(tok, expected=list(PREDICT["<stmt_after_access>"].keys()),
                     details="Invalid continuation after identifier/access in statement")

def _assign_op_string(self: Parser, ttype: Any) -> str:
    return {
        TK_OP_ASSIGN: "=",
        TK_OP_PLUS_EQ: "+=",
        TK_OP_MINUS_EQ: "-=",
        TK_OP_MUL_EQ: "*=",
        TK_OP_DIV_EQ: "/=",
        TK_OP_MOD_EQ: "%=",
        TK_OP_POW_EQ: "^=",
    }.get(ttype, str(ttype))


# --------------------------
# IO
# --------------------------
def parse_io_stmt(self: Parser) -> Statement:
    self.choose_prod("<io_stmt>")
    if self.la(0) == TK_IO_RECEIVE:
        tok = self.expect(TK_IO_RECEIVE)
        self.expect(TK_SYM_OPPAREN)
        target = self.parse_lvalue()
        self.expect(TK_SYM_CLSPAREN)
        self.expect(TK_SYM_SEMICOL)
        return ReceiveStmt(pos=_tok_pos(tok), target=target)

    tok = self.expect(TK_IO_PROCLAIM)
    self.expect(TK_SYM_OPPAREN)
    args = self.parse_output_list_opt()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_SEMICOL)
    return ProclaimStmt(pos=_tok_pos(tok), args=args)

def parse_output_list_opt(self: Parser) -> List[Expr]:
    prod = self.choose_prod("<output_list_opt>")
    if prod == [EPSILON]:
        return []
    return self.parse_output_list()

def parse_output_list(self: Parser) -> List[Expr]:
    self.choose_prod("<output_list>")
    args = [self.parse_expr()]
    args.extend(self.parse_output_tail())
    return args

def parse_output_tail(self: Parser) -> List[Expr]:
    prod = self.choose_prod("<output_tail>")
    if prod == [EPSILON]:
        return []
    self.expect(TK_SYM_COMMA)
    args = [self.parse_expr()]
    args.extend(self.parse_output_tail())
    return args


# --------------------------
# CONDITIONS
# --------------------------
def parse_cond_stmt(self: Parser) -> Statement:
    self.choose_prod("<cond_stmt>")
    if self.la(0) == TK_CF_DECREE:
        return self.parse_decree_chain()
    return self.parse_discern_stmt()

def parse_decree_chain(self: Parser) -> DecreeStmt:
    self.choose_prod("<decree_chain>")
    tok = self.expect(TK_CF_DECREE)
    self.expect(TK_SYM_OPPAREN)
    cond = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    body = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)

    edicts = self.parse_edict_list_opt()
    absolution = self.parse_absolution_opt()

    return DecreeStmt(pos=_tok_pos(tok), expr=cond, body=body, edicts=edicts, absolution=absolution)

def parse_edict_list_opt(self: Parser) -> List[EdictClause]:
    prod = self.choose_prod("<edict_list_opt>")
    if prod == [EPSILON]:
        return []
    edicts: List[EdictClause] = []
    while self.la(0) == TK_CF_EDICT:
        edicts.append(self.parse_edict())
    return edicts

def parse_edict(self: Parser) -> EdictClause:
    self.choose_prod("<edict>")
    tok = self.expect(TK_CF_EDICT)
    self.expect(TK_SYM_OPPAREN)
    cond = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    body = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)
    return EdictClause(pos=_tok_pos(tok), expr=cond, body=body)

def parse_absolution_opt(self: Parser) -> Optional[AbsolutionClause]:
    prod = self.choose_prod("<absolution_opt>")
    if prod == [EPSILON]:
        return None
    tok = self.expect(TK_CF_ABSOLUTION)
    self.expect(TK_SYM_OPBRACE)
    body = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)
    return AbsolutionClause(pos=_tok_pos(tok), body=body)

def parse_discern_stmt(self: Parser) -> DiscernStmt:
    self.choose_prod("<discern_stmt>")
    tok = self.expect(TK_CF_DISCERN)
    self.expect(TK_SYM_OPPAREN)
    expr = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    verses = self.parse_verse_list()
    grace = self.parse_grace_opt()
    self.expect(TK_SYM_CLSBRACE)
    return DiscernStmt(pos=_tok_pos(tok), expr=expr, verses=verses, grace=grace)

def parse_verse_list(self: Parser) -> List[VerseCase]:
    prod = self.choose_prod("<verse_list>")
    if prod == [EPSILON]:
        return []
    cases: List[VerseCase] = []
    while self.la(0) == TK_CF_VERSE:
        vtok = self.expect(TK_CF_VERSE)
        match = self.parse_literal_or_identifier()
        self.expect(TK_SYM_COLON)
        body = self.parse_case_statement_list()
        end = self.parse_verse_end_opt()
        cases.append(VerseCase(pos=_tok_pos(vtok), match=match, body=body, end=end))
    return cases

def parse_case_statement_list(self: Parser) -> List[Statement]:
    prod = self.choose_prod("<case_statement_list>")
    if prod == [EPSILON]:
        return []
    stmts: List[Statement] = []
    while True:
        table = PREDICT.get("<case_statement_list>", {})
        la = self.la(0)
        if la in table and table[la] == [EPSILON]:
            break
        if la in (TK_CF_ABSOLVE, TK_CF_FALL, TK_CF_VERSE, TK_CF_GRACE, TK_SYM_CLSBRACE):
            break
        stmts.append(self.parse_statement())
    return stmts

def parse_literal_or_identifier(self: Parser) -> Union[Expr, IdentifierRef]:
    self.choose_prod("<literal_or_identifier>")
    if self.la(0) == TK_IDENTIFIER:
        tok = self.expect(TK_IDENTIFIER)
        return IdentifierRef(pos=_tok_pos(tok), name=_tok_lexeme(tok))
    return self.parse_literal_expr()

def parse_verse_end_opt(self: Parser) -> Optional[VerseEnd]:
    prod = self.choose_prod("<verse_end_opt>")
    if prod == [EPSILON]:
        return None
    return self.parse_verse_end()

def parse_verse_end(self: Parser) -> VerseEnd:
    self.choose_prod("<verse_end>")
    if self.la(0) == TK_CF_ABSOLVE:
        tok = self.expect(TK_CF_ABSOLVE)
        self.expect(TK_SYM_SEMICOL)
        return VerseEnd(pos=_tok_pos(tok), kind="absolve")
    tok = self.expect(TK_CF_FALL)
    self.expect(TK_SYM_SEMICOL)
    return VerseEnd(pos=_tok_pos(tok), kind="fall")

def parse_grace_opt(self: Parser) -> Optional[GraceDefault]:
    prod = self.choose_prod("<grace_opt>")
    if prod == [EPSILON]:
        return None
    tok = self.expect(TK_CF_GRACE)
    self.expect(TK_SYM_COLON)
    body = self.parse_case_statement_list()
    end = self.parse_verse_end_opt()
    return GraceDefault(pos=_tok_pos(tok), body=body, end=end)

# --------------------------
# LOOPS
# --------------------------
def parse_loop_stmt(self: Parser) -> Statement:
    self.choose_prod("<loop_stmt>")
    if self.la(0) == TK_CF_PROCESSION:
        return self.parse_procession_stmt()
    if self.la(0) == TK_CF_ENDURE:
        return self.parse_endure_stmt()
    return self.parse_ritual_stmt()

def parse_procession_stmt(self: Parser) -> ProcessionStmt:
    self.choose_prod("<procession_stmt>")
    tok = self.expect(TK_CF_PROCESSION)
    self.expect(TK_SYM_OPPAREN)

    init = self.parse_init_opt()
    self.expect(TK_SYM_SEMICOL)
    cond = self.parse_expr_opt()
    self.expect(TK_SYM_SEMICOL)
    update = self.parse_update_opt()
    self.expect(TK_SYM_CLSPAREN)

    self.expect(TK_SYM_OPBRACE)
    body = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)
    return ProcessionStmt(pos=_tok_pos(tok), init=init, condition=cond, update=update, body=body)

def parse_init_opt(self: Parser) -> Optional[Statement]:
    prod = self.choose_prod("<init_opt>")
    if prod == [EPSILON]:
        return None

    if self.la(0) in (TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY):
        type_name = self.parse_data_type()
        id_tok = self.expect(TK_IDENTIFIER)
        self.expect(TK_OP_ASSIGN)
        value = self.parse_expr()
        decl = VarDecl(
            pos=_tok_pos(id_tok),
            type_name=type_name,
            items=[VarItem(pos=_tok_pos(id_tok), name=_tok_lexeme(id_tok), dims=[], init=value)],
        )
        return VarDeclStmt(pos=decl.pos, decl=decl)

    target = self.parse_lvalue()
    self.expect(TK_OP_ASSIGN)
    value = self.parse_expr()
    return AssignStmt(pos=_tok_pos(self.peek(-1)), target=target, op="=", value=value)

def parse_expr_opt(self: Parser) -> Optional[Expr]:
    prod = self.choose_prod("<expr_opt>")
    if prod == [EPSILON]:
        return None
    return self.parse_expr()

def parse_update_opt(self: Parser) -> Optional[Statement]:
    prod = self.choose_prod("<update_opt>")
    if prod == [EPSILON]:
        return None
    return self.parse_update_expr()

def parse_update_expr(self: Parser) -> Statement:
    self.choose_prod("<update_expr>")
    la = self.la(0)

    if la == TK_OP_INC:
        tok = self.expect(TK_OP_INC)
        target = self.parse_lvalue_core()
        return IncDecStmt(pos=_tok_pos(tok), target=target, op="++", prefix=True)

    if la == TK_OP_DEC:
        tok = self.expect(TK_OP_DEC)
        target = self.parse_lvalue_core()
        return IncDecStmt(pos=_tok_pos(tok), target=target, op="--", prefix=True)

    if la == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        inner = self.parse_update_expr()
        self.expect(TK_SYM_CLSPAREN)
        return inner

    lv = self.parse_lvalue()
    return self.parse_update_tail(lv)

def parse_update_tail(self: Parser, lv: LValue) -> Statement:
    self.choose_prod("<update_tail>")
    la = self.la(0)

    if la == TK_OP_INC:
        tok = self.expect(TK_OP_INC)
        return IncDecStmt(pos=_tok_pos(tok), target=lv, op="++", prefix=False)

    if la == TK_OP_DEC:
        tok = self.expect(TK_OP_DEC)
        return IncDecStmt(pos=_tok_pos(tok), target=lv, op="--", prefix=False)

    if la in (TK_OP_ASSIGN, TK_OP_PLUS_EQ, TK_OP_MINUS_EQ, TK_OP_MUL_EQ, TK_OP_DIV_EQ, TK_OP_MOD_EQ, TK_OP_POW_EQ):
        op_tok = self.advance()
        op = _tok_lexeme(op_tok) or self._assign_op_string(op_tok.type)
        value = self.parse_expr()
        return AssignStmt(pos=_tok_pos(op_tok), target=lv, op=op, value=value)

    tok = self.peek(0) or self.peek(-1)
    raise ParserError(tok, expected=[TK_OP_INC, TK_OP_DEC, TK_OP_ASSIGN, TK_OP_PLUS_EQ, TK_OP_MINUS_EQ,
                                    TK_OP_MUL_EQ, TK_OP_DIV_EQ, TK_OP_MOD_EQ, TK_OP_POW_EQ], details="Invalid update tail")

def parse_endure_stmt(self: Parser) -> EndureStmt:
    self.choose_prod("<endure_stmt>")
    tok = self.expect(TK_CF_ENDURE)
    self.expect(TK_SYM_OPPAREN)
    cond = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    body = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)
    return EndureStmt(pos=_tok_pos(tok), condition=cond, body=body)

def parse_ritual_stmt(self: Parser) -> RitualStmt:
    self.choose_prod("<ritual_stmt>")
    tok = self.expect(TK_CF_RITUAL)
    self.expect(TK_SYM_OPBRACE)
    body = self.parse_statement_list()
    self.expect(TK_SYM_CLSBRACE)
    self.expect(TK_CF_ENDURE)
    self.expect(TK_SYM_OPPAREN)
    cond = self.parse_expr()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_SEMICOL)
    return RitualStmt(pos=_tok_pos(tok), body=body, condition=cond)


# --------------------------
# JUMPS + DISMISS OPT
# --------------------------
def parse_jump_stmt(self: Parser) -> Statement:
    self.choose_prod("<jump_stmt>")
    la = self.la(0)

    if la == TK_CF_DISMISS:
        tok = self.expect(TK_CF_DISMISS)
        value = self.parse_expr_opt()
        self.expect(TK_SYM_SEMICOL)
        return DismissStmt(pos=_tok_pos(tok), value=value)

    if la == TK_CF_PROCEED:
        tok = self.expect(TK_CF_PROCEED)
        self.expect(TK_SYM_SEMICOL)
        return ProceedStmt(pos=_tok_pos(tok))

    if la == TK_CF_FALL:
        tok = self.expect(TK_CF_FALL)
        self.expect(TK_SYM_SEMICOL)
        return FallStmt(pos=_tok_pos(tok))

    tok = self.expect(TK_CF_ABSOLVE)
    self.expect(TK_SYM_SEMICOL)
    return AbsolveStmt(pos=_tok_pos(tok))

def parse_dismiss_opt(self: Parser) -> Optional[DismissStmt]:
    prod = self.choose_prod("<dismiss_opt>")
    if prod == [EPSILON]:
        return None
    tok = self.expect(TK_CF_DISMISS)
    value = self.parse_dismiss_tail(tok)
    return DismissStmt(pos=_tok_pos(tok), value=value)

def parse_dismiss_tail(self: Parser, dismiss_tok: Any) -> Optional[Expr]:
    self.choose_prod("<dismiss_tail>")
    if self.la(0) == TK_SYM_SEMICOL:
        self.expect(TK_SYM_SEMICOL)
        return None
    expr = self.parse_expr()
    self.expect(TK_SYM_SEMICOL)
    return expr


# ---- attach ----
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