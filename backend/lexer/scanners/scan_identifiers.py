from backend.lexer.reserved_words import RESERVED_WORDS
from backend.lexer.tokens import Token, TK_IDENTIFIER
from backend.lexer.delimiters import idnt_delim, id_sym
from backend.lexer.errors import LexicalError

MAX_IDENTIFIER_LENGTH = 31

def scan_identifier(lexer, allow_reserved_as_type=True):
    pos = lexer.pos.copy()
    text = ""

    # identifier must start with alphabet
    if not lexer.current_char.isalpha():
        raise LexicalError(pos, f"Invalid start of identifier '{lexer.current_char}'")

    while lexer.current_char is not None and lexer.current_char in id_sym:
        if len(text) < MAX_IDENTIFIER_LENGTH:
            text += lexer.current_char
        lexer.advance()

    # Delimiter check (space, newline, semicolon, comma, EOF, etc.)
    if lexer.current_char is not None and lexer.current_char not in idnt_delim:
        if lexer.current_char == "\n":
            return Token(TK_IDENTIFIER, text, pos)
        raise LexicalError(pos, f"Invalid character '{lexer.current_char}' in identifier '{text}'")

    # Exact reserved word?
    if text in RESERVED_WORDS:
        if allow_reserved_as_type:
            return Token(RESERVED_WORDS[text], text, pos)
        else:
            raise LexicalError(pos, f"Reserved word '{text}' cannot be used as identifier")

    # Reserved keyword prefix protection
    for kw in RESERVED_WORDS:
        if text.startswith(kw) and text != kw:
            # Allow numbers or underscores after a keyword
            if text[len(kw):] and not text[len(kw):].isalnum() and text[len(kw):] != "_":
                raise LexicalError(pos, f"Illegal continuation after reserved word '{kw}' in '{text}'")
        if kw.startswith(text) and text != kw:
            raise LexicalError(pos, f"Incomplete reserved keyword '{text}'")
    return Token(TK_IDENTIFIER, text, pos)
