from __future__ import annotations
from typing import Any, List, Union

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT, EPSILON
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos

# ARGUMENT LIST
def parse_arg_list_opt(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<arg_list_opt>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<arg_list_opt>"].keys())
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    return self.parse_arg_list()

def parse_arg_list(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<arg_list>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<arg_list>"].keys())
        )

    argument_list = [self.parse_expr()]
    argument_list.extend(self.parse_arg_list_tail())
    return argument_list

def parse_arg_list_tail(self: Parser) -> List[Expr]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<arg_list_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<arg_list_tail>"].keys())
        )

    if lookahead_type == TK_SYM_CLSPAREN:
        return []

    self.expect(TK_SYM_COMMA)
    remaining_arguments = [self.parse_expr()]
    remaining_arguments.extend(self.parse_arg_list_tail())
    return remaining_arguments

# EXPRESSIONS
def parse_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<expr>"].keys())
        )

    return self.parse_logic_or()

def parse_logic_or(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<logic_or>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<logic_or>"].keys())
        )

    left_expr = self.parse_logic_and()

    while self.current_type(0) == TK_OP_OR:
        operator_token = self.advance()
        right_expr = self.parse_logic_and()
        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=_tok_lexeme(operator_token) or "or",
            right=right_expr
        )

    return left_expr

def parse_logic_and(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<logic_and>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<logic_and>"].keys())
        )

    left_expr = self.parse_equality()

    while self.current_type(0) == TK_OP_AND:
        operator_token = self.advance()
        right_expr = self.parse_equality()
        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=_tok_lexeme(operator_token) or "and",
            right=right_expr
        )

    return left_expr

def parse_equality(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<equality>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<equality>"].keys())
        )

    left_expr = self.parse_relational()

    while self.current_type(0) in (TK_OP_EQ, TK_OP_NOT_EQ):
        operator_token = self.advance()
        right_expr = self.parse_relational()
        operator_lexeme = _tok_lexeme(operator_token) or (
            "==" if operator_token.type == TK_OP_EQ else "!="
        )
        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=operator_lexeme,
            right=right_expr
        )

    return left_expr

def parse_relational(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<relational>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<relational>"].keys())
        )

    left_expr = self.parse_arith_expr()

    while self.current_type(0) in (TK_OP_GT, TK_OP_LT, TK_OP_GTE, TK_OP_LTE):
        operator_token = self.advance()
        right_expr = self.parse_arith_expr()
        operator_lexeme = _tok_lexeme(operator_token) or {
            TK_OP_GT: ">",
            TK_OP_LT: "<",
            TK_OP_GTE: ">=",
            TK_OP_LTE: "<=",
        }.get(operator_token.type, str(operator_token.type))

        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=operator_lexeme,
            right=right_expr
        )

    return left_expr

def parse_arith_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<arith_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<arith_expr>"].keys())
        )

    left_expr = self.parse_mul_expr()

    while self.current_type(0) in (TK_OP_PLUS, TK_OP_MINUS, TK_OP_CONCAT):
        operator_token = self.advance()
        right_expr = self.parse_mul_expr()
        operator_lexeme = _tok_lexeme(operator_token) or {
            TK_OP_PLUS: "+",
            TK_OP_MINUS: "-",
            TK_OP_CONCAT: "&",
        }.get(operator_token.type, str(operator_token.type))

        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=operator_lexeme,
            right=right_expr
        )

    return left_expr

def parse_mul_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<mul_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<mul_expr>"].keys())
        )

    left_expr = self.parse_pow_expr()

    while self.current_type(0) in (TK_OP_MUL, TK_OP_DIV, TK_OP_MOD):
        operator_token = self.advance()
        right_expr = self.parse_pow_expr()
        operator_lexeme = _tok_lexeme(operator_token) or {
            TK_OP_MUL: "*",
            TK_OP_DIV: "/",
            TK_OP_MOD: "%",
        }.get(operator_token.type, str(operator_token.type))

        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=operator_lexeme,
            right=right_expr
        )

    return left_expr

def parse_pow_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<pow_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<pow_expr>"].keys())
        )

    left_expr = self.parse_unary_expr()

    if self.current_type(0) == TK_OP_POW:
        operator_token = self.advance()
        right_expr = self.parse_pow_expr()
        left_expr = BinaryExpr(
            pos=_tok_pos(operator_token),
            left=left_expr,
            op=_tok_lexeme(operator_token) or "^",
            right=right_expr
        )

    return left_expr

def parse_unary_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<unary_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<unary_expr>"].keys())
        )

    if lookahead_type in (TK_OP_NOT, TK_OP_TILDE):
        operator_token = self.advance()
        operand_expr = self.parse_unary_expr()
        operator_lexeme = _tok_lexeme(operator_token) or (
            "!" if lookahead_type == TK_OP_NOT else "~"
        )
        return UnaryExpr(
            pos=_tok_pos(operator_token),
            op=operator_lexeme,
            operand=operand_expr,
            prefix=True
        )

    if lookahead_type in (TK_OP_INC, TK_OP_DEC):
        operator_token = self.advance()
        target_reference = self.parse_lvalue_core()
        return UnaryExpr(
            pos=_tok_pos(operator_token),
            op=_tok_lexeme(operator_token) or (
                "++" if lookahead_type == TK_OP_INC else "--"
            ),
            operand=VarExpr(pos=_tok_pos(operator_token), ref=target_reference),
            prefix=True,
        )

    return self.parse_postfix_expr()

def parse_postfix_expr(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<postfix_expr>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<postfix_expr>"].keys())
        )

    base_expr = self.parse_primary()

    if self.current_type(0) in (TK_OP_INC, TK_OP_DEC):
        operator_token = self.advance()
        operator_lexeme = _tok_lexeme(operator_token) or (
            "++" if operator_token.type == TK_OP_INC else "--"
        )
        return UnaryExpr(
            pos=_tok_pos(operator_token),
            op=operator_lexeme,
            operand=base_expr,
            prefix=False
        )

    return base_expr

def parse_primary(self: Parser) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<primary>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<primary>"].keys())
        )

    if lookahead_type in (
        TK_LIT_INT,
        TK_LIT_DECIMAL,
        TK_LIT_CHAR,
        TK_LIT_STRING,
        TK_LIT_BOOL
    ):
        return self.parse_literal_expr()

    if lookahead_type == TK_SYM_OPPAREN:
        opening_paren_token = self.expect(TK_SYM_OPPAREN)
        inner_expr = self.parse_expr()
        self.expect(TK_SYM_CLSPAREN)
        return GroupExpr(pos=_tok_pos(opening_paren_token), expr=inner_expr)

    if lookahead_type == TK_OTHERS_VERSEOF:
        verseof_token = self.expect(TK_OTHERS_VERSEOF)
        self.expect(TK_SYM_OPPAREN)
        inner_expr = self.parse_expr()
        self.expect(TK_SYM_CLSPAREN)
        return VerseOfExpr(pos=_tok_pos(verseof_token), expr=inner_expr)

    if lookahead_type == TK_IDENTIFIER:
        identifier_token = self.expect(TK_IDENTIFIER)
        identifier_name = _tok_lexeme(identifier_token)
        return self.parse_id_primary_tail(identifier_token, identifier_name)

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=list(PREDICT["<primary>"].keys())
    )

def parse_id_primary_tail(self: Parser, identifier_token: Any, identifier_name: str) -> Expr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<id_primary_tail>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<id_primary_tail>"].keys())
        )

    if lookahead_type == TK_SYM_OPPAREN:
        self.expect(TK_SYM_OPPAREN)
        argument_list = self.parse_arg_list_opt()
        self.expect(TK_SYM_CLSPAREN)

        base_reference = NameRef(pos=_tok_pos(identifier_token), name=identifier_name)
        access_chain = self.parse_access_chain_opt(base_reference)

        return CallExpr(
            pos=_tok_pos(identifier_token),
            callee=identifier_name,
            args=argument_list,
            access=access_chain
        )

    base_reference: LValue = NameRef(pos=_tok_pos(identifier_token), name=identifier_name)
    access_chain = self.parse_access_chain_opt(base_reference)
    resolved_reference = access_chain if access_chain is not None else base_reference
    return VarExpr(pos=_tok_pos(identifier_token), ref=resolved_reference)

def parse_literal_expr(self: Parser) -> LiteralExpr:
    lookahead_type = self.current_type(0)

    if lookahead_type not in (
        TK_LIT_INT,
        TK_LIT_DECIMAL,
        TK_LIT_CHAR,
        TK_LIT_STRING,
        TK_LIT_BOOL
    ):
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=[TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL]
        )

    literal_token = self.advance()
    literal_lexeme = _tok_lexeme(literal_token)

    if lookahead_type == TK_LIT_INT:
        try:
            literal_value = int(literal_lexeme)
        except Exception:
            literal_value = literal_lexeme
        return LiteralExpr(pos=_tok_pos(literal_token), value=literal_value, literal_type="int")

    if lookahead_type == TK_LIT_DECIMAL:
        try:
            literal_value = float(literal_lexeme)
        except Exception:
            literal_value = literal_lexeme
        return LiteralExpr(pos=_tok_pos(literal_token), value=literal_value, literal_type="decimal")

    if lookahead_type == TK_LIT_CHAR:
        char_value = literal_lexeme

        if not isinstance(char_value, str):
            self.error_expected([TK_LIT_CHAR], "Invalid sigil literal.")

        if len(char_value) == 3 and char_value[0] == "'" and char_value[2] == "'":
            char_value = char_value[1]
        else:
            self.error_expected([TK_LIT_CHAR], "Invalid sigil literal format.")

        return LiteralExpr(
            pos=_tok_pos(literal_token),
            value=char_value,
            literal_type="char",
        )

    if lookahead_type == TK_LIT_STRING:
        string_value = literal_lexeme

        if isinstance(string_value, str) and len(string_value) >= 2 and string_value[0] == '"' and string_value[-1] == '"':
            string_value = string_value[1:-1]

        return LiteralExpr(
            pos=_tok_pos(literal_token),
            value=string_value,
            literal_type="string",
        )

    if lookahead_type == TK_LIT_BOOL:
        normalized_bool_lexeme = (
            literal_lexeme.lower() if isinstance(literal_lexeme, str) else literal_lexeme
        )
        if normalized_bool_lexeme in ("true", "false", "holy", "unholy"):
            return LiteralExpr(
                pos=_tok_pos(literal_token),
                value=(normalized_bool_lexeme == "true" or normalized_bool_lexeme == "holy"),
                literal_type="bool"
            )
        return LiteralExpr(pos=_tok_pos(literal_token), value=literal_lexeme, literal_type="bool")

    raise ParserError(
        literal_token,
        expected=[TK_LIT_INT, TK_LIT_DECIMAL, TK_LIT_CHAR, TK_LIT_STRING, TK_LIT_BOOL]
    )

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