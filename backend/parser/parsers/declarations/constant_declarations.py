from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseSacredInitializationList(self: Parser) -> List[SacredItem]:
    currentTokenType = self.currentType(0)

    # check sacred list
    if currentTokenType not in PREDICT["<sacred_init_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<sacred_init_list>"].keys())
        )

    sacredItems = [self.parseSacredInitialization()]
    sacredItems.extend(self.parseSacredInitializationTail())

    return sacredItems

def parseSacredInitializationTail(self: Parser) -> List[SacredItem]:
    currentTokenType = self.currentType(0)

    # check next sacred
    if currentTokenType not in PREDICT["<sacred_init_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<sacred_init_tail>"].keys())
        )

    # end of sacred list
    if currentTokenType == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)

    remainingSacredItems = [self.parseSacredInitialization()]
    remainingSacredItems.extend(self.parseSacredInitializationTail())

    return remainingSacredItems

def parseSacredInitialization(self: Parser) -> SacredItem:
    currentTokenType = self.currentType(0)

    # check sacred item
    if currentTokenType not in PREDICT["<sacred_init>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<sacred_init>"].keys())
        )

    identifierToken = self.expect(TK_IDENTIFIER)
    initialValue = self.parseSacredAssignmentOptional()

    return SacredItem(
        position=getTokenPosition(identifierToken),
        name=getTokenValue(identifierToken),
        value=initialValue
    )

def parseSacredAssignmentOptional(self: Parser) -> Optional[Expression]:
    currentTokenType = self.currentType(0)

    # check sacred assign
    if currentTokenType not in PREDICT["<sacred_assign_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<sacred_assign_opt>"].keys())
        )

    # no initial value
    if currentTokenType in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)

    return self.parseConstantExpression()

Parser.parseSacredInitializationList = parseSacredInitializationList
Parser.parseSacredInitializationTail = parseSacredInitializationTail
Parser.parseSacredInitialization = parseSacredInitialization
Parser.parseSacredAssignmentOptional = parseSacredAssignmentOptional