from __future__ import annotations

from typing import Any, List, Union

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *

from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


# --------------------------
# ARG LIST (also used in call expr)
# --------------------------
def parse_arg_list_opt(self: Parser) -> List[Expr]:
    prod = self.choose_prod("<arg_list_opt>")
    if prod == [EPSILON]:
        return []
    return self.parse_arg_list()

def parse_arg_list(self: Parser) -> List[Expr]:
    self.choose_prod("<arg_list>")
    args = [self.parse_expr()]
    args.extend(self.parse_arg_list_tail())
    return args

def parse_arg_list_tail(self: Parser) -> List[Expr]:
    prod = self.choose_prod("<arg_list_tail>")
    if prod == [EPSILON]:
        return []
    self.expect(TK_SYM_COMMA)
    args = [self.parse_expr()]
    args.extend(self.parse_arg_list_tail())
    return args


# --------------------------
# EXPRESSIONS
# --------------------------
def parse_expr(self: Parser) -> Expr:
    self.choose_prod("<expr>")
    return self.parse_logic_or()

def parse_logic_or(self: Parser) -> Expr:
    self.choose_prod("<logic_or>")
    left = self.parse_logic_and()
    while self.la(0) == TK_OP_OR:
        op_tok = self.advance()
        right = self.parse_logic_and()
        left = BinaryExpr(pos=_tok_pos(op_tok), left=left, op=_tok_lexeme(op_tok) or "or", right=right)
    return left

def parse_logic_and(self: Parser) -> Expr:
    self.choose_prod("<logic_and>")
    left = self.parse_equality()
    while self.la(0) == TK_OP_AND:
        op_tok = self.advance()
        right = self.parse_equality()
        left = BinaryExpr(pos=_tok_pos(op_tok), left=left, op=_tok_lexeme(op_tok) or "and", right=right)
    return left

def parse_equality(self: Parser) -> Expr:
    self.choose_prod("<equality>")
    left = self.parse_relational()
    while self.la(0) in (TK_OP_EQ, TK_OP_NOT_EQ):
        op_tok = self.advance()
        right = self.parse_relational()
        op = _tok_lexeme(op_tok) or ("==" if op_tok.type == TK_OP_EQ else "!=")
        left = BinaryExpr(pos=_tok_pos(op_tok), left=left, op=op, right=right)
    return left

def parse_relational(self: Parser) -> Expr:
    self.choose_prod("<relational>")
    left = self.parse_arith_expr()
    while self.la(0) in (TK_OP_GT, TK_OP_LT, TK_OP_GTE, TK_OP_LTE):
        op_tok = self.advance()
        right = self.parse_arith_expr()
        op = _tok_lexeme(op_tok) or {
            TK_OP_GT: ">",
            TK_OP_LT: "<",
            TK_OP_GTE: ">=",
            TK_OP_LTE: "<=",
        }.get(op_tok.type, str(op_tok.type))
        left = BinaryExpr(pos=_tok_pos(op_tok), left=left, op=op, right=right)
    return left

def parse_arith_expr(self: Parser) -> Expr:
    self.choose_prod("<arith_expr>")
    left = self.parse_mul_expr()
    while self.la(0) in (TK_OP_PLUS, TK_OP_MINUS, TK_OP_CONCAT):
        op_tok = self.advance()
        right = self.parse_mul_expr()
        op = _tok_lexeme(op_tok) or {
            TK_OP_PLUS: "+",
            TK_OP_MINUS: "-",
            TK_OP_CONCAT: "++",
        }.get(op_tok.type, str(op_tok.type))
        left = BinaryExpr(pos=_tok_pos(op_tok), left=left, op=op, right=right)
    return left

def parse_mul_expr(self: Parser) -> Expr:
    self.choose_prod("<mul_expr>")
    left = self.parse_pow_expr()
    while self.la(0) in (TK_OP_MUL, TK_OP_DIV, TK_OP_MOD):
        op_tok = self.advance()
        right = self.parse_pow_expr()
        op = _tok_lexeme(op_tok) or {
            TK_OP_MUL: "*",
            TK_OP_DIV: "/",
            TK_OP_MOD: "%",
        }.get(op_tok.type, str(op_tok.type))
        left = BinaryExpr(pos=_tok_pos(op_tok), left=left, op=op, right=right)
    return left

def parse_pow_expr(self: Parser) -> Expr:
    self.choose_prod("<pow_expr>")
    left = self.parse_unary_expr()
    if self.la(0) == TK_OP_POW:
        op_tok = self.advance()
        right = self.parse_pow_expr()
        left = BinaryExpr(pos=_tok_pos(op_tok), left=left, op=_tok_lexeme(op_tok) or "^", right=right)
    return left

def parse_unary_expr(self: Parser) -> Expr:
    self.choose_prod("<unary_expr>")
    la = self.la(0)

    if la in (TK_OP_NOT, TK_OP_TILDE):
        op_tok = self.advance()
        operand = self.parse_unary_expr()
        op = _tok_lexeme(op_tok) or ("!" if la == TK_OP_NOT else "~")
        return UnaryExpr(pos=_tok_pos(op_tok), op=op, operand=operand, prefix=True)

    if la in (TK_OP_INC, TK_OP_DEC):
        op_tok = self.advance()
        lv = self.parse_lvalue_core()
        return UnaryExpr(
            pos=_tok_pos(op_tok),
            op=_tok_lexeme(op_tok) or ("++" if la == TK_OP_INC else "--"),
            operand=VarExpr(pos=_tok_pos(op_tok), ref=lv),
            prefix=True,
        )

    return self.parse_postfix_expr()

def parse_postfix_expr(self: Parser) -> Expr:
    self.choose_prod("<postfix_expr>")
    primary = self.parse_primary()

    if self.la(0) in (TK_OP_INC, TK_OP_DEC):
        op_tok = self.advance()
        op = _tok_lexeme(op_tok) or ("++" if op_tok.type == TK_OP_INC else "--")
        return UnaryExpr(pos=_tok_pos(op_tok), op=op, operand=primary, prefix=False)

    return primary

def parse_primary(self: Parser) -> Expr:
    self.choose_prod("<primary>")
    la = self.la(0)

    if la in (TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL):
        return self.parse_literal_expr()

    if la == TK_SYM_OPPAREN:
        lpar = self.expect(TK_SYM_OPPAREN)
        inner = self.parse_expr()
        self.expect(TK_SYM_CLSPAREN)
        return GroupExpr(pos=_tok_pos(lpar), expr=inner)

    if la == TK_OTHERS_VERSEOF:
        tok = self.expect(TK_OTHERS_VERSEOF)
        self.expect(TK_SYM_OPPAREN)
        inner = self.parse_expr()
        self.expect(TK_SYM_CLSPAREN)
        return VerseOfExpr(pos=_tok_pos(tok), expr=inner)

    if la == TK_IDENTIFIER:
        id_tok = self.expect(TK_IDENTIFIER)
        name = _tok_lexeme(id_tok)
        return self.parse_id_primary_tail(id_tok, name)

    tok = self.peek(0) or self.peek(-1)
    raise ParserError(tok, expected=list(PREDICT["<primary>"].keys()), details="Invalid <primary>")

def parse_id_primary_tail(self: Parser, id_tok: Any, name: str) -> Expr:
    self.choose_prod("<id_primary_tail>")
    la = self.la(0)

    if la == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        args = self.parse_arg_list_opt()
        self.expect(TK_SYM_CLSPAREN)

        base_access = NameRef(pos=_tok_pos(id_tok), name=name)
        access = self.parse_access_chain_opt(base_access)
        return CallExpr(pos=_tok_pos(id_tok), callee=name, args=args, access=access)

    base_lv: LValue = NameRef(pos=_tok_pos(id_tok), name=name)
    access = self.parse_access_chain_opt(base_lv)
    lv = access if access is not None else base_lv
    return VarExpr(pos=_tok_pos(id_tok), ref=lv)

def parse_literal_expr(self: Parser) -> LiteralExpr:
    la = self.la(0)
    tok = self.advance()
    lex = _tok_lexeme(tok)

    if la == TK_LIT_INT:
        try:
            val = int(lex)
        except Exception:
            val = lex
        return LiteralExpr(pos=_tok_pos(tok), value=val, literal_type="int")

    if la == TK_LIT_DECIMAL:
        try:
            val = float(lex)
        except Exception:
            val = lex
        return LiteralExpr(pos=_tok_pos(tok), value=val, literal_type="decimal")

    if la == TK_LIT_CHAR:
        return LiteralExpr(pos=_tok_pos(tok), value=lex, literal_type="char")

    if la == TK_LIT_STRING:
        return LiteralExpr(pos=_tok_pos(tok), value=lex, literal_type="string")

    if la == TK_LIT_BOOL:
        v = lex.lower() if isinstance(lex, str) else lex
        if v in ("true", "false"):
            return LiteralExpr(pos=_tok_pos(tok), value=(v == "true"), literal_type="bool")
        return LiteralExpr(pos=_tok_pos(tok), value=lex, literal_type="bool")

    raise ParserError(tok, expected=[TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL], details="Not a literal token")


# ---- attach ----
Parser.parse_arg_list_opt = parse_arg_list_opt
Parser.parse_arg_list = parse_arg_list
Parser.parse_arg_list_tail = parse_arg_list_tail

Parser.parse_expr = parse_expr
Parser.parse_logic_or = parse_logic_or
Parser.parse_logic_and = parse_logic_and
Parser.parse_equality = parse_equality
Parser.parse_relational = parse_relational
Parser.parse_arith_expr = parse_arith_expr
Parser.parse_mul_expr = parse_mul_expr
Parser.parse_pow_expr = parse_pow_expr
Parser.parse_unary_expr = parse_unary_expr
Parser.parse_postfix_expr = parse_postfix_expr
Parser.parse_primary = parse_primary
Parser.parse_id_primary_tail = parse_id_primary_tail
Parser.parse_literal_expr = parse_literal_expr