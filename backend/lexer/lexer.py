from backend.tokens import *
from backend.errors import LexicalError
from backend.positions import Position

from backend.lexer.scanners.scan_identifiers import scanIdentifier
from backend.lexer.scanners.scan_comments import scanComment
from backend.lexer.scanners.scan_numbers import scanNumbers
from backend.lexer.scanners.scan_chars import scanCharacter
from backend.lexer.scanners.scan_strings import scanString
from backend.lexer.scanners.scan_operator import scanOperator
from backend.lexer.scanners.scan_symbol import scanSymbol
from backend.lexer.scanners.scan_keywords import scanKeywords


class Lexer:
    def __init__(self, sourceCode):
        self.sourceCode = sourceCode.replace("\r", "")
        self.currentPosition = Position(-1, 1)
        self.currentCharacter = None
        self.advance()

    def peek_Non_Whitespace(self):
        nextCharacterIndex = self.currentPosition.index + 1

        while nextCharacterIndex < len(self.sourceCode):
            nextCharacter = self.sourceCode[nextCharacterIndex]

            if nextCharacter in (" ", "\t", "\n", "\r"):
                nextCharacterIndex = nextCharacterIndex + 1
                continue

            return nextCharacter

        return None

    def advance(self):
        self.currentPosition.advance(self.currentCharacter)

        if self.currentPosition.index < len(self.sourceCode):
            self.currentCharacter = self.sourceCode[self.currentPosition.index]
        else:
            self.currentCharacter = None

    def peek(self):
        nextCharacterIndex = self.currentPosition.index + 1

        if nextCharacterIndex < len(self.sourceCode):
            return self.sourceCode[nextCharacterIndex]

        return None

    def make_Tokens(self):
        tokenList = []
        errorList = []

        while self.currentCharacter is not None:

            # SPACES AND NEWLINES
            if self.currentCharacter == " ":
                tokenList.append(Token(TK_SYM_SPACE, " ", self.currentPosition.copy()))
                self.advance()
                continue

            if self.currentCharacter == "\t":
                tokenList.append(Token(TK_SYM_TAB, "\t", self.currentPosition.copy()))
                self.advance()
                continue

            if self.currentCharacter == "\n":
                tokenList.append(Token(TK_SYM_NEWLINE, "\n", self.currentPosition.copy()))
                self.advance()
                continue

            # COMMENTS
            if scanComment(self, tokenList, errorList):
                continue

            # NUMBERS
            if scanNumbers(self, tokenList, errorList):
                continue

            # STRINGS
            if self.currentCharacter == '"':
                if scanString(self, tokenList, errorList):
                    continue

            # CHARACTERS
            if self.currentCharacter == "'":
                if scanCharacter(self, tokenList, errorList):
                    continue

            # KEYWORDS
            if self.currentCharacter.isalpha():
                if scanKeywords(self, tokenList, errorList):
                    continue

            # IDENTIFIERS
            if scanIdentifier(self, tokenList, errorList):
                continue

            # OPERATORS
            try:
                if scanOperator(self, tokenList, errorList):
                    continue

            except LexicalError as lexicalError:
                errorList.append(lexicalError)

                if self.currentCharacter is not None:
                    self.advance()

                continue

            # SYMBOLS
            try:
                if scanSymbol(self, tokenList, errorList):
                    continue

            except LexicalError as lexicalError:
                errorList.append(lexicalError)

                if self.currentCharacter is not None:
                    self.advance()

                continue

            # INVALID OR UNRECOGNIZED CHARACTER
            errorPosition = self.currentPosition.copy()
            unexpectedCharacter = self.currentCharacter

            errorList.append(
                LexicalError(
                    errorPosition,
                    f"Unexpected character '{unexpectedCharacter}'"
                )
            )

            self.advance()

        tokenList.append(Token(TK_EOF, None, self.currentPosition.copy()))

        return tokenList, errorList