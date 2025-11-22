from backend.lexer.tokens import Token, TK_LIT_CHAR
from backend.lexer.errors import LexicalError

def scan_char(lexer):
    pos = lexer.pos.copy()
    if lexer.current_char != "'":
        raise LexicalError(pos, "Expected opening single quote for char literal")

    lexer.advance()

    if lexer.current_char is None:
        raise LexicalError(pos, "Unterminated char literal (found end-of-file)")
    if lexer.current_char == "'":
        raise LexicalError(pos, "Empty char literal '' is not allowed")

    if lexer.current_char == "\\":
        lexer.advance()
        if lexer.current_char is None:
            raise LexicalError(pos, "Unterminated escape sequence in char literal")

        escape_map = {
            "n": "\n",
            "t": "\t",
            "'": "'",
            "\\": "\\",
        }

        if lexer.current_char not in escape_map:
            raise LexicalError(pos, f"Unknown escape sequence '\\{lexer.current_char}'")

        ch = escape_map[lexer.current_char]
        lexer.advance()

    else:
        ch = lexer.current_char
        lexer.advance()
    if lexer.current_char != "'":
        raise LexicalError(
            pos,
            "Char literal must contain exactly one character (or valid escape)"
        )

    lexer.advance()
    return Token(TK_LIT_CHAR, ch, pos)
