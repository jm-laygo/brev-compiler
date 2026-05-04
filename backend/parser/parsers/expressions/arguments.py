from __future__ import annotations
from typing import List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser


def parseArgumentListOptional(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    # check argument list start
    if currentTokenType not in PREDICT["<arg_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<arg_list_opt>"].keys())
        )

    # no arguments
    if currentTokenType == TK_SYM_CLSPAREN:
        return []

    return self.parseArgumentList()

def parseArgumentList(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    # check first argument
    if currentTokenType not in PREDICT["<arg_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<arg_list>"].keys())
        )

    argumentList = [self.parseExpressionession()]
    argumentList.extend(self.parseArgumentListTail())

    return argumentList

def parseArgumentListTail(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    # check next argument
    if currentTokenType not in PREDICT["<arg_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<arg_list_tail>"].keys())
        )

    # end of argument list
    if currentTokenType == TK_SYM_CLSPAREN:
        return []

    self.expect(TK_SYM_COMMA)

    remainingArguments = [self.parseExpressionession()]
    remainingArguments.extend(self.parseArgumentListTail())

    return remainingArguments

Parser.parseArgumentListOptional = parseArgumentListOptional
Parser.parseArgumentList = parseArgumentList
Parser.parseArgumentListTail = parseArgumentListTail