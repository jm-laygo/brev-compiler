from __future__ import annotations
from typing import Any

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parsePrefixIncrementDecrementStatement(self: Parser) -> IncrementDecrementStatement:
    currentTokenType = self.currentType(0)

    # check prefix incdec
    if currentTokenType not in PREDICT["<prefix_incdec_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<prefix_incdec_stmt>"].keys())
        )

    operatorToken = self.advance()
    operatorLexeme = getTokenValue(operatorToken) or (
        "++" if operatorToken.type == TK_OP_INC else "--"
    )

    targetReference = self.parseLeftHandValueCore()
    self.expect(TK_SYM_SEMICOL)

    return IncrementDecrementStatement(
        position=getTokenPosition(operatorToken),
        target=targetReference,
        operator=operatorLexeme,
        isPrefix=True
    )

def parseParenthesizedPostfixIncrementDecrementStatement(self: Parser) -> IncrementDecrementStatement:
    currentTokenType = self.currentType(0)

    # check paren postfix incdec
    if currentTokenType not in PREDICT["<paren_postfix_incdec_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<paren_postfix_incdec_stmt>"].keys())
        )

    openingParenthesisToken = self.expect(TK_SYM_OPPAREN)
    targetReference = self.parseLeftHandValueCore()
    self.expect(TK_SYM_CLSPAREN)

    # require incdec after paren
    if self.currentType(0) not in (TK_OP_INC, TK_OP_DEC):
        raise ParserError(
            self.peek(0) or self.peek(-1),
            [TK_OP_INC, TK_OP_DEC]
        )

    operatorToken = self.advance()
    operatorLexeme = getTokenValue(operatorToken) or (
        "++" if operatorToken.type == TK_OP_INC else "--"
    )

    self.expect(TK_SYM_SEMICOL)

    return IncrementDecrementStatement(
        position=getTokenPosition(openingParenthesisToken),
        target=targetReference,
        operator=operatorLexeme,
        isPrefix=False
    )

def parseStatementIdentifierTail(self: Parser, identifierToken: Any, identifierName: str) -> Statement:
    currentTokenType = self.currentType(0)

    # check identifier statement
    if currentTokenType not in PREDICT["<stmt_id_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<stmt_id_tail>"].keys())
        )

    # function call
    if currentTokenType == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        argumentList = self.parseArgumentListOptional()
        self.expect(TK_SYM_CLSPAREN)

        baseReference = NameReference(
            position=getTokenPosition(identifierToken),
            name=identifierName
        )

        accessReference = self.parseAccessChainOptional(
            baseReference=baseReference
        )

        self.expect(TK_SYM_SEMICOL)

        return FunctionCallStatement(
            position=getTokenPosition(identifierToken),
            calleeName=identifierName,
            arguments=argumentList,
            accessChain=accessReference
        )

    baseReference: LeftHandValue = NameReference(
        position=getTokenPosition(identifierToken),
        name=identifierName
    )

    accessReference = self.parseAccessChainOptional(
        baseReference=baseReference
    )

    if accessReference is not None:
        targetReference = accessReference
    else:
        targetReference = baseReference

    currentTokenType = self.currentType(0)

    # check assignment or postfix
    if currentTokenType not in PREDICT["<stmt_after_access>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<stmt_after_access>"].keys())
        )

    # assignment
    if currentTokenType in (
        TK_OP_ASSIGN,
        TK_OP_PLUS_EQ,
        TK_OP_MINUS_EQ,
        TK_OP_MUL_EQ,
        TK_OP_DIV_EQ,
        TK_OP_MOD_EQ,
        TK_OP_POW_EQ
    ):
        operatorToken = self.advance()
        operatorLexeme = getTokenValue(operatorToken) or self.getAssignmentOperatorText(operatorToken.type)
        valueExpression = self.parseExpression()
        self.expect(TK_SYM_SEMICOL)

        return AssignmentStatement(
            position=getTokenPosition(operatorToken),
            target=targetReference,
            operator=operatorLexeme,
            value=valueExpression
        )

    # postfix incdec
    if currentTokenType in (TK_OP_INC, TK_OP_DEC):
        operatorToken = self.advance()
        operatorLexeme = getTokenValue(operatorToken) or (
            "++" if operatorToken.type == TK_OP_INC else "--"
        )

        self.expect(TK_SYM_SEMICOL)

        return IncrementDecrementStatement(
            position=getTokenPosition(operatorToken),
            target=targetReference,
            operator=operatorLexeme,
            isPrefix=False
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        list(PREDICT["<stmt_after_access>"].keys())
    )

def getAssignmentOperatorText(self: Parser, tokenType: Any) -> str:
    return {
        TK_OP_ASSIGN: "=",
        TK_OP_PLUS_EQ: "+=",
        TK_OP_MINUS_EQ: "-=",
        TK_OP_MUL_EQ: "*=",
        TK_OP_DIV_EQ: "/=",
        TK_OP_MOD_EQ: "%=",
        TK_OP_POW_EQ: "^=",
    }.get(tokenType, str(tokenType))

Parser.parsePrefixIncrementDecrementStatement = parsePrefixIncrementDecrementStatement
Parser.parseParenthesizedPostfixIncrementDecrementStatement = parseParenthesizedPostfixIncrementDecrementStatement
Parser.parseStatementIdentifierTail = parseStatementIdentifierTail
Parser.getAssignmentOperatorText = getAssignmentOperatorText