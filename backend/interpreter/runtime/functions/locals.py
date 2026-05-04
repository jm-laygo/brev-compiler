from __future__ import annotations

from backend.ast.ast_nodes import (
    OrderDeclaration,
    OrdainDeclaration,
    SacredDeclaration,
    VariableDeclaration,
)


# local declarations
def executeLocalDeclarations(self, localDeclarations, riteEnvironment):
    for localDeclaration in localDeclarations:
        if isinstance(localDeclaration, SacredDeclaration):
            self.executeSacredDeclaration(
                localDeclaration,
                riteEnvironment
            )

        elif isinstance(localDeclaration, VariableDeclaration):
            self.executeVariableDeclaration(
                localDeclaration,
                riteEnvironment
            )

        elif isinstance(localDeclaration, OrdainDeclaration):
            self.executeOrdainDeclaration(
                localDeclaration,
                riteEnvironment
            )

        elif isinstance(localDeclaration, OrderDeclaration):
            self.orderDeclarations[localDeclaration.name] = localDeclaration