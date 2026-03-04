from __future__ import annotations
from typing import Any, List, Optional, Union
from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# GLOBAL DECLS
def parse_global_dec_opt(self: Parser) -> List[Any]:
    prod = self.choose_prod("<global_dec_opt>")
    if prod == [EPSILON]:
        return []
    return self.parse_global_dec_list()

def parse_global_dec_list(self: Parser) -> List[Any]:
    self.choose_prod("<global_dec_list>")
    items: List[Any] = []
    items.append(self.parse_global_dec_item())
    items.extend(self.parse_global_dec_list_tail())
    return items

def parse_global_dec_list_tail(self: Parser) -> List[Any]:
    prod = self.choose_prod("<global_dec_list_tail>")
    if prod == [EPSILON]:
        return []
    items: List[Any] = []
    items.append(self.parse_global_dec_item())
    items.extend(self.parse_global_dec_list_tail())
    return items

def parse_global_dec_item(self: Parser) -> Any:
    self.choose_prod("<global_dec_item>")
    la = self.la(0)

    # sacred const decl
    if la == TK_SACRED:
        sacred_tok = self.expect(TK_SACRED)
        type_name = self.parse_data_type()  # <data_type>
        items = self.parse_sacred_init_list()
        self.expect(TK_SYM_SEMICOL)
        return SacredDecl(pos=_tok_pos(sacred_tok), type_name=type_name, items=items)

    # normal var decl (starts with data_type)
    if la in (TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY):
        type_name = self.parse_data_type()
        items = self.parse_var_decl_group()
        self.expect(TK_SYM_SEMICOL)
        return VarDecl(pos=_tok_pos(self.peek(-1)), type_name=type_name, items=items)

    # order decl
    if la == TK_OTHERS_ORDER:
        tok = self.expect(TK_OTHERS_ORDER)
        name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        self.expect(TK_SYM_OPBRACE)
        members = self.parse_member_list_opt()
        self.expect(TK_SYM_CLSBRACE)
        self.expect(TK_SYM_SEMICOL)
        return OrderDecl(pos=_tok_pos(tok), name=name, members=members)

    # ordain decl
    if la == TK_OTHERS_ORDAIN:
        tok = self.expect(TK_OTHERS_ORDAIN)
        name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        items = self.parse_ordain_dec_list()
        self.expect(TK_SYM_SEMICOL)
        return OrdainDecl(pos=_tok_pos(tok), name=name, items=items)

    tok = self.peek(0) or self.peek(-1)
    raise ParserError(tok, expected=list(PREDICT["<global_dec_item>"].keys()), details="Unhandled <global_dec_item> alternative")

# ORDER MEMBERS
def parse_member_list_opt(self: Parser) -> List[OrderMember]:
    prod = self.choose_prod("<member_list_opt>")
    if prod == [EPSILON]:
        return []
    return self.parse_member_list()

def parse_member_list(self: Parser) -> List[OrderMember]:
    self.choose_prod("<member_list>")
    members = [self.parse_member()]
    members.extend(self.parse_member_list_tail())
    return members

def parse_member_list_tail(self: Parser) -> List[OrderMember]:
    prod = self.choose_prod("<member_list_tail>")
    if prod == [EPSILON]:
        return []
    members = [self.parse_member()]
    members.extend(self.parse_member_list_tail())
    return members

def parse_member(self: Parser) -> OrderMember:
    self.choose_prod("<member>")
    type_name = self.parse_data_type_id()
    name_tok = self.expect(TK_IDENTIFIER)
    dims = self.parse_array_dims_tail()
    init = self.parse_member_init_opt()
    self.expect(TK_SYM_SEMICOL)
    return OrderMember(pos=_tok_pos(name_tok), type_name=type_name, name=_tok_lexeme(name_tok), dims=dims, init=init)

def parse_member_init_opt(self: Parser) -> Optional[Expr]:
    prod = self.choose_prod("<member_init_opt>")
    if prod == [EPSILON]:
        return None
    self.expect(TK_OP_ASSIGN)
    return self.parse_member_init_val()

def parse_member_init_val(self: Parser) -> Expr:
    self.choose_prod("<member_init_val>")
    if self.la(0) == TK_SYM_OPBRACE:
        return self.parse_array_init()
    return self.parse_expr()

# SACRED INIT LIST
def parse_sacred_init_list(self: Parser) -> List[SacredItem]:
    self.choose_prod("<sacred_init_list>")
    items = [self.parse_sacred_init()]
    items.extend(self.parse_sacred_init_tail())
    return items

def parse_sacred_init_tail(self: Parser) -> List[SacredItem]:
    prod = self.choose_prod("<sacred_init_tail>")
    if prod == [EPSILON]:
        return []
    self.expect(TK_SYM_COMMA)
    items = [self.parse_sacred_init()]
    items.extend(self.parse_sacred_init_tail())
    return items

def parse_sacred_init(self: Parser) -> SacredItem:
    self.choose_prod("<sacred_init>")
    name_tok = self.expect(TK_IDENTIFIER)
    value = self.parse_sacred_assign_opt()
    return SacredItem(pos=_tok_pos(name_tok), name=_tok_lexeme(name_tok), value=value)

def parse_sacred_assign_opt(self: Parser) -> Optional[Expr]:
    prod = self.choose_prod("<sacred_assign_opt>")
    if prod == [EPSILON]:
        return None
    self.expect(TK_OP_ASSIGN)
    return self.parse_const_expr()

# VAR DECL GROUP
def parse_var_decl_group(self: Parser) -> List[VarItem]:
    self.choose_prod("<var_decl_group>")
    items = [self.parse_var_decl_item()]
    items.extend(self.parse_var_decl_tail())
    return items

def parse_var_decl_tail(self: Parser) -> List[VarItem]:
    prod = self.choose_prod("<var_decl_tail>")
    if prod == [EPSILON]:
        return []
    self.expect(TK_SYM_COMMA)
    items = [self.parse_var_decl_item()]
    items.extend(self.parse_var_decl_tail())
    return items

def parse_var_decl_item(self: Parser) -> VarItem:
    self.choose_prod("<var_decl_item>")
    name_tok = self.expect(TK_IDENTIFIER)
    dims = self.parse_array_dims_tail()
    init = self.parse_var_decl_item_tail()
    return VarItem(pos=_tok_pos(name_tok), name=_tok_lexeme(name_tok), dims=dims, init=init)

def parse_var_decl_item_tail(self: Parser) -> Optional[Expr]:
    prod = self.choose_prod("<var_decl_item_tail>")
    if prod == [EPSILON]:
        return None
    self.expect(TK_OP_ASSIGN)
    return self.parse_var_after_eq()

def parse_var_after_eq(self: Parser) -> Expr:
    self.choose_prod("<var_after_eq>")
    if self.la(0) == TK_SYM_OPBRACE:
        return self.parse_array_init()
    return self.parse_expr()


# ARRAYS
def parse_array_dims_tail(self: Parser) -> List[Expr]:
    prod = self.choose_prod("<array_dims_tail>")
    if prod == [EPSILON]:
        return []
    self.expect(TK_SYM_OPBRACK)
    idx = self.parse_expr()
    self.expect(TK_SYM_CLSBRACK)
    rest = self.parse_array_dims_tail()
    return [idx] + rest

def parse_array_init(self: Parser) -> ArrayInit:
    self.choose_prod("<array_init>")
    lbrace = self.expect(TK_SYM_OPBRACE)
    items = self.parse_array_vals_opt()
    self.expect(TK_SYM_CLSBRACE)
    return ArrayInit(pos=_tok_pos(lbrace), items=items)

def parse_array_vals_opt(self: Parser) -> List[Expr]:
    prod = self.choose_prod("<array_vals_opt>")
    if prod == [EPSILON]:
        return []
    return self.parse_array_vals()

def parse_array_vals(self: Parser) -> List[Expr]:
    self.choose_prod("<array_vals>")
    items = [self.parse_array_val()]
    items.extend(self.parse_array_vals_tail())
    return items

def parse_array_vals_tail(self: Parser) -> List[Expr]:
    prod = self.choose_prod("<array_vals_tail>")
    if prod == [EPSILON]:
        return []
    self.expect(TK_SYM_COMMA)
    items = [self.parse_array_val()]
    items.extend(self.parse_array_vals_tail())
    return items

def parse_array_val(self: Parser) -> Expr:
    self.choose_prod("<array_val>")
    if self.la(0) == TK_SYM_OPBRACE:
        lb = self.expect(TK_SYM_OPBRACE)
        items = self.parse_array_vals_opt()
        self.expect(TK_SYM_CLSBRACE)
        return ArrayInit(pos=_tok_pos(lb), items=items)
    return self.parse_expr()

# DATA TYPES
def parse_data_type(self: Parser) -> str:
    self.choose_prod("<data_type>")
    t = self.advance()
    return _tok_lexeme(t) if _tok_lexeme(t) else str(getattr(t, "type", ""))

def parse_data_type_id(self: Parser) -> str:
    self.choose_prod("<data_type_id>")
    if self.la(0) == TK_IDENTIFIER:
        return _tok_lexeme(self.expect(TK_IDENTIFIER))
    return self.parse_data_type()

# Ordain List
def parse_ordain_dec_list(self: Parser) -> List[OrdainItem]:
    self.choose_prod("<ordain_dec_list>")
    items = [self.parse_ordain_dec()]
    items.extend(self.parse_ordain_dec_tail())
    return items

def parse_ordain_dec_tail(self: Parser) -> List[OrdainItem]:
    prod = self.choose_prod("<ordain_dec_tail>")
    if prod == [EPSILON]:
        return []
    self.expect(TK_SYM_COMMA)
    items = [self.parse_ordain_dec()]
    items.extend(self.parse_ordain_dec_tail())
    return items

def parse_ordain_dec(self: Parser) -> OrdainItem:
    self.choose_prod("<ordain_dec>")
    name_tok = self.expect(TK_IDENTIFIER)
    dims = self.parse_array_dims_tail()
    init = self.parse_ordain_init_opt()
    return OrdainItem(pos=_tok_pos(name_tok), name=_tok_lexeme(name_tok), dims=dims, init=init)

def parse_ordain_init_opt(self: Parser) -> Optional[Expr]:
    prod = self.choose_prod("<ordain_init_opt>")
    if prod == [EPSILON]:
        return None
    self.expect(TK_OP_ASSIGN)
    return self.parse_expr()

# CONST EXPR
def parse_const_expr(self: Parser) -> Expr:
    self.choose_prod("<const_expr>")
    return self.parse_expr()

Parser.parse_global_dec_opt = parse_global_dec_opt
Parser.parse_global_dec_list = parse_global_dec_list
Parser.parse_global_dec_list_tail = parse_global_dec_list_tail
Parser.parse_global_dec_item = parse_global_dec_item
Parser.parse_member_list_opt = parse_member_list_opt
Parser.parse_member_list = parse_member_list
Parser.parse_member_list_tail = parse_member_list_tail
Parser.parse_member = parse_member
Parser.parse_member_init_opt = parse_member_init_opt
Parser.parse_member_init_val = parse_member_init_val
Parser.parse_sacred_init_list = parse_sacred_init_list
Parser.parse_sacred_init_tail = parse_sacred_init_tail
Parser.parse_sacred_init = parse_sacred_init
Parser.parse_sacred_assign_opt = parse_sacred_assign_opt
Parser.parse_var_decl_group = parse_var_decl_group
Parser.parse_var_decl_tail = parse_var_decl_tail
Parser.parse_var_decl_item = parse_var_decl_item
Parser.parse_var_decl_item_tail = parse_var_decl_item_tail
Parser.parse_var_after_eq = parse_var_after_eq
Parser.parse_array_dims_tail = parse_array_dims_tail
Parser.parse_array_init = parse_array_init
Parser.parse_array_vals_opt = parse_array_vals_opt
Parser.parse_array_vals = parse_array_vals
Parser.parse_array_vals_tail = parse_array_vals_tail
Parser.parse_array_val = parse_array_val
Parser.parse_data_type = parse_data_type
Parser.parse_data_type_id = parse_data_type_id
Parser.parse_ordain_dec_list = parse_ordain_dec_list
Parser.parse_ordain_dec_tail = parse_ordain_dec_tail
Parser.parse_ordain_dec = parse_ordain_dec
Parser.parse_ordain_init_opt = parse_ordain_init_opt
Parser.parse_const_expr = parse_const_expr