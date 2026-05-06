from __future__ import annotations

from backend.tokens import *
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseLeftHandValue(self: Parser) -> LeftHandValue:
    currentTokenType = self.currentType(0)

    # check lvalue
    if currentTokenType not in PREDICT["<lvalue>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<lvalue>"].keys())
        )

    identifierToken = self.expect(TK_IDENTIFIER)

    baseReference: LeftHandValue = NameReference(
        position=getTokenPosition(identifierToken),
        name=getTokenValue(identifierToken)
    )

    accessReference = self.parseAccessChainOptional(baseReference=baseReference)

    if accessReference is not None:
        return accessReference

    return baseReference

def parseLeftHandValueCore(self: Parser) -> LeftHandValue:
    currentTokenType = self.currentType(0)

    # check lvalue core
    if currentTokenType not in PREDICT["<lvalue_core>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<lvalue_core>"].keys())
        )

    # grouped lvalue
    if currentTokenType == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        innerReference = self.parseLeftHandValueCore()
        self.expect(TK_SYM_CLSPAREN)

        return innerReference

    identifierToken = self.expect(TK_IDENTIFIER)

    baseReference: LeftHandValue = NameReference(
        position=getTokenPosition(identifierToken),
        name=getTokenValue(identifierToken)
    )

    accessReference = self.parseAccessChainOptional(baseReference=baseReference)

    if accessReference is not None:
        return accessReference

    return baseReference

Parser.parseLeftHandValue = parseLeftHandValue
Parser.parseLeftHandValueCore = parseLeftHandValueCore