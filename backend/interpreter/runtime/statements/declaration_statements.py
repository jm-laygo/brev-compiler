from __future__ import annotations

from backend.ast.ast_nodes import (
    OrdainDeclarationStatement,
    OrderDeclarationStatement,
    VariableDeclarationStatement,
)


def handleDeclarationStatement(self, statementNode, currentEnvironment):
    if isinstance(statementNode, VariableDeclarationStatement):
        self.executeVariableDeclaration(
            statementNode.declaration,
            currentEnvironment
        )

        return True

    if isinstance(statementNode, OrderDeclarationStatement):
        self.orderDeclarations[statementNode.declaration.name] = statementNode.declaration

        return True

    if isinstance(statementNode, OrdainDeclarationStatement):
        self.executeOrdainDeclaration(
            statementNode.declaration,
            currentEnvironment
        )

        return True

    return False