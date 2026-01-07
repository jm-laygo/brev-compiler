from backend.lexer.tokens import Token, TK_IDENTIFIER
from backend.lexer.reserved_words import RESERVED_WORDS
from backend.lexer.delimiters import idnt_delim
from backend.lexer.errors import LexicalError

MAX_IDENTIFIER_LENGTH = 31

def scan_identifier(lexer, allow_reserved_as_keyword=True):
    pos = lexer.pos.copy()
    text = ""

    if lexer.current_char is None or not lexer.current_char.isalpha():
        raise LexicalError(pos, f"Invalid start of identifier '{lexer.current_char}'")

    text += lexer.current_char
    lexer.advance()

    while lexer.current_char is not None:
        ch = lexer.current_char
        if ch.isalnum() or ch == "_":
            text += ch
            lexer.advance()
            continue
        if ch in idnt_delim:
            break
        raise LexicalError(pos, f"Invalid character '{ch}' in identifier '{text}'")

    if len(text) > MAX_IDENTIFIER_LENGTH:
        raise LexicalError(pos, f"Identifier '{text}' exceeds maximum length")

    if lexer.current_char is None or lexer.current_char not in idnt_delim:
        raise LexicalError(pos, f"Missing delimiter after identifier '{text}'")

    # Reserved word handling:
    if text in RESERVED_WORDS:
        if allow_reserved_as_keyword:
            return Token(RESERVED_WORDS[text], text, pos)  # valid keyword usage
        else:
            raise LexicalError(pos, f"Reserved word '{text}' cannot be used as identifier")

    # Normal identifier
    return Token(TK_IDENTIFIER, text, pos)
