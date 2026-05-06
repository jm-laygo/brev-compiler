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
            errorList.append(
                LexicalError(
                    startingPosition,
                    f"Missing delimiter after '{keywordText}'. Expected: {expectedDelimiters}"
                )
            )
            return True

        if currentCharacter is not None and currentCharacter not in allowedDelimiters:
            errorList.append(
                LexicalError(
                    startingPosition,
                    f"Invalid delimiter {repr(currentCharacter)} after '{keywordText}'. Expected: {expectedDelimiters}"
                )
            )
            return True

        tokenList.append(
            Token(
                tokenType,
                keywordText,
                startingPosition
            )
        )

        return True

    startingPosition = lexer.currentPosition.copy()
    firstCharacter = lexer.currentCharacter

    keywordBeforeOpenParen = whitespace | {op_par}
    keywordBeforeOpenBrace = whitespace | {op_bra}
    keywordBeforeSemicolon = whitespace | {semicolon}
    keywordBeforeColon = whitespace | {colon}
    keywordBeforeDeclarationName = whitespace

    # LETTER A
    if firstCharacter == "a":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # ABSOLUTION
        restoreLexerState(savedPosition)
        keywordText = "a"

        if lexer.currentCharacter == "b":
            keywordText += "b"
            lexer.advance()

            if lexer.currentCharacter == "s":
                keywordText += "s"
                lexer.advance()

                if lexer.currentCharacter == "o":
                    keywordText += "o"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText += "l"
                        lexer.advance()

                        if lexer.currentCharacter == "u":
                            keywordText += "u"
                            lexer.advance()

                            if lexer.currentCharacter == "t":
                                keywordText += "t"
                                lexer.advance()

                                if lexer.currentCharacter == "i":
                                    keywordText += "i"
                                    lexer.advance()

                                    if lexer.currentCharacter == "o":
                                        keywordText += "o"
                                        lexer.advance()

                                        if lexer.currentCharacter == "n":
                                            keywordText += "n"
                                            lexer.advance()

                                            return acceptKeyword(
                                                TK_CF_ABSOLUTION,
                                                keywordText,
                                                startingPosition,
                                                keywordBeforeOpenBrace
                                            )

        # ABSOLVE
        restoreLexerState(savedPosition)
        keywordText = "a"

        if lexer.currentCharacter == "b":
            keywordText += "b"
            lexer.advance()

            if lexer.currentCharacter == "s":
                keywordText += "s"
                lexer.advance()

                if lexer.currentCharacter == "o":
                    keywordText += "o"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText += "l"
                        lexer.advance()

                        if lexer.currentCharacter == "v":
                            keywordText += "v"
                            lexer.advance()

                            if lexer.currentCharacter == "e":
                                keywordText += "e"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_CF_ABSOLVE,
                                    keywordText,
                                    startingPosition,
                                    keywordBeforeSemicolon
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
            keywordText += "e"
            lexer.advance()

            if lexer.currentCharacter == "c":
                keywordText += "c"
                lexer.advance()

                if lexer.currentCharacter == "r":
                    keywordText += "r"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText += "e"
                        lexer.advance()

                        if lexer.currentCharacter == "e":
                            keywordText += "e"
                            lexer.advance()

                            return acceptKeyword(
                                TK_CF_DECREE,
                                keywordText,
                                startingPosition,
                                keywordBeforeOpenParen
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
                keywordText += "s"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText += "c"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText += "e"
                        lexer.advance()

                        if lexer.currentCharacter == "r":
                            keywordText += "r"
                            lexer.advance()

                            if lexer.currentCharacter == "n":
                                keywordText += "n"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_CF_DISCERN,
                                    keywordText,
                                    startingPosition,
                                    keywordBeforeOpenParen
                                )

            # DISMISS
            restoreLexerState(savedPositionAfterDi)
            keywordText = keywordTextWithDi

            if lexer.currentCharacter == "s":
                keywordText += "s"
                lexer.advance()

                if lexer.currentCharacter == "m":
                    keywordText += "m"
                    lexer.advance()

                    if lexer.currentCharacter == "i":
                        keywordText += "i"
                        lexer.advance()

                        if lexer.currentCharacter == "s":
                            keywordText += "s"
                            lexer.advance()

                            if lexer.currentCharacter == "s":
                                keywordText += "s"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_CF_DISMISS,
                                    keywordText,
                                    startingPosition,
                                    keywordBeforeSemicolon
                                )

            # DIVINE
            restoreLexerState(savedPositionAfterDi)
            keywordText = keywordTextWithDi

            if lexer.currentCharacter == "v":
                keywordText += "v"
                lexer.advance()

                if lexer.currentCharacter == "i":
                    keywordText += "i"
                    lexer.advance()

                    if lexer.currentCharacter == "n":
                        keywordText += "n"
                        lexer.advance()

                        if lexer.currentCharacter == "e":
                            keywordText += "e"
                            lexer.advance()

                            return acceptKeyword(
                                TK_DTYPE_DIVINE,
                                keywordText,
                                startingPosition,
                                keywordBeforeDeclarationName
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
            keywordText += "d"
            lexer.advance()

            if lexer.currentCharacter == "i":
                keywordText += "i"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText += "c"
                    lexer.advance()

                    if lexer.currentCharacter == "t":
                        keywordText += "t"
                        lexer.advance()

                        return acceptKeyword(
                            TK_CF_EDICT,
                            keywordText,
                            startingPosition,
                            keywordBeforeOpenParen
                        )

        # ENDURE
        restoreLexerState(savedPosition)
        keywordText = "e"

        if lexer.currentCharacter == "n":
            keywordText += "n"
            lexer.advance()

            if lexer.currentCharacter == "d":
                keywordText += "d"
                lexer.advance()

                if lexer.currentCharacter == "u":
                    keywordText += "u"
                    lexer.advance()

                    if lexer.currentCharacter == "r":
                        keywordText += "r"
                        lexer.advance()

                        if lexer.currentCharacter == "e":
                            keywordText += "e"
                            lexer.advance()

                            return acceptKeyword(
                                TK_CF_ENDURE,
                                keywordText,
                                startingPosition,
                                keywordBeforeOpenParen
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
            keywordText += "a"
            lexer.advance()

            if lexer.currentCharacter == "l":
                keywordText += "l"
                lexer.advance()

                if lexer.currentCharacter == "l":
                    keywordText += "l"
                    lexer.advance()

                    return acceptKeyword(
                        TK_CF_FALL,
                        keywordText,
                        startingPosition,
                        keywordBeforeSemicolon
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
            keywordText += "e"
            lexer.advance()

            if lexer.currentCharacter == "n":
                keywordText += "n"
                lexer.advance()

                if lexer.currentCharacter == "e":
                    keywordText += "e"
                    lexer.advance()

                    if lexer.currentCharacter == "s":
                        keywordText += "s"
                        lexer.advance()

                        if lexer.currentCharacter == "i":
                            keywordText += "i"
                            lexer.advance()

                            if lexer.currentCharacter == "s":
                                keywordText += "s"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_OTHERS_GENESIS,
                                    keywordText,
                                    startingPosition,
                                    keywordBeforeOpenParen
                                )

        # GRACE
        restoreLexerState(savedPosition)
        keywordText = "g"

        if lexer.currentCharacter == "r":
            keywordText += "r"
            lexer.advance()

            if lexer.currentCharacter == "a":
                keywordText += "a"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText += "c"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText += "e"
                        lexer.advance()

                        return acceptKeyword(
                            TK_CF_GRACE,
                            keywordText,
                            startingPosition,
                            keywordBeforeColon
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
            keywordText += "o"
            lexer.advance()

            if lexer.currentCharacter == "l":
                keywordText += "l"
                lexer.advance()

                if lexer.currentCharacter == "l":
                    keywordText += "l"
                    lexer.advance()

                    if lexer.currentCharacter == "o":
                        keywordText += "o"
                        lexer.advance()

                        if lexer.currentCharacter == "w":
                            keywordText += "w"
                            lexer.advance()

                            return acceptKeyword(
                                TK_DTYPE_HOLLOW,
                                keywordText,
                                startingPosition,
                                keywordBeforeDeclarationName
                            )

        # HOLY
        restoreLexerState(savedPosition)
        keywordText = "h"

        if lexer.currentCharacter == "o":
            keywordText += "o"
            lexer.advance()

            if lexer.currentCharacter == "l":
                keywordText += "l"
                lexer.advance()

                if lexer.currentCharacter == "y":
                    keywordText += "y"
                    lexer.advance()

                    return acceptKeyword(
                        TK_LIT_BOOL,
                        keywordText,
                        startingPosition,
                        bool_delim
                    )

        restoreLexerState(startingPosition)
        return False

    # LETTER O
    if firstCharacter == "o":
        lexer.advance()
        savedPosition = lexer.currentPosition.copy()

        # ORDAIN
        restoreLexerState(savedPosition)
        keywordText = "o"

        if lexer.currentCharacter == "r":
            keywordText += "r"
            lexer.advance()

            if lexer.currentCharacter == "d":
                keywordText += "d"
                lexer.advance()

                if lexer.currentCharacter == "a":
                    keywordText += "a"
                    lexer.advance()

                    if lexer.currentCharacter == "i":
                        keywordText += "i"
                        lexer.advance()

                        if lexer.currentCharacter == "n":
                            keywordText += "n"
                            lexer.advance()

                            return acceptKeyword(
                                TK_OTHERS_ORDAIN,
                                keywordText,
                                startingPosition,
                                keywordBeforeDeclarationName
                            )

        # ORDER
        restoreLexerState(savedPosition)
        keywordText = "o"

        if lexer.currentCharacter == "r":
            keywordText += "r"
            lexer.advance()

            if lexer.currentCharacter == "d":
                keywordText += "d"
                lexer.advance()

                if lexer.currentCharacter == "e":
                    keywordText += "e"
                    lexer.advance()

                    if lexer.currentCharacter == "r":
                        keywordText += "r"
                        lexer.advance()

                        return acceptKeyword(
                            TK_OTHERS_ORDER,
                            keywordText,
                            startingPosition,
                            keywordBeforeDeclarationName
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
                keywordText += "o"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText += "c"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText += "e"
                        lexer.advance()

                        if lexer.currentCharacter == "e":
                            keywordText += "e"
                            lexer.advance()

                            if lexer.currentCharacter == "d":
                                keywordText += "d"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_CF_PROCEED,
                                    keywordText,
                                    startingPosition,
                                    keywordBeforeSemicolon
                                )

            # PROCLAIM
            restoreLexerState(savedPositionAfterPr)
            keywordText = keywordTextWithPr

            if lexer.currentCharacter == "o":
                keywordText += "o"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText += "c"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText += "l"
                        lexer.advance()

                        if lexer.currentCharacter == "a":
                            keywordText += "a"
                            lexer.advance()

                            if lexer.currentCharacter == "i":
                                keywordText += "i"
                                lexer.advance()

                                if lexer.currentCharacter == "m":
                                    keywordText += "m"
                                    lexer.advance()

                                    return acceptKeyword(
                                        TK_IO_PROCLAIM,
                                        keywordText,
                                        startingPosition,
                                        keywordBeforeOpenParen
                                    )

            # PROCESSION
            restoreLexerState(savedPositionAfterPr)
            keywordText = keywordTextWithPr

            if lexer.currentCharacter == "o":
                keywordText += "o"
                lexer.advance()

                if lexer.currentCharacter == "c":
                    keywordText += "c"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText += "e"
                        lexer.advance()

                        if lexer.currentCharacter == "s":
                            keywordText += "s"
                            lexer.advance()

                            if lexer.currentCharacter == "s":
                                keywordText += "s"
                                lexer.advance()

                                if lexer.currentCharacter == "i":
                                    keywordText += "i"
                                    lexer.advance()

                                    if lexer.currentCharacter == "o":
                                        keywordText += "o"
                                        lexer.advance()

                                        if lexer.currentCharacter == "n":
                                            keywordText += "n"
                                            lexer.advance()

                                            return acceptKeyword(
                                                TK_CF_PROCESSION,
                                                keywordText,
                                                startingPosition,
                                                keywordBeforeOpenParen
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
            keywordText += "e"
            lexer.advance()

            if lexer.currentCharacter == "c":
                keywordText += "c"
                lexer.advance()

                if lexer.currentCharacter == "e":
                    keywordText += "e"
                    lexer.advance()

                    if lexer.currentCharacter == "i":
                        keywordText += "i"
                        lexer.advance()

                        if lexer.currentCharacter == "v":
                            keywordText += "v"
                            lexer.advance()

                            if lexer.currentCharacter == "e":
                                keywordText += "e"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_IO_RECEIVE,
                                    keywordText,
                                    startingPosition,
                                    keywordBeforeOpenParen
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
                keywordText += "t"
                lexer.advance()

                if lexer.currentCharacter == "u":
                    keywordText += "u"
                    lexer.advance()

                    if lexer.currentCharacter == "a":
                        keywordText += "a"
                        lexer.advance()

                        if lexer.currentCharacter == "l":
                            keywordText += "l"
                            lexer.advance()

                            return acceptKeyword(
                                TK_CF_RITUAL,
                                keywordText,
                                startingPosition,
                                keywordBeforeOpenBrace
                            )

            # RITE
            restoreLexerState(savedPositionAfterRi)
            keywordText = keywordTextWithRi

            if lexer.currentCharacter == "t":
                keywordText += "t"
                lexer.advance()

                if lexer.currentCharacter == "e":
                    keywordText += "e"
                    lexer.advance()

                    return acceptKeyword(
                        TK_CF_RITE,
                        keywordText,
                        startingPosition,
                        keywordBeforeDeclarationName
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
            keywordText += "a"
            lexer.advance()

            if lexer.currentCharacter == "c":
                keywordText += "c"
                lexer.advance()

                if lexer.currentCharacter == "r":
                    keywordText += "r"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText += "e"
                        lexer.advance()

                        if lexer.currentCharacter == "d":
                            keywordText += "d"
                            lexer.advance()

                            return acceptKeyword(
                                TK_SACRED,
                                keywordText,
                                startingPosition,
                                keywordBeforeDeclarationName
                            )

        # SCRIPTURE
        restoreLexerState(savedPosition)
        keywordText = "s"

        if lexer.currentCharacter == "c":
            keywordText += "c"
            lexer.advance()

            if lexer.currentCharacter == "r":
                keywordText += "r"
                lexer.advance()

                if lexer.currentCharacter == "i":
                    keywordText += "i"
                    lexer.advance()

                    if lexer.currentCharacter == "p":
                        keywordText += "p"
                        lexer.advance()

                        if lexer.currentCharacter == "t":
                            keywordText += "t"
                            lexer.advance()

                            if lexer.currentCharacter == "u":
                                keywordText += "u"
                                lexer.advance()

                                if lexer.currentCharacter == "r":
                                    keywordText += "r"
                                    lexer.advance()

                                    if lexer.currentCharacter == "e":
                                        keywordText += "e"
                                        lexer.advance()

                                        return acceptKeyword(
                                            TK_DTYPE_SCRIPTURE,
                                            keywordText,
                                            startingPosition,
                                            keywordBeforeDeclarationName
                                        )

        # SIGIL
        restoreLexerState(savedPosition)
        keywordText = "s"

        if lexer.currentCharacter == "i":
            keywordText += "i"
            lexer.advance()

            if lexer.currentCharacter == "g":
                keywordText += "g"
                lexer.advance()

                if lexer.currentCharacter == "i":
                    keywordText += "i"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText += "l"
                        lexer.advance()

                        return acceptKeyword(
                            TK_DTYPE_SIGIL,
                            keywordText,
                            startingPosition,
                            keywordBeforeDeclarationName
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
            keywordText += "a"
            lexer.advance()

            if lexer.currentCharacter == "l":
                keywordText += "l"
                lexer.advance()

                if lexer.currentCharacter == "l":
                    keywordText += "l"
                    lexer.advance()

                    if lexer.currentCharacter == "y":
                        keywordText += "y"
                        lexer.advance()

                        return acceptKeyword(
                            TK_DTYPE_TALLY,
                            keywordText,
                            startingPosition,
                            keywordBeforeDeclarationName
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
            keywordText += "n"
            lexer.advance()

            if lexer.currentCharacter == "h":
                keywordText += "h"
                lexer.advance()

                if lexer.currentCharacter == "o":
                    keywordText += "o"
                    lexer.advance()

                    if lexer.currentCharacter == "l":
                        keywordText += "l"
                        lexer.advance()

                        if lexer.currentCharacter == "y":
                            keywordText += "y"
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
                keywordText += "r"
                lexer.advance()

                if lexer.currentCharacter == "i":
                    keywordText += "i"
                    lexer.advance()

                    if lexer.currentCharacter == "t":
                        keywordText += "t"
                        lexer.advance()

                        if lexer.currentCharacter == "y":
                            keywordText += "y"
                            lexer.advance()

                            return acceptKeyword(
                                TK_DTYPE_VERITY,
                                keywordText,
                                startingPosition,
                                keywordBeforeDeclarationName
                            )

            # VERSE / VERSEOF
            restoreLexerState(savedPositionAfterVe)
            keywordText = keywordTextWithVe

            if lexer.currentCharacter == "r":
                keywordText += "r"
                lexer.advance()

                if lexer.currentCharacter == "s":
                    keywordText += "s"
                    lexer.advance()

                    if lexer.currentCharacter == "e":
                        keywordText += "e"
                        lexer.advance()

                        # VERSEOF
                        if lexer.currentCharacter == "o":
                            savedPositionAtLetterO = lexer.currentPosition.copy()
                            keywordTextBeforeVerseOf = keywordText

                            keywordText += "o"
                            lexer.advance()

                            if lexer.currentCharacter == "f":
                                keywordText += "f"
                                lexer.advance()

                                return acceptKeyword(
                                    TK_OTHERS_VERSEOF,
                                    keywordText,
                                    startingPosition,
                                    keywordBeforeOpenParen
                                )

                            restoreLexerState(savedPositionAtLetterO)
                            keywordText = keywordTextBeforeVerseOf

                        # VERSE
                        return acceptKeyword(
                            TK_CF_VERSE,
                            keywordText,
                            startingPosition,
                            keywordBeforeDeclarationName
                        )

        restoreLexerState(startingPosition)
        return False

    restoreLexerState(startingPosition)
    return False


def scanKeywords(lexer, tokenList, errorList):
    return scanReservedWord(lexer, tokenList, errorList)