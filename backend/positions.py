class Position:
    def __init__(self, characterIndex, lineNumber, columnNumber=0):
        self.characterIndex = characterIndex
        self.lineNumber = lineNumber
        self.columnNumber = columnNumber

    def advance(self, currentCharacter):
        self.characterIndex += 1

        if currentCharacter == "\n":
            self.lineNumber += 1
            self.columnNumber = 1

        else:
            self.columnNumber += 1

    def copy(self):
        return Position(
            self.characterIndex,
            self.lineNumber,
            self.columnNumber
        )