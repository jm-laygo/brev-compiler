from backend.tokens import (
    Token,
    TK_SYM_OPBRACE,
    TK_SYM_CLSBRACE,
    TK_SYM_OPPAREN,
    TK_SYM_CLSPAREN,
    TK_SYM_OPBRACK,
    TK_SYM_CLSBRACK,
    TK_SYM_SEMICOL,
    TK_SYM_COMMA,
    TK_SYM_COLON,
    TK_SYM_DOT,
    TK_SYM_TERNARY,
)

symbolMap = {
    "{": (TK_SYM_OPBRACE, "{"),
    "}": (TK_SYM_CLSBRACE, "}"),
    "(": (TK_SYM_OPPAREN, "("),
    ")": (TK_SYM_CLSPAREN, ")"),
    "[": (TK_SYM_OPBRACK, "["),
    "]": (TK_SYM_CLSBRACK, "]"),
    ";": (TK_SYM_SEMICOL, ";"),
    ",": (TK_SYM_COMMA, ","),
    ":": (TK_SYM_COLON, ":"),
    ".": (TK_SYM_DOT, "."),
    "?": (TK_SYM_TERNARY, "?"),
}

def scanSymbol(lexer, tokenList, errorList):
    currentCharacter = lexer.currentCharacter

    # no char to scan
    if currentCharacter is None:
        return False

    startingPosition = lexer.currentPosition.copy()

    # known symbol
    if currentCharacter in symbolMap:
        tokenType, symbolLexeme = symbolMap[currentCharacter]

        lexer.advance()

        symbolToken = Token(
            tokenType,
            symbolLexeme,
            startingPosition
        )

        tokenList.extend([symbolToken])
        return True

    return False