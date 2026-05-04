from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseLiteralExpression(self: Parser) -> LiteralExpression:
    currentTokenType = self.currentType(0)

    if currentTokenType not in (
        TK_LIT_INT,
        TK_LIT_DECIMAL,
        TK_LIT_CHAR,
        TK_LIT_STRING,
        TK_LIT_BOOL,
    ):
        raise ParserError(
            self.peek(0) or self.peek(-1),
            [
                TK_LIT_INT,
                TK_LIT_DECIMAL,
                TK_LIT_CHAR,
                TK_LIT_STRING,
                TK_LIT_BOOL,
            ]
        )

    literalToken = self.advance()
    literalValueText = getTokenValue(literalToken)

    if currentTokenType == TK_LIT_INT:
        try:
            literalValue = int(literalValueText)
        except Exception:
            literalValue = literalValueText

        return LiteralExpression(
            position=getTokenPosition(literalToken),
            value=literalValue,
            literalType="int"
        )

    if currentTokenType == TK_LIT_DECIMAL:
        try:
            literalValue = float(literalValueText)
        except Exception:
            literalValue = literalValueText

        return LiteralExpression(
            position=getTokenPosition(literalToken),
            value=literalValue,
            literalType="decimal"
        )

    if currentTokenType == TK_LIT_CHAR:
        characterValue = literalValueText

        if not isinstance(characterValue, str):
            raise ParserError(
                literalToken,
                [TK_LIT_CHAR],
                "Invalid sigil literal."
            )

        if (
            len(characterValue) == 3
            and characterValue[0] == "'"
            and characterValue[2] == "'"
        ):
            characterValue = characterValue[1]
        else:
            raise ParserError(
                literalToken,
                [TK_LIT_CHAR],
                "Invalid sigil literal format."
            )

        return LiteralExpression(
            position=getTokenPosition(literalToken),
            value=characterValue,
            literalType="char"
        )

    if currentTokenType == TK_LIT_STRING:
        stringValue = literalValueText

        if (
            isinstance(stringValue, str)
            and len(stringValue) >= 2
            and stringValue[0] == '"'
            and stringValue[-1] == '"'
        ):
            stringValue = stringValue[1:-1]

        return LiteralExpression(
            position=getTokenPosition(literalToken),
            value=stringValue,
            literalType="string"
        )

    if currentTokenType == TK_LIT_BOOL:
        if isinstance(literalValueText, str):
            normalizedBooleanText = literalValueText.lower()
        else:
            normalizedBooleanText = literalValueText

        if normalizedBooleanText in ("true", "holy"):
            literalValue = True
        elif normalizedBooleanText in ("false", "unholy"):
            literalValue = False
        else:
            literalValue = literalValueText

        return LiteralExpression(
            position=getTokenPosition(literalToken),
            value=literalValue,
            literalType="bool"
        )

    raise ParserError(
        literalToken,
        [
            TK_LIT_INT,
            TK_LIT_DECIMAL,
            TK_LIT_CHAR,
            TK_LIT_STRING,
            TK_LIT_BOOL,
        ]
    )


Parser.parseLiteralExpression = parseLiteralExpression