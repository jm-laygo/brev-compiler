from backend.tokens import Token, TK_LIT_CHAR
from backend.errors import LexicalError
from backend.delimiters import chr_delim as characterDelimiters
from backend.delimiters import format_expected_delims

def acceptCharacterLiteral(
    lexer,
    tokenList,
    errorList,
    startingPosition,
    displayedCharacterValue,
    allowedDelimiters
):
    # check delimiter
    currentCharacter = lexer.currentCharacter
    expectedDelimiters = format_expected_delims(allowedDelimiters)

    if currentCharacter is None and None not in allowedDelimiters:
        lexicalError = LexicalError(
            startingPosition,
            f"Missing delimiter after char literal {displayedCharacterValue}. Expected: {expectedDelimiters}"
        )

        errorList.extend([lexicalError])
        return True

    if currentCharacter is not None and currentCharacter not in allowedDelimiters:
        lexicalError = LexicalError(
            startingPosition,
            f"Invalid delimiter {repr(currentCharacter)} after char literal {displayedCharacterValue}. Expected: {expectedDelimiters}"
        )

        errorList.extend([lexicalError])
        return True

    characterToken = Token(
        TK_LIT_CHAR,
        displayedCharacterValue,
        startingPosition
    )

    tokenList.extend([characterToken])
    return True

def recoverCharacterLiteral(lexer):
    # skip invalid char
    while lexer.currentCharacter is not None and lexer.currentCharacter not in {"'", "\n"}:
        lexer.advance()

    if lexer.currentCharacter == "'":
        lexer.advance()

def scanCharacter(lexer, tokenList, errorList):
    # must start with quote
    if lexer.currentCharacter != "'":
        return False

    startingPosition = lexer.currentPosition.copy()
    lexer.advance()

    # missing closing quote
    if lexer.currentCharacter is None:
        lexicalError = LexicalError(
            startingPosition,
            "Unterminated char literal"
        )

        errorList.extend([lexicalError])
        return True

    # newline not allowed
    if lexer.currentCharacter == "\n":
        lexicalError = LexicalError(
            startingPosition,
            "Unterminated char literal (newline in char literal)"
        )

        errorList.extend([lexicalError])
        return True

    # empty char
    if lexer.currentCharacter == "'":
        lexer.advance()

        return acceptCharacterLiteral(
            lexer,
            tokenList,
            errorList,
            startingPosition,
            "''",
            characterDelimiters
        )

    # escape char
    if lexer.currentCharacter == "\\":
        lexer.advance()

        if lexer.currentCharacter is None:
            lexicalError = LexicalError(
                startingPosition,
                "Unterminated escape sequence in char literal"
            )

            errorList.extend([lexicalError])
            return True

        escapeSequenceMap = {
            "n": "\n",
            "t": "\t",
            "0": "\0",
            "'": "'",
            "\\": "\\",
        }

        escapeCharacter = lexer.currentCharacter

        # invalid escape
        if escapeCharacter not in escapeSequenceMap:
            lexicalError = LexicalError(
                startingPosition,
                f"Unknown escape sequence '\\{escapeCharacter}'"
            )

            errorList.extend([lexicalError])
            lexer.advance()
            recoverCharacterLiteral(lexer)

            return True

        characterValue = escapeSequenceMap[escapeCharacter]
        lexer.advance()

    else:
        # normal char
        characterValue = lexer.currentCharacter
        lexer.advance()

    # one char only
    if lexer.currentCharacter != "'":
        lexicalError = LexicalError(
            startingPosition,
            "Char literal must contain exactly one character"
        )

        errorList.extend([lexicalError])
        recoverCharacterLiteral(lexer)

        return True

    lexer.advance()

    # ascii only
    if ord(characterValue) > 127:
        lexicalError = LexicalError(
            startingPosition,
            f"Non-ASCII character '{characterValue}' is not allowed in char literal"
        )

        errorList.extend([lexicalError])
        return True

    # display escape value
    if characterValue == "\n":
        displayedCharacter = "\\n"

    elif characterValue == "\t":
        displayedCharacter = "\\t"

    elif characterValue == "\0":
        displayedCharacter = "\\0"

    else:
        displayedCharacter = characterValue

    return acceptCharacterLiteral(
        lexer,
        tokenList,
        errorList,
        startingPosition,
        f"'{displayedCharacter}'",
        characterDelimiters
    )