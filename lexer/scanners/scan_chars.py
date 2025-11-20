from lexer.tokens import Token, TK_LIT_CHAR
from lexer.errors import LexicalError

def scan_char(lexer):
    pos = lexer.pos.copy()

    if lexer.current_char != "'":
        raise LexicalError(pos, "Expected opening single quote for char literal")

    lexer.advance()

    if lexer.current_char is None:
        raise LexicalError(pos, "Unterminated char literal")

    ch = ""
    if lexer.current_char == "\\":
        lexer.advance()
        if lexer.current_char is None:
            raise LexicalError(pos, "Unterminated escape sequence in char literal")

        if lexer.current_char == "n":
            ch = "\n"
        elif lexer.current_char == "t":
            ch = "\t"
        elif lexer.current_char == "'":
            ch = "'"
        elif lexer.current_char == "\\":
            ch = "\\"
        else:
            raise LexicalError(pos, f"Unknown escape sequence '\\{lexer.current_char}'")
        lexer.advance()
    else:
        ch = lexer.current_char
        lexer.advance()

    if lexer.current_char != "'":
        raise LexicalError(pos, "Unterminated char literal or too many characters")
    
    lexer.advance()
    return Token(TK_LIT_CHAR, ch, pos)
