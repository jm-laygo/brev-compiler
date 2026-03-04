from backend.errors import LexicalError
from backend.tokens import *
from backend.delimiters import *

def accept_operator(lexer, tokens, errors, tok_type, lexeme, start_pos, allowed_delims):
    if isinstance(allowed_delims, str):
        allowed_delims = {allowed_delims}

    ch = lexer.current_char

    expected = format_expected_delims(allowed_delims)

    if ch is None and None not in allowed_delims:
        errors.append(LexicalError(start_pos, f"Missing delimiter after operator '{lexeme}'. Expected: {expected}"))
        return True

    if ch is not None and ch not in allowed_delims:
        errors.append(LexicalError(start_pos, f"Invalid delimiter {repr(ch)} after operator '{lexeme}'. Expected: {expected}"))
        return True

    tokens.append(Token(tok_type, lexeme, start_pos))
    return True

def scan_operator(lexer, tokens, errors):
    ch = lexer.current_char
    if ch is None:
        return False

    pos = lexer.pos.copy()

    if ch == "~":
        lexer.advance()
        return accept_operator(
            lexer, tokens, errors,
            TK_OP_TILDE, "~", pos, delim3)

    # ASSIGN / EQUALITY
    if ch == "=":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_EQ, "==", pos, delim5)
        return accept_operator(lexer, tokens, errors, TK_OP_ASSIGN, "=", pos, delim4)

    # PLUS
    if ch == "+":
        lexer.advance()
        if lexer.current_char == "+":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_INC, "++", pos, delim2)
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_PLUS_EQ, "+=", pos, delim3)
        return accept_operator(lexer, tokens, errors, TK_OP_PLUS, "+", pos, delim3)

    # MINUS
    if ch == "-":
        lexer.advance()
        if lexer.current_char == "-":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_DEC, "--", pos, delim2)
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_MINUS_EQ, "-=", pos, delim3)
        return accept_operator(lexer, tokens, errors, TK_OP_MINUS, "-", pos, delim3)

    # MULT / POW
    if ch == "*":
        lexer.advance()
        if lexer.current_char == "*":
            lexer.advance()
            if lexer.current_char == "=":
                lexer.advance()
                return accept_operator(lexer, tokens, errors, TK_OP_POW_EQ, "**=", pos, delim3)
            return accept_operator(lexer, tokens, errors, TK_OP_POW, "**", pos, delim3)
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_MUL_EQ, "*=", pos, delim3)
        return accept_operator(lexer, tokens, errors, TK_OP_MUL, "*", pos, delim3)

    # DIV
    if ch == "/":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_DIV_EQ, "/=", pos, delim3)
        return accept_operator(lexer, tokens, errors, TK_OP_DIV, "/", pos, delim3)

    # MOD
    if ch == "%":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_MOD_EQ, "%=", pos, delim3)
        return accept_operator(lexer, tokens, errors, TK_OP_MOD, "%", pos, delim3)

    # NOT / NOTEQ / !!
    if ch == "!":
        lexer.advance()

        # !=
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_NOT_EQ, "!=", pos, delim5)

        # !!
        if lexer.current_char == "!":
            lexer.advance()
            return accept_operator(
                lexer, tokens, errors,
                TK_OP_NOT, "!!", pos,
                {None, space, newline, tab, op_par, cl_par, cl_brc, cl_bra, semicolon, comma, "~", '"', "'", "!"}
                | set(ALPHABET) | set(ALPHA_DIG)
            )

        errors.append(LexicalError(pos, "Invalid operator '!'. Use '!!' for NOT, or '!=' for NOT-EQUAL."))
        return True

    # AND / CONCAT
    if ch == "&":
        # &&
        if lexer.peek() == "&":
            lexer.advance()
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_AND, "&&", pos, delim3)

        # &
        lexer.advance()
        return accept_operator(lexer, tokens, errors, TK_OP_CONCAT, "&", pos, delim12 | {op_par})

    # OR
    if ch == "|":
        if lexer.peek() == "|":
            lexer.advance()
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_OR, "||", pos, delim3)

        lexer.advance()
        errors.append(LexicalError(pos, "Invalid operator '|'. Use '||' for OR."))
        return True

    # RELATIONAL
    if ch == "<":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_LTE, "<=", pos, delim3)
        return accept_operator(lexer, tokens, errors, TK_OP_LT, "<", pos, delim3)

    if ch == ">":
        lexer.advance()
        if lexer.current_char == "=":
            lexer.advance()
            return accept_operator(lexer, tokens, errors, TK_OP_GTE, ">=", pos, delim3)
        return accept_operator(lexer, tokens, errors, TK_OP_GT, ">", pos, delim3)

    return False