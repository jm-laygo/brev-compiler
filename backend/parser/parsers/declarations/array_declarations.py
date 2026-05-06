from __future__ import annotations
from typing import List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenPosition


def parseArrayDimensionsTail(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    # check array dimension
    if currentTokenType not in PREDICT["<array_dims_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<array_dims_tail>"].keys())
        )

    # no more dimension
    if PREDICT["<array_dims_tail>"][currentTokenType] == [EPSILON]:
        return []

    self.expect(TK_SYM_OPBRACK)
    dimensionExpression = self.parseExpression()
    self.expect(TK_SYM_CLSBRACK)

    remainingDimensions = self.parseArrayDimensionsTail()

    return [dimensionExpression] + remainingDimensions

def parseArrayInitialization(self: Parser) -> ArrayInitializationExpression:
    currentTokenType = self.currentType(0)

    # check array init
    if currentTokenType not in PREDICT["<array_init>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<array_init>"].keys())
        )

    openingBraceToken = self.expect(TK_SYM_OPBRACE)
    arrayItems = self.parseArrayValuesOptional()
    self.expect(TK_SYM_CLSBRACE)

    return ArrayInitializationExpression(
        position=getTokenPosition(openingBraceToken),
        items=arrayItems
    )

def parseArrayValuesOptional(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    # check array values
    if currentTokenType not in PREDICT["<array_vals_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<array_vals_opt>"].keys())
        )

    # empty array
    if currentTokenType == TK_SYM_CLSBRACE:
        return []

    return self.parseArrayValues()

def parseArrayValues(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    # check first value
    if currentTokenType not in PREDICT["<array_vals>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<array_vals>"].keys())
        )

    arrayValues = [self.parseArrayValue()]
    arrayValues.extend(self.parseArrayValuesTail())

    return arrayValues

def parseArrayValuesTail(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    # check next value
    if currentTokenType not in PREDICT["<array_vals_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<array_vals_tail>"].keys())
        )

    # end of array
    if currentTokenType == TK_SYM_CLSBRACE:
        return []

    self.expect(TK_SYM_COMMA)

    remainingArrayValues = [self.parseArrayValue()]
    remainingArrayValues.extend(self.parseArrayValuesTail())

    return remainingArrayValues

def parseArrayValue(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check array value
    if currentTokenType not in PREDICT["<array_val>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<array_val>"].keys())
        )

    # nested array
    if currentTokenType == TK_SYM_OPBRACE:
        openingBraceToken = self.expect(TK_SYM_OPBRACE)
        nestedArrayItems = self.parseArrayValuesOptional()
        self.expect(TK_SYM_CLSBRACE)

        return ArrayInitializationExpression(
            position=getTokenPosition(openingBraceToken),
            items=nestedArrayItems
        )

    return self.parseExpression()

Parser.parseArrayDimensionsTail = parseArrayDimensionsTail
Parser.parseArrayInitialization = parseArrayInitialization
Parser.parseArrayValuesOptional = parseArrayValuesOptional
Parser.parseArrayValues = parseArrayValues
Parser.parseArrayValuesTail = parseArrayValuesTail
Parser.parseArrayValue = parseArrayValue