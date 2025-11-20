from lexer.tokens import Token, TK_CONST
from lexer.errors import LexicalError
from lexer.reserved_words import RESERVED_WORDS

def scan_constant(lexer):
    pos = lexer.pos.copy()
    lexeme = ""
    while lexer.current_char is not None and lexer.current_char.isalpha():
        lexeme += lexer.current_char
        lexer.advance()

    if lexeme != "sacred":
        raise LexicalError(pos, f"Unexpected keyword {lexeme}")
    
    return Token(TK_CONST, lexeme, pos)
