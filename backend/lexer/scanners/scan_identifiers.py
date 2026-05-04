from backend.tokens import Token, TK_IDENTIFIER
from backend.errors import LexicalError
from backend.delimiters import (
    idnt_delim as identifierDelimiters,
    formatExpectedDelimiters,
    ALPHABET,
    ALPHA_DIG,
)

MAX_IDENTIFIER_LENGTH = 48


def scanIdentifier(lexer, tokenList, errorList):
    # no char to scan
    if lexer.currentCharacter is None:
        return False

    startingPosition = lexer.currentPosition.copy()

    # invalid first char
    if lexer.currentCharacter.isdigit() or lexer.currentCharacter == "_":
        invalidIdentifier = ""

        while lexer.currentCharacter is not None and (
            lexer.currentCharacter in ALPHA_DIG or lexer.currentCharacter == "_"
        ):
            invalidIdentifier = invalidIdentifier + lexer.currentCharacter
            lexer.advance()

        lexicalError = LexicalError(
            startingPosition,
            f"Invalid identifier starting with '{invalidIdentifier[0]}' '{invalidIdentifier}'"
        )

        errorList.extend([lexicalError])
        return True

    # must start with letter
    if lexer.currentCharacter not in ALPHABET:
        return False

    identifierName = ""

    # read identifier name
    while lexer.currentCharacter is not None and (
        lexer.currentCharacter in ALPHA_DIG or lexer.currentCharacter == "_"
    ):
        # max length check
        if len(identifierName) >= MAX_IDENTIFIER_LENGTH:
            while lexer.currentCharacter is not None and (
                lexer.currentCharacter in ALPHA_DIG or lexer.currentCharacter == "_"
            ):
                lexer.advance()

            lexicalError = LexicalError(
                startingPosition,
                f"Identifier too long (max {MAX_IDENTIFIER_LENGTH})."
            )

            errorList.extend([lexicalError])
            return True

        identifierName = identifierName + lexer.currentCharacter
        lexer.advance()

    # check delimiter
    currentCharacter = lexer.currentCharacter
    expectedDelimiters = formatExpectedDelimiters(identifierDelimiters)

    if currentCharacter is None and None not in identifierDelimiters:
        lexicalError = LexicalError(
            startingPosition,
            f"Missing delimiter after identifier '{identifierName}'. Expected: {expectedDelimiters}"
        )

        errorList.extend([lexicalError])
        return True

    if currentCharacter is not None and currentCharacter not in identifierDelimiters:
        lexicalError = LexicalError(
            startingPosition,
            f"Invalid delimiter {repr(currentCharacter)} after identifier '{identifierName}'. Expected: {expectedDelimiters}"
        )

        errorList.extend([lexicalError])
        return True

    identifierToken = Token(
        TK_IDENTIFIER,
        identifierName,
        startingPosition
    )

    tokenList.extend([identifierToken])
    return True