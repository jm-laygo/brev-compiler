from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.ast.ast_nodes import (
    Node,
    Expr,
    SacredDecl, SacredItem,
    VarDecl, VarItem,
    OrderDecl, OrderMember,
    OrdainDecl, OrdainItem,
    ArrayInit,
)


class DeclsMixin:
    # ---------- declarations ----------
    def parse_decl_item(self, global_scope: bool) -> Node:
        t = self.peek().type

        # sacred <data_type> <sacred_init_list> ;
        if t == TK_SACRED:
            s_tok = self.match(TK_SACRED)
            type_name = self.parse_data_type()  # only built-in types
            items = self.parse_sacred_init_list()
            self.match(TK_SYM_SEMICOL)
            return SacredDecl(type_name=type_name, items=items, pos=s_tok.pos)

        # <data_type> <var_decl_group> ;
        if t in (TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY):
            dt_tok = self.peek()
            type_name = self.parse_data_type()
            items = self.parse_var_decl_group()
            self.match(TK_SYM_SEMICOL)
            return VarDecl(type_name=type_name, items=items, pos=dt_tok.pos)

        # order ID { <member_list_opt> } ;
        if t == TK_OTHERS_ORDER:
            o_tok = self.match(TK_OTHERS_ORDER)
            name_tok = self.match(TK_IDENTIFIER)
            self.match(TK_SYM_OPBRACE)
            members = []
            if not self.at(TK_SYM_CLSBRACE):
                members = self.parse_order_member_list()
            self.match(TK_SYM_CLSBRACE)
            self.match(TK_SYM_SEMICOL)
            return OrderDecl(name=name_tok.value, members=members, pos=o_tok.pos)

        # ordain ID <ordain_dec_list> ;
        if t == TK_OTHERS_ORDAIN:
            o_tok = self.match(TK_OTHERS_ORDAIN)
            name_tok = self.match(TK_IDENTIFIER)
            items = self.parse_ordain_dec_list()
            self.match(TK_SYM_SEMICOL)
            return OrdainDecl(name=name_tok.value, items=items, pos=o_tok.pos)

        self.expect_one_of(self.DECL_START)

    # ---------- types ----------
    def parse_data_type(self) -> str:
        tok = self.peek()
        if tok.type in (TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY):
            self.i += 1
            return tok.type
        raise ParserError(
            tok,
            expected=[TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY],
            details=None
        )

    def parse_data_type_id(self) -> str:
        tok = self.peek()
        if tok.type in (TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY):
            self.i += 1
            return tok.type
        if tok.type == TK_IDENTIFIER:
            self.i += 1
            return tok.value
        raise ParserError(
            tok,
            expected=[TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY, TK_IDENTIFIER],
            details=None
        )

    # ---------- sacred ----------
    # sacred_init_list: id (= const_expr)? (, ... )*
    def parse_sacred_init_list(self) -> list[SacredItem]:
        items = [self.parse_sacred_init()]
        while self.accept(TK_SYM_COMMA):
            items.append(self.parse_sacred_init())
        return items

    def parse_sacred_init(self) -> SacredItem:
        id_tok = self.match(TK_IDENTIFIER)
        value = None
        if self.accept(TK_OP_ASSIGN):
            value = self.parse_const_expr()
        return SacredItem(name=id_tok.value, value=value, pos=id_tok.pos)

    # ---------- vars ----------
    # var_decl_group: var_decl_item (, var_decl_item)*
    def parse_var_decl_group(self) -> list[VarItem]:
        items = [self.parse_var_decl_item()]
        while self.accept(TK_SYM_COMMA):
            items.append(self.parse_var_decl_item())
        return items

    # var_decl_item: id array_dims_tail (= (array_init|expr))?
    def parse_var_decl_item(self) -> VarItem:
        id_tok = self.match(TK_IDENTIFIER)
        dims = self.parse_array_dims_tail()
        init = None
        if self.accept(TK_OP_ASSIGN):
            init = self.parse_var_after_eq()
        return VarItem(name=id_tok.value, dims=dims, init=init, pos=id_tok.pos)

    # ---------- arrays ----------
    def parse_array_dims_tail(self) -> list[Expr]:
        dims = []
        while self.accept(TK_SYM_OPBRACK):
            dims.append(self.parse_expr())
            self.match(TK_SYM_CLSBRACK)
        return dims

    def parse_var_after_eq(self) -> Expr:
        if self.at(TK_SYM_OPBRACE):
            return self.parse_array_init()
        return self.parse_expr()

    def parse_array_init(self) -> ArrayInit:
        ob = self.match(TK_SYM_OPBRACE)
        items = []
        if not self.at(TK_SYM_CLSBRACE):
            items.append(self.parse_array_val())
            while self.accept(TK_SYM_COMMA):
                items.append(self.parse_array_val())
        self.match(TK_SYM_CLSBRACE)
        return ArrayInit(items=items, pos=ob.pos)

    def parse_array_val(self) -> Expr:
        # array_val: '{' array_vals_opt '}' | expr
        if self.at(TK_SYM_OPBRACE):
            return self.parse_array_init()
        return self.parse_expr()

    # ---------- order members ----------
    def parse_order_member_list(self) -> list[OrderMember]:
        members = []
        while self.peek().type in (
            TK_DTYPE_TALLY, TK_DTYPE_DIVINE, TK_DTYPE_SIGIL, TK_DTYPE_SCRIPTURE, TK_DTYPE_VERITY, TK_IDENTIFIER
        ):
            members.append(self.parse_order_member())
        return members

    def parse_order_member(self) -> OrderMember:
        type_tok = self.peek()
        type_name = self.parse_data_type_id()
        name_tok = self.match(TK_IDENTIFIER)
        dims = self.parse_array_dims_tail()
        init = None
        if self.accept(TK_OP_ASSIGN):
            init = self.parse_array_init() if self.at(TK_SYM_OPBRACE) else self.parse_expr()
        self.match(TK_SYM_SEMICOL)
        return OrderMember(type_name=type_name, name=name_tok.value, dims=dims, init=init, pos=type_tok.pos)

    # ---------- ordain ----------
    def parse_ordain_dec_list(self) -> list[OrdainItem]:
        items = [self.parse_ordain_dec()]
        while self.accept(TK_SYM_COMMA):
            items.append(self.parse_ordain_dec())
        return items

    def parse_ordain_dec(self) -> OrdainItem:
        id_tok = self.match(TK_IDENTIFIER)
        dims = self.parse_array_dims_tail()
        init = None
        if self.accept(TK_OP_ASSIGN):
            init = self.parse_expr()
        return OrdainItem(name=id_tok.value, dims=dims, init=init, pos=id_tok.pos)