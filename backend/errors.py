from backend.tokens import TOKEN_DISPLAY_NAMES


def getLineAndColumn(position):
    # no position
    if position is None:
        return "?", "?"

    lineNumber = getattr(position, "lineNumber", "?")
    columnNumber = getattr(position, "columnNumber", "?")

    return lineNumber, columnNumber

def cleanErrorDetails(errorDetails):
    # show hidden chars
    errorDetails = errorDetails.replace("\n", "\\n")
    errorDetails = errorDetails.replace("\t", "\\t")
    errorDetails = errorDetails.replace("\r", "\\r")

    return errorDetails

def getPositionFromNode(nodeOrToken):
    # direct position
    if nodeOrToken is not None and hasattr(nodeOrToken, "lineNumber") and hasattr(nodeOrToken, "columnNumber"):
        return nodeOrToken

    # node or token position
    return getattr(nodeOrToken, "position", None)

def normalizeExpectedTokens(expectedTokens):
    # no expected token
    if expectedTokens is None:
        return []

    if isinstance(expectedTokens, list):
        return expectedTokens

    if isinstance(expectedTokens, (set, tuple)):
        return list(expectedTokens)

    return [expectedTokens]


def getTokenDisplayName(tokenType):
    # readable token name
    return TOKEN_DISPLAY_NAMES.get(tokenType, tokenType)

class LexicalError(Exception):
    def __init__(self, position, errorDetails: str, suggestion: str | None = None):
        super().__init__(errorDetails)

        self.position = position
        self.errorDetails = errorDetails
        self.suggestion = suggestion

    def asString(self) -> str:
        lineNumber, columnNumber = getLineAndColumn(self.position)
        cleanDetails = cleanErrorDetails(self.errorDetails)

        errorMessage = f"Ln {lineNumber}, Col {columnNumber} Lexical Error: {cleanDetails}"

        if self.suggestion:
            errorMessage = errorMessage + f" Did you mean '{self.suggestion}'?"

        return errorMessage

    def __str__(self) -> str:
        return self.asString()

class ParserError(Exception):
    def __init__(self, token, expectedTokens, errorDetails=None):
        super().__init__(errorDetails)

        self.token = token
        self.expectedTokens = normalizeExpectedTokens(expectedTokens)
        self.errorDetails = errorDetails

    def asString(self) -> str:
        tokenPosition = getattr(self.token, "position", None)
        lineNumber, columnNumber = getLineAndColumn(tokenPosition)

        if self.expectedTokens:
            expectedText = ", ".join(
                getTokenDisplayName(tokenType)
                for tokenType in self.expectedTokens
            )
        else:
            expectedText = None

        foundTokenType = getattr(self.token, "type", None)

        if foundTokenType:
            foundText = getTokenDisplayName(foundTokenType)
        else:
            foundText = "<?>"

        if expectedText is None and self.errorDetails:
            errorMessage = (
                f"Ln {lineNumber}, Col {columnNumber} Syntax Error: "
                f"{self.errorDetails}"
            )

        elif expectedText is None:
            errorMessage = (
                f"Ln {lineNumber}, Col {columnNumber} Syntax Error: "
                f"Unexpected token '{foundText}'."
            )

        else:
            errorMessage = (
                f"Ln {lineNumber}, Col {columnNumber} Syntax Error: "
                f"Expected {expectedText} but found '{foundText}'."
            )

            if self.errorDetails:
                errorMessage = errorMessage + f" ({self.errorDetails})"

        return errorMessage

    def __str__(self) -> str:
        return self.asString()

class SemanticError(Exception):
    def __init__(self, nodeOrToken, errorDetails: str):
        super().__init__(errorDetails)

        self.nodeOrToken = nodeOrToken
        self.errorDetails = errorDetails

    def asString(self) -> str:
        position = getPositionFromNode(self.nodeOrToken)
        lineNumber, columnNumber = getLineAndColumn(position)

        cleanDetails = cleanErrorDetails(self.errorDetails)

        return f"Ln {lineNumber}, Col {columnNumber} Semantic Error: {cleanDetails}"

    def __str__(self) -> str:
        return self.asString()

class RuntimeErrorBase(Exception):
    def __init__(self, nodeOrPosition=None, errorDetails: str = "Runtime error"):
        super().__init__(errorDetails)

        self.nodeOrPosition = nodeOrPosition
        self.errorDetails = errorDetails

    def asString(self) -> str:
        position = getPositionFromNode(self.nodeOrPosition)
        lineNumber, columnNumber = getLineAndColumn(position)

        cleanDetails = cleanErrorDetails(self.errorDetails)

        return f"Ln {lineNumber}, Col {columnNumber} Runtime Error: {cleanDetails}"

    def __str__(self) -> str:
        return self.asString()

class RuntimeNameError(RuntimeErrorBase):
    pass

class RuntimeTypeError(RuntimeErrorBase):
    pass

class DivisionByZeroRuntimeError(RuntimeErrorBase):
    pass

class IndexOutOfBoundsRuntimeError(RuntimeErrorBase):
    pass

class ConstAssignmentRuntimeError(RuntimeErrorBase):
    pass

class InvalidMemberAccessRuntimeError(RuntimeErrorBase):
    pass

class InputConversionRuntimeError(RuntimeErrorBase):
    pass