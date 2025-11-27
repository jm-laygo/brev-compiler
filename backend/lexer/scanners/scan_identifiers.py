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
            text += lexer.current_char
            lexer.advance()
            continue
        if lexer.current_char in idnt_delim or lexer.current_char == "\n":
            break
        raise LexicalError(pos, f"Invalid character '{lexer.current_char}' in identifier '{text}'")

    # Check for max length
    if len(text) > MAX_IDENTIFIER_LENGTH:
        raise LexicalError(pos, f"Identifier '{text}' exceeds maximum length of {MAX_IDENTIFIER_LENGTH} characters")

    # Reserved word handling
    if text in RESERVED_WORDS:
        if allow_reserved_as_type:
            return Token(RESERVED_WORDS[text], text, pos)
        else:
            raise LexicalError(pos, f"Reserved word '{text}' cannot be used as identifier")

    return Token(TK_IDENTIFIER, text, pos)
