from __future__ import annotations
from typing import Any, List, Optional, Tuple

from backend.tokens import *
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# RITES / FUNCTIONS
def parse_rite_seq(self: Parser) -> Tuple[Optional[RiteDecl], List[RiteDecl]]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<rite_seq>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<rite_seq>"].keys()),
        )

    self.expect(TK_CF_RITE)
    return_type_name = self.parse_return_type_any()

    lookahead_type = self.current_type(0)
    if lookahead_type not in PREDICT["<rite_after_type>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<rite_after_type>"].keys()),
        )

    entry_rite: Optional[RiteDecl] = None
    rite_declarations: List[RiteDecl] = []

    if lookahead_type == TK_OTHERS_GENESIS:
        genesis_token = self.expect(TK_OTHERS_GENESIS)
        self.expect(TK_SYM_OPPAREN)
        self.expect(TK_SYM_CLSPAREN)
        self.expect(TK_SYM_OPBRACE)

        local_declarations = self.parse_main_local_dec_opt()
        statement_list = self.parse_statement_list()
        dismiss_stmt = self.parse_dismiss_opt()

        self.expect(TK_SYM_CLSBRACE)

        entry_rite = RiteDecl(
            pos=_tok_pos(genesis_token),
            name="genesis",
            return_type=return_type_name,
            params=[],
            local_decls=local_declarations,
            body=statement_list,
            dismiss=dismiss_stmt,
        )
        return entry_rite, rite_declarations

    if lookahead_type == TK_IDENTIFIER:
        identifier_token = self.expect(TK_IDENTIFIER)
        rite_name = _tok_lexeme(identifier_token)

        self.expect(TK_SYM_OPPAREN)
        parameter_list = self.parse_param_list_opt()
        self.expect(TK_SYM_CLSPAREN)

        self.expect(TK_SYM_OPBRACE)
        local_declarations = self.parse_func_local_dec_opt()
        statement_list = self.parse_statement_list()
        dismiss_stmt = self.parse_dismiss_opt()
        self.expect(TK_SYM_CLSBRACE)

        rite_decl = RiteDecl(
            pos=_tok_pos(identifier_token),
            name=rite_name,
            return_type=return_type_name,
            params=parameter_list,
            local_decls=local_declarations,
            body=statement_list,
            dismiss=dismiss_stmt,
        )

        rite_declarations.append(rite_decl)

        if self.current_type(0) == TK_CF_RITE:
            next_entry_rite, next_rite_declarations = self.parse_rite_seq()
            if next_entry_rite is not None and entry_rite is None:
                entry_rite = next_entry_rite
            rite_declarations.extend(next_rite_declarations)

        return entry_rite, rite_declarations

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=list(PREDICT["<rite_after_type>"].keys()),
    )

def parse_return_type_any(self: Parser) -> str:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<return_type_any>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<return_type_any>"].keys()),
        )

    if lookahead_type == TK_DTYPE_HOLLOW:
        self.expect(TK_DTYPE_HOLLOW)
        return "hollow"

    return self.parse_data_type_id()

# PARAMS
def parse_param_list_opt(self: Parser) -> List[Param]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_list_opt>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    return self.parse_param_list()

def parse_param_list(self: Parser) -> List[Param]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_list>"].keys()),
        )

    parameter_list = [self.parse_param()]
    parameter_list.extend(self.parse_param_list_tail())
    return parameter_list

def parse_param_list_tail(self: Parser) -> List[Param]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_list_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_parameters = [self.parse_param()]
    remaining_parameters.extend(self.parse_param_list_tail())
    return remaining_parameters

def parse_param(self: Parser) -> Param:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param>"].keys()),
        )

    type_name = self.parse_data_type_id()
    identifier_token = self.expect(TK_IDENTIFIER)
    dims = self.parse_param_array_tail()

    return Param(
        pos=_tok_pos(identifier_token),
        type_name=type_name,
        name=_tok_lexeme(identifier_token),
        dims=dims
    )

def parse_param_array_tail(self: Parser) -> List[Optional[Expr]]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_array_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_array_tail>"].keys()),
        )

    dims: List[Optional[Expr]] = []

    while self.current_type(0) == TK_SYM_OPBRACK:
        self.expect(TK_SYM_OPBRACK)
        dim_expr = self.parse_param_dim_expr_opt()
        self.expect(TK_SYM_CLSBRACK)
        dims.append(dim_expr)

    return dims

def parse_param_dim_expr_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<param_dim_expr_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<param_dim_expr_opt>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSBRACK:
        return None

    return self.parse_expr()

# LOCAL DECLS (func / main)
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

Parser.parse_rite_seq = parse_rite_seq
Parser.parse_return_type_any = parse_return_type_any

Parser.parse_param_list_opt = parse_param_list_opt
Parser.parse_param_list = parse_param_list
Parser.parse_param_list_tail = parse_param_list_tail
Parser.parse_param = parse_param
Parser.parse_param_array_tail = parse_param_array_tail
Parser.parse_param_dim_expr_opt = parse_param_dim_expr_opt

Parser.parse_func_local_dec_opt = parse_func_local_dec_opt
Parser.parse_func_local_dec = parse_func_local_dec
Parser.parse_func_local_dec_tail = parse_func_local_dec_tail
Parser.parse_func_local_item = parse_func_local_item

Parser.parse_main_local_dec_opt = parse_main_local_dec_opt
Parser.parse_main_local_dec = parse_main_local_dec
Parser.parse_main_local_dec_tail = parse_main_local_dec_tail
Parser.parse_main_dec_item = parse_main_dec_item