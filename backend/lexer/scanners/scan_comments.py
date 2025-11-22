from backend.lexer.tokens import Token, TK_COMMENT, TK_COMMENT_BLOCK
from backend.lexer.errors import LexicalError

def scan_comment(lexer):
    pos = lexer.pos.copy()

    if lexer.current_char == "/" and lexer.peek() == "/":
        start_pos = lexer.pos.copy()
        lexeme = "//"
        lexer.advance()
        lexer.advance()
        while lexer.current_char is not None and lexer.current_char != "\n":
            lexeme += lexer.current_char
            lexer.advance()
        return Token(TK_COMMENT, lexeme, start_pos)
    if lexer.current_char == "/" and lexer.peek() == "*":
        start_pos = lexer.pos.copy()
        lexeme = "/*"
        lexer.advance()
        lexer.advance()
        while True:
            if lexer.current_char is None:
                raise LexicalError(pos, "Unterminated block comment")
            if lexer.current_char == "*" and lexer.peek() == "/":
                lexeme += "*"
                lexer.advance()
                lexeme += "/"
                lexer.advance()
                break
            lexeme += lexer.current_char
            lexer.advance()
        return Token(TK_COMMENT_BLOCK, lexeme, start_pos)
    
    raise LexicalError(pos, "Not a comment")
