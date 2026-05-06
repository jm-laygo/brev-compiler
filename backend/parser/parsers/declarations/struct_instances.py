from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseOrdainDeclarationList(self: Parser) -> List[OrdainItem]:
    currentTokenType = self.currentType(0)

    # check ordain list
    if currentTokenType not in PREDICT["<ordain_dec_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<ordain_dec_list>"].keys())
        )

    ordainItems = [self.parseOrdainDeclaration()]
    ordainItems.extend(self.parseOrdainDeclarationTail())

    return ordainItems

def parseOrdainDeclarationTail(self: Parser) -> List[OrdainItem]:
    currentTokenType = self.currentType(0)

    # check next ordain
    if currentTokenType not in PREDICT["<ordain_dec_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<ordain_dec_tail>"].keys())
        )

    # end of ordain list
    if currentTokenType == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)

    remainingOrdainItems = [self.parseOrdainDeclaration()]
    remainingOrdainItems.extend(self.parseOrdainDeclarationTail())

    return remainingOrdainItems

def parseOrdainDeclaration(self: Parser) -> OrdainItem:
    currentTokenType = self.currentType(0)

    # check ordain item
    if currentTokenType not in PREDICT["<ordain_dec>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<ordain_dec>"].keys())
        )

    identifierToken = self.expect(TK_IDENTIFIER)
    arrayDimensions = self.parseArrayDimensionsTail()
    initialValue = self.parseOrdainInitialValueOptional()

    return OrdainItem(
        position=getTokenPosition(identifierToken),
        name=getTokenValue(identifierToken),
        dimensions=arrayDimensions,
        initialValue=initialValue
    )

def parseOrdainInitialValueOptional(self: Parser) -> Optional[Expression]:
    currentTokenType = self.currentType(0)

    # check ordain init
    if currentTokenType not in PREDICT["<ordain_init_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<ordain_init_opt>"].keys())
        )

    # no initial value
    if currentTokenType in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)

    return self.parseExpression()

Parser.parseOrdainDeclarationList = parseOrdainDeclarationList
Parser.parseOrdainDeclarationTail = parseOrdainDeclarationTail
Parser.parseOrdainDeclaration = parseOrdainDeclaration
Parser.parseOrdainInitialValueOptional = parseOrdainInitialValueOptional