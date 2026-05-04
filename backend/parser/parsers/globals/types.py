from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue


def parseDataType(self: Parser) -> str:
    currentTokenType = self.currentType(0)

    # check data type
    if currentTokenType not in PREDICT["<data_type>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<data_type>"].keys())
        )

    if currentTokenType == TK_DTYPE_TALLY:
        self.expect(TK_DTYPE_TALLY)
        return "tally"

    if currentTokenType == TK_DTYPE_DIVINE:
        self.expect(TK_DTYPE_DIVINE)
        return "divine"

    if currentTokenType == TK_DTYPE_SIGIL:
        self.expect(TK_DTYPE_SIGIL)
        return "sigil"

    if currentTokenType == TK_DTYPE_SCRIPTURE:
        self.expect(TK_DTYPE_SCRIPTURE)
        return "scripture"

    if currentTokenType == TK_DTYPE_VERITY:
        self.expect(TK_DTYPE_VERITY)
        return "verity"

    raise ParserError(
        self.peek(0) or self.peek(-1),
        [
            TK_DTYPE_TALLY,
            TK_DTYPE_DIVINE,
            TK_DTYPE_SIGIL,
            TK_DTYPE_SCRIPTURE,
            TK_DTYPE_VERITY
        ]
    )

def parseDataTypeIdentifier(self: Parser) -> str:
    currentTokenType = self.currentType(0)

    # check data type or identifier
    if currentTokenType not in PREDICT["<data_type_id>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<data_type_id>"].keys())
        )

    # user defined type
    if currentTokenType == TK_IDENTIFIER:
        return getTokenValue(self.expect(TK_IDENTIFIER))

    return self.parseDataType()

def parseConstantExpression(self: Parser) -> Expression:
    currentTokenType = self.currentType(0)

    # check constant expression
    if currentTokenType not in PREDICT["<const_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<const_expr>"].keys())
        )

    return self.parseExpression()

Parser.parseDataType = parseDataType
Parser.parseDataTypeIdentifier = parseDataTypeIdentifier
Parser.parseConstantExpression = parseConstantExpression