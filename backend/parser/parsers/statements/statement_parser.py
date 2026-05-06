from __future__ import annotations
from typing import List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue


def parseStatementList(self: Parser) -> List[Statement]:
    currentTokenType = self.currentType(0)

    # check statement list
    if currentTokenType not in PREDICT["<statement_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<statement_list>"].keys())
        )

    # no statement
    if PREDICT["<statement_list>"][currentTokenType] == [EPSILON]:
        return []

    statementList: List[Statement] = []

    while True:
        currentTokenType = self.currentType(0)

        # end of block
        if currentTokenType == TK_SYM_CLSBRACE:
            break

        # epsilon stop
        if (
            currentTokenType in PREDICT["<statement_list>"]
            and PREDICT["<statement_list>"][currentTokenType] == [EPSILON]
        ):
            break

        statementList.extend([self.parseStatement()])

    return statementList

def parseStatement(self: Parser) -> Statement:
    currentTokenType = self.currentType(0)

    # check statement
    if currentTokenType not in PREDICT["<statement>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<statement>"].keys())
        )

    # declaration statement
    if currentTokenType in (
        TK_DTYPE_TALLY,
        TK_DTYPE_DIVINE,
        TK_DTYPE_SIGIL,
        TK_DTYPE_SCRIPTURE,
        TK_DTYPE_VERITY,
        TK_OTHERS_ORDAIN,
        TK_OTHERS_ORDER,
    ):
        return self.parseDeclarationStatement()

    # input/output statement
    if currentTokenType in (TK_IO_RECEIVE, TK_IO_PROCLAIM):
        return self.parseInputOutputStatement()

    # condition statement
    if currentTokenType in (TK_CF_DECREE, TK_CF_DISCERN):
        return self.parseConditionStatement()

    # loop statement
    if currentTokenType in (TK_CF_PROCESSION, TK_CF_ENDURE, TK_CF_RITUAL):
        return self.parseLoopStatement()

    # jump statement
    if currentTokenType in (TK_CF_DISMISS, TK_CF_PROCEED, TK_CF_FALL, TK_CF_ABSOLVE):
        return self.parseJumpStatement()

    # prefix incdec statement
    if currentTokenType in (TK_OP_INC, TK_OP_DEC):
        return self.parsePrefixIncrementDecrementStatement()

    # parenthesized postfix incdec
    if currentTokenType == TK_SYM_OPPAREN:
        return self.parseParenthesizedPostfixIncrementDecrementStatement()

    # identifier statement
    if currentTokenType == TK_IDENTIFIER:
        identifierToken = self.expect(TK_IDENTIFIER)
        identifierName = getTokenValue(identifierToken)

        return self.parseStatementIdentifierTail(
            identifierToken,
            identifierName
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        list(PREDICT["<statement>"].keys())
    )

Parser.parseStatementList = parseStatementList
Parser.parseStatement = parseStatement