from lexer.reserved_words import RESERVED_WORDS, is_prefix
from lexer.tokens import Token
from lexer.delimiters import idnt_delim, id_sym
from lexer.errors import LexicalError

MAX_IDENTIFIER_LENGTH = 31

def scan_identifier(lexer, allow_reserved_as_type=True):
    pos = lexer.pos.copy()
    text = ""

    if not lexer.current_char.isalpha():
        raise LexicalError(pos, f"Invalid start of identifier '{lexer.current_char}'")

    while lexer.current_char is not None and lexer.current_char in id_sym:
        if len(text) < MAX_IDENTIFIER_LENGTH:
            text += lexer.current_char
        lexer.advance()

    if lexer.current_char is not None and lexer.current_char not in idnt_delim:
        raise LexicalError(pos, f"Invalid character '{lexer.current_char}' in identifier '{text}'")

    if text in RESERVED_WORDS:
        if allow_reserved_as_type:
            return Token(RESERVED_WORDS[text], text, pos)
        else:
            raise LexicalError(pos, f"Reserved word '{text}' cannot be used as identifier")

    for kw in RESERVED_WORDS:
        if text.startswith(kw) and text != kw:
            raise LexicalError(pos, f"Illegal continuation after reserved word '{kw}' in '{text}'")

    if is_prefix(text):
        raise LexicalError(pos, f"Incomplete reserved keyword '{text}'")

    return Token("TK_IDENTIFIER", text, pos)
