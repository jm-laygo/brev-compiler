from backend.errors import LexicalError

from backend.tokens import (
    Token,
    TK_OP_TILDE,
    TK_OP_EQ,
    TK_OP_ASSIGN,
    TK_OP_INC,
    TK_OP_PLUS_EQ,
    TK_OP_PLUS,
    TK_OP_DEC,
    TK_OP_MINUS_EQ,
    TK_OP_MINUS,
    TK_OP_POW_EQ,
    TK_OP_POW,
    TK_OP_MUL_EQ,
    TK_OP_MUL,
    TK_OP_DIV_EQ,
    TK_OP_DIV,
    TK_OP_MOD_EQ,
    TK_OP_MOD,
    TK_OP_NOT_EQ,
    TK_OP_NOT,
    TK_OP_AND,
    TK_OP_CONCAT,
    TK_OP_OR,
    TK_OP_LTE,
    TK_OP_LT,
    TK_OP_GTE,
    TK_OP_GT,
)

from backend.delimiters import (
    format_expected_delims,
    delim2,
    delim3,
    delim4,
    delim5,
    delim12,
    space,
    newline,
    tab,
    op_par,
    cl_par,
    cl_brc,
    cl_bra,
    semicolon,
    comma,
    ALPHABET,
    ALPHA_DIG,
)


def acceptOperator(
    lexer,
    tokenList,
    errorList,
    tokenType,
    operatorLexeme,
    startingPosition,
    allowedDelimiters
):
    # check delimiter
    if isinstance(allowedDelimiters, str):
        allowedDelimiters = {allowedDelimiters}

    currentCharacter = lexer.currentCharacter
    expectedDelimiters = format_expected_delims(allowedDelimiters)

    if currentCharacter is None and None not in allowedDelimiters:
        lexicalError = LexicalError(
            startingPosition,
            f"Missing delimiter after operator '{operatorLexeme}'. Expected: {expectedDelimiters}"
        )

        errorList.extend([lexicalError])
        return True

    if currentCharacter is not None and currentCharacter not in allowedDelimiters:
        lexicalError = LexicalError(
            startingPosition,
            f"Invalid delimiter {repr(currentCharacter)} after operator '{operatorLexeme}'. Expected: {expectedDelimiters}"
        )

        errorList.extend([lexicalError])
        return True

    operatorToken = Token(
        tokenType,
        operatorLexeme,
        startingPosition
    )

    tokenList.extend([operatorToken])
    return True

def scanOperator(lexer, tokenList, errorList):
    currentCharacter = lexer.currentCharacter

    # no char to scan
    if currentCharacter is None:
        return False

    startingPosition = lexer.currentPosition.copy()

    # tilde
    if currentCharacter == "~":
        lexer.advance()

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_TILDE,
            "~",
            startingPosition,
            delim3
        )

    # assign or equal
    if currentCharacter == "=":
        lexer.advance()

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_EQ,
                "==",
                startingPosition,
                delim5
            )

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_ASSIGN,
            "=",
            startingPosition,
            delim4
        )

    # plus
    if currentCharacter == "+":
        lexer.advance()

        if lexer.currentCharacter == "+":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_INC,
                "++",
                startingPosition,
                delim2
            )

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_PLUS_EQ,
                "+=",
                startingPosition,
                delim3
            )

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_PLUS,
            "+",
            startingPosition,
            delim3
        )

    # minus
    if currentCharacter == "-":
        lexer.advance()

        if lexer.currentCharacter == "-":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_DEC,
                "--",
                startingPosition,
                delim2
            )

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_MINUS_EQ,
                "-=",
                startingPosition,
                delim3
            )

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_MINUS,
            "-",
            startingPosition,
            delim3
        )

    # multiply or power
    if currentCharacter == "*":
        lexer.advance()

        if lexer.currentCharacter == "*":
            lexer.advance()

            if lexer.currentCharacter == "=":
                lexer.advance()

                return acceptOperator(
                    lexer,
                    tokenList,
                    errorList,
                    TK_OP_POW_EQ,
                    "**=",
                    startingPosition,
                    delim3
                )

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_POW,
                "**",
                startingPosition,
                delim3
            )

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_MUL_EQ,
                "*=",
                startingPosition,
                delim3
            )

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_MUL,
            "*",
            startingPosition,
            delim3
        )

    # divide
    if currentCharacter == "/":
        lexer.advance()

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_DIV_EQ,
                "/=",
                startingPosition,
                delim3
            )

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_DIV,
            "/",
            startingPosition,
            delim3
        )

    # modulo
    if currentCharacter == "%":
        lexer.advance()

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_MOD_EQ,
                "%=",
                startingPosition,
                delim3
            )

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_MOD,
            "%",
            startingPosition,
            delim3
        )

    # not or not equal
    if currentCharacter == "!":
        lexer.advance()

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_NOT_EQ,
                "!=",
                startingPosition,
                delim5
            )

        if lexer.currentCharacter == "!":
            lexer.advance()

            notOperatorDelimiters = (
                {
                    None,
                    space,
                    newline,
                    tab,
                    op_par,
                    cl_par,
                    cl_brc,
                    cl_bra,
                    semicolon,
                    comma,
                    "~",
                    '"',
                    "'",
                    "!",
                }
                | set(ALPHABET)
                | set(ALPHA_DIG)
            )

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_NOT,
                "!!",
                startingPosition,
                notOperatorDelimiters
            )

        lexicalError = LexicalError(
            startingPosition,
            "Invalid operator '!'. Use '!!' for NOT, or '!=' for NOT-EQUAL."
        )

        errorList.extend([lexicalError])
        return True

    # and or concat
    if currentCharacter == "&":
        if lexer.peek() == "&":
            lexer.advance()
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_AND,
                "&&",
                startingPosition,
                delim3
            )

        lexer.advance()

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_CONCAT,
            "&",
            startingPosition,
            delim12 | {op_par}
        )

    # or
    if currentCharacter == "|":
        if lexer.peek() == "|":
            lexer.advance()
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_OR,
                "||",
                startingPosition,
                delim3
            )

        lexer.advance()

        lexicalError = LexicalError(
            startingPosition,
            "Invalid operator '|'. Use '||' for OR."
        )

        errorList.extend([lexicalError])
        return True

    # less than
    if currentCharacter == "<":
        lexer.advance()

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_LTE,
                "<=",
                startingPosition,
                delim3
            )

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_LT,
            "<",
            startingPosition,
            delim3
        )

    # greater than
    if currentCharacter == ">":
        lexer.advance()

        if lexer.currentCharacter == "=":
            lexer.advance()

            return acceptOperator(
                lexer,
                tokenList,
                errorList,
                TK_OP_GTE,
                ">=",
                startingPosition,
                delim3
            )

        return acceptOperator(
            lexer,
            tokenList,
            errorList,
            TK_OP_GT,
            ">",
            startingPosition,
            delim3
        )

    return False