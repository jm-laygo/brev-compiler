from __future__ import annotations
from typing import Any

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseUnaryExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # reject minus
    if currentTokenType == TK_OP_MINUS:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            [TK_OP_TILDE],
            "Unary minus (-) is not allowed. Use ~ for negation."
        )

    # check unary expression
    if currentTokenType not in PREDICT["<unary_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<unary_expr>"].keys())
        )

    # prefix not or negation
    if currentTokenType in (TK_OP_NOT, TK_OP_TILDE):
        operatorToken = self.advance()
        operandExpression = self.parseUnaryExpression()

        operatorLexeme = getTokenValue(operatorToken) or (
            "!" if currentTokenType == TK_OP_NOT else "~"
        )

        return UnaryExpression(
            position=getTokenPosition(operatorToken),
            operator=operatorLexeme,
            operand=operandExpression,
            isPrefix=True
        )

    # prefix increment or decrement
    if currentTokenType in (TK_OP_INC, TK_OP_DEC):
        operatorToken = self.advance()
        targetReference = self.parseLeftHandValueCore()

        return UnaryExpression(
            position=getTokenPosition(operatorToken),
            operator=getTokenValue(operatorToken) or (
                "++" if currentTokenType == TK_OP_INC else "--"
            ),
            operand=VariableExpression(
                position=getTokenPosition(operatorToken),
                reference=targetReference
            ),
            isPrefix=True
        )

    return self.parsePostfixExpression()

def parsePostfixExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check postfix expression
    if currentTokenType not in PREDICT["<postfix_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<postfix_expr>"].keys())
        )

    baseExpression = self.parsePrimaryExpression()

    # postfix increment or decrement
    if self.currentType(0) in (TK_OP_INC, TK_OP_DEC):
        operatorToken = self.advance()

        operatorLexeme = getTokenValue(operatorToken) or (
            "++" if operatorToken.type == TK_OP_INC else "--"
        )

        return UnaryExpression(
            position=getTokenPosition(operatorToken),
            operator=operatorLexeme,
            operand=baseExpression,
            isPrefix=False
        )

    return baseExpression

def parsePrimaryExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check primary expression
    if currentTokenType not in PREDICT["<primary>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<primary>"].keys())
        )

    # literal
    if currentTokenType in (
        TK_LIT_INT,
        TK_LIT_DECIMAL,
        TK_LIT_CHAR,
        TK_LIT_STRING,
        TK_LIT_BOOL
    ):
        return self.parseLiteralExpression()

    # grouped expression
    if currentTokenType == TK_SYM_OPPAREN:
        openingParenthesisToken = self.expect(TK_SYM_OPPAREN)
        innerExpression = self.parseExpression()
        self.expect(TK_SYM_CLSPAREN)

        return GroupExpression(
            position=getTokenPosition(openingParenthesisToken),
            expression=innerExpression
        )

    # verseof expression
    if currentTokenType == TK_OTHERS_VERSEOF:
        verseOfToken = self.expect(TK_OTHERS_VERSEOF)
        self.expect(TK_SYM_OPPAREN)
        innerExpression = self.parseExpression()
        self.expect(TK_SYM_CLSPAREN)

        return VerseOfExpression(
            position=getTokenPosition(verseOfToken),
            expression=innerExpression
        )

    # identifier expression
    if currentTokenType == TK_IDENTIFIER:
        identifierToken = self.expect(TK_IDENTIFIER)
        identifierName = getTokenValue(identifierToken)

        return self.parseIdentifierPrimaryTail(
            identifierToken,
            identifierName
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        list(PREDICT["<primary>"].keys())
    )

def parseIdentifierPrimaryTail(self: Parser, identifierToken: Any, identifierName: str) -> Expression:
    currentTokenType = self.currentType(0)

    # check identifier tail
    if currentTokenType not in PREDICT["<id_primary_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<id_primary_tail>"].keys())
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

        accessChain = self.parseAccessChainOptional(baseReference)

        return FunctionCallExpression(
            position=getTokenPosition(identifierToken),
            calleeName=identifierName,
            arguments=argumentList,
            accessChain=accessChain
        )

    # variable or member access
    baseReference: LeftHandValue = NameReference(
        position=getTokenPosition(identifierToken),
        name=identifierName
    )

    accessChain = self.parseAccessChainOptional(baseReference)

    if accessChain is not None:
        resolvedReference = accessChain
    else:
        resolvedReference = baseReference

    return VariableExpression(
        position=getTokenPosition(identifierToken),
        reference=resolvedReference
    )

Parser.parseUnaryExpression = parseUnaryExpression
Parser.parsePostfixExpression = parsePostfixExpression
Parser.parsePrimaryExpression = parsePrimaryExpression
Parser.parseIdentifierPrimaryTail = parseIdentifierPrimaryTail