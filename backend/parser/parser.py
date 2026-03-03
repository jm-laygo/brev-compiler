from __future__ import annotations
from typing import Any, List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *

def _tok_lexeme(tok):
    return getattr(tok, "value", None)

def _tok_pos(tok):
    return getattr(tok, "pos", None)

class Parser:
    def __init__(self, tokens: List[Any]):
        self.tokens = tokens
        self.i = 0

    def at_end(self) -> bool:
        return self.i >= len(self.tokens)

    def peek(self, k: int = 0) -> Any:
        idx = self.i + k
        if idx < 0 or idx >= len(self.tokens):
            return None
        return self.tokens[idx]

    def la(self, k: int = 0) -> Any:
        t = self.peek(k)
        return getattr(t, "type", None) if t is not None else None

    def advance(self) -> Any:
        t = self.peek(0)
        self.i += 1
        return t

    def expect(self, token_type):
        tok = self.peek(0)
        if tok is None:
            raise ParserError(self.peek(-1), expected=token_type, details="Unexpected end of input")
        if tok.type != token_type:
            raise ParserError(tok, expected=token_type)
        return self.advance()

    def accept(self, token_type: Any):
        if self.la(0) == token_type:
            return self.advance()
        return None

    def choose_prod(self, nonterminal: str):
        la = self.la(0)
        table = PREDICT.get(nonterminal)
        if table is None:
            tok = self.peek(0) or self.peek(-1)
            raise ParserError(tok, expected=[], details="Invalid grammar table")
        prod = table.get(la)
        if prod is None:
            tok = self.peek(0) or self.peek(-1)
            expected = list(table.keys())
            raise ParserError(tok, expected=expected)
        return prod

    # Entry
    def parse(self) -> Program:
        return self.parse_program()

    def parse_program(self) -> Program:
        self.choose_prod("<program>")
        prog = Program(pos=_tok_pos(self.peek(0)))
        prog.globals = self.parse_global_dec_opt()
        entry, funcs = self.parse_rite_seq()
        prog.entry = entry
        prog.functions = funcs
        return prog

import backend.parser.parsers.globals as _globals
import backend.parser.parsers.rites as _rites
import backend.parser.parsers.statements as _statements
import backend.parser.parsers.lvalues as _lvalues
import backend.parser.parsers.expressions as _expressions

def parse_tokens_to_ast(tokens: List[Any]) -> Program:
    return Parser(tokens).parse()

def validate(tokens):
    parser = Parser(tokens)
    ast = parser.parse()
    if parser.la(0) != TK_EOF:
        raise ParserError(parser.peek(0), expected=[TK_EOF], details="Trailing tokens")
    return ast