from backend.lexer.reserved_words import RESERVED_WORDS
from backend.lexer.tokens import Token, TK_IDENTIFIER
from backend.lexer.delimiters import idnt_delim, id_sym
from backend.lexer.errors import LexicalError

MAX_IDENTIFIER_LENGTH = 31

def scan_identifier(lexer, allow_reserved_as_type=True):
    pos = lexer.pos.copy()
    text = ""

    if not lexer.current_char or not lexer.current_char.isalpha():
        raise LexicalError(pos, f"Invalid start of identifier '{lexer.current_char}'")

    while lexer.current_char is not None:
        if lexer.current_char in id_sym:
            if len(text) < MAX_IDENTIFIER_LENGTH:
                text += lexer.current_char
            lexer.advance()
            continue
        if lexer.current_char in idnt_delim or lexer.current_char == "\n":
            break
        raise LexicalError(pos, f"Invalid character '{lexer.current_char}' in identifier '{text}'")
    
    if text in RESERVED_WORDS:
        if allow_reserved_as_type:
            return Token(RESERVED_WORDS[text], text, pos)
        else:
            raise LexicalError(pos, f"Reserved word '{text}' cannot be used as identifier")
    
    for kw in RESERVED_WORDS:
        if text.startswith(kw) and text != kw:
            nxt = lexer.current_char
            if nxt is not None and nxt.isalpha():
                raise LexicalError(pos, f"Illegal continuation after reserved word '{kw}' in '{text}'")
            
    if lexer.current_char is not None and lexer.current_char not in idnt_delim and lexer.current_char != "\n":
        raise LexicalError(pos, f"Invalid character '{lexer.current_char}' in identifier '{text}'")

    return Token(TK_IDENTIFIER, text, pos)
