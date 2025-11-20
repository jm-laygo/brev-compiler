from lexer.tokens import Token, TK_LIT_BOOL
from lexer.errors import LexicalError

BOOLEAN_LITERALS = ["holy", "unholy"]

def scan_boolean_value(lexer):
    pos = lexer.pos.copy()
    value_str = ""
    
    while lexer.current_char is not None and lexer.current_char.isalpha():
        value_str += lexer.current_char
        lexer.advance()
    
    if value_str not in BOOLEAN_LITERALS:
        raise LexicalError(pos, f"Invalid boolean literal '{value_str}'")
    
    return Token(TK_LIT_BOOL, value_str, pos)
