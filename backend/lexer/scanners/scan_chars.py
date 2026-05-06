from backend.tokens import Token, TK_LIT_CHAR
from backend.errors import LexicalError
from backend.delimiters import chr_delim as characterDelimiters
from backend.delimiters import formatExpectedDelimiters


def acceptCharacterLiteral(
    lexer,
    tokenList,
    errorList,
    startingPosition,
    characterValue,
    displayedCharacterValue,
    allowedDelimiters
):
    currentCharacter = lexer.currentCharacter
    expectedDelimiters = formatExpectedDelimiters(allowedDelimiters)

    if currentCharacter is None and None not in allowedDelimiters:
        errorList.append(
            LexicalError(
                startingPosition,
                f"Missing delimiter after char literal {displayedCharacterValue}. Expected: {expectedDelimiters}"
            )
        )
        return True

    if currentCharacter is not None and currentCharacter not in allowedDelimiters:
        errorList.append(
            LexicalError(
                startingPosition,
                f"Invalid delimiter {repr(currentCharacter)} after char literal {displayedCharacterValue}. Expected: {expectedDelimiters}"
            )
        )
        return True

    tokenList.append(
        Token(
            TK_LIT_CHAR,
            characterValue,
            startingPosition
        )
    )

    return True


def recoverCharacterLiteral(lexer):
    while lexer.currentCharacter is not None and lexer.currentCharacter not in {"'", "\n"}:
        lexer.advance()

    if lexer.currentCharacter == "'":
        lexer.advance()


def scanCharacter(lexer, tokenList, errorList):
    if lexer.currentCharacter != "'":
        return False

    startingPosition = lexer.currentPosition.copy()
    lexer.advance()

    if lexer.currentCharacter is None:
        lexicalError = LexicalError(
            startingPosition,
            "Unterminated char literal"
        )

        errorList.extend([lexicalError])
        return True

    if lexer.currentCharacter == "\n":
        lexicalError = LexicalError(
            startingPosition,
            "Unterminated char literal (newline in char literal)"
        )

        errorList.extend([lexicalError])
        return True

    if lexer.currentCharacter == "'":
        lexer.advance()

        errorList.append(
            LexicalError(
                startingPosition,
                "Empty char literal is invalid"
            )
        )

        return True

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
            '"': '"',
            "\\": "\\",
        }

        escapeCharacter = lexer.currentCharacter

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
        characterValue = lexer.currentCharacter
        lexer.advance()

    if lexer.currentCharacter != "'":
        lexicalError = LexicalError(
            startingPosition,
            "Char literal must contain exactly one character"
        )

        errorList.extend([lexicalError])
        recoverCharacterLiteral(lexer)

        return True

    lexer.advance()

    if ord(characterValue) > 127:
        lexicalError = LexicalError(
            startingPosition,
            f"Non-ASCII character '{characterValue}' is not allowed in char literal"
        )

        errorList.extend([lexicalError])
        return True

    if characterValue == "\n":
        displayedCharacter = "\\n"

    elif characterValue == "\t":
        displayedCharacter = "\\t"

    elif characterValue == "\0":
        displayedCharacter = "\\0"

    elif characterValue == "'":
        displayedCharacter = "\\'"

    elif characterValue == '"':
        displayedCharacter = '\\"'

    elif characterValue == "\\":
        displayedCharacter = "\\\\"

    else:
        displayedCharacter = characterValue

    return acceptCharacterLiteral(
        lexer,
        tokenList,
        errorList,
        startingPosition,
        characterValue,
        f"'{displayedCharacter}'",
        characterDelimiters
    )