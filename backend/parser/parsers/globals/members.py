from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseMemberListOptional(self: Parser) -> List[OrderMember]:
    currentTokenType = self.currentType(0)

    # check member list
    if currentTokenType not in PREDICT["<member_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<member_list_opt>"].keys())
        )

    # no member
    if PREDICT["<member_list_opt>"][currentTokenType] == [EPSILON]:
        return []

    return self.parseMemberList()

def parseMemberList(self: Parser) -> List[OrderMember]:
    currentTokenType = self.currentType(0)

    # check first member
    if currentTokenType not in PREDICT["<member_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<member_list>"].keys())
        )

    memberList = [self.parseMember()]
    memberList.extend(self.parseMemberListTail())

    return memberList

def parseMemberListTail(self: Parser) -> List[OrderMember]:
    currentTokenType = self.currentType(0)

    # check next member
    if currentTokenType not in PREDICT["<member_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<member_list_tail>"].keys())
        )

    # no more member
    if PREDICT["<member_list_tail>"][currentTokenType] == [EPSILON]:
        return []

    remainingMembers = [self.parseMember()]
    remainingMembers.extend(self.parseMemberListTail())

    return remainingMembers

def parseMember(self: Parser) -> OrderMember:
    currentTokenType = self.currentType(0)

    # check member
    if currentTokenType not in PREDICT["<member>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<member>"].keys())
        )

    typeName = self.parseDataTypeIdentifier()
    memberNameToken = self.expect(TK_IDENTIFIER)
    arrayDimensions = self.parseArrayDimensionsTail()
    initialValue = self.parseMemberInitialValueOptional()
    self.expect(TK_SYM_SEMICOL)

    return OrderMember(
        position=getTokenPosition(memberNameToken),
        typeName=typeName,
        name=getTokenValue(memberNameToken),
        dimensions=arrayDimensions,
        initialValue=initialValue
    )

def parseMemberInitialValueOptional(self: Parser) -> Optional[Expression]:
    currentTokenType = self.currentType(0)

    # check member init
    if currentTokenType not in PREDICT["<member_init_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<member_init_opt>"].keys())
        )

    # no initial value
    if currentTokenType == TK_SYM_SEMICOL:
        return None

    self.expect(TK_OP_ASSIGN)

    return self.parseMemberInitialValue()

def parseMemberInitialValue(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check init value
    if currentTokenType not in PREDICT["<member_init_val>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<member_init_val>"].keys())
        )

    # array init
    if currentTokenType == TK_SYM_OPBRACE:
        return self.parseArrayInitialization()

    return self.parseExpression()

Parser.parseMemberListOptional = parseMemberListOptional
Parser.parseMemberList = parseMemberList
Parser.parseMemberListTail = parseMemberListTail
Parser.parseMember = parseMember
Parser.parseMemberInitialValueOptional = parseMemberInitialValueOptional
Parser.parseMemberInitialValue = parseMemberInitialValue