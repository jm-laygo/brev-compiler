from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def createBinaryExpression(operatorToken, leftExpression, rightExpression, fallbackOperator):
    return BinaryExpression(
        position=getTokenPosition(operatorToken),
        leftExpression=leftExpression,
        operator=getTokenValue(operatorToken) or fallbackOperator,
        rightExpression=rightExpression
    )


def parseExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<expr>"].keys())
        )

    return self.parseLogicOr()


def parseLogicOr(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<logic_or>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<logic_or>"].keys())
        )

    leftExpression = self.parseLogicAnd()

    while self.currentType(0) == TK_OP_OR:
        operatorToken = self.advance()
        rightExpression = self.parseLogicAnd()

        leftExpression = createBinaryExpression(
            operatorToken,
            leftExpression,
            rightExpression,
            "or"
        )

    return leftExpression


def parseLogicAnd(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<logic_and>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<logic_and>"].keys())
        )

    leftExpression = self.parseEquality()

    while self.currentType(0) == TK_OP_AND:
        operatorToken = self.advance()
        rightExpression = self.parseEquality()

        leftExpression = createBinaryExpression(
            operatorToken,
            leftExpression,
            rightExpression,
            "and"
        )

    return leftExpression


def parseEquality(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<equality>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<equality>"].keys())
        )

    leftExpression = self.parseRelational()

    while self.currentType(0) in (TK_OP_EQ, TK_OP_NOT_EQ):
        operatorToken = self.advance()
        rightExpression = self.parseRelational()

        fallbackOperator = "==" if operatorToken.type == TK_OP_EQ else "!="

        leftExpression = createBinaryExpression(
            operatorToken,
            leftExpression,
            rightExpression,
            fallbackOperator
        )

    return leftExpression


def parseRelational(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<relational>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<relational>"].keys())
        )

    leftExpression = self.parseArithmeticExpression()

    while self.currentType(0) in (TK_OP_GT, TK_OP_LT, TK_OP_GTE, TK_OP_LTE):
        operatorToken = self.advance()
        rightExpression = self.parseArithmeticExpression()

        fallbackOperator = {
            TK_OP_GT: ">",
            TK_OP_LT: "<",
            TK_OP_GTE: ">=",
            TK_OP_LTE: "<=",
        }.get(operatorToken.type, str(operatorToken.type))

        leftExpression = createBinaryExpression(
            operatorToken,
            leftExpression,
            rightExpression,
            fallbackOperator
        )

    return leftExpression


def parseArithmeticExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<arith_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<arith_expr>"].keys())
        )

    leftExpression = self.parseMultiplicativeExpression()

    while self.currentType(0) in (TK_OP_PLUS, TK_OP_MINUS, TK_OP_CONCAT):
        operatorToken = self.advance()
        rightExpression = self.parseMultiplicativeExpression()

        fallbackOperator = {
            TK_OP_PLUS: "+",
            TK_OP_MINUS: "-",
            TK_OP_CONCAT: "&",
        }.get(operatorToken.type, str(operatorToken.type))

        leftExpression = createBinaryExpression(
            operatorToken,
            leftExpression,
            rightExpression,
            fallbackOperator
        )

    return leftExpression


def parseMultiplicativeExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<mul_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<mul_expr>"].keys())
        )

    leftExpression = self.parsePowerExpression()

    while self.currentType(0) in (TK_OP_MUL, TK_OP_DIV, TK_OP_MOD):
        operatorToken = self.advance()
        rightExpression = self.parsePowerExpression()

        fallbackOperator = {
            TK_OP_MUL: "*",
            TK_OP_DIV: "/",
            TK_OP_MOD: "%",
        }.get(operatorToken.type, str(operatorToken.type))

        leftExpression = createBinaryExpression(
            operatorToken,
            leftExpression,
            rightExpression,
            fallbackOperator
        )

    return leftExpression


def parsePowerExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<pow_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<pow_expr>"].keys())
        )

    leftExpression = self.parseUnaryExpression()

    if self.currentType(0) == TK_OP_POW:
        operatorToken = self.advance()
        rightExpression = self.parsePowerExpression()

        leftExpression = createBinaryExpression(
            operatorToken,
            leftExpression,
            rightExpression,
            "^"
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