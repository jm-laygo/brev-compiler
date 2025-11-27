from backend.lexer.tokens import Token, TK_COMMENT, TK_COMMENT_BLOCK
from backend.lexer.errors import LexicalError

def scan_comment(lexer):
    start_pos = lexer.pos.copy()

    # SINGLELINE COMMENT
    if lexer.current_char == "/" and lexer.peek() == "/":
        lexeme = "//"
        lexer.advance()
        lexer.advance()
        while lexer.current_char is not None and lexer.current_char != "\n":
            lexeme += lexer.current_char
            lexer.advance()
        return Token(TK_COMMENT, lexeme, start_pos)

    # MULTILINE COMMENT
    if lexer.current_char == "/" and lexer.peek() == "*":
        lexeme = "/*"
        lexer.advance()
        lexer.advance()

        while True:
            if lexer.current_char is None:
                raise LexicalError(start_pos, "Unterminated block comment")

            if lexer.current_char == "/" and lexer.peek() == "*":
                err_pos = lexer.pos.copy()
                raise LexicalError(err_pos, "Nested block comments are not allowed")
            
            if lexer.current_char == "*" and lexer.peek() == "/":
                lexeme += "*"
                lexer.advance()
                lexeme += "/"
                lexer.advance()
                break

            lexeme += lexer.current_char
            lexer.advance()

        return Token(TK_COMMENT_BLOCK, lexeme, start_pos)

    raise LexicalError(lexer.pos.copy(), "Not a comment")
