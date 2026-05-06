from __future__ import annotations
from typing import Any


class StatementDeclarationsMixin:
    def checkVariableDeclarationStatement(self, statementNode: Any) -> None:
        declarationNode = getattr(statementNode, "declaration", None)

        if declarationNode:
            self.declareVariableDeclaration(declarationNode, isGlobal=False)
            self.checkVariableDeclarationInitialValues(declarationNode)

    def checkOrdainDeclarationStatement(self, statementNode: Any) -> None:
        declarationNode = getattr(statementNode, "declaration", None)

        if declarationNode:
            self.declareOrdainDeclaration(declarationNode, isGlobal=False)
            self.checkOrdainDeclarationInitialValues(declarationNode)

    def checkOrderDeclarationStatement(self, statementNode: Any) -> None:
        self.addError(
            statementNode,
            "Order declarations are only allowed in the global declaration section."
        )