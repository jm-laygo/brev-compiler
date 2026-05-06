from backend.tokens import Token, TK_LIT_INT, TK_LIT_DECIMAL
from backend.errors import LexicalError
from backend.delimiters import int_decdelim as integerDecimalDelimiters
from backend.delimiters import formatExpectedDelimiters


MAX_INTEGER_DIGITS = 9
MAX_FRACTIONAL_DIGITS = 9


def acceptNumber(
    lexer,
    tokenList,
    errorList,
    startingPosition,
    numberText,
    allowedDelimiters,
    hasDecimalPoint
):
    # check delimiter
    if isinstance(allowedDelimiters, str):
        allowedDelimiters = {allowedDelimiters}

    currentCharacter = lexer.currentCharacter

    if currentCharacter == "\r":
        currentCharacter = "\n"

    expectedDelimiters = formatExpectedDelimiters(allowedDelimiters)

    if currentCharacter is None and None not in allowedDelimiters:
        errorList.append(
            LexicalError(
                startingPosition,
                f"Missing delimiter after number '{numberText}'. Expected: {expectedDelimiters}"
            )
        )
        return True

    if currentCharacter is not None and currentCharacter not in allowedDelimiters:
        errorList.append(
            LexicalError(
                startingPosition,
                f"Invalid delimiter {repr(currentCharacter)} after number '{numberText}'. Expected: {expectedDelimiters}"
            )
        )
        return True

    # pick token type
    if hasDecimalPoint:
        tokenType = TK_LIT_DECIMAL
    else:
        tokenType = TK_LIT_INT

    tokenList.append(Token(tokenType, numberText, startingPosition))
    return True

def consumeInvalidNumberTail(lexer):
    # skip invalid number
    while lexer.currentCharacter is not None and (
        lexer.currentCharacter.isalnum()
        or lexer.currentCharacter in {".", "_", "-"}
    ):
        lexer.advance()

def scanNumbers(lexer, tokenList, errorList):
    currentCharacter = lexer.currentCharacter

    # no char to scan
    if currentCharacter is None:
        return False

    # must start with digit or -digit
    if not currentCharacter.isdigit():
        return False

    startingPosition = lexer.currentPosition.copy()
    numberText = ""
    hasDecimalPoint = False
    integerDigitCount = 0
    fractionalDigitCount = 0
    hasDigitAfterDecimalPoint = False

    # read number
    while lexer.currentCharacter is not None:
        currentCharacter = lexer.currentCharacter

        # digit part
        if currentCharacter.isdigit():
            if not hasDecimalPoint:
                integerDigitCount += 1

                # int limit
                if integerDigitCount > MAX_INTEGER_DIGITS:
                    consumeInvalidNumberTail(lexer)
                    errorList.append(
                        LexicalError(
                            startingPosition,
                            f"Integer part exceeds {MAX_INTEGER_DIGITS} digits"
                        )
                    )
                    return True

            else:
                fractionalDigitCount += 1
                hasDigitAfterDecimalPoint = True

                # decimal limit
                if fractionalDigitCount > MAX_FRACTIONAL_DIGITS:
                    consumeInvalidNumberTail(lexer)
                    errorList.append(
                        LexicalError(
                            startingPosition,
                            f"Fractional part exceeds {MAX_FRACTIONAL_DIGITS} digits"
                        )
                    )
                    return True

            numberText += currentCharacter
            lexer.advance()
            continue

        # decimal point
        if currentCharacter == ".":
            if hasDecimalPoint:
                consumeInvalidNumberTail(lexer)
                errorList.append(
                    LexicalError(
                        startingPosition,
                        f"Multiple decimal points in number '{numberText + currentCharacter}'"
                    )
                )
                return True

            if integerDigitCount == 0:
                consumeInvalidNumberTail(lexer)
                errorList.append(
                    LexicalError(
                        startingPosition,
                        "Decimal must have integer part before '.'"
                    )
                )
                return True

            hasDecimalPoint = True
            numberText += currentCharacter
            lexer.advance()
            continue

        # invalid identifier
        if currentCharacter.isalpha() or currentCharacter == "_":
            consumeInvalidNumberTail(lexer)
            errorList.append(
                LexicalError(
                    startingPosition,
                    f"Invalid identifier starting with digit '{numberText + currentCharacter}'"
                )
            )
            return True

        # valid delimiter
        if currentCharacter in integerDecimalDelimiters:
            break

        # invalid number char
        consumeInvalidNumberTail(lexer)
        errorList.append(
            LexicalError(
                startingPosition,
                f"Invalid character '{currentCharacter}' in number '{numberText}'"
            )
        )
        return True

    # dot needs digit after
    if hasDecimalPoint and not hasDigitAfterDecimalPoint:
        errorList.append(
            LexicalError(
                startingPosition,
                f"Decimal point requires digits after '.' in '{numberText}'"
            )
        )
        return True

    return acceptNumber(
        lexer,
        tokenList,
        errorList,
        startingPosition,
        numberText,
        integerDecimalDelimiters,
        hasDecimalPoint
    )