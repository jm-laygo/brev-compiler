from __future__ import annotations
from typing import Any, List

from backend.tokens import *
from backend.parser.predict_set import PREDICT, EPSILON
from backend.errors import ParserError
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseFunctionLocalDeclarationOptional(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check local declaration
    if currentTokenType not in PREDICT["<func_local_dec_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<func_local_dec_opt>"].keys())
        )

    # no local declaration
    if PREDICT["<func_local_dec_opt>"][currentTokenType] == [EPSILON]:
        return []

    return self.parseFunctionLocalDeclaration()


def parseFunctionLocalDeclaration(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check declaration list
    if currentTokenType not in PREDICT["<func_local_dec>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<func_local_dec>"].keys())
        )

    localDeclarations = [self.parseFunctionLocalItem()]
    localDeclarations.extend(self.parseFunctionLocalDeclarationTail())

    return localDeclarations


def parseFunctionLocalDeclarationTail(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check next declaration
    if currentTokenType not in PREDICT["<func_local_dec_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<func_local_dec_tail>"].keys())
        )

    # no more declaration
    if PREDICT["<func_local_dec_tail>"][currentTokenType] == [EPSILON]:
        return []

    remainingLocalDeclarations = [self.parseFunctionLocalItem()]
    remainingLocalDeclarations.extend(self.parseFunctionLocalDeclarationTail())

    return remainingLocalDeclarations


def parseFunctionLocalItem(self: Parser) -> Any:
    currentTokenType = self.currentType(0)

    # check local item
    if currentTokenType not in PREDICT["<func_local_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<func_local_item>"].keys())
        )

    # local sacred declaration
    if currentTokenType == TK_SACRED:
        sacredToken = self.expect(TK_SACRED)
        typeName = self.parseDataType()
        declarationItems = self.parseSacredInitializationList()
        self.expect(TK_SYM_SEMICOL)

        return SacredDeclaration(
            position=getTokenPosition(sacredToken),
            typeName=typeName,
            items=declarationItems
        )

    # local primitive variable declaration
    if currentTokenType in (
        TK_DTYPE_TALLY,
        TK_DTYPE_DIVINE,
        TK_DTYPE_SIGIL,
        TK_DTYPE_SCRIPTURE,
        TK_DTYPE_VERITY,
    ):
        declarationStartToken = self.peek(0)
        typeName = self.parseDataType()
        declarationItems = self.parseVariableDeclarationGroup()
        self.expect(TK_SYM_SEMICOL)

        return VariableDeclaration(
            position=getTokenPosition(declarationStartToken),
            typeName=typeName,
            items=declarationItems
        )

    # local ordain declaration
    if currentTokenType == TK_OTHERS_ORDAIN:
        ordainToken = self.expect(TK_OTHERS_ORDAIN)
        identifierName = getTokenValue(self.expect(TK_IDENTIFIER))
        declarationItems = self.parseOrdainDeclarationList()
        self.expect(TK_SYM_SEMICOL)

        return OrdainDeclaration(
            position=getTokenPosition(ordainToken),
            name=identifierName,
            items=declarationItems
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        list(PREDICT["<func_local_item>"].keys())
    )


def parseMainLocalDeclarationOptional(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check main declaration
    if currentTokenType not in PREDICT["<main_local_dec_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<main_local_dec_opt>"].keys())
        )

    # no main declaration
    if PREDICT["<main_local_dec_opt>"][currentTokenType] == [EPSILON]:
        return []

    return self.parseMainLocalDeclaration()


def parseMainLocalDeclaration(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check main declaration list
    if currentTokenType not in PREDICT["<main_local_dec>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<main_local_dec>"].keys())
        )

    localDeclarations = [self.parseMainDeclarationItem()]
    localDeclarations.extend(self.parseMainLocalDeclarationTail())

    return localDeclarations


def parseMainLocalDeclarationTail(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check next main declaration
    if currentTokenType not in PREDICT["<main_local_dec_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<main_local_dec_tail>"].keys())
        )

    # no more declaration
    if PREDICT["<main_local_dec_tail>"][currentTokenType] == [EPSILON]:
        return []

    remainingLocalDeclarations = [self.parseMainDeclarationItem()]
    remainingLocalDeclarations.extend(self.parseMainLocalDeclarationTail())

    return remainingLocalDeclarations


def parseMainDeclarationItem(self: Parser) -> Any:
    currentTokenType = self.currentType(0)

    # check main item
    if currentTokenType not in PREDICT["<main_dec_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<main_dec_item>"].keys())
        )

    return self.parseFunctionLocalItem()


Parser.parseFunctionLocalDeclarationOptional = parseFunctionLocalDeclarationOptional
Parser.parseFunctionLocalDeclaration = parseFunctionLocalDeclaration
Parser.parseFunctionLocalDeclarationTail = parseFunctionLocalDeclarationTail
Parser.parseFunctionLocalItem = parseFunctionLocalItem
Parser.parseMainLocalDeclarationOptional = parseMainLocalDeclarationOptional
Parser.parseMainLocalDeclaration = parseMainLocalDeclaration
Parser.parseMainLocalDeclarationTail = parseMainLocalDeclarationTail
Parser.parseMainDeclarationItem = parseMainDeclarationItem