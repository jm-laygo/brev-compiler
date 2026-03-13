from __future__ import annotations
from typing import Any, List

from backend.parser.predict_set import PREDICT, EPSILON
from backend.errors import ParserError
from backend.parser.parser import Parser


def parse_func_local_dec_opt(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<func_local_dec_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<func_local_dec_opt>"].keys()),
        )

    if PREDICT["<func_local_dec_opt>"][lookahead_type] == [EPSILON]:
        return []

    return self.parse_func_local_dec()


def parse_func_local_dec(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<func_local_dec>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<func_local_dec>"].keys()),
        )

    local_declarations = [self.parse_func_local_item()]
    local_declarations.extend(self.parse_func_local_dec_tail())
    return local_declarations


def parse_func_local_dec_tail(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<func_local_dec_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<func_local_dec_tail>"].keys()),
        )

    if PREDICT["<func_local_dec_tail>"][lookahead_type] == [EPSILON]:
        return []

    remaining_local_declarations = [self.parse_func_local_item()]
    remaining_local_declarations.extend(self.parse_func_local_dec_tail())
    return remaining_local_declarations


def parse_func_local_item(self: Parser) -> Any:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<func_local_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<func_local_item>"].keys()),
        )

    return self.parse_global_dec_item()


def parse_main_local_dec_opt(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<main_local_dec_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<main_local_dec_opt>"].keys()),
        )

    if PREDICT["<main_local_dec_opt>"][lookahead_type] == [EPSILON]:
        return []

    return self.parse_main_local_dec()


def parse_main_local_dec(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<main_local_dec>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<main_local_dec>"].keys()),
        )

    local_declarations = [self.parse_main_dec_item()]
    local_declarations.extend(self.parse_main_local_dec_tail())
    return local_declarations


def parse_main_local_dec_tail(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<main_local_dec_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<main_local_dec_tail>"].keys()),
        )

    if PREDICT["<main_local_dec_tail>"][lookahead_type] == [EPSILON]:
        return []

    remaining_local_declarations = [self.parse_main_dec_item()]
    remaining_local_declarations.extend(self.parse_main_local_dec_tail())
    return remaining_local_declarations


def parse_main_dec_item(self: Parser) -> Any:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<main_dec_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<main_dec_item>"].keys()),
        )

    return self.parse_func_local_item()


Parser.parse_func_local_dec_opt = parse_func_local_dec_opt
Parser.parse_func_local_dec = parse_func_local_dec
Parser.parse_func_local_dec_tail = parse_func_local_dec_tail
Parser.parse_func_local_item = parse_func_local_item
Parser.parse_main_local_dec_opt = parse_main_local_dec_opt
Parser.parse_main_local_dec = parse_main_local_dec
Parser.parse_main_local_dec_tail = parse_main_local_dec_tail
Parser.parse_main_dec_item = parse_main_dec_item
