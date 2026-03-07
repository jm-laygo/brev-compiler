from __future__ import annotations
from typing import Any, List, Optional, Union

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# GLOBAL DECLS
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

    # sacred const decl
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

    # normal var decl
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

    # order decl
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

    # ordain decl
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

# ORDER MEMBERS
def parse_member_list_opt(self: Parser) -> List[OrderMember]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_list_opt>"].keys()),
        )

    if PREDICT["<member_list_opt>"][lookahead_type] == [EPSILON]:
        return []

    return self.parse_member_list()

def parse_member_list(self: Parser) -> List[OrderMember]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_list>"].keys()),
        )

    member_list = [self.parse_member()]
    member_list.extend(self.parse_member_list_tail())
    return member_list

def parse_member_list_tail(self: Parser) -> List[OrderMember]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_list_tail>"].keys()),
        )

    if PREDICT["<member_list_tail>"][lookahead_type] == [EPSILON]:
        return []

    remaining_members = [self.parse_member()]
    remaining_members.extend(self.parse_member_list_tail())
    return remaining_members

def parse_member(self: Parser) -> OrderMember:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member>"].keys()),
        )

    type_name = self.parse_data_type_id()
    member_name_token = self.expect(TK_IDENTIFIER)
    array_dimensions = self.parse_array_dims_tail()
    initializer = self.parse_member_init_opt()
    self.expect(TK_SYM_SEMICOL)

    return OrderMember(
        pos=_tok_pos(member_name_token),
        type_name=type_name,
        name=_tok_lexeme(member_name_token),
        dims=array_dimensions,
        init=initializer
    )

def parse_member_init_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_init_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_init_opt>"].keys()),
        )

    if lookahead_type == TK_SYM_SEMICOL:
        return None

    self.expect(TK_OP_ASSIGN)
    return self.parse_member_init_val()

def parse_member_init_val(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<member_init_val>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<member_init_val>"].keys()),
        )

    if lookahead_type == TK_SYM_OPBRACE:
        return self.parse_array_init()

    return self.parse_expr()

# SACRED INIT LIST
def parse_sacred_init_list(self: Parser) -> List[SacredItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<sacred_init_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<sacred_init_list>"].keys()),
        )

    sacred_items = [self.parse_sacred_init()]
    sacred_items.extend(self.parse_sacred_init_tail())
    return sacred_items

def parse_sacred_init_tail(self: Parser) -> List[SacredItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<sacred_init_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<sacred_init_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_sacred_items = [self.parse_sacred_init()]
    remaining_sacred_items.extend(self.parse_sacred_init_tail())
    return remaining_sacred_items

def parse_sacred_init(self: Parser) -> SacredItem:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<sacred_init>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<sacred_init>"].keys()),
        )

    identifier_token = self.expect(TK_IDENTIFIER)
    initializer_value = self.parse_sacred_assign_opt()

    return SacredItem(
        pos=_tok_pos(identifier_token),
        name=_tok_lexeme(identifier_token),
        value=initializer_value
    )

def parse_sacred_assign_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<sacred_assign_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<sacred_assign_opt>"].keys()),
        )

    if lookahead_type in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)
    return self.parse_const_expr()

# VAR DECL GROUP
def parse_var_decl_group(self: Parser) -> List[VarItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_decl_group>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_decl_group>"].keys()),
        )

    variable_items = [self.parse_var_decl_item()]
    variable_items.extend(self.parse_var_decl_tail())
    return variable_items

def parse_var_decl_tail(self: Parser) -> List[VarItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_decl_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_decl_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_variable_items = [self.parse_var_decl_item()]
    remaining_variable_items.extend(self.parse_var_decl_tail())
    return remaining_variable_items

def parse_var_decl_item(self: Parser) -> VarItem:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_decl_item>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_decl_item>"].keys()),
        )

    variable_name_token = self.expect(TK_IDENTIFIER)
    array_dimensions = self.parse_array_dims_tail()
    initializer = self.parse_var_decl_item_tail()

    return VarItem(
        pos=_tok_pos(variable_name_token),
        name=_tok_lexeme(variable_name_token),
        dims=array_dimensions,
        init=initializer
    )

def parse_var_decl_item_tail(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_decl_item_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_decl_item_tail>"].keys()),
        )

    if lookahead_type in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)
    return self.parse_var_after_eq()

def parse_var_after_eq(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<var_after_eq>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<var_after_eq>"].keys()),
        )

    if lookahead_type == TK_SYM_OPBRACE:
        return self.parse_array_init()

    return self.parse_expr()

# ARRAYS
def parse_array_dims_tail(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_dims_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_dims_tail>"].keys()),
        )

    if PREDICT["<array_dims_tail>"][lookahead_type] == [EPSILON]:
        return []

    self.expect(TK_SYM_OPBRACK)
    dimension_expr = self.parse_expr()
    self.expect(TK_SYM_CLSBRACK)
    remaining_dimensions = self.parse_array_dims_tail()
    return [dimension_expr] + remaining_dimensions

def parse_array_init(self: Parser) -> ArrayInit:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_init>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_init>"].keys()),
        )

    opening_brace_token = self.expect(TK_SYM_OPBRACE)
    array_items = self.parse_array_vals_opt()
    self.expect(TK_SYM_CLSBRACE)

    return ArrayInit(
        pos=_tok_pos(opening_brace_token),
        items=array_items
    )

def parse_array_vals_opt(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_vals_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_vals_opt>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSBRACE:
        return []

    return self.parse_array_vals()

def parse_array_vals(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_vals>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_vals>"].keys()),
        )

    array_values = [self.parse_array_val()]
    array_values.extend(self.parse_array_vals_tail())
    return array_values

def parse_array_vals_tail(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_vals_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_vals_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_CLSBRACE:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_array_values = [self.parse_array_val()]
    remaining_array_values.extend(self.parse_array_vals_tail())
    return remaining_array_values

def parse_array_val(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<array_val>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<array_val>"].keys()),
        )

    if lookahead_type == TK_SYM_OPBRACE:
        opening_brace_token = self.expect(TK_SYM_OPBRACE)
        nested_array_items = self.parse_array_vals_opt()
        self.expect(TK_SYM_CLSBRACE)
        return ArrayInit(
            pos=_tok_pos(opening_brace_token),
            items=nested_array_items
        )

    return self.parse_expr()

# DATA TYPES
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

# ORDAIN LIST
def parse_ordain_dec_list(self: Parser) -> List[OrdainItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ordain_dec_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ordain_dec_list>"].keys()),
        )

    ordain_items = [self.parse_ordain_dec()]
    ordain_items.extend(self.parse_ordain_dec_tail())
    return ordain_items

def parse_ordain_dec_tail(self: Parser) -> List[OrdainItem]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ordain_dec_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ordain_dec_tail>"].keys()),
        )

    if lookahead_type == TK_SYM_SEMICOL:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_ordain_items = [self.parse_ordain_dec()]
    remaining_ordain_items.extend(self.parse_ordain_dec_tail())
    return remaining_ordain_items

def parse_ordain_dec(self: Parser) -> OrdainItem:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ordain_dec>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ordain_dec>"].keys()),
        )

    identifier_token = self.expect(TK_IDENTIFIER)
    array_dimensions = self.parse_array_dims_tail()
    initializer = self.parse_ordain_init_opt()

    return OrdainItem(
        pos=_tok_pos(identifier_token),
        name=_tok_lexeme(identifier_token),
        dims=array_dimensions,
        init=initializer
    )

def parse_ordain_init_opt(self: Parser) -> Optional[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<ordain_init_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<ordain_init_opt>"].keys()),
        )

    if lookahead_type in (TK_SYM_COMMA, TK_SYM_SEMICOL):
        return None

    self.expect(TK_OP_ASSIGN)
    return self.parse_expr()

# CONST EXPR
def parse_const_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<const_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<const_expr>"].keys()),
        )

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