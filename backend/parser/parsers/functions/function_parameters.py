from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseParameterListOptional(self: Parser) -> List[Parameter]:
    currentTokenType = self.currentType(0)

    # check parameter list
    if currentTokenType not in PREDICT["<param_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<param_list_opt>"].keys())
        )

    # no parameter
    if currentTokenType == TK_SYM_CLSPAREN:
        return []

    return self.parseParameterList()

def parseParameterList(self: Parser) -> List[Parameter]:
    currentTokenType = self.currentType(0)

    # check first parameter
    if currentTokenType not in PREDICT["<param_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<param_list>"].keys())
        )

    parameterList = [self.parseParameter()]
    parameterList.extend(self.parseParameterListTail())

    return parameterList

def parseParameterListTail(self: Parser) -> List[Parameter]:
    currentTokenType = self.currentType(0)

    # check next parameter
    if currentTokenType not in PREDICT["<param_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<param_list_tail>"].keys())
        )

    # end of parameter list
    if currentTokenType == TK_SYM_CLSPAREN:
        return []

    self.expect(TK_SYM_COMMA)

    remainingParameters = [self.parseParameter()]
    remainingParameters.extend(self.parseParameterListTail())

    return remainingParameters

def parseParameter(self: Parser) -> Parameter:
    currentTokenType = self.currentType(0)

    # check parameter
    if currentTokenType not in PREDICT["<param>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<param>"].keys())
        )

    typeName = self.parseDataTypeIdentifier()
    identifierToken = self.expect(TK_IDENTIFIER)
    dimensions = self.parseParameterArrayTail()

    return Parameter(
        position=getTokenPosition(identifierToken),
        typeName=typeName,
        name=getTokenValue(identifierToken),
        dimensions=dimensions
    )

def parseParameterArrayTail(self: Parser) -> List[Optional[Expression]]:
    currentTokenType = self.currentType(0)

    # check parameter array
    if currentTokenType not in PREDICT["<param_array_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<param_array_tail>"].keys())
        )

    dimensions: List[Optional[Expression]] = []

    # read dimensions
    while self.currentType(0) == TK_SYM_OPBRACK:
        self.expect(TK_SYM_OPBRACK)
        dimensionExpression = self.parseParameterDimensionExpressionOptional()
        self.expect(TK_SYM_CLSBRACK)

        dimensions.extend([dimensionExpression])

    return dimensions

def parseParameterDimensionExpressionOptional(self: Parser) -> Optional[Expression]:
    currentTokenType = self.currentType(0)

    # check dimension value
    if currentTokenType not in PREDICT["<param_dim_expr_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<param_dim_expr_opt>"].keys())
        )

    # empty dimension
    if currentTokenType == TK_SYM_CLSBRACK:
        return None

    return self.parseExpression()

Parser.parseParameterListOptional = parseParameterListOptional
Parser.parseParameterList = parseParameterList
Parser.parseParameterListTail = parseParameterListTail
Parser.parseParameter = parseParameter
Parser.parseParameterArrayTail = parseParameterArrayTail
Parser.parseParameterDimensionExpressionOptional = parseParameterDimensionExpressionOptional