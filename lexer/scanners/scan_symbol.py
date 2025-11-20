from lexer.tokens import Token
from lexer.tokens import (
    TK_SYM_SPACE,
    TK_SYM_COMMA,
    TK_SYM_SEMICOL,
    TK_SYM_SINGLEQ,
    TK_SYM_DOUBLEQ,
    TK_SYM_PAREN,
    TK_SYM_OPPAREN,
    TK_SYM_CLSPAREN,
    TK_SYM_BRACK,
    TK_SYM_OPBRACK,
    TK_SYM_CLSBRACK,
    TK_SYM_BRACE,
    TK_SYM_OPBRACE,
    TK_SYM_CLSBRACE,
    TK_SYM_COLON,
    TK_SYM_DOT,
    TK_SYM_AMP
)

from lexer.errors import LexicalError

def scan_symbol(lexer):
    ch = lexer.current_char
    pos = lexer.pos.copy()

    SYMBOLS = {''
        "{": TK_SYM_OPBRACE,
        "}": TK_SYM_CLSBRACE,
        "(": TK_SYM_OPPAREN,
        ")": TK_SYM_CLSPAREN,
        "[": TK_SYM_OPBRACK,
        "]": TK_SYM_CLSBRACK,
        ";": TK_SYM_SEMICOL,
        ",": TK_SYM_COMMA,
        ":": TK_SYM_COLON,
        ".": TK_SYM_DOT,
        " ": TK_SYM_SPACE,
    }

    if ch in SYMBOLS:
        lexer.advance()
        return Token(SYMBOLS[ch], ch, pos)

    return None
