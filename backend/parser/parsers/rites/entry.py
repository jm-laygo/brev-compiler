from __future__ import annotations
from typing import List, Optional, Tuple

from backend.tokens import *
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseRiteSequence(self: Parser) -> Tuple[Optional[RiteDeclaration], List[RiteDeclaration]]:
    currentTokenType = self.currentType(0)

    # check rite sequence
    if currentTokenType not in PREDICT["<rite_seq>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<rite_seq>"].keys())
        )

    self.expect(TK_CF_RITE)
    returnTypeName = self.parseAnyReturnType()

    currentTokenType = self.currentType(0)

    # check rite name
    if currentTokenType not in PREDICT["<rite_after_type>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<rite_after_type>"].keys())
        )

    entryRite: Optional[RiteDeclaration] = None
    riteDeclarations: List[RiteDeclaration] = []

    # genesis rite
    if currentTokenType == TK_OTHERS_GENESIS:
        genesisToken = self.expect(TK_OTHERS_GENESIS)
        self.expect(TK_SYM_OPPAREN)
        self.expect(TK_SYM_CLSPAREN)
        self.expect(TK_SYM_OPBRACE)

        localDeclarations = self.parseMainLocalDeclarationOptional()
        statementList = self.parseStatementList()
        dismissStatement = self.parseDismissOptional()

        self.expect(TK_SYM_CLSBRACE)

        entryRite = RiteDeclaration(
            position=getTokenPosition(genesisToken),
            name="genesis",
            returnType=returnTypeName,
            parameters=[],
            localDeclarations=localDeclarations,
            bodyStatements=statementList,
            dismissStatement=dismissStatement
        )

        return entryRite, riteDeclarations

    # normal rite
    if currentTokenType == TK_IDENTIFIER:
        identifierToken = self.expect(TK_IDENTIFIER)
        riteName = getTokenValue(identifierToken)

        self.expect(TK_SYM_OPPAREN)
        parameterList = self.parseParameterListOptional()
        self.expect(TK_SYM_CLSPAREN)

        self.expect(TK_SYM_OPBRACE)
        localDeclarations = self.parseFunctionLocalDeclarationOptional()
        statementList = self.parseStatementList()
        dismissStatement = self.parseDismissOptional()
        self.expect(TK_SYM_CLSBRACE)

        riteDeclaration = RiteDeclaration(
            position=getTokenPosition(identifierToken),
            name=riteName,
            returnType=returnTypeName,
            parameters=parameterList,
            localDeclarations=localDeclarations,
            bodyStatements=statementList,
            dismissStatement=dismissStatement
        )

        riteDeclarations.extend([riteDeclaration])

        # next rite
        if self.currentType(0) == TK_CF_RITE:
            nextEntryRite, nextRiteDeclarations = self.parseRiteSequence()

            if nextEntryRite is not None and entryRite is None:
                entryRite = nextEntryRite

            riteDeclarations.extend(nextRiteDeclarations)

        return entryRite, riteDeclarations

    raise ParserError(
        self.peek(0) or self.peek(-1),
        list(PREDICT["<rite_after_type>"].keys())
    )

def parseAnyReturnType(self: Parser) -> str:
    currentTokenType = self.currentType(0)

    # check return type
    if currentTokenType not in PREDICT["<return_type_any>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            list(PREDICT["<return_type_any>"].keys())
        )

    # hollow return
    if currentTokenType == TK_DTYPE_HOLLOW:
        self.expect(TK_DTYPE_HOLLOW)
        return "hollow"

    return self.parseDataTypeIdentifier()

Parser.parseRiteSequence = parseRiteSequence
Parser.parseAnyReturnType = parseAnyReturnType