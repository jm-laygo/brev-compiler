from __future__ import annotations
from typing import List, Optional, Union

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


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
