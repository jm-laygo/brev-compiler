from __future__ import annotations
from typing import Any, List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseGlobalDeclarationOptional(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check global declaration
    if currentTokenType not in PREDICT["<global_dec_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<global_dec_opt>"].keys())
        )

    # no global declaration
    if PREDICT["<global_dec_opt>"][currentTokenType] == [EPSILON]:
        return []

    return self.parseGlobalDeclarationList()

def parseGlobalDeclarationList(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check declaration list
    if currentTokenType not in PREDICT["<global_dec_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<global_dec_list>"].keys())
        )

    globalDeclarations: List[Any] = []
    globalDeclarations.extend([self.parseGlobalDeclarationItem()])
    globalDeclarations.extend(self.parseGlobalDeclarationListTail())

    return globalDeclarations

def parseGlobalDeclarationListTail(self: Parser) -> List[Any]:
    currentTokenType = self.currentType(0)

    # check next declaration
    if currentTokenType not in PREDICT["<global_dec_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<global_dec_list_tail>"].keys())
        )

    # no more declaration
    if PREDICT["<global_dec_list_tail>"][currentTokenType] == [EPSILON]:
        return []

    remainingGlobalDeclarations: List[Any] = []
    remainingGlobalDeclarations.extend([self.parseGlobalDeclarationItem()])
    remainingGlobalDeclarations.extend(self.parseGlobalDeclarationListTail())

    return remainingGlobalDeclarations

def parseGlobalDeclarationItem(self: Parser) -> Any:
    currentTokenType = self.currentType(0)

    # check declaration item
    if currentTokenType not in PREDICT["<global_dec_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<global_dec_item>"].keys())
        )

    # sacred declaration
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

    # variable declaration
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

    # order declaration
    if currentTokenType == TK_OTHERS_ORDER:
        orderToken = self.expect(TK_OTHERS_ORDER)
        identifierName = getTokenValue(self.expect(TK_IDENTIFIER))
        self.expect(TK_SYM_OPBRACE)
        memberList = self.parseMemberListOptional()
        self.expect(TK_SYM_CLSBRACE)
        self.expect(TK_SYM_SEMICOL)

        return OrderDeclaration(
            position=getTokenPosition(orderToken),
            name=identifierName,
            members=memberList
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        list(PREDICT["<global_dec_item>"].keys())
    )

Parser.parseGlobalDeclarationOptional = parseGlobalDeclarationOptional
Parser.parseGlobalDeclarationList = parseGlobalDeclarationList
Parser.parseGlobalDeclarationListTail = parseGlobalDeclarationListTail
Parser.parseGlobalDeclarationItem = parseGlobalDeclarationItem