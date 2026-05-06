from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, getTokenValue, getTokenPosition


def parseDeclarationStatement(self: Parser) -> Statement:
    currentTokenType = self.currentType(0)

    # variable declaration
    if currentTokenType in (
        TK_DTYPE_TALLY,
        TK_DTYPE_DIVINE,
        TK_DTYPE_SIGIL,
        TK_DTYPE_SCRIPTURE,
        TK_DTYPE_VERITY,
    ):
        declarationStartToken = self.peek(0)

        declarationNode = VariableDeclaration(
            position=getTokenPosition(declarationStartToken),
            typeName=self.parseDataType(),
            items=self.parseVariableDeclarationGroup()
        )

        self.expect(TK_SYM_SEMICOL)

        return VariableDeclarationStatement(
            position=declarationNode.position,
            declaration=declarationNode
        )

    # ordain declaration
    if currentTokenType == TK_OTHERS_ORDAIN:
        ordainToken = self.expect(TK_OTHERS_ORDAIN)
        declarationName = getTokenValue(self.expect(TK_IDENTIFIER))
        declarationItems = self.parseOrdainDeclarationList()
        self.expect(TK_SYM_SEMICOL)

        return OrdainDeclarationStatement(
            position=getTokenPosition(ordainToken),
            declaration=OrdainDeclaration(
                position=getTokenPosition(ordainToken),
                name=declarationName,
                items=declarationItems
            )
        )

    # order declaration
    if currentTokenType == TK_OTHERS_ORDER:
        orderToken = self.expect(TK_OTHERS_ORDER)
        declarationName = getTokenValue(self.expect(TK_IDENTIFIER))
        self.expect(TK_SYM_OPBRACE)
        memberList = self.parseMemberListOptional()
        self.expect(TK_SYM_CLSBRACE)
        self.expect(TK_SYM_SEMICOL)

        return OrderDeclarationStatement(
            position=getTokenPosition(orderToken),
            declaration=OrderDeclaration(
                position=getTokenPosition(orderToken),
                name=declarationName,
                members=memberList
            )
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        list(PREDICT["<statement>"].keys())
    )

Parser.parseDeclarationStatement = parseDeclarationStatement