from __future__ import annotations
from typing import Any, List

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *

def getTokenValue(token):
    return getattr(token, "value", None)

def getTokenPosition(token):
    return getattr(token, "position", None)

class Parser:
    def __init__(self, tokenList: List[Any]):
        self.tokenList = tokenList
        self.currentTokenIndex = 0

    def isAtEnd(self) -> bool:
        return self.currentTokenIndex >= len(self.tokenList)

    def peek(self, offset: int = 0) -> Any:
        targetIndex = self.currentTokenIndex + offset

        if targetIndex < 0 or targetIndex >= len(self.tokenList):
            return None

        return self.tokenList[targetIndex]

    def currentType(self, offset: int = 0) -> Any:
        currentToken = self.peek(offset)

        if currentToken is None:
            return None

        return getattr(currentToken, "type", None)

    def advance(self) -> Any:
        currentToken = self.peek(0)
        self.currentTokenIndex += 1

        return currentToken

    def expect(self, expectedTokenType):
        currentToken = self.peek(0)

        # no more token
        if currentToken is None:
            raise ParserError(
                self.peek(-1),
                expectedTokenType,
                "Unexpected end of input"
            )

        # wrong token
        if currentToken.type != expectedTokenType:
            raise ParserError(
                currentToken,
                expectedTokenType
            )

        return self.advance()

    def accept(self, expectedTokenType: Any):
        # optional token
        if self.currentType(0) == expectedTokenType:
            return self.advance()

        return None

    def chooseProduction(self, nonTerminal: str):
        currentTokenType = self.currentType(0)
        predictTable = PREDICT.get(nonTerminal)

        # missing table
        if predictTable is None:
            currentToken = self.peek(0) or self.peek(-1)

            raise ParserError(
                currentToken,
                [],
                f"Missing PREDICT entry for {nonTerminal}"
            )

        production = predictTable.get(currentTokenType)

        # no matching production
        if production is None:
            currentToken = self.peek(0) or self.peek(-1)
            expectedTokenList = list(predictTable.keys())

            raise ParserError(
                currentToken,
                expectedTokenList
            )

        return production

    def raiseExpectedError(self, expectedTokenList, errorDetails="Invalid syntax"):
        currentToken = self.peek(0) or self.peek(-1)

        raise ParserError(
            currentToken,
            expectedTokenList,
            errorDetails
        )

    def parse(self) -> Program:
        # parser entry
        return self.parseProgram()

    def parseProgram(self) -> Program:
        currentTokenType = self.currentType(0)

        # invalid start
        if currentTokenType != TK_EOF and currentTokenType not in PREDICT["<program>"]:
            raise ParserError(
                self.peek(0) or self.peek(-1),
                list(PREDICT["<program>"].keys())
            )

        programNode = Program(position=getTokenPosition(self.peek(0)))
        programNode.globalDeclarations = []
        programNode.riteDeclarations = []
        programNode.entryRite = None

        # parse until eof
        while self.currentType(0) != TK_EOF:
            currentTokenType = self.currentType(0)

            # rite section
            if currentTokenType == TK_CF_RITE:
                entryRite, functionNodeList = self.parseRiteSequence()

                if entryRite is not None:
                    if programNode.entryRite is not None:
                        raise ParserError(
                            self.peek(-1),
                            [],
                            "Multiple genesis() rites are not allowed"
                        ) 

                    programNode.entryRite = entryRite

                programNode.riteDeclarations.extend(functionNodeList)
                continue

            # global declaration
            if currentTokenType in PREDICT["<global_dec_item>"]:
                programNode.globalDeclarations.append(self.parseGlobalDeclarationItem())
                continue

            raise ParserError(
                self.peek(0),
                list(PREDICT["<global_dec_item>"].keys()) + [TK_CF_RITE, TK_EOF]
            )

        # no genesis
        if programNode.entryRite is None:
            raise ParserError(
                self.peek(0) or self.peek(-1),
                [TK_OTHERS_GENESIS]
            )

        return programNode


import backend.parser.parsers.declarations as globalsParserModule
import backend.parser.parsers.functions as ritesParserModule
import backend.parser.parsers.statements as statementsParserModule
import backend.parser.parsers.lvalues as lvaluesParserModule
import backend.parser.parsers.expressions as expressionsParserModule

from backend.parser.token_filter import filterParserTokens


def parseTokensToAst(tokenList: List[Any]) -> Program:
    filteredTokenList = filterParserTokens(tokenList)
    return Parser(filteredTokenList).parse()


def validate(tokenList):
    filteredTokenList = filterParserTokens(tokenList)

    parser = Parser(filteredTokenList)
    abstractSyntaxTree = parser.parse()

    # extra token after parse
    if parser.currentType(0) != TK_EOF:
        raise ParserError(
            parser.peek(0),
            [TK_EOF],
            "Trailing tokens"
        )

    return abstractSyntaxTree