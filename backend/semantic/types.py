from __future__ import annotations
from dataclasses import dataclass
from backend.tokens import *

T_TALLY = "tally"
T_DIVINE = "divine"
T_SIGIL = "sigil"
T_SCRIPTURE = "scripture"
T_VERITY = "verity"
T_HOLLOW = "hollow"

NUMERIC = {T_TALLY, T_DIVINE}
COMPARABLE = {T_TALLY, T_DIVINE, T_SIGIL, T_SCRIPTURE, T_VERITY}


def token_dtype_to_type(tok_type: str) -> str:
    return {
        TK_DTYPE_TALLY: T_TALLY,
        TK_DTYPE_DIVINE: T_DIVINE,
        TK_DTYPE_SIGIL: T_SIGIL,
        TK_DTYPE_SCRIPTURE: T_SCRIPTURE,
        TK_DTYPE_VERITY: T_VERITY,
        TK_DTYPE_HOLLOW: T_HOLLOW,
    }.get(tok_type, tok_type)


def literal_token_to_type(tok_type: str) -> str:
    return {
        TK_LIT_INT: T_TALLY,
        TK_LIT_DECIMAL: T_DIVINE,
        TK_LIT_CHAR: T_SIGIL,
        TK_LIT_STRING: T_SCRIPTURE,
        TK_LIT_BOOL: T_VERITY,
    }[tok_type]

def is_numeric(t: str) -> bool:
    return t in NUMERIC

def is_bool(t: str) -> bool:
    return t == T_VERITY

def can_assign(dst: str, src: str) -> bool:
    if dst == src:
        return True
    if dst == T_DIVINE and src == T_TALLY:
        return True
    return False

def unary_result(op_tok: str, operand_type: str) -> str | None:
    if op_tok == TK_OP_NOT:
        return T_VERITY if operand_type == T_VERITY else None

# ~ : unary negation (negative numbers)
    if op_tok == TK_OP_TILDE:
        return operand_type if operand_type in NUMERIC else None

    # ++ / -- : numeric only (result same numeric type)
    if op_tok in (TK_OP_INC, TK_OP_DEC):
        return operand_type if operand_type in NUMERIC else None

    # unary minus: numeric only
    if op_tok == TK_OP_MINUS:
        return operand_type if operand_type in NUMERIC else None

    return None


def binary_result(op_tok: str, left: str, right: str) -> str | None:
    # arithmetic / concat
    if op_tok in (TK_OP_PLUS, TK_OP_MINUS, TK_OP_MUL, TK_OP_DIV, TK_OP_MOD, TK_OP_POW):
        if left in NUMERIC and right in NUMERIC:
            # promote to divine if any side is divine
            return T_DIVINE if (left == T_DIVINE or right == T_DIVINE) else T_TALLY
        return None

    if op_tok == TK_OP_CONCAT:
        # allow string concat with anything? (here: only scripture + scripture)
        return T_SCRIPTURE if (left == T_SCRIPTURE and right == T_SCRIPTURE) else None

    # logical
    if op_tok in (TK_OP_AND, TK_OP_OR):
        return T_VERITY if (left == T_VERITY and right == T_VERITY) else None

    # comparisons (return bool)
    if op_tok in (TK_OP_EQ, TK_OP_NOT_EQ, TK_OP_GT, TK_OP_LT, TK_OP_GTE, TK_OP_LTE):
        if left in NUMERIC and right in NUMERIC:
            return T_VERITY
        if left == right and left in COMPARABLE:
            return T_VERITY
        return None

    return None