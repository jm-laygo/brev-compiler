from lexer.tokens import Token
from lexer.tokens import (
    TK_OP_PLUS,
    TK_OP_MINUS,
    TK_OP_MUL,
    TK_OP_DIV,
    TK_OP_MOD,
    TK_OP_POW,
    TK_OP_TILDE,

    TK_OP_ASSIGN,
    TK_OP_PLUS_EQ,
    TK_OP_MINUS_EQ,
    TK_OP_MUL_EQ,
    TK_OP_DIV_EQ,
    TK_OP_MOD_EQ,
    TK_OP_POW_EQ,

    TK_OP_EQ,
    TK_OP_NOTEQ,
    TK_OP_GT,
    TK_OP_LT,
    TK_OP_GTE,
    TK_OP_LTE,

    TK_OP_AND,
    TK_OP_OR,
    TK_OP_NOT,

    TK_OP_INC,
    TK_OP_DEC,
)
from lexer.errors import LexicalError

def scan_operator(lexer):
    ch = lexer.current_char
    pos = lexer.pos.copy()

    if ch == "=":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return Token(TK_OP_EQ, "==", pos)
        return Token(TK_OP_ASSIGN, "=", pos)

    if ch == "+":
        lexer.advance()
        if lexer.current_char == "+":
            lexer.advance()
            return Token(TK_OP_INC, "++", pos)
        if lexer.current_char == "=":
            lexer.advance()
            return Token(TK_OP_PLUS_EQ, "+=", pos)
        return Token(TK_OP_PLUS, "+", pos)

    if ch == "-":
        lexer.advance()
        if lexer.current_char == "-":
            lexer.advance()
            return Token(TK_OP_DEC, "--", pos)
        if lexer.current_char == "=":
            lexer.advance()
            return Token(TK_OP_MINUS_EQ, "-=", pos)
        return Token(TK_OP_MINUS, "-", pos)

    if ch == "*":
        lexer.advance()
        if lexer.current_char == "*":
            lexer.advance()
            if lexer.current_char == "=":
                lexer.advance()
                return Token(TK_OP_POW_EQ, "**=", pos)
            return Token(TK_OP_POW, "**", pos)
        if lexer.current_char == "=":
            lexer.advance()
            return Token(TK_OP_MUL_EQ, "*=", pos)
        return Token(TK_OP_MUL, "*", pos)

    if ch == "/":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return Token(TK_OP_DIV_EQ, "/=", pos)
        return Token(TK_OP_DIV, "/", pos)

    if ch == "%":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return Token(TK_OP_MOD_EQ, "%=", pos)
        return Token(TK_OP_MOD, "%", pos)

    if ch == "!":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return Token(TK_OP_NOTEQ, "!=", pos)
        return Token(TK_OP_NOT, "!!", pos)

    if ch == "&":
        lexer.advance()
        if lexer.current_char == "&":
            lexer.advance()
            return Token(TK_OP_AND, "&&", pos)
        return Token(TK_OP_AND, "&", pos)

    if ch == "|":
        lexer.advance()
        if lexer.current_char == "|":
            lexer.advance()
            return Token(TK_OP_OR, "||", pos)
        raise LexicalError(pos, f"Unexpected character '{ch}'")

    if ch == "~":
        lexer.advance()
        return Token(TK_OP_TILDE, "~", pos)

    return None
