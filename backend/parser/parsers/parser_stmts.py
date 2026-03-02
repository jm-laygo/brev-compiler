from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.ast.ast_nodes import (
    Statement,
    VarDecl, VarItem,
    VarDeclStmt, OrderStmt, OrdainStmt,
    CallStmt, IOStmt, ReceiveStmt, ProclaimStmt,
    AssignStmt, IncDecStmt,
    DismissStmt, ProceedStmt, AbsolveStmt,
    DecreeStmt, EdictClause, AbsolutionClause,
    DiscernStmt, VerseCase, VerseEnd, GraceDefault, IdentifierRef,
    EndureStmt, ProcessionStmt, RitualStmt,
    NameRef,
)

try:
    from backend.ast.ast_nodes import FallStmt
except Exception:
    FallStmt = None


class StmtsMixin:
    # ---------- statements ----------
    def parse_statement_list_until(self, *end_tokens) -> list[Statement]:
        stmts: list[Statement] = []
        while self.peek().type not in end_tokens:
            stmts.append(self.parse_statement())
        return stmts

    def parse_statement(self) -> Statement:
        t = self.peek().type

        # control flow
        if t in (TK_CF_DECREE, TK_CF_DISCERN):
            return self.parse_cond_stmt()
        if t in (TK_CF_PROCESSION, TK_CF_ENDURE, TK_CF_RITUAL):
            return self.parse_loop_stmt()

        # fall = continue
        if t == TK_CF_FALL:
            if FallStmt is None:
                raise ParserError(self.peek(), expected=["FallStmt"], details="FallStmt AST node missing. Add FallStmt to ast_nodes.")
            tok = self.match(TK_CF_FALL)
            self.match(TK_SYM_SEMICOL)
            return FallStmt(pos=tok.pos)

        # var decl stmt
        if t in (TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY):
            dt_tok = self.peek()
            type_name = self.parse_data_type()
            items = self.parse_var_decl_group()
            self.match(TK_SYM_SEMICOL)
            return VarDeclStmt(decl=VarDecl(type_name=type_name, items=items, pos=dt_tok.pos), pos=dt_tok.pos)

        # order stmt
        if t == TK_OTHERS_ORDER:
            decl = self.parse_decl_item(global_scope=False)
            return OrderStmt(decl=decl, pos=decl.pos)

        # ordain stmt
        if t == TK_OTHERS_ORDAIN:
            decl = self.parse_decl_item(global_scope=False)
            return OrdainStmt(decl=decl, pos=decl.pos)

        # io
        if t in (TK_IO_RECEIVE, TK_IO_PROCLAIM):
            return self.parse_io_stmt()

        # dismiss as a statement
        if t == TK_CF_DISMISS:
            return self.parse_dismiss_stmt()

        # proceed
        if t == TK_CF_PROCEED:
            tok = self.match(TK_CF_PROCEED)
            self.match(TK_SYM_SEMICOL)
            return ProceedStmt(pos=tok.pos)

        # absolve
        if t == TK_CF_ABSOLVE:
            tok = self.match(TK_CF_ABSOLVE)
            self.match(TK_SYM_SEMICOL)
            return AbsolveStmt(pos=tok.pos)

        # prefix inc/dec statement: ++ lvalue_core ; / -- lvalue_core ;
        if t in (TK_OP_INC, TK_OP_DEC):
            op_tok = self.match(t)
            lv = self.parse_lvalue_core()
            self.match(TK_SYM_SEMICOL)
            return IncDecStmt(target=lv, op=op_tok.type, prefix=True, pos=op_tok.pos)

        # paren_postfix_incdec_stmt: ( lvalue_core ) postfix_inc_opt ;
        if t == TK_SYM_OPPAREN:
            open_tok = self.match(TK_SYM_OPPAREN)
            lv = self.parse_lvalue_core()
            self.match(TK_SYM_CLSPAREN)
            if self.peek().type not in (TK_OP_INC, TK_OP_DEC):
                raise ParserError(self.peek(), expected=[TK_OP_INC, TK_OP_DEC], details="Expected postfix ++/-- after (lvalue)")
            op_tok = self.match(self.peek().type)
            self.match(TK_SYM_SEMICOL)
            return IncDecStmt(target=lv, op=op_tok.type, prefix=False, pos=open_tok.pos)

        # identifier-led statement
        if t == TK_IDENTIFIER:
            id_tok = self.match(TK_IDENTIFIER)

            # call stmt: id (args) access? ;
            if self.accept(TK_SYM_OPPAREN):
                args = self.parse_arg_list_opt_until_rparen()
                self.match(TK_SYM_CLSPAREN)

                access = None
                if self.peek().type in (TK_SYM_OPBRACK, TK_SYM_DOT):
                    access = self.parse_access_chain(NameRef(name="$call", pos=id_tok.pos))

                self.match(TK_SYM_SEMICOL)
                return CallStmt(callee=id_tok.value, args=args, access=access, pos=id_tok.pos)

            # lvalue statement (assignment or postfix inc/dec)
            lv = self.parse_access_chain(NameRef(name=id_tok.value, pos=id_tok.pos))

            # assignment
            if self.peek().type in self.ASSIGN_OPS:
                op_tok = self.match(self.peek().type)
                val = self.parse_expr()
                self.match(TK_SYM_SEMICOL)
                return AssignStmt(target=lv, op=op_tok.type, value=val, pos=op_tok.pos)

            # postfix ++/--
            if self.peek().type in (TK_OP_INC, TK_OP_DEC):
                op_tok = self.match(self.peek().type)
                self.match(TK_SYM_SEMICOL)
                return IncDecStmt(target=lv, op=op_tok.type, prefix=False, pos=op_tok.pos)

            raise ParserError(
                self.peek(),
                expected=[*self.ASSIGN_OPS, TK_OP_INC, TK_OP_DEC, TK_SYM_OPPAREN],
                details="Invalid identifier statement",
            )

        raise ParserError(self.peek(), expected=["<statement>"], details="Statement start token not recognized")

    # ---------- conditions ----------
    def parse_cond_stmt(self) -> Statement:
        if self.at(TK_CF_DECREE):
            return self.parse_decree_stmt()
        if self.at(TK_CF_DISCERN):
            return self.parse_discern_stmt()
        raise ParserError(self.peek(), expected=[TK_CF_DECREE, TK_CF_DISCERN], details=None)

    def parse_decree_stmt(self) -> DecreeStmt:
        d_tok = self.match(TK_CF_DECREE)
        self.match(TK_SYM_OPPAREN)
        cond = self.parse_expr()
        self.match(TK_SYM_CLSPAREN)

        self.match(TK_SYM_OPBRACE)
        body = self.parse_statement_list_until(TK_SYM_CLSBRACE)
        self.match(TK_SYM_CLSBRACE)

        edicts = []
        while self.at(TK_CF_EDICT):
            e_tok = self.match(TK_CF_EDICT)
            self.match(TK_SYM_OPPAREN)
            e_cond = self.parse_expr()
            self.match(TK_SYM_CLSPAREN)

            self.match(TK_SYM_OPBRACE)
            e_body = self.parse_statement_list_until(TK_SYM_CLSBRACE)
            self.match(TK_SYM_CLSBRACE)

            edicts.append(EdictClause(expr=e_cond, body=e_body, pos=e_tok.pos))

        absolution = None
        if self.at(TK_CF_ABSOLUTION):
            a_tok = self.match(TK_CF_ABSOLUTION)
            self.match(TK_SYM_OPBRACE)
            a_body = self.parse_statement_list_until(TK_SYM_CLSBRACE)
            self.match(TK_SYM_CLSBRACE)
            absolution = AbsolutionClause(body=a_body, pos=a_tok.pos)

        return DecreeStmt(expr=cond, body=body, edicts=edicts, absolution=absolution, pos=d_tok.pos)

    def parse_discern_stmt(self) -> DiscernStmt:
        s_tok = self.match(TK_CF_DISCERN)
        self.match(TK_SYM_OPPAREN)
        expr = self.parse_expr()
        self.match(TK_SYM_CLSPAREN)

        self.match(TK_SYM_OPBRACE)

        verses = []
        while self.at(TK_CF_VERSE):
            v_tok = self.match(TK_CF_VERSE)

            # literal_or_identifier
            if self.peek().type == TK_IDENTIFIER:
                m_tok = self.match(TK_IDENTIFIER)
                match_node = IdentifierRef(name=m_tok.value, pos=m_tok.pos)
            elif self.peek().type in (TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL):
                match_node = self.parse_primary()  # LiteralExpr
            else:
                raise ParserError(
                    self.peek(),
                    expected=[TK_IDENTIFIER, TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL],
                    details="Expected verse match",
                )

            self.match(TK_SYM_COLON)

            body = self.parse_statement_list_until(TK_CF_ABSOLVE, TK_CF_FALL, TK_CF_VERSE, TK_CF_GRACE, TK_SYM_CLSBRACE)

            end = None
            if self.at(TK_CF_ABSOLVE):
                e = self.match(TK_CF_ABSOLVE)
                self.match(TK_SYM_SEMICOL)
                end = VerseEnd(kind="absolve", pos=e.pos)
            elif self.at(TK_CF_FALL):
                e = self.match(TK_CF_FALL)
                self.match(TK_SYM_SEMICOL)
                end = VerseEnd(kind="fall", pos=e.pos)

            verses.append(VerseCase(match=match_node, body=body, end=end, pos=v_tok.pos))

        grace = None
        if self.at(TK_CF_GRACE):
            g_tok = self.match(TK_CF_GRACE)
            self.match(TK_SYM_COLON)
            g_body = self.parse_statement_list_until(TK_SYM_CLSBRACE)
            grace = GraceDefault(body=g_body, pos=g_tok.pos)

        self.match(TK_SYM_CLSBRACE)
        return DiscernStmt(expr=expr, verses=verses, grace=grace, pos=s_tok.pos)

    # ---------- loops ----------
    def parse_loop_stmt(self) -> Statement:
        if self.at(TK_CF_ENDURE):
            return self.parse_endure_stmt()
        if self.at(TK_CF_PROCESSION):
            return self.parse_procession_stmt()
        if self.at(TK_CF_RITUAL):
            return self.parse_ritual_stmt()
        raise ParserError(self.peek(), expected=[TK_CF_ENDURE, TK_CF_PROCESSION, TK_CF_RITUAL], details=None)

    def parse_endure_stmt(self) -> EndureStmt:
        tok = self.match(TK_CF_ENDURE)
        self.match(TK_SYM_OPPAREN)
        cond = self.parse_expr()
        self.match(TK_SYM_CLSPAREN)
        self.match(TK_SYM_OPBRACE)
        body = self.parse_statement_list_until(TK_SYM_CLSBRACE)
        self.match(TK_SYM_CLSBRACE)
        return EndureStmt(condition=cond, body=body, pos=tok.pos)

    def parse_procession_stmt(self) -> ProcessionStmt:
        tok = self.match(TK_CF_PROCESSION)
        self.match(TK_SYM_OPPAREN)

        init = None
        if not self.at(TK_SYM_SEMICOL):
            init = self.parse_procession_init_part()
        self.match(TK_SYM_SEMICOL)

        cond = None
        if not self.at(TK_SYM_SEMICOL):
            cond = self.parse_expr()
        self.match(TK_SYM_SEMICOL)

        update = None
        if not self.at(TK_SYM_CLSPAREN):
            update = self.parse_procession_update_part()
        self.match(TK_SYM_CLSPAREN)

        self.match(TK_SYM_OPBRACE)
        body = self.parse_statement_list_until(TK_SYM_CLSBRACE)
        self.match(TK_SYM_CLSBRACE)
        return ProcessionStmt(init=init, condition=cond, update=update, body=body, pos=tok.pos)

    def parse_procession_init_part(self) -> Statement:
        t = self.peek().type

        # data_type id = expr
        if t in (TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY):
            dt_tok = self.peek()
            type_name = self.parse_data_type()
            name_tok = self.match(TK_IDENTIFIER)
            self.match(TK_OP_ASSIGN)
            init_expr = self.parse_expr()

            decl = VarDecl(
                type_name=type_name,
                items=[VarItem(name=name_tok.value, dims=[], init=init_expr, pos=name_tok.pos)],
                pos=dt_tok.pos,
            )
            return VarDeclStmt(decl=decl, pos=dt_tok.pos)

        # lvalue = expr
        lv = self.parse_lvalue()
        op_tok = self.match(TK_OP_ASSIGN)
        val = self.parse_expr()
        return AssignStmt(target=lv, op=op_tok.type, value=val, pos=op_tok.pos)

    def parse_procession_update_part(self) -> Statement:
        if self.at(TK_SYM_OPPAREN):
            self.match(TK_SYM_OPPAREN)
            inner = self.parse_procession_update_part()
            self.match(TK_SYM_CLSPAREN)
            return inner

        if self.peek().type in (TK_OP_INC, TK_OP_DEC):
            op_tok = self.match(self.peek().type)
            lv = self.parse_lvalue_core()
            return IncDecStmt(target=lv, op=op_tok.type, prefix=True, pos=op_tok.pos)

        if self.at(TK_IDENTIFIER):
            lv = self.parse_lvalue()

            if self.peek().type in (TK_OP_INC, TK_OP_DEC):
                op_tok = self.match(self.peek().type)
                return IncDecStmt(target=lv, op=op_tok.type, prefix=False, pos=op_tok.pos)

            if self.peek().type in self.ASSIGN_OPS:
                op_tok = self.match(self.peek().type)
                val = self.parse_expr()
                return AssignStmt(target=lv, op=op_tok.type, value=val, pos=op_tok.pos)

            raise ParserError(
                self.peek(),
                expected=[*self.ASSIGN_OPS, TK_OP_INC, TK_OP_DEC],
                details="Invalid procession update expression",
            )

        raise ParserError(
            self.peek(),
            expected=[TK_IDENTIFIER, TK_OP_INC, TK_OP_DEC, TK_SYM_OPPAREN],
            details="Invalid procession update expression",
        )

    def parse_ritual_stmt(self) -> RitualStmt:
        tok = self.match(TK_CF_RITUAL)
        self.match(TK_SYM_OPBRACE)
        body = self.parse_statement_list_until(TK_SYM_CLSBRACE)
        self.match(TK_SYM_CLSBRACE)

        self.match(TK_CF_ENDURE)
        self.match(TK_SYM_OPPAREN)
        cond = self.parse_expr()
        self.match(TK_SYM_CLSPAREN)
        self.match(TK_SYM_SEMICOL)
        return RitualStmt(body=body, condition=cond, pos=tok.pos)

    # ---------- io ----------
    def parse_io_stmt(self) -> IOStmt:
        if self.at(TK_IO_RECEIVE):
            tok = self.match(TK_IO_RECEIVE)
            self.match(TK_SYM_OPPAREN)
            lv = self.parse_lvalue()
            self.match(TK_SYM_CLSPAREN)
            self.match(TK_SYM_SEMICOL)
            return ReceiveStmt(target=lv, pos=tok.pos)

        if self.at(TK_IO_PROCLAIM):
            tok = self.match(TK_IO_PROCLAIM)
            self.match(TK_SYM_OPPAREN)
            args = []
            if not self.at(TK_SYM_CLSPAREN):
                args.append(self.parse_expr())
                while self.accept(TK_SYM_COMMA):
                    args.append(self.parse_expr())
            self.match(TK_SYM_CLSPAREN)
            self.match(TK_SYM_SEMICOL)
            return ProclaimStmt(args=args, pos=tok.pos)

        raise ParserError(self.peek(), expected=[TK_IO_RECEIVE, TK_IO_PROCLAIM], details=None)

    # ---------- dismiss ----------
    def parse_dismiss_stmt(self) -> DismissStmt:
        tok = self.match(TK_CF_DISMISS)
        value = None
        if not self.at(TK_SYM_SEMICOL):
            value = self.parse_expr()
        self.match(TK_SYM_SEMICOL)
        return DismissStmt(value=value, pos=tok.pos)