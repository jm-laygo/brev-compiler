from __future__ import annotations
from typing import Any, List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *

def _tok_lexeme(token):
    return getattr(token, "value", None)

def _tok_pos(token):
    return getattr(token, "pos", None)

class Parser:
    def __init__(self, tokens: List[Any]):
        self.tokens = tokens
        self.current_index = 0

    def at_end(self) -> bool:
        return self.current_index >= len(self.tokens)

    def peek(self, offset: int = 0) -> Any:
        target_index = self.current_index + offset
        if target_index < 0 or target_index >= len(self.tokens):
            return None
        return self.tokens[target_index]

    def current_type(self, offset: int = 0) -> Any:
        current_token = self.peek(offset)
        return getattr(current_token, "type", None) if current_token is not None else None

    def advance(self) -> Any:
        current_token = self.peek(0)
        self.current_index += 1
        return current_token

    def expect(self, expected_token_type):
        current_token = self.peek(0)

        if current_token is None:
            raise ParserError(
                self.peek(-1),
                expected=expected_token_type,
                details="Unexpected end of input"
            )

        if current_token.type != expected_token_type:
            raise ParserError(current_token, expected=expected_token_type)

        return self.advance()

    def accept(self, expected_token_type: Any):
        if self.current_type(0) == expected_token_type:
            return self.advance()
        return None

    def choose_prod(self, nonterminal: str):
        current_token_type = self.current_type(0)
        predict_table = PREDICT.get(nonterminal)

        if predict_table is None:
            current_token = self.peek(0) or self.peek(-1)
            raise ParserError(
                current_token,
                expected=[],
                details=f"Missing PREDICT entry for {nonterminal}"
            )

        production = predict_table.get(current_token_type)
        if production is None:
            current_token = self.peek(0) or self.peek(-1)
            expected_tokens = list(predict_table.keys())
            raise ParserError(current_token, expected=expected_tokens)

        return production

    def error_expected(self, expected_tokens, details="Invalid syntax"):
        current_token = self.peek(0) or self.peek(-1)
        raise ParserError(current_token, expected=expected_tokens, details=details)

    # Entry
    def parse(self) -> Program:
        return self.parse_program()

    def parse_program(self) -> Program:
        current_token_type = self.current_type(0)

        if current_token_type != TK_EOF and current_token_type not in PREDICT["<program>"]:
            raise ParserError(
                self.peek(0) or self.peek(-1),
                expected=list(PREDICT["<program>"].keys())
            )

        program_node = Program(pos=_tok_pos(self.peek(0)))
        program_node.globals = []
        program_node.functions = []
        program_node.entry = None

        while self.current_type(0) != TK_EOF:
            current_token_type = self.current_type(0)

            if current_token_type == TK_CF_RITE:
                entry_rite, function_nodes = self.parse_rite_seq()

                if entry_rite is not None:
                    if program_node.entry is not None:
                        raise ParserError(
                            self.peek(-1),
                            expected=[],
                            details="Multiple genesis() rites are not allowed"
                        )
                    program_node.entry = entry_rite

                program_node.functions.extend(function_nodes)
                continue

            if current_token_type in PREDICT["<global_dec_item>"]:
                program_node.globals.append(self.parse_global_dec_item())
                continue

            raise ParserError(
                self.peek(0),
                expected=list(PREDICT["<global_dec_item>"].keys()) + [TK_CF_RITE, TK_EOF]
            )

        if program_node.entry is None:
            raise ParserError(
                self.peek(0) or self.peek(-1),
                expected=[TK_OTHERS_GENESIS]
            )

        return program_node

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

    if parser.current_type(0) != TK_EOF:
        raise ParserError(
            parser.peek(0),
            expected=[TK_EOF],
            details="Trailing tokens"
        )

    return ast