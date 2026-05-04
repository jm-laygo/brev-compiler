from backend.tokens import *
from backend.delimiters import *
from backend.errors import LexicalError
from backend.delimiters import formatExpectedDelimiters


def scanReservedWord(lexer, tokenList, errorList):
    def restoreLexerState(savedPosition):
        lexer.currentPosition = savedPosition.copy()

        if 0 <= lexer.currentPosition.characterIndex < len(lexer.sourceCode):
            lexer.currentCharacter = lexer.sourceCode[lexer.currentPosition.characterIndex]
        else:
            lexer.currentCharacter = None

    def acceptKeyword(tokenType, keywordText, startingPosition, allowedDelimiters):
        if isinstance(allowedDelimiters, str):
            allowedDelimiters = {allowedDelimiters}

        currentCharacter = lexer.currentCharacter

        if currentCharacter == "\r":
            currentCharacter = "\n"

        expectedDelimiters = formatExpectedDelimiters(allowedDelimiters)

        if currentCharacter is not None and (currentCharacter.isalnum() or currentCharacter == "_"):
            restoreLexerState(startingPosition)
            return False

        if currentCharacter is None and None not in allowedDelimiters:
            lexicalError = LexicalError(
                startingPosition,
                f"Missing delimiter after '{keywordText}'. Expected: {expectedDelimiters}"
            )

            errorList.extend([lexicalError])
            return True

        if currentCharacter is not None and currentCharacter in allowedDelimiters:
            keywordToken = Token(
                tokenType,
                keywordText,
                startingPosition
            )

            tokenList.extend([keywordToken])
            return True

        if currentCharacter is not None and currentCharacter not in allowedDelimiters:
            lexicalError = LexicalError(
                startingPosition,
                f"Invalid delimiter {repr(currentCharacter)} after '{keywordText}'. Expected: {expectedDelimiters}"
            )

            errorList.extend([lexicalError])
            return True

        keywordToken = Token(
            tokenType,
            keywordText,
            startingPosition
        )

        tokenList.extend([keywordToken])
        return True

    startingPosition = lexer.currentPosition.copy()
    firstCharacter = lexer.currentCharacter

    # LETTER A
    if firstCharacter == "a":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # ABSOLUTION
        restoreLexerState(savedPosition)
        keywordText = "a"

        if lexer.currentCharacter == "b":
            keywordText = keywordText + "b"
            lexer.advance()

            if lexer.currentCharacter == "s":
                keywordText = keywordText + "s"
                lexer.advance()

                if lexer.currentCharacter == "o":
                    keywordText = keywordText + "o"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText = keywordText + "l"
                        lexer.advance()

                        if lexer.currentCharacter == "u":
                            keywordText = keywordText + "u"
                            lexer.advance()

                            if lexer.currentCharacter == "t":
                                keywordText = keywordText + "t"
                                lexer.advance()

                                if lexer.currentCharacter == "i":
                                    keywordText = keywordText + "i"
                                    lexer.advance()

                                    if lexer.currentCharacter == "o":
                                        keywordText = keywordText + "o"
                                        lexer.advance()

                                        if lexer.currentCharacter == "n":
                                            keywordText = keywordText + "n"
                                            lexer.advance()

                                            return acceptKeyword(
                                                TK_CF_ABSOLUTION,
                                                keywordText,
                                                startingPosition,
                                                els_delim
                                            )

        # ABSOLVE
        restoreLexerState(savedPosition)
        keywordText = "a"

        if lexer.currentCharacter == "b":
            keywordText = keywordText + "b"
            lexer.advance()

            if lexer.currentCharacter == "s":
                keywordText = keywordText + "s"
                lexer.advance()

                if lexer.currentCharacter == "o":
                    keywordText = keywordText + "o"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText = keywordText + "l"
                        lexer.advance()

                        if lexer.currentCharacter == "v":
                            keywordText = keywordText + "v"
                            lexer.advance()

                            if lexer.currentCharacter == "e":
                                keywordText = keywordText + "e"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_CF_ABSOLVE,
                                    keywordText,
                                    startingPosition,
                                    {semicolon}
                                )

        restoreLexerState(startingPosition)
        return False

    # LETTER D
    if firstCharacter == "d":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # DECREE
        restoreLexerState(savedPosition)
        keywordText = "d"

        if lexer.currentCharacter == "e":
            keywordText = keywordText + "e"
            lexer.advance()

            if lexer.currentCharacter == "c":
                keywordText = keywordText + "c"
                lexer.advance()

                if lexer.currentCharacter == "r":
                    keywordText = keywordText + "r"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText = keywordText + "e"
                        lexer.advance()

                        if lexer.currentCharacter == "e":
                            keywordText = keywordText + "e"
                            lexer.advance()

                            return acceptKeyword(
                                TK_CF_DECREE,
                                keywordText,
                                startingPosition,
                                {op_par, space}
                            )

        # DISCERN / DISMISS / DIVINE
        restoreLexerState(savedPosition)
        keywordText = "d"

        if lexer.currentCharacter == "i":
            keywordTextWithDi = "di"
            lexer.advance()
            savedPositionAfterDi = lexer.currentPosition.copy()

            # DISCERN
            restoreLexerState(savedPositionAfterDi)
            keywordText = keywordTextWithDi

            if lexer.currentCharacter == "s":
                keywordText = keywordText + "s"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText = keywordText + "c"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText = keywordText + "e"
                        lexer.advance()

                        if lexer.currentCharacter == "r":
                            keywordText = keywordText + "r"
                            lexer.advance()

                            if lexer.currentCharacter == "n":
                                keywordText = keywordText + "n"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_CF_DISCERN,
                                    keywordText,
                                    startingPosition,
                                    {op_par, space}
                                )

            # DISMISS
            restoreLexerState(savedPositionAfterDi)
            keywordText = keywordTextWithDi

            if lexer.currentCharacter == "s":
                keywordText = keywordText + "s"
                lexer.advance()

                if lexer.currentCharacter == "m":
                    keywordText = keywordText + "m"
                    lexer.advance()

                    if lexer.currentCharacter == "i":
                        keywordText = keywordText + "i"
                        lexer.advance()

                        if lexer.currentCharacter == "s":
                            keywordText = keywordText + "s"
                            lexer.advance()

                            if lexer.currentCharacter == "s":
                                keywordText = keywordText + "s"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_CF_DISMISS,
                                    keywordText,
                                    startingPosition,
                                    {space, semicolon}
                                )

            # DIVINE
            restoreLexerState(savedPositionAfterDi)
            keywordText = keywordTextWithDi

            if lexer.currentCharacter == "v":
                keywordText = keywordText + "v"
                lexer.advance()

                if lexer.currentCharacter == "i":
                    keywordText = keywordText + "i"
                    lexer.advance()

                    if lexer.currentCharacter == "n":
                        keywordText = keywordText + "n"
                        lexer.advance()

                        if lexer.currentCharacter == "e":
                            keywordText = keywordText + "e"
                            lexer.advance()

                            return acceptKeyword(
                                TK_DTYPE_DIVINE,
                                keywordText,
                                startingPosition,
                                {space}
                            )

        restoreLexerState(startingPosition)
        return False

    # LETTER E
    if firstCharacter == "e":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # EDICT
        restoreLexerState(savedPosition)
        keywordText = "e"

        if lexer.currentCharacter == "d":
            keywordText = keywordText + "d"
            lexer.advance()

            if lexer.currentCharacter == "i":
                keywordText = keywordText + "i"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText = keywordText + "c"
                    lexer.advance()

                    if lexer.currentCharacter == "t":
                        keywordText = keywordText + "t"
                        lexer.advance()

                        return acceptKeyword(
                            TK_CF_EDICT,
                            keywordText,
                            startingPosition,
                            {op_par, space}
                        )

        # ENDURE
        restoreLexerState(savedPosition)
        keywordText = "e"

        if lexer.currentCharacter == "n":
            keywordText = keywordText + "n"
            lexer.advance()

            if lexer.currentCharacter == "d":
                keywordText = keywordText + "d"
                lexer.advance()

                if lexer.currentCharacter == "u":
                    keywordText = keywordText + "u"
                    lexer.advance()

                    if lexer.currentCharacter == "r":
                        keywordText = keywordText + "r"
                        lexer.advance()

                        if lexer.currentCharacter == "e":
                            keywordText = keywordText + "e"
                            lexer.advance()

                            return acceptKeyword(
                                TK_CF_ENDURE,
                                keywordText,
                                startingPosition,
                                {op_par, space}
                            )

        restoreLexerState(startingPosition)
        return False

    # LETTER F
    if firstCharacter == "f":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # FALL
        restoreLexerState(savedPosition)
        keywordText = "f"

        if lexer.currentCharacter == "a":
            keywordText = keywordText + "a"
            lexer.advance()

            if lexer.currentCharacter == "l":
                keywordText = keywordText + "l"
                lexer.advance()

                if lexer.currentCharacter == "l":
                    keywordText = keywordText + "l"
                    lexer.advance()

                    return acceptKeyword(
                        TK_CF_FALL,
                        keywordText,
                        startingPosition,
                        {semicolon}
                    )

        restoreLexerState(startingPosition)
        return False

    # LETTER G
    if firstCharacter == "g":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # GENESIS
        restoreLexerState(savedPosition)
        keywordText = "g"

        if lexer.currentCharacter == "e":
            keywordText = keywordText + "e"
            lexer.advance()

            if lexer.currentCharacter == "n":
                keywordText = keywordText + "n"
                lexer.advance()

                if lexer.currentCharacter == "e":
                    keywordText = keywordText + "e"
                    lexer.advance()

                    if lexer.currentCharacter == "s":
                        keywordText = keywordText + "s"
                        lexer.advance()

                        if lexer.currentCharacter == "i":
                            keywordText = keywordText + "i"
                            lexer.advance()

                            if lexer.currentCharacter == "s":
                                keywordText = keywordText + "s"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_OTHERS_GENESIS,
                                    keywordText,
                                    startingPosition,
                                    {op_par, space}
                                )

        # GRACE
        restoreLexerState(savedPosition)
        keywordText = "g"

        if lexer.currentCharacter == "r":
            keywordText = keywordText + "r"
            lexer.advance()

            if lexer.currentCharacter == "a":
                keywordText = keywordText + "a"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText = keywordText + "c"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText = keywordText + "e"
                        lexer.advance()

                        return acceptKeyword(
                            TK_CF_GRACE,
                            keywordText,
                            startingPosition,
                            {colon}
                        )

        restoreLexerState(startingPosition)
        return False

    # LETTER H
    if firstCharacter == "h":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # HOLLOW
        restoreLexerState(savedPosition)
        keywordText = "h"

        if lexer.currentCharacter == "o":
            keywordText = keywordText + "o"
            lexer.advance()

            if lexer.currentCharacter == "l":
                keywordText = keywordText + "l"
                lexer.advance()

                if lexer.currentCharacter == "l":
                    keywordText = keywordText + "l"
                    lexer.advance()

                    if lexer.currentCharacter == "o":
                        keywordText = keywordText + "o"
                        lexer.advance()

                        if lexer.currentCharacter == "w":
                            keywordText = keywordText + "w"
                            lexer.advance()

                            return acceptKeyword(
                                TK_DTYPE_HOLLOW,
                                keywordText,
                                startingPosition,
                                {space}
                            )

        # HOLY
        restoreLexerState(savedPosition)
        keywordText = "h"

        if lexer.currentCharacter == "o":
            keywordText = keywordText + "o"
            lexer.advance()

            if lexer.currentCharacter == "l":
                keywordText = keywordText + "l"
                lexer.advance()

                if lexer.currentCharacter == "y":
                    keywordText = keywordText + "y"
                    lexer.advance()

                    return acceptKeyword(
                        TK_LIT_BOOL,
                        keywordText,
                        startingPosition,
                        bool_delim
                    )
                    # LETTER O
    if firstCharacter == "o":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # ORDAIN
        restoreLexerState(savedPosition)
        keywordText = "o"

        if lexer.currentCharacter == "r":
            keywordText = keywordText + "r"
            lexer.advance()

            if lexer.currentCharacter == "d":
                keywordText = keywordText + "d"
                lexer.advance()

                if lexer.currentCharacter == "a":
                    keywordText = keywordText + "a"
                    lexer.advance()

                    if lexer.currentCharacter == "i":
                        keywordText = keywordText + "i"
                        lexer.advance()

                        if lexer.currentCharacter == "n":
                            keywordText = keywordText + "n"
                            lexer.advance()

                            return acceptKeyword(
                                TK_OTHERS_ORDAIN,
                                keywordText,
                                startingPosition,
                                {space}
                            )

        # ORDER
        restoreLexerState(savedPosition)
        keywordText = "o"

        if lexer.currentCharacter == "r":
            keywordText = keywordText + "r"
            lexer.advance()

            if lexer.currentCharacter == "d":
                keywordText = keywordText + "d"
                lexer.advance()

                if lexer.currentCharacter == "e":
                    keywordText = keywordText + "e"
                    lexer.advance()

                    if lexer.currentCharacter == "r":
                        keywordText = keywordText + "r"
                        lexer.advance()

                        return acceptKeyword(
                            TK_OTHERS_ORDER,
                            keywordText,
                            startingPosition,
                            space
                        )

        restoreLexerState(startingPosition)
        return False

    # LETTER P
    if firstCharacter == "p":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # PROCEED / PROCLAIM / PROCESSION
        restoreLexerState(savedPosition)
        keywordText = "p"

        if lexer.currentCharacter == "r":
            keywordTextWithPr = "pr"
            lexer.advance()
            savedPositionAfterPr = lexer.currentPosition.copy()

            # PROCEED
            restoreLexerState(savedPositionAfterPr)
            keywordText = keywordTextWithPr

            if lexer.currentCharacter == "o":
                keywordText = keywordText + "o"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText = keywordText + "c"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText = keywordText + "e"
                        lexer.advance()

                        if lexer.currentCharacter == "e":
                            keywordText = keywordText + "e"
                            lexer.advance()

                            if lexer.currentCharacter == "d":
                                keywordText = keywordText + "d"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_CF_PROCEED,
                                    keywordText,
                                    startingPosition,
                                    {semicolon}
                                )

            # PROCLAIM
            restoreLexerState(savedPositionAfterPr)
            keywordText = keywordTextWithPr

            if lexer.currentCharacter == "o":
                keywordText = keywordText + "o"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText = keywordText + "c"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText = keywordText + "l"
                        lexer.advance()

                        if lexer.currentCharacter == "a":
                            keywordText = keywordText + "a"
                            lexer.advance()

                            if lexer.currentCharacter == "i":
                                keywordText = keywordText + "i"
                                lexer.advance()

                                if lexer.currentCharacter == "m":
                                    keywordText = keywordText + "m"
                                    lexer.advance()

                                    return acceptKeyword(
                                        TK_IO_PROCLAIM,
                                        keywordText,
                                        startingPosition,
                                        {op_par}
                                    )

            # PROCESSION
            restoreLexerState(savedPositionAfterPr)
            keywordText = keywordTextWithPr

            if lexer.currentCharacter == "o":
                keywordText = keywordText + "o"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText = keywordText + "c"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText = keywordText + "e"
                        lexer.advance()

                        if lexer.currentCharacter == "s":
                            keywordText = keywordText + "s"
                            lexer.advance()

                            if lexer.currentCharacter == "s":
                                keywordText = keywordText + "s"
                                lexer.advance()

                                if lexer.currentCharacter == "i":
                                    keywordText = keywordText + "i"
                                    lexer.advance()

                                    if lexer.currentCharacter == "o":
                                        keywordText = keywordText + "o"
                                        lexer.advance()

                                        if lexer.currentCharacter == "n":
                                            keywordText = keywordText + "n"
                                            lexer.advance()

                                            return acceptKeyword(
                                                TK_CF_PROCESSION,
                                                keywordText,
                                                startingPosition,
                                                {op_par, space}
                                            )

        restoreLexerState(startingPosition)
        return False

    # LETTER R
    if firstCharacter == "r":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # RECEIVE
        restoreLexerState(savedPosition)
        keywordText = "r"

        if lexer.currentCharacter == "e":
            keywordText = keywordText + "e"
            lexer.advance()

            if lexer.currentCharacter == "c":
                keywordText = keywordText + "c"
                lexer.advance()

                if lexer.currentCharacter == "e":
                    keywordText = keywordText + "e"
                    lexer.advance()

                    if lexer.currentCharacter == "i":
                        keywordText = keywordText + "i"
                        lexer.advance()

                        if lexer.currentCharacter == "v":
                            keywordText = keywordText + "v"
                            lexer.advance()

                            if lexer.currentCharacter == "e":
                                keywordText = keywordText + "e"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_IO_RECEIVE,
                                    keywordText,
                                    startingPosition,
                                    {op_par}
                                )

        # RITUAL / RITE
        restoreLexerState(savedPosition)
        keywordText = "r"

        if lexer.currentCharacter == "i":
            keywordTextWithRi = "ri"
            lexer.advance()
            savedPositionAfterRi = lexer.currentPosition.copy()

            # RITUAL
            restoreLexerState(savedPositionAfterRi)
            keywordText = keywordTextWithRi

            if lexer.currentCharacter == "t":
                keywordText = keywordText + "t"
                lexer.advance()

                if lexer.currentCharacter == "u":
                    keywordText = keywordText + "u"
                    lexer.advance()

                    if lexer.currentCharacter == "a":
                        keywordText = keywordText + "a"
                        lexer.advance()

                        if lexer.currentCharacter == "l":
                            keywordText = keywordText + "l"
                            lexer.advance()

                            return acceptKeyword(
                                TK_CF_RITUAL,
                                keywordText,
                                startingPosition,
                                {space, op_bra}
                            )

            # RITE
            restoreLexerState(savedPositionAfterRi)
            keywordText = keywordTextWithRi

            if lexer.currentCharacter == "t":
                keywordText = keywordText + "t"
                lexer.advance()

                if lexer.currentCharacter == "e":
                    keywordText = keywordText + "e"
                    lexer.advance()

                    return acceptKeyword(
                        TK_CF_RITE,
                        keywordText,
                        startingPosition,
                        {space}
                    )

        restoreLexerState(startingPosition)
        return False

    # LETTER S
    if firstCharacter == "s":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # SACRED
        restoreLexerState(savedPosition)
        keywordText = "s"

        if lexer.currentCharacter == "a":
            keywordText = keywordText + "a"
            lexer.advance()

            if lexer.currentCharacter == "c":
                keywordText = keywordText + "c"
                lexer.advance()

                if lexer.currentCharacter == "r":
                    keywordText = keywordText + "r"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText = keywordText + "e"
                        lexer.advance()

                        if lexer.currentCharacter == "d":
                            keywordText = keywordText + "d"
                            lexer.advance()

                            return acceptKeyword(
                                TK_SACRED,
                                keywordText,
                                startingPosition,
                                {space}
                            )

        # SCRIPTURE
        restoreLexerState(savedPosition)
        keywordText = "s"

        if lexer.currentCharacter == "c":
            keywordText = keywordText + "c"
            lexer.advance()

            if lexer.currentCharacter == "r":
                keywordText = keywordText + "r"
                lexer.advance()

                if lexer.currentCharacter == "i":
                    keywordText = keywordText + "i"
                    lexer.advance()

                    if lexer.currentCharacter == "p":
                        keywordText = keywordText + "p"
                        lexer.advance()

                        if lexer.currentCharacter == "t":
                            keywordText = keywordText + "t"
                            lexer.advance()

                            if lexer.currentCharacter == "u":
                                keywordText = keywordText + "u"
                                lexer.advance()

                                if lexer.currentCharacter == "r":
                                    keywordText = keywordText + "r"
                                    lexer.advance()

                                    if lexer.currentCharacter == "e":
                                        keywordText = keywordText + "e"
                                        lexer.advance()

                                        return acceptKeyword(
                                            TK_DTYPE_SCRIPTURE,
                                            keywordText,
                                            startingPosition,
                                            {space}
                                        )

        # SIGIL
        restoreLexerState(savedPosition)
        keywordText = "s"

        if lexer.currentCharacter == "i":
            keywordText = keywordText + "i"
            lexer.advance()

            if lexer.currentCharacter == "g":
                keywordText = keywordText + "g"
                lexer.advance()

                if lexer.currentCharacter == "i":
                    keywordText = keywordText + "i"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText = keywordText + "l"
                        lexer.advance()

                        return acceptKeyword(
                            TK_DTYPE_SIGIL,
                            keywordText,
                            startingPosition,
                            {space}
                        )

        restoreLexerState(startingPosition)
        return False

    # LETTER T
    if firstCharacter == "t":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # TALLY
        restoreLexerState(savedPosition)
        keywordText = "t"

        if lexer.currentCharacter == "a":
            keywordText = keywordText + "a"
            lexer.advance()

            if lexer.currentCharacter == "l":
                keywordText = keywordText + "l"
                lexer.advance()

                if lexer.currentCharacter == "l":
                    keywordText = keywordText + "l"
                    lexer.advance()

                    if lexer.currentCharacter == "y":
                        keywordText = keywordText + "y"
                        lexer.advance()

                        return acceptKeyword(
                            TK_DTYPE_TALLY,
                            keywordText,
                            startingPosition,
                            {space}
                        )

        restoreLexerState(startingPosition)
        return False

    # LETTER U
    if firstCharacter == "u":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # UNHOLY
        restoreLexerState(savedPosition)
        keywordText = "u"

        if lexer.currentCharacter == "n":
            keywordText = keywordText + "n"
            lexer.advance()

            if lexer.currentCharacter == "h":
                keywordText = keywordText + "h"
                lexer.advance()

                if lexer.currentCharacter == "o":
                    keywordText = keywordText + "o"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText = keywordText + "l"
                        lexer.advance()

                        if lexer.currentCharacter == "y":
                            keywordText = keywordText + "y"
                            lexer.advance()

                            return acceptKeyword(
                                TK_LIT_BOOL,
                                keywordText,
                                startingPosition,
                                bool_delim
                            )

        restoreLexerState(startingPosition)
        return False

    # LETTER V
    if firstCharacter == "v":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # VERITY / VERSE / VERSEOF
        restoreLexerState(savedPosition)
        keywordText = "v"

        if lexer.currentCharacter == "e":
            keywordTextWithVe = "ve"
            lexer.advance()
            savedPositionAfterVe = lexer.currentPosition.copy()

            # VERITY
            restoreLexerState(savedPositionAfterVe)
            keywordText = keywordTextWithVe

            if lexer.currentCharacter == "r":
                keywordText = keywordText + "r"
                lexer.advance()

                if lexer.currentCharacter == "i":
                    keywordText = keywordText + "i"
                    lexer.advance()

                    if lexer.currentCharacter == "t":
                        keywordText = keywordText + "t"
                        lexer.advance()

                        if lexer.currentCharacter == "y":
                            keywordText = keywordText + "y"
                            lexer.advance()

                            return acceptKeyword(
                                TK_DTYPE_VERITY,
                                keywordText,
                                startingPosition,
                                {space}
                            )

            # VERSE / VERSEOF
            restoreLexerState(savedPositionAfterVe)
            keywordText = keywordTextWithVe

            if lexer.currentCharacter == "r":
                keywordText = keywordText + "r"
                lexer.advance()

                if lexer.currentCharacter == "s":
                    keywordText = keywordText + "s"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText = keywordText + "e"
                        lexer.advance()

                        # VERSEOF
                        if lexer.currentCharacter == "o":
                            savedPositionAtLetterO = lexer.currentPosition.copy()
                            keywordTextBeforeVerseOf = keywordText

                            keywordText = keywordText + "o"
                            lexer.advance()

                            if lexer.currentCharacter == "f":
                                keywordText = keywordText + "f"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_OTHERS_VERSEOF,
                                    keywordText,
                                    startingPosition,
                                    {op_par}
                                )

                            restoreLexerState(savedPositionAtLetterO)
                            keywordText = keywordTextBeforeVerseOf

                        # VERSE
                        return acceptKeyword(
                            TK_CF_VERSE,
                            keywordText,
                            startingPosition,
                            {space}
                        )

        restoreLexerState(startingPosition)
        return False

    restoreLexerState(startingPosition)
    return False


def scanKeywords(lexer, tokenList, errorList):
    return scanReservedWord(lexer, tokenList, errorList)