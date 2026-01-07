from backend.lexer.tokens import Token, TK_LIT_STRING
from backend.lexer.errors import LexicalError
from backend.lexer.delimiters import str_delim

def scan_string(lexer):
    pos = lexer.pos.copy()
    string_val = ""

    lexer.advance()

    while True:
        ch = lexer.current_char

        if ch is None or ch == "\n":
            raise LexicalError(pos, "Unterminated string literal")

        if ch == "\\":
            lexer.advance()
            if lexer.current_char in ["n", "t", "\\", '"']:
                if lexer.current_char == "n":
                    string_val += "\n"
                elif lexer.current_char == "t":
                    string_val += "\t"
                elif lexer.current_char == "\\":
                    string_val += "\\"
                elif lexer.current_char == '"':
                    string_val += '"'
                lexer.advance()
                continue
            else:
                raise LexicalError(pos, f"Invalid escape sequence '\\{lexer.current_char}'")

        if ch == '"':
            lexer.advance()
            break

        string_val += ch
        lexer.advance()

    while lexer.current_char == "&":
        lexer.advance()
        if lexer.current_char != '"':
            raise LexicalError(
                pos,
                "String concatenation operator '&' must be followed by another string literal"
            )
        next_token = scan_string(lexer)
        string_val += next_token.value[1:-1]

    if lexer.current_char is None:
        raise LexicalError(pos, "Missing delimiter after string literal")

    if lexer.current_char not in str_delim:
        raise LexicalError(
            pos,
            f"Invalid character '{lexer.current_char}' after string literal"
        )

    return Token(TK_LIT_STRING, f"\"{string_val}\"", pos)
