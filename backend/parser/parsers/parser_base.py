from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError

class ParserBase:
    DECL_START = (
        TK_SACRED,
        TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY,
        TK_OTHERS_ORDER, TK_OTHERS_ORDAIN,
    )

    STMT_START = (
        TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY,
        TK_OTHERS_ORDER, TK_OTHERS_ORDAIN,
        TK_IO_RECEIVE, TK_IO_PROCLAIM,
        TK_CF_DECREE, TK_CF_DISCERN,
        TK_CF_PROCESSION, TK_CF_ENDURE, TK_CF_RITUAL,
        TK_CF_DISMISS, TK_CF_PROCEED, TK_CF_ABSOLVE, TK_CF_FALL,
        TK_IDENTIFIER, TK_OP_INC, TK_OP_DEC, TK_SYM_OPPAREN,
    )

    ASSIGN_OPS = (
        TK_OP_ASSIGN,
        TK_OP_PLUS_EQ, TK_OP_MINUS_EQ, TK_OP_MUL_EQ, TK_OP_DIV_EQ, TK_OP_MOD_EQ, TK_OP_POW_EQ,
    )

    def __init__(self, tokens):
        self.tokens = list(tokens)
        if not self.tokens or self.tokens[-1].type != TK_EOF:
            last = self.tokens[-1] if self.tokens else None
            self.tokens.append(Token(TK_EOF, None, getattr(last, "pos", None)))
        self.i = 0

    def peek(self, k: int = 0):
        j = self.i + k
        if j < len(self.tokens):
            return self.tokens[j]
        return self.tokens[-1]

    def at(self, token_type: str) -> bool:
        return self.peek().type == token_type

    def match(self, token_type: str):
        tok = self.peek()
        if tok.type != token_type:
            raise ParserError(tok, expected=[token_type], details=None)
        self.i += 1
        return tok

    def accept(self, token_type: str):
        if self.at(token_type):
            return self.match(token_type)
        return None

    def expect_one_of(self, expected_types):
        tok = self.peek()
        raise ParserError(tok, expected=list(expected_types), details=None)