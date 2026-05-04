from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check expression start
    if currentTokenType not in PREDICT["<Expression>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<Expression>"].keys())
        )

    return self.parseLogicOr()


def parseLogicOr(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check or expression
    if currentTokenType not in PREDICT["<logic_or>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<logic_or>"].keys())
        )

    leftExpression = self.parseLogicAnd()

    # parse ||
    while self.currentType(0) == TK_OP_OR:
        operatorToken = self.advance()
        rightExpression = self.parseLogicAnd()

        leftExpression = BinaryExpression(
            position=getTokenPosition(operatorToken),
            left=leftExpression,
            op=getTokenValue(operatorToken) or "or",
            right=rightExpression
        )

    return leftExpression


def parseLogicAnd(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check and expression
    if currentTokenType not in PREDICT["<logic_and>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<logic_and>"].keys())
        )

    leftExpression = self.parseEquality()

    # parse &&
    while self.currentType(0) == TK_OP_AND:
        operatorToken = self.advance()
        rightExpression = self.parseEquality()

        leftExpression = BinaryExpression(
            position=getTokenPosition(operatorToken),
            left=leftExpression,
            op=getTokenValue(operatorToken) or "and",
            right=rightExpression
        )

    return leftExpression


def parseEquality(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check equality expression
    if currentTokenType not in PREDICT["<equality>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<equality>"].keys())
        )

    leftExpression = self.parseRelational()

    # parse == and !=
    while self.currentType(0) in (TK_OP_EQ, TK_OP_NOT_EQ):
        operatorToken = self.advance()
        rightExpression = self.parseRelational()

        operatorLexeme = getTokenValue(operatorToken) or (
            "==" if operatorToken.type == TK_OP_EQ else "!="
        )

        leftExpression = BinaryExpression(
            position=getTokenPosition(operatorToken),
            left=leftExpression,
            op=operatorLexeme,
            right=rightExpression
        )

    return leftExpression


def parseRelational(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check relational expression
    if currentTokenType not in PREDICT["<relational>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<relational>"].keys())
        )

    leftExpression = self.parseArithmeticExpression()

    # parse comparisons
    while self.currentType(0) in (TK_OP_GT, TK_OP_LT, TK_OP_GTE, TK_OP_LTE):
        operatorToken = self.advance()
        rightExpression = self.parseArithmeticExpression()

        operatorLexeme = getTokenValue(operatorToken) or {
            TK_OP_GT: ">",
            TK_OP_LT: "<",
            TK_OP_GTE: ">=",
            TK_OP_LTE: "<=",
        }.get(operatorToken.type, str(operatorToken.type))

        leftExpression = BinaryExpression(
            position=getTokenPosition(operatorToken),
            left=leftExpression,
            op=operatorLexeme,
            right=rightExpression
        )

    return leftExpression


def parseArithmeticExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check arithmetic expression
    if currentTokenType not in PREDICT["<arith_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<arith_expr>"].keys())
        )

    leftExpression = self.parseMultiplicativeExpression()

    # parse + - and &
    while self.currentType(0) in (TK_OP_PLUS, TK_OP_MINUS, TK_OP_CONCAT):
        operatorToken = self.advance()
        rightExpression = self.parseMultiplicativeExpression()

        operatorLexeme = getTokenValue(operatorToken) or {
            TK_OP_PLUS: "+",
            TK_OP_MINUS: "-",
            TK_OP_CONCAT: "&",
        }.get(operatorToken.type, str(operatorToken.type))

        leftExpression = BinaryExpression(
            position=getTokenPosition(operatorToken),
            left=leftExpression,
            op=operatorLexeme,
            right=rightExpression
        )

    return leftExpression


def parseMultiplicativeExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check mult expression
    if currentTokenType not in PREDICT["<mul_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<mul_expr>"].keys())
        )

    leftExpression = self.parsePowerExpression()

    # parse * / %
    while self.currentType(0) in (TK_OP_MUL, TK_OP_DIV, TK_OP_MOD):
        operatorToken = self.advance()
        rightExpression = self.parsePowerExpression()

        operatorLexeme = getTokenValue(operatorToken) or {
            TK_OP_MUL: "*",
            TK_OP_DIV: "/",
            TK_OP_MOD: "%",
        }.get(operatorToken.type, str(operatorToken.type))

        leftExpression = BinaryExpression(
            position=getTokenPosition(operatorToken),
            left=leftExpression,
            op=operatorLexeme,
            right=rightExpression
        )

    return leftExpression


def parsePowerExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check power expression
    if currentTokenType not in PREDICT["<pow_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<pow_expr>"].keys())
        )

    leftExpression = self.parseUnaryExpression()

    # right associative power
    if self.currentType(0) == TK_OP_POW:
        operatorToken = self.advance()
        rightExpression = self.parsePowerExpression()

        leftExpression = BinaryExpression(
            position=getTokenPosition(operatorToken),
            left=leftExpression,
            op=getTokenValue(operatorToken) or "^",
            right=rightExpression
        )

    return leftExpression


Parser.parseExpression = parseExpression
Parser.parseLogicOr = parseLogicOr
Parser.parseLogicAnd = parseLogicAnd
Parser.parseEquality = parseEquality
Parser.parseRelational = parseRelational
Parser.parseArithmeticExpression = parseArithmeticExpression
Parser.parseMultiplicativeExpression = parseMultiplicativeExpression
Parser.parsePowerExpression = parsePowerExpression