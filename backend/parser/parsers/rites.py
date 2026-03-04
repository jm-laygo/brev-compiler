from __future__ import annotations
from typing import Any, List, Optional, Tuple
from backend.tokens import *
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# RITES / FUNCTIONS
def parse_rite_seq(self: Parser) -> Tuple[Optional[RiteDecl], List[RiteDecl]]:
    self.choose_prod("<rite_seq>")
    self.expect(TK_CF_RITE)

    ret_type = self.parse_return_type_any()

    la = self.la(0)
    self.choose_prod("<rite_after_type>")

    entry: Optional[RiteDecl] = None
    funcs: List[RiteDecl] = []

    if la == TK_OTHERS_GENESIS:
        genesis_tok = self.expect(TK_OTHERS_GENESIS)
        self.expect(TK_SYM_OPPAREN)
        self.expect(TK_SYM_CLSPAREN)
        self.expect(TK_SYM_OPBRACE)
        local_decls = self.parse_main_local_dec_opt()
        body = self.parse_statement_list()
        dismiss = self.parse_dismiss_opt()
        self.expect(TK_SYM_CLSBRACE)

        entry = RiteDecl(
            pos=_tok_pos(genesis_tok),
            name="genesis",
            return_type=ret_type,
            params=[],
            local_decls=local_decls,
            body=body,
            dismiss=dismiss,
        )
        return entry, funcs

    if la == TK_IDENTIFIER:
        name_tok = self.expect(TK_IDENTIFIER)
        fname = _tok_lexeme(name_tok)

        self.expect(TK_SYM_OPPAREN)
        params = self.parse_param_list_opt()
        self.expect(TK_SYM_CLSPAREN)

        self.expect(TK_SYM_OPBRACE)
        local_decls = self.parse_func_local_dec_opt()
        body = self.parse_statement_list()
        dismiss = self.parse_dismiss_opt()
        self.expect(TK_SYM_CLSBRACE)

        func = RiteDecl(
            pos=_tok_pos(name_tok),
            name=fname,
            return_type=ret_type,
            params=params,
            local_decls=local_decls,
            body=body,
            dismiss=dismiss,
        )

        funcs.append(func)

        if self.la(0) == TK_CF_RITE:
            nxt_entry, nxt_funcs = self.parse_rite_seq()
            if nxt_entry is not None and entry is None:
                entry = nxt_entry
            funcs.extend(nxt_funcs)

        return entry, funcs

    tok = self.peek(0) or self.peek(-1)
    raise ParserError(tok, expected=list(PREDICT["<rite_after_type>"].keys()), details="Invalid <rite_after_type>")

def parse_return_type_any(self: Parser) -> str:
    self.choose_prod("<return_type_any>")
    if self.la(0) == TK_DTYPE_HOLLOW:
        self.expect(TK_DTYPE_HOLLOW)
        return "hollow"
    return self.parse_data_type_id()


# PARAMS
def parse_param_list_opt(self: Parser) -> List[Param]:
    prod = self.choose_prod("<param_list_opt>")
    if prod == [EPSILON]:
        return []
    return self.parse_param_list()

def parse_param_list(self: Parser) -> List[Param]:
    self.choose_prod("<param_list>")
    params = [self.parse_param()]
    params.extend(self.parse_param_list_tail())
    return params

def parse_param_list_tail(self: Parser) -> List[Param]:
    prod = self.choose_prod("<param_list_tail>")
    if prod == [EPSILON]:
        return []
    self.expect(TK_SYM_COMMA)
    params = [self.parse_param()]
    params.extend(self.parse_param_list_tail())
    return params

def parse_param(self: Parser) -> Param:
    self.choose_prod("<param>")
    type_name = self.parse_data_type_id()
    name_tok = self.expect(TK_IDENTIFIER)
    array_dims = self.parse_param_array_tail()
    return Param(pos=_tok_pos(name_tok), type_name=type_name, name=_tok_lexeme(name_tok), array_dims=array_dims)

def parse_param_array_tail(self: Parser) -> int:
    prod = self.choose_prod("<param_array_tail>")
    if prod == [EPSILON]:
        return 0
    dims = 0
    while self.la(0) == TK_SYM_OPBRACK:
        self.expect(TK_SYM_OPBRACK)
        self.expect(TK_SYM_CLSBRACK)
        dims += 1
    return dims

# LOCAL DECLS (func / main)
def parse_func_local_dec_opt(self: Parser) -> List[Any]:
    prod = self.choose_prod("<func_local_dec_opt>")
    if prod == [EPSILON]:
        return []
    return self.parse_func_local_dec()

def parse_func_local_dec(self: Parser) -> List[Any]:
    self.choose_prod("<func_local_dec>")
    items = [self.parse_func_local_item()]
    items.extend(self.parse_func_local_dec_tail())
    return items

def parse_func_local_dec_tail(self: Parser) -> List[Any]:
    prod = self.choose_prod("<func_local_dec_tail>")
    if prod == [EPSILON]:
        return []
    items = [self.parse_func_local_item()]
    items.extend(self.parse_func_local_dec_tail())
    return items

def parse_func_local_item(self: Parser) -> Any:
    self.choose_prod("<func_local_item>")
    return self.parse_global_dec_item()

def parse_main_local_dec_opt(self: Parser) -> List[Any]:
    prod = self.choose_prod("<main_local_dec_opt>")
    if prod == [EPSILON]:
        return []
    return self.parse_main_local_dec()

def parse_main_local_dec(self: Parser) -> List[Any]:
    self.choose_prod("<main_local_dec>")
    items = [self.parse_main_dec_item()]
    items.extend(self.parse_main_local_dec_tail())
    return items

def parse_main_local_dec_tail(self: Parser) -> List[Any]:
    prod = self.choose_prod("<main_local_dec_tail>")
    if prod == [EPSILON]:
        return []
    items = [self.parse_main_dec_item()]
    items.extend(self.parse_main_local_dec_tail())
    return items

def parse_main_dec_item(self: Parser) -> Any:
    self.choose_prod("<main_dec_item>")
    return self.parse_func_local_item()

Parser.parse_rite_seq = parse_rite_seq
Parser.parse_return_type_any = parse_return_type_any
Parser.parse_param_list_opt = parse_param_list_opt
Parser.parse_param_list = parse_param_list
Parser.parse_param_list_tail = parse_param_list_tail
Parser.parse_param = parse_param
Parser.parse_param_array_tail = parse_param_array_tail
Parser.parse_func_local_dec_opt = parse_func_local_dec_opt
Parser.parse_func_local_dec = parse_func_local_dec
Parser.parse_func_local_dec_tail = parse_func_local_dec_tail
Parser.parse_func_local_item = parse_func_local_item
Parser.parse_main_local_dec_opt = parse_main_local_dec_opt
Parser.parse_main_local_dec = parse_main_local_dec
Parser.parse_main_local_dec_tail = parse_main_local_dec_tail
Parser.parse_main_dec_item = parse_main_dec_item