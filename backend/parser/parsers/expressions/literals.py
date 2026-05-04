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
        characterText = literalValueText

        if not isinstance(characterText, str):
            raise ParserError(
                literalToken,
                [],
                "Invalid sigil literal."
            )

        if characterText == "''":
            raise ParserError(
                literalToken,
                [],
                "Empty sigil literal is invalid. A sigil must contain exactly one character or a valid escape sequence."
            )

        if len(characterText) < 2 or characterText[0] != "'" or characterText[-1] != "'":
            raise ParserError(
                literalToken,
                [],
                "Invalid sigil literal format. A sigil must be enclosed in single quotes."
            )

        innerText = characterText[1:-1]

        escapeMap = {
            r"\n": "\n",
            r"\t": "\t",
            r"\0": "\0",
            r"\'": "'",
            r"\"": '"',
            r"\\": "\\",
        }

        if innerText in escapeMap:
            characterValue = escapeMap[innerText]

        elif len(innerText) == 1:
            characterValue = innerText

        else:
            raise ParserError(
                literalToken,
                [],
                "Invalid sigil literal format. A sigil must contain exactly one character or a valid escape sequence."
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