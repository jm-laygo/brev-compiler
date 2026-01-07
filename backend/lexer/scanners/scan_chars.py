from backend.lexer.tokens import Token, TK_LIT_CHAR
from backend.lexer.errors import LexicalError
from backend.lexer.delimiters import chr_delim

def scan_char(lexer):
    pos = lexer.pos.copy()

    # must start with single quote
    if lexer.current_char != "'":
        raise LexicalError(pos, "Char literal must start with single quote (')")

    lexer.advance()

    if lexer.current_char is None:
        raise LexicalError(pos, "Unterminated char literal")

    # check if it's empty char ''
    if lexer.current_char == "'":
        ch = ""  # empty char is valid
        lexer.advance()
    else:
        # handle escape sequences
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
            raise LexicalError(pos, "Char literal must end with single quote (')")

        lexer.advance()

    if lexer.current_char is not None and lexer.current_char not in chr_delim:
        raise LexicalError(
            pos,
            f"Invalid character '{lexer.current_char}' after char literal"
        )

    return Token(TK_LIT_CHAR, f"'{ch}'", pos)
