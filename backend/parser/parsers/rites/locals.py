from __future__ import annotations
from typing import Any, List

from backend.parser.predict_set import PREDICT, EPSILON
from backend.errors import ParserError
from backend.parser.parser import Parser


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

    return self.parseGlobalDeclarationItem()

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