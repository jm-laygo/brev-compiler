from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme


def parse_data_type(self: Parser) -> str:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<data_type>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<data_type>"].keys()),
        )

    if lookahead_type == TK_DTYPE_TALLY:
        self.expect(TK_DTYPE_TALLY)
        return "tally"

    if lookahead_type == TK_DTYPE_DIVINE:
        self.expect(TK_DTYPE_DIVINE)
        return "divine"

    if lookahead_type == TK_DTYPE_SIGIL:
        self.expect(TK_DTYPE_SIGIL)
        return "sigil"

    if lookahead_type == TK_DTYPE_SCRIPTURE:
        self.expect(TK_DTYPE_SCRIPTURE)
        return "scripture"

    if lookahead_type == TK_DTYPE_VERITY:
        self.expect(TK_DTYPE_VERITY)
        return "verity"

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=[
            TK_DTYPE_TALLY,
            TK_DTYPE_DIVINE,
            TK_DTYPE_SIGIL,
            TK_DTYPE_SCRIPTURE,
            TK_DTYPE_VERITY
        ],
    )


def parse_data_type_id(self: Parser) -> str:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<data_type_id>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<data_type_id>"].keys()),
        )

    if lookahead_type == TK_IDENTIFIER:
        return _tok_lexeme(self.expect(TK_IDENTIFIER))

    return self.parse_data_type()


def parse_const_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<const_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<const_expr>"].keys()),
        )

    return self.parse_expr()


Parser.parse_data_type = parse_data_type
Parser.parse_data_type_id = parse_data_type_id
Parser.parse_const_expr = parse_const_expr
