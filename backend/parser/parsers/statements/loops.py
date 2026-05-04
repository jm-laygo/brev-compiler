from __future__ import annotations
from typing import Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseLoopStatement(self: Parser) -> Statement:
    currentTokenType = self.currentType(0)

    # check loop statement
    if currentTokenType not in PREDICT["<loop_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<loop_stmt>"].keys())
        )

    # procession loop
    if currentTokenType == TK_CF_PROCESSION:
        return self.parseProcessionStatement()

    # endure loop
    if currentTokenType == TK_CF_ENDURE:
        return self.parseEndureStatement()

    return self.parseRitualStatement()

def parseProcessionStatement(self: Parser) -> ProcessionStatement:
    currentTokenType = self.currentType(0)

    # check procession
    if currentTokenType not in PREDICT["<procession_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<procession_stmt>"].keys())
        )

    processionToken = self.expect(TK_CF_PROCESSION)
    self.expect(TK_SYM_OPPAREN)

    initializerStatement = self.parseInitializerOptional()
    self.expect(TK_SYM_SEMICOL)

    conditionExpression = self.parseExpressionOptional()
    self.expect(TK_SYM_SEMICOL)

    updateStatement = self.parseUpdateOptional()
    self.expect(TK_SYM_CLSPAREN)

    self.expect(TK_SYM_OPBRACE)
    bodyStatements = self.parseStatementList()
    self.expect(TK_SYM_CLSBRACE)

    return ProcessionStatement(
        position=getTokenPosition(processionToken),
        initializerStatement=initializerStatement,
        condition=conditionExpression,
        updateStatement=updateStatement,
        bodyStatements=bodyStatements
    )

def parseInitializerOptional(self: Parser) -> Optional[Statement]:
    currentTokenType = self.currentType(0)

    # check initializer
    if currentTokenType not in PREDICT["<init_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<init_opt>"].keys())
        )

    # no initializer
    if PREDICT["<init_opt>"][currentTokenType] == [EPSILON]:
        return None

    # variable initializer
    if currentTokenType in (
        TK_DTYPE_TALLY,
        TK_DTYPE_DIVINE,
        TK_DTYPE_SIGIL,
        TK_DTYPE_SCRIPTURE,
        TK_DTYPE_VERITY
    ):
        typeName = self.parseDataType()
        identifierToken = self.expect(TK_IDENTIFIER)
        self.expect(TK_OP_ASSIGN)
        valueExpression = self.parseExpression()

        variableDeclaration = VariableDeclaration(
            position=getTokenPosition(identifierToken),
            typeName=typeName,
            items=[
                VariableItem(
                    position=getTokenPosition(identifierToken),
                    name=getTokenValue(identifierToken),
                    dimensions=[],
                    initialValue=valueExpression
                )
            ]
        )

        return VariableDeclarationStatement(
            position=variableDeclaration.position,
            declaration=variableDeclaration
        )

    targetReference = self.parseLeftHandValue()
    self.expect(TK_OP_ASSIGN)
    valueExpression = self.parseExpression()

    return AssignmentStatement(
        position=getTokenPosition(self.peek(-1)),
        target=targetReference,
        operator="=",
        value=valueExpression
    )

def parseExpressionOptional(self: Parser) -> Optional[Expression]:
    currentTokenType = self.currentType(0)

    # check optional expression
    if currentTokenType not in PREDICT["<expr_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<expr_opt>"].keys())
        )

    # no expression
    if PREDICT["<expr_opt>"][currentTokenType] == [EPSILON]:
        return None

    return self.parseExpression()

def parseUpdateOptional(self: Parser) -> Optional[Statement]:
    currentTokenType = self.currentType(0)

    # check update
    if currentTokenType not in PREDICT["<update_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<update_opt>"].keys())
        )

    # no update
    if PREDICT["<update_opt>"][currentTokenType] == [EPSILON]:
        return None

    return self.parseUpdateExpression()

def parseUpdateExpression(self: Parser) -> Statement:
    currentTokenType = self.currentType(0)

    # check update expression
    if currentTokenType not in PREDICT["<update_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<update_expr>"].keys())
        )

    # prefix increment
    if currentTokenType == TK_OP_INC:
        operatorToken = self.expect(TK_OP_INC)
        targetReference = self.parseLeftHandValueCore()

        return IncrementDecrementStatement(
            position=getTokenPosition(operatorToken),
            target=targetReference,
            operator="++",
            isPrefix=True
        )

    # prefix decrement
    if currentTokenType == TK_OP_DEC:
        operatorToken = self.expect(TK_OP_DEC)
        targetReference = self.parseLeftHandValueCore()

        return IncrementDecrementStatement(
            position=getTokenPosition(operatorToken),
            target=targetReference,
            operator="--",
            isPrefix=True
        )

    # grouped update
    if currentTokenType == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        innerStatement = self.parseUpdateExpression()
        self.expect(TK_SYM_CLSPAREN)

        return innerStatement

    targetReference = self.parseLeftHandValue()

    return self.parseUpdateTail(targetReference)

def parseUpdateTail(self: Parser, targetReference: LeftHandValue) -> Statement:
    currentTokenType = self.currentType(0)

    # check update tail
    if currentTokenType not in PREDICT["<update_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<update_tail>"].keys())
        )

    # postfix increment
    if currentTokenType == TK_OP_INC:
        operatorToken = self.expect(TK_OP_INC)

        return IncrementDecrementStatement(
            position=getTokenPosition(operatorToken),
            target=targetReference,
            operator="++",
            isPrefix=False
        )

    # postfix decrement
    if currentTokenType == TK_OP_DEC:
        operatorToken = self.expect(TK_OP_DEC)

        return IncrementDecrementStatement(
            position=getTokenPosition(operatorToken),
            target=targetReference,
            operator="--",
            isPrefix=False
        )

    # assignment update
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

        return AssignmentStatement(
            position=getTokenPosition(operatorToken),
            target=targetReference,
            operator=operatorLexeme,
            value=valueExpression
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        [
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

def parseEndureStatement(self: Parser) -> EndureStatement:
    currentTokenType = self.currentType(0)

    # check endure
    if currentTokenType not in PREDICT["<endure_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<endure_stmt>"].keys())
        )

    endureToken = self.expect(TK_CF_ENDURE)
    self.expect(TK_SYM_OPPAREN)
    conditionExpression = self.parseExpression()
    self.expect(TK_SYM_CLSPAREN)

    self.expect(TK_SYM_OPBRACE)
    bodyStatements = self.parseStatementList()
    self.expect(TK_SYM_CLSBRACE)

    return EndureStatement(
        position=getTokenPosition(endureToken),
        condition=conditionExpression,
        bodyStatements=bodyStatements
    )

def parseRitualStatement(self: Parser) -> RitualStatement:
    currentTokenType = self.currentType(0)

    # check ritual
    if currentTokenType not in PREDICT["<ritual_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<ritual_stmt>"].keys())
        )

    ritualToken = self.expect(TK_CF_RITUAL)
    self.expect(TK_SYM_OPBRACE)
    bodyStatements = self.parseStatementList()
    self.expect(TK_SYM_CLSBRACE)

    self.expect(TK_CF_ENDURE)
    self.expect(TK_SYM_OPPAREN)
    conditionExpression = self.parseExpression()
    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_SEMICOL)

    return RitualStatement(
        position=getTokenPosition(ritualToken),
        bodyStatements=bodyStatements,
        condition=conditionExpression
    )

Parser.parseLoopStatement = parseLoopStatement
Parser.parseProcessionStatement = parseProcessionStatement
Parser.parseInitializerOptional = parseInitializerOptional
Parser.parseExpressionOptional = parseExpressionOptional
Parser.parseUpdateOptional = parseUpdateOptional
Parser.parseUpdateExpression = parseUpdateExpression
Parser.parseUpdateTail = parseUpdateTail
Parser.parseEndureStatement = parseEndureStatement
Parser.parseRitualStatement = parseRitualStatement