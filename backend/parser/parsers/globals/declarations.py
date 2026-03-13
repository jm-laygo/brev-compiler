from __future__ import annotations
from typing import Any, List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_global_dec_opt(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<global_dec_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<global_dec_opt>"].keys()),
        )

    if PREDICT["<global_dec_opt>"][lookahead_type] == [EPSILON]:
        return []

    return self.parse_global_dec_list()


def parse_global_dec_list(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<global_dec_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<global_dec_list>"].keys()),
        )

    global_declarations: List[Any] = []
    global_declarations.append(self.parse_global_dec_item())
    global_declarations.extend(self.parse_global_dec_list_tail())
    return global_declarations


def parse_global_dec_list_tail(self: Parser) -> List[Any]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<global_dec_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<global_dec_list_tail>"].keys()),
        )

    if PREDICT["<global_dec_list_tail>"][lookahead_type] == [EPSILON]:
        return []

    remaining_global_declarations: List[Any] = []
    remaining_global_declarations.append(self.parse_global_dec_item())
    remaining_global_declarations.extend(self.parse_global_dec_list_tail())
    return remaining_global_declarations


def parse_global_dec_item(self: Parser) -> Any:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<global_dec_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<global_dec_item>"].keys()),
        )

    if lookahead_type == TK_SACRED:
        sacred_token = self.expect(TK_SACRED)
        type_name = self.parse_data_type()
        declaration_items = self.parse_sacred_init_list()
        self.expect(TK_SYM_SEMICOL)
        return SacredDecl(
            pos=_tok_pos(sacred_token),
            type_name=type_name,
            items=declaration_items
        )

    if lookahead_type in (
        TK_DTYPE_TALLY,
        TK_DTYPE_DIVINE,
        TK_DTYPE_SIGIL,
        TK_DTYPE_SCRIPTURE,
        TK_DTYPE_VERITY,
    ):
        declaration_start_token = self.peek(0)
        type_name = self.parse_data_type()
        declaration_items = self.parse_var_decl_group()
        self.expect(TK_SYM_SEMICOL)
        return VarDecl(
            pos=_tok_pos(declaration_start_token),
            type_name=type_name,
            items=declaration_items
        )

    if lookahead_type == TK_OTHERS_ORDER:
        order_token = self.expect(TK_OTHERS_ORDER)
        identifier_name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        self.expect(TK_SYM_OPBRACE)
        member_list = self.parse_member_list_opt()
        self.expect(TK_SYM_CLSBRACE)
        self.expect(TK_SYM_SEMICOL)
        return OrderDecl(
            pos=_tok_pos(order_token),
            name=identifier_name,
            members=member_list
        )

    if lookahead_type == TK_OTHERS_ORDAIN:
        ordain_token = self.expect(TK_OTHERS_ORDAIN)
        identifier_name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        declaration_items = self.parse_ordain_dec_list()
        self.expect(TK_SYM_SEMICOL)
        return OrdainDecl(
            pos=_tok_pos(ordain_token),
            name=identifier_name,
            items=declaration_items
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=list(PREDICT["<global_dec_item>"].keys()),
    )


Parser.parse_global_dec_opt = parse_global_dec_opt
Parser.parse_global_dec_list = parse_global_dec_list
Parser.parse_global_dec_list_tail = parse_global_dec_list_tail
Parser.parse_global_dec_item = parse_global_dec_item
