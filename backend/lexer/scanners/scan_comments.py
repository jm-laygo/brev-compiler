from backend.tokens import Token, TK_COMMENT, TK_COMMENT_BLOCK
from backend.errors import LexicalError


def scanComment(lexer, tokenList, errorList):
    # not a comment
    if lexer.currentCharacter != "/" or lexer.peek() not in ("/", "*"):
        return False

    startingPosition = lexer.currentPosition.copy()

    # line comment
    if lexer.peek() == "/":
        commentLexeme = "//"

        lexer.advance()
        lexer.advance()

        # read until newline
        while lexer.currentCharacter is not None and lexer.currentCharacter != "\n":
            commentLexeme = commentLexeme + lexer.currentCharacter
            lexer.advance()

        commentToken = Token(
            TK_COMMENT,
            commentLexeme,
            startingPosition
        )

        tokenList.extend([commentToken])
        return True

    # block comment
    commentLexeme = "/*"

    lexer.advance()
    lexer.advance()

    while True:
        # no closing block
        if lexer.currentCharacter is None:
            lexicalError = LexicalError(
                startingPosition,
                "Unterminated block comment"
            )

            errorList.extend([lexicalError])
            return True

        # end of block
        if lexer.currentCharacter == "*" and lexer.peek() == "/":
            commentLexeme = commentLexeme + "*/"

            lexer.advance()
            lexer.advance()

            break

        # nested block not allowed
        if lexer.currentCharacter == "/" and lexer.peek() == "*":
            lexicalError = LexicalError(
                lexer.currentPosition.copy(),
                "Nested block comments are not allowed"
            )

            errorList.extend([lexicalError])
            commentLexeme = commentLexeme + lexer.currentCharacter
            lexer.advance()

            continue

        commentLexeme = commentLexeme + lexer.currentCharacter
        lexer.advance()

    blockCommentToken = Token(
        TK_COMMENT_BLOCK,
        commentLexeme,
        startingPosition
    )

    tokenList.extend([blockCommentToken])
    return True