from backend.lexer.tokens import Token, TK_LIT_STRING
from backend.lexer.errors import LexicalError

def scan_string(lexer):
    pos = lexer.pos.copy()
    string_val = ""
    lexer.advance()

    while True:
        if lexer.current_char is None or lexer.current_char == "\n":
            raise LexicalError(pos, "Unterminated string literal")

        if lexer.current_char == "\\":
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
            else:
                raise LexicalError(pos, f"Invalid escape sequence '\\{lexer.current_char}'")
            continue

        if lexer.current_char == '"':
            lexer.advance()
            break

        string_val += lexer.current_char
        lexer.advance()

    while lexer.current_char == "&":
        lexer.advance()
        if lexer.current_char != '"':
            raise LexicalError(pos, "String concatenation must be followed by another string literal")
        next_token = scan_string(lexer)
        string_val += next_token.value[1:-1]

    return Token(TK_LIT_STRING, f"\"{string_val}\"", pos)
