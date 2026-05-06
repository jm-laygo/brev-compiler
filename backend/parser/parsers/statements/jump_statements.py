from __future__ import annotations
from typing import Any, Optional

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenPosition


def parseJumpStatement(self: Parser) -> Statement:
    currentTokenType = self.currentType(0)

    # check jump stmt
    if currentTokenType not in PREDICT["<jump_stmt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<jump_stmt>"].keys())
        )

    # dismiss stmt
    if currentTokenType == TK_CF_DISMISS:
        dismissToken = self.expect(TK_CF_DISMISS)
        valueExpression = self.parseExpressionOptional()
        self.expect(TK_SYM_SEMICOL)

        return DismissStatement(
            position=getTokenPosition(dismissToken),
            value=valueExpression
        )

    # proceed stmt
    if currentTokenType == TK_CF_PROCEED:
        proceedToken = self.expect(TK_CF_PROCEED)
        self.expect(TK_SYM_SEMICOL)

        return ProceedStatement(
            position=getTokenPosition(proceedToken)
        )

    # fall stmt
    if currentTokenType == TK_CF_FALL:
        fallToken = self.expect(TK_CF_FALL)
        self.expect(TK_SYM_SEMICOL)

        return FallStatement(
            position=getTokenPosition(fallToken)
        )

    # absolve stmt
    absolveToken = self.expect(TK_CF_ABSOLVE)
    self.expect(TK_SYM_SEMICOL)

    return AbsolveStatement(
        position=getTokenPosition(absolveToken)
    )

def parseDismissOptional(self: Parser) -> Optional[DismissStatement]:
    currentTokenType = self.currentType(0)

    # check dismiss
    if currentTokenType not in PREDICT["<dismiss_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<dismiss_opt>"].keys())
        )

    # no dismiss
    if PREDICT["<dismiss_opt>"][currentTokenType] == [EPSILON]:
        return None

    dismissToken = self.expect(TK_CF_DISMISS)
    valueExpression = self.parseDismissTail(dismissToken)

    return DismissStatement(
        position=getTokenPosition(dismissToken),
        value=valueExpression
    )

def parseDismissTail(self: Parser, dismissToken: Any) -> Optional[Expression]:
    currentTokenType = self.currentType(0)

    # check dismiss tail
    if currentTokenType not in PREDICT["<dismiss_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<dismiss_tail>"].keys())
        )

    # dismiss without value
    if currentTokenType == TK_SYM_SEMICOL:
        self.expect(TK_SYM_SEMICOL)
        return None

    valueExpression = self.parseExpression()
    self.expect(TK_SYM_SEMICOL)

    return valueExpression

Parser.parseJumpStatement = parseJumpStatement
Parser.parseDismissOptional = parseDismissOptional
Parser.parseDismissTail = parseDismissTail