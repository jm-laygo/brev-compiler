from backend.tokens import *

SYMBOL_MAP = {
    "{": (TK_SYM_OPBRACE, "{"),
    "}": (TK_SYM_CLSBRACE, "}"),
    "(": (TK_SYM_OPPAREN, "("),
    ")": (TK_SYM_CLSPAREN, ")"),
    "[": (TK_SYM_OPBRACK, "["),
    "]": (TK_SYM_CLSBRACK, "]"),
    ";": (TK_SYM_SEMICOL, ";"),
    ",": (TK_SYM_COMMA, ","),
    ":": (TK_SYM_COLON, ":"),
    ".": (TK_SYM_DOT, "."),
    "?": (TK_SYM_TERNARY, "?"),
}

def scan_symbol(lexer, tokens, errors):
    ch = lexer.current_char
    if ch is None:
        return False

    start_pos = lexer.pos.copy()

    if ch in SYMBOL_MAP:
        tok_type, lexeme = SYMBOL_MAP[ch]
        lexer.advance()
        tokens.append(Token(tok_type, lexeme, start_pos))
        return True

    return False