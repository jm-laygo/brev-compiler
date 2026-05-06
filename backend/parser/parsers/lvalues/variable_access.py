from __future__ import annotations
from typing import Optional

from backend.tokens import *
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseAccessChainOptional(self: Parser, baseReference: LeftHandValue) -> Optional[LeftHandValue]:
    currentTokenType = self.currentType(0)

    # check access chain
    if currentTokenType not in PREDICT["<access_chain_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<access_chain_opt>"].keys())
        )

    # no access chain
    if PREDICT["<access_chain_opt>"][currentTokenType] == [EPSILON]:
        return None

    return self.parseAccessChain(baseReference)

def parseAccessChain(self: Parser, baseReference: LeftHandValue) -> LeftHandValue:
    currentTokenType = self.currentType(0)

    # check access chain
    if currentTokenType not in PREDICT["<access_chain>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<access_chain>"].keys())
        )

    currentReference = baseReference

    # read index or member access
    while self.currentType(0) in (TK_SYM_OPBRACK, TK_SYM_DOT):
        currentReference = self.parseAccessStep(currentReference)

    return currentReference

def parseAccessStep(self: Parser, baseReference: LeftHandValue) -> LeftHandValue:
    currentTokenType = self.currentType(0)

    # check access step
    if currentTokenType not in PREDICT["<access_step>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<access_step>"].keys())
        )

    # array index
    if currentTokenType == TK_SYM_OPBRACK:
        openingBracketToken = self.expect(TK_SYM_OPBRACK)
        indexExpression = self.parseExpression()
        self.expect(TK_SYM_CLSBRACK)

        return IndexReference(
            position=getTokenPosition(openingBracketToken),
            baseReference=baseReference,
            indexExpression=indexExpression
        )

    # member access
    dotToken = self.expect(TK_SYM_DOT)
    memberToken = self.expect(TK_IDENTIFIER)

    return MemberReference(
        position=getTokenPosition(dotToken),
        baseReference=baseReference,
        memberName=getTokenValue(memberToken)
    )

Parser.parseAccessChainOptional = parseAccessChainOptional
Parser.parseAccessChain = parseAccessChain
Parser.parseAccessStep = parseAccessStep