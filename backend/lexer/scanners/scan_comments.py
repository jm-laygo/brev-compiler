from backend.tokens import Token, TK_COMMENT, TK_COMMENT_BLOCK
from backend.errors import LexicalError

def scan_comment(lexer, tokens, errors):
    if lexer.current_char != "/" or lexer.peek() not in ("/", "*"):
        return False

    start_pos = lexer.pos.copy()

    if lexer.peek() == "/":
        lexeme = "//"
        lexer.advance()
        lexer.advance()

        while lexer.current_char is not None and lexer.current_char != "\n":
            lexeme += lexer.current_char
            lexer.advance()

        tokens.append(Token(TK_COMMENT, lexeme, start_pos))
        return True

    lexeme = "/*"
    lexer.advance()
    lexer.advance()

    while True:
        if lexer.current_char is None:
            errors.append(LexicalError(start_pos, "Unterminated block comment"))
            return True

        # Detect end of block comment
        if lexer.current_char == "*" and lexer.peek() == "/":
            lexeme += "*/"
            lexer.advance()
            lexer.advance()
            break

        # Nested block comment start (disallowed)
        if lexer.current_char == "/" and lexer.peek() == "*":
            errors.append(LexicalError(lexer.pos.copy(), "Nested block comments are not allowed"))
            lexeme += lexer.current_char
            lexer.advance()
            continue

        lexeme += lexer.current_char
        lexer.advance()

    tokens.append(Token(TK_COMMENT_BLOCK, lexeme, start_pos))
    return True