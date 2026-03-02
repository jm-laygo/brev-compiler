from __future__ import annotations
from backend.errors import ParserError

from backend.tokens import *
from backend.ast.ast_nodes import (
    Expr,
    LiteralExpr, UnaryExpr, BinaryExpr,
    GroupExpr, CallExpr, VarExpr, VerseOfExpr,
    NameRef,
)

class ExprsMixin:
    # ---------- expressions ----------
    def parse_const_expr(self) -> Expr:
        return self.parse_expr()

    def parse_expr(self) -> Expr:
        return self.parse_logic_or()

    def parse_logic_or(self) -> Expr:
        left = self.parse_logic_and()
        while self.accept(TK_OP_OR):
            right = self.parse_logic_and()
            left = BinaryExpr(left=left, op=TK_OP_OR, right=right, pos=getattr(left, "pos", None))
        return left

    def parse_logic_and(self) -> Expr:
        left = self.parse_equality()
        while self.accept(TK_OP_AND):
            right = self.parse_equality()
            left = BinaryExpr(left=left, op=TK_OP_AND, right=right, pos=getattr(left, "pos", None))
        return left

    def parse_equality(self) -> Expr:
        left = self.parse_relational()
        while self.peek().type in (TK_OP_EQ, TK_OP_NOT_EQ):
            op_tok = self.match(self.peek().type)
            right = self.parse_relational()
            left = BinaryExpr(left=left, op=op_tok.type, right=right, pos=op_tok.pos)
        return left

    def parse_relational(self) -> Expr:
        left = self.parse_arith()
        while self.peek().type in (TK_OP_GT, TK_OP_LT, TK_OP_GTE, TK_OP_LTE):
            op_tok = self.match(self.peek().type)
            right = self.parse_arith()
            left = BinaryExpr(left=left, op=op_tok.type, right=right, pos=op_tok.pos)
        return left

    def parse_arith(self) -> Expr:
        left = self.parse_mul()
        while self.peek().type in (TK_OP_PLUS, TK_OP_MINUS, TK_OP_CONCAT):
            op_tok = self.match(self.peek().type)
            right = self.parse_mul()
            left = BinaryExpr(left=left, op=op_tok.type, right=right, pos=op_tok.pos)
        return left

    def parse_mul(self) -> Expr:
        left = self.parse_pow()
        while self.peek().type in (TK_OP_MUL, TK_OP_DIV, TK_OP_MOD):
            op_tok = self.match(self.peek().type)
            right = self.parse_pow()
            left = BinaryExpr(left=left, op=op_tok.type, right=right, pos=op_tok.pos)
        return left

    def parse_pow(self) -> Expr:
        left = self.parse_unary()
        if self.accept(TK_OP_POW):
            right = self.parse_pow()  # right associative
            return BinaryExpr(left=left, op=TK_OP_POW, right=right, pos=getattr(left, "pos", None))
        return left

    def parse_unary(self) -> Expr:
        if self.peek().type in (TK_OP_NOT, TK_OP_TILDE, TK_OP_INC, TK_OP_DEC):
            op_tok = self.match(self.peek().type)
            operand = self.parse_unary()
            return UnaryExpr(op=op_tok.type, operand=operand, prefix=True, pos=op_tok.pos)
        return self.parse_postfix()

    def parse_postfix(self) -> Expr:
        node = self.parse_primary()

        # postfix ++/-- in expression
        if self.peek().type in (TK_OP_INC, TK_OP_DEC):
            op_tok = self.match(self.peek().type)
            return UnaryExpr(op=op_tok.type, operand=node, prefix=False, pos=op_tok.pos)

        return node

    def parse_primary(self) -> Expr:
        tok = self.peek()
        # literals
        if tok.type in (TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL):
            self.i += 1
            if tok.type == TK_LIT_INT:
                return LiteralExpr(value=tok.value, literal_type = "tally", pos=tok.pos)
            if tok.type == TK_LIT_DECIMAL:
                return LiteralExpr(value=tok.value, literal_type = "divine", pos=tok.pos)
            if tok.type == TK_LIT_CHAR:
                return LiteralExpr(value=tok.value, literal_type = "sigil", pos=tok.pos)
            if tok.type == TK_LIT_STRING:
                return LiteralExpr(value=tok.value, literal_type = "scripture", pos=tok.pos)
            return LiteralExpr(value=tok.value, literal_type = "verity", pos=tok.pos)

        # (expr)
        if self.accept(TK_SYM_OPPAREN):
            expr = self.parse_expr()
            self.match(TK_SYM_CLSPAREN)
            return GroupExpr(expr=expr, pos=getattr(expr, "pos", None))

        # verseof(expr)
        if tok.type == TK_OTHERS_VERSEOF:
            vtok = self.match(TK_OTHERS_VERSEOF)
            self.match(TK_SYM_OPPAREN)
            inner = self.parse_expr()
            self.match(TK_SYM_CLSPAREN)
            return VerseOfExpr(expr=inner, pos=vtok.pos)

        # identifier: call expr or var expr
        if tok.type == TK_IDENTIFIER:
            id_tok = self.match(TK_IDENTIFIER)

            # call expr: id(arg_list_opt) access_chain_opt?
            if self.accept(TK_SYM_OPPAREN):
                args = self.parse_arg_list_opt_until_rparen()
                self.match(TK_SYM_CLSPAREN)

                access = None
                if self.peek().type in (TK_SYM_OPBRACK, TK_SYM_DOT):
                    # store chain rooted at dummy NameRef (same pattern you used)
                    access = self.parse_access_chain(NameRef(name="$call", pos=id_tok.pos))

                return CallExpr(callee=id_tok.value, args=args, access=access, pos=id_tok.pos)

            # var expr: lvalue (+ access chain)
            lv = self.parse_access_chain(NameRef(name=id_tok.value, pos=id_tok.pos))
            return VarExpr(ref=lv, pos=id_tok.pos)

        raise ParserError(tok, expected=["<primary>"], details=None)

    # ---------- arg lists ----------
    def parse_arg_list_opt_until_rparen(self) -> list[Expr]:
        args: list[Expr] = []
        if self.at(TK_SYM_CLSPAREN):
            return args
        args.append(self.parse_expr())
        while self.accept(TK_SYM_COMMA):
            args.append(self.parse_expr())
        return args