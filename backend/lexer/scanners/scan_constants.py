from backend.lexer.tokens import Token, TK_CONST
from backend.lexer.errors import LexicalError
from backend.lexer.reserved_words import RESERVED_WORDS
from backend.lexer.delimiters import idnt_delim

def scan_constant(lexer):
    pos = lexer.pos.copy()
    lexeme = ""
    while lexer.current_char is not None and lexer.current_char.isalpha():
        lexeme += lexer.current_char
        lexer.advance()

    if lexeme != "sacred":
        raise LexicalError(pos, f"Unexpected keyword {lexeme}")

    if lexer.current_char is None:
        raise LexicalError(pos, f"Missing delimiter after constant '{lexeme}'")

    if lexer.current_char not in idnt_delim:
        if lexer.current_char == "\n":
            raise LexicalError(pos, f"Missing delimiter after constant '{lexeme}'")
        raise LexicalError(pos, f"Invalid character '{lexer.current_char}' after constant '{lexeme}'")

    return Token(TK_CONST, lexeme, pos)
