from backend.tokens import Token, TK_LIT_STRING
from backend.errors import LexicalError
from backend.delimiters import str_delim as stringDelimiters
from backend.delimiters import format_expected_delims


def acceptStringLiteral(
    lexer,
    tokenList,
    errorList,
    startingPosition,
    stringValue,
    allowedDelimiters
):
    # check delimiter
    currentCharacter = lexer.currentCharacter
    expectedDelimiters = format_expected_delims(allowedDelimiters)

    if currentCharacter is None and None not in allowedDelimiters:
        lexicalError = LexicalError(
            startingPosition,
            f"Missing delimiter after string literal. Expected: {expectedDelimiters}"
        )

        errorList.extend([lexicalError])
        return True

    if currentCharacter is not None and currentCharacter not in allowedDelimiters:
        lexicalError = LexicalError(
            startingPosition,
            f"Invalid delimiter {repr(currentCharacter)} after string literal. Expected: {expectedDelimiters}"
        )

        errorList.extend([lexicalError])
        return True

    stringToken = Token(
        TK_LIT_STRING,
        stringValue,
        startingPosition
    )

    tokenList.extend([stringToken])
    return True

def recoverStringLiteral(lexer):
    # skip invalid string
    while lexer.currentCharacter is not None and lexer.currentCharacter not in {'"', "\n"}:
        lexer.advance()

    if lexer.currentCharacter == '"':
        lexer.advance()

def scanString(lexer, tokenList, errorList):
    # must start with quote
    if lexer.currentCharacter != '"':
        return False

    startingPosition = lexer.currentPosition.copy()
    stringValue = ""

    lexer.advance()

    # read string
    while lexer.currentCharacter is not None:
        currentCharacter = lexer.currentCharacter

        # newline not allowed
        if currentCharacter == "\n":
            lexicalError = LexicalError(
                startingPosition,
                "Unterminated string literal"
            )

            errorList.extend([lexicalError])
            return True

        # escape char
        if currentCharacter == "\\":
            lexer.advance()
            escapeCharacter = lexer.currentCharacter

            if escapeCharacter is None:
                lexicalError = LexicalError(
                    startingPosition,
                    "Unterminated escape sequence"
                )

                errorList.extend([lexicalError])
                return True

            if escapeCharacter == "n":
                stringValue += "\n"

            elif escapeCharacter == "t":
                stringValue += "\t"

            elif escapeCharacter == "0":
                stringValue += "\0"

            elif escapeCharacter == "\\":
                stringValue += "\\"

            elif escapeCharacter == '"':
                stringValue += '"'

            else:
                lexicalError = LexicalError(
                    startingPosition,
                    f"Invalid escape sequence '\\{escapeCharacter}'"
                )

                errorList.extend([lexicalError])
                lexer.advance()
                recoverStringLiteral(lexer)

                return True

            lexer.advance()
            continue

        # closing quote
        if currentCharacter == '"':
            lexer.advance()

            return acceptStringLiteral(
                lexer,
                tokenList,
                errorList,
                startingPosition,
                stringValue,
                stringDelimiters
            )

        stringValue += currentCharacter
        lexer.advance()

    # no closing quote
    lexicalError = LexicalError(
        startingPosition,
        "Unterminated string literal"
    )

    errorList.extend([lexicalError])
    return True