from __future__ import annotations
from typing import List, Optional, Union

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseConditionStatement(self: Parser) -> Statement:
    currentTokenType = self.currentType(0)

    # check condition stmt
    if currentTokenType not in PREDICT["<cond_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<cond_stmt>"].keys())
        )

    # decree stmt
    if currentTokenType == TK_CF_DECREE:
        return self.parseDecreeChain()

    return self.parseDiscernStatement()

def parseDecreeChain(self: Parser) -> DecreeStatement:
    currentTokenType = self.currentType(0)

    # check decree chain
    if currentTokenType not in PREDICT["<decree_chain>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<decree_chain>"].keys())
        )

    decreeToken = self.expect(TK_CF_DECREE)
    self.expect(TK_SYM_OPPAREN)
    conditionExpression = self.parseExpression()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    bodyStatements = self.parseStatementList()
    self.expect(TK_SYM_CLSBRACE)

    edictClauses = self.parseEdictListOptional()
    absolutionClause = self.parseAbsolutionOptional()

    return DecreeStatement(
        position=getTokenPosition(decreeToken),
        condition=conditionExpression,
        bodyStatements=bodyStatements,
        edictClauses=edictClauses,
        absolutionClause=absolutionClause
    )

def parseEdictListOptional(self: Parser) -> List[EdictClause]:
    currentTokenType = self.currentType(0)

    # check edict list
    if currentTokenType not in PREDICT["<edict_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<edict_list_opt>"].keys())
        )

    # no edict
    if PREDICT["<edict_list_opt>"][currentTokenType] == [EPSILON]:
        return []

    edictClauses: List[EdictClause] = []

    while self.currentType(0) == TK_CF_EDICT:
        edictClauses.extend([self.parseEdict()])

    return edictClauses

def parseEdict(self: Parser) -> EdictClause:
    currentTokenType = self.currentType(0)

    # check edict
    if currentTokenType not in PREDICT["<edict>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<edict>"].keys())
        )

    edictToken = self.expect(TK_CF_EDICT)
    self.expect(TK_SYM_OPPAREN)
    conditionExpression = self.parseExpression()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    bodyStatements = self.parseStatementList()
    self.expect(TK_SYM_CLSBRACE)

    return EdictClause(
        position=getTokenPosition(edictToken),
        condition=conditionExpression,
        bodyStatements=bodyStatements
    )

def parseAbsolutionOptional(self: Parser) -> Optional[AbsolutionClause]:
    currentTokenType = self.currentType(0)

    # check absolution
    if currentTokenType not in PREDICT["<absolution_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<absolution_opt>"].keys())
        )

    # no absolution
    if PREDICT["<absolution_opt>"][currentTokenType] == [EPSILON]:
        return None

    absolutionToken = self.expect(TK_CF_ABSOLUTION)
    self.expect(TK_SYM_OPBRACE)
    bodyStatements = self.parseStatementList()
    self.expect(TK_SYM_CLSBRACE)

    return AbsolutionClause(
        position=getTokenPosition(absolutionToken),
        bodyStatements=bodyStatements
    )

def parseDiscernStatement(self: Parser) -> DiscernStatement:
    currentTokenType = self.currentType(0)

    # check discern stmt
    if currentTokenType not in PREDICT["<discern_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<discern_stmt>"].keys())
        )

    discernToken = self.expect(TK_CF_DISCERN)
    self.expect(TK_SYM_OPPAREN)
    conditionExpression = self.parseExpression()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_OPBRACE)
    verseCases = self.parseVerseList()
    graceClause = self.parseGraceOptional()
    self.expect(TK_SYM_CLSBRACE)

    return DiscernStatement(
        position=getTokenPosition(discernToken),
        expression=conditionExpression,
        verseCases=verseCases,
        graceDefault=graceClause
    )

def parseVerseList(self: Parser) -> List[VerseCase]:
    currentTokenType = self.currentType(0)

    # check verse list
    if currentTokenType not in PREDICT["<verse_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<verse_list>"].keys())
        )

    # no verse
    if PREDICT["<verse_list>"][currentTokenType] == [EPSILON]:
        return []

    verseCases: List[VerseCase] = []

    while self.currentType(0) == TK_CF_VERSE:
        verseToken = self.expect(TK_CF_VERSE)
        matchValue = self.parseLiteralOrIdentifier()
        self.expect(TK_SYM_COLON)

        bodyStatements = self.parseCaseStatementList()

        verseCases.append(
            VerseCase(
                position=getTokenPosition(verseToken),
                matchValue=matchValue,
                bodyStatements=bodyStatements
            )
        )

    return verseCases

def parseCaseStatementList(self: Parser) -> List[Statement]:
    currentTokenType = self.currentType(0)

    # check case body
    if currentTokenType not in PREDICT["<case_statement_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<case_statement_list>"].keys())
        )

    # empty case body
    if PREDICT["<case_statement_list>"][currentTokenType] == [EPSILON]:
        return []

    statementList: List[Statement] = []

    while True:
        currentTokenType = self.currentType(0)

        # These are the only real endings of a case body now.
        if currentTokenType in (
            TK_CF_VERSE,
            TK_CF_GRACE,
            TK_SYM_CLSBRACE
        ):
            break

        if (
            currentTokenType in PREDICT["<case_statement_list>"]
            and PREDICT["<case_statement_list>"][currentTokenType] == [EPSILON]
        ):
            break

        statementList.append(self.parseStatement())

    return statementList

def parseLiteralOrIdentifier(self: Parser) -> Union[Expression, IdentifierReference]:
    currentTokenType = self.currentType(0)

    # check literal or identifier
    if currentTokenType not in PREDICT["<literal_or_identifier>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<literal_or_identifier>"].keys())
        )

    # identifier case
    if currentTokenType == TK_IDENTIFIER:
        identifierToken = self.expect(TK_IDENTIFIER)

        return IdentifierReference(
            position=getTokenPosition(identifierToken),
            name=getTokenValue(identifierToken)
        )

    return self.parseLiteralExpression()

def parseGraceOptional(self: Parser) -> Optional[GraceDefault]:
    currentTokenType = self.currentType(0)

    # check grace
    if currentTokenType not in PREDICT["<grace_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<grace_opt>"].keys())
        )

    # no grace
    if PREDICT["<grace_opt>"][currentTokenType] == [EPSILON]:
        return None

    graceToken = self.expect(TK_CF_GRACE)
    self.expect(TK_SYM_COLON)

    bodyStatements = self.parseCaseStatementList()

    return GraceDefault(
        position=getTokenPosition(graceToken),
        bodyStatements=bodyStatements
    )

Parser.parseConditionStatement = parseConditionStatement
Parser.parseDecreeChain = parseDecreeChain
Parser.parseEdictListOptional = parseEdictListOptional
Parser.parseEdict = parseEdict
Parser.parseAbsolutionOptional = parseAbsolutionOptional
Parser.parseDiscernStatement = parseDiscernStatement
Parser.parseVerseList = parseVerseList
Parser.parseCaseStatementList = parseCaseStatementList
Parser.parseLiteralOrIdentifier = parseLiteralOrIdentifier
Parser.parseGraceOptional = parseGraceOptional