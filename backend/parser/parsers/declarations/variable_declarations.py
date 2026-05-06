from __future__ import annotations
from typing import List, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseVariableDeclarationGroup(self: Parser) -> List[VariableItem]:
    currentTokenType = self.currentType(0)

    # check variable group
    if currentTokenType not in PREDICT["<var_decl_group>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<var_decl_group>"].keys())
        )

    variableItems = [self.parseVariableDeclarationItem()]
    variableItems.extend(self.parseVariableDeclarationTail())

    return variableItems

def parseVariableDeclarationTail(self: Parser) -> List[VariableItem]:
    currentTokenType = self.currentType(0)

    # check next variable
    if currentTokenType not in PREDICT["<var_decl_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<var_decl_tail>"].keys())
        )

    # end of variable list
    if currentTokenType == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)

    remainingVariableItems = [self.parseVariableDeclarationItem()]
    remainingVariableItems.extend(self.parseVariableDeclarationTail())

    return remainingVariableItems

def parseVariableDeclarationItem(self: Parser) -> VariableItem:
    currentTokenType = self.currentType(0)

    # check variable item
    if currentTokenType not in PREDICT["<var_decl_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<var_decl_item>"].keys())
        )

    variableNameToken = self.expect(TK_IDENTIFIER)
    arrayDimensions = self.parseArrayDimensionsTail()
    initialValue = self.parseVariableDeclarationItemTail()

    return VariableItem(
        position=getTokenPosition(variableNameToken),
        name=getTokenValue(variableNameToken),
        dimensions=arrayDimensions,
        initialValue=initialValue
    )

def parseVariableDeclarationItemTail(self: Parser) -> Optional[Expression]:
    currentTokenType = self.currentType(0)

    # check variable init
    if currentTokenType not in PREDICT["<var_decl_item_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<var_decl_item_tail>"].keys())
        )

    # no initial value
    if currentTokenType in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)

    return self.parseVariableValueAfterAssignment()

def parseVariableValueAfterAssignment(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check assigned value
    if currentTokenType not in PREDICT["<var_after_eq>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<var_after_eq>"].keys())
        )

    # array init
    if currentTokenType == TK_SYM_OPBRACE:
        return self.parseArrayInitialization()

    return self.parseExpression()

Parser.parseVariableDeclarationGroup = parseVariableDeclarationGroup
Parser.parseVariableDeclarationTail = parseVariableDeclarationTail
Parser.parseVariableDeclarationItem = parseVariableDeclarationItem
Parser.parseVariableDeclarationItemTail = parseVariableDeclarationItemTail
Parser.parseVariableValueAfterAssignment = parseVariableValueAfterAssignment