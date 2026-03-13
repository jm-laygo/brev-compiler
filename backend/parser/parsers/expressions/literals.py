from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_literal_expr(self: Parser) -> LiteralExpr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in (
        TK_LIT_INT,
        TK_LIT_DECIMAL,
        TK_LIT_CHAR,
        TK_LIT_STRING,
        TK_LIT_BOOL
    ):
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=[TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL]
        )

    literal_token = self.advance()
    literal_lexeme = _tok_lexeme(literal_token)

    if lookahead_type == TK_LIT_INT:
        try:
            literal_value = int(literal_lexeme)
        except Exception:
            literal_value = literal_lexeme
        return LiteralExpr(pos=_tok_pos(literal_token), value=literal_value, literal_type="int")

    if lookahead_type == TK_LIT_DECIMAL:
        try:
            literal_value = float(literal_lexeme)
        except Exception:
            literal_value = literal_lexeme
        return LiteralExpr(pos=_tok_pos(literal_token), value=literal_value, literal_type="decimal")

    if lookahead_type == TK_LIT_CHAR:
        char_value = literal_lexeme

        if not isinstance(char_value, str):
            self.error_expected([TK_LIT_CHAR], "Invalid sigil literal.")

        if len(char_value) == 3 and char_value[0] == "'" and char_value[2] == "'":
            char_value = char_value[1]
        else:
            self.error_expected([TK_LIT_CHAR], "Invalid sigil literal format.")

        return LiteralExpr(
            pos=_tok_pos(literal_token),
            value=char_value,
            literal_type="char",
        )

    if lookahead_type == TK_LIT_STRING:
        string_value = literal_lexeme

        if isinstance(string_value, str) and len(string_value) >= 2 and string_value[0] == '"' and string_value[-1] == '"':
            string_value = string_value[1:-1]

        return LiteralExpr(
            pos=_tok_pos(literal_token),
            value=string_value,
            literal_type="string",
        )

    if lookahead_type == TK_LIT_BOOL:
        normalized_bool_lexeme = (
            literal_lexeme.lower() if isinstance(literal_lexeme, str) else literal_lexeme
        )
        if normalized_bool_lexeme in ("true", "false", "holy", "unholy"):
            return LiteralExpr(
                pos=_tok_pos(literal_token),
                value=(normalized_bool_lexeme == "true" or normalized_bool_lexeme == "holy"),
                literal_type="bool"
            )
        return LiteralExpr(pos=_tok_pos(literal_token), value=literal_lexeme, literal_type="bool")

    raise ParserError(
        literal_token,
        expected=[TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL]
    )


Parser.parse_literal_expr = parse_literal_expr
