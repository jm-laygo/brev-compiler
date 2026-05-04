from __future__ import annotations
from typing import List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenPosition


def parseInputOutputStatement(self: Parser) -> Statement:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<io_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<io_stmt>"].keys())
        )

    if currentTokenType == TK_IO_RECEIVE:
        receiveToken = self.expect(TK_IO_RECEIVE)
        self.expect(TK_SYM_OPPAREN)

        targetReference = self.parseLeftHandValue()

        self.expect(TK_SYM_CLSPAREN)
        self.expect(TK_SYM_SEMICOL)

        return ReceiveStatement(
            position=getTokenPosition(receiveToken),
            target=targetReference
        )

    proclaimToken = self.expect(TK_IO_PROCLAIM)
    self.expect(TK_SYM_OPPAREN)

    if self.currentType(0) == TK_SYM_CLSPAREN:
        raise ParserError(
            self.peek(0),
            list(PREDICT["<output_list>"].keys()),
            "proclaim requires at least one expression."
        )

    outputArguments = self.parseOutputList()

    self.expect(TK_SYM_CLSPAREN)
    self.expect(TK_SYM_SEMICOL)

    return ProclaimStatement(
        position=getTokenPosition(proclaimToken),
        arguments=outputArguments
    )


def parseOutputListOptional(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<output_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<output_list_opt>"].keys())
        )

    if currentTokenType == TK_SYM_CLSPAREN:
        return []

    return self.parseOutputList()


def parseOutputList(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<output_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<output_list>"].keys())
        )

    outputArguments = [self.parseExpression()]
    outputArguments.extend(self.parseOutputTail())

    return outputArguments


def parseOutputTail(self: Parser) -> List[Expression]:
    currentTokenType = self.currentType(0)

    if currentTokenType not in PREDICT["<output_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<output_tail>"].keys())
        )

    if currentTokenType == TK_SYM_CLSPAREN:
        return []

    self.expect(TK_SYM_COMMA)

    remainingOutputArguments = [self.parseExpression()]
    remainingOutputArguments.extend(self.parseOutputTail())

    return remainingOutputArguments


Parser.parseInputOutputStatement = parseInputOutputStatement
Parser.parseOutputListOptional = parseOutputListOptional
Parser.parseOutputList = parseOutputList
Parser.parseOutputTail = parseOutputTail