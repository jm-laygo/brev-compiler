from backend.lexer.tokens import Token, TK_LIT_BOOL
from backend.lexer.errors import LexicalError
from backend.lexer.delimiters import bool_delim

BOOLEAN_LITERALS = ["holy", "unholy"]

def scan_booleans(lexer):
    pos = lexer.pos.copy()
    value_str = ""

    # read alphabetic characters
    while lexer.current_char is not None and lexer.current_char.isalpha():
        value_str += lexer.current_char
        lexer.advance()

    # validate literal
    if value_str not in BOOLEAN_LITERALS:
        raise LexicalError(pos, f"Invalid boolean literal '{value_str}'")

    # delimiter is required
    if lexer.current_char is None:
        raise LexicalError(pos, f"Missing delimiter after boolean literal '{value_str}'")

    if lexer.current_char not in bool_delim:
        raise LexicalError(
            pos,
            f"Invalid delimiter '{lexer.current_char}' after boolean literal '{value_str}'"
        )

    return Token(TK_LIT_BOOL, value_str, pos)
