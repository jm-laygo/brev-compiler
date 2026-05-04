from __future__ import annotations

from backend.interpreter.environment import Environment
from backend.errors import RuntimeErrorBase

from .assignments import handleAssignmentIncrementDecrementStatement
from .conditionals import (
    evaluateVerseMatch,
    handleConditionalStatement,
    handleVerseEnd,
    isTruthy,
)
from .control import handleControlStatement
from .declarations import handleDeclarationStatement
from .io import handleInputOutputStatement
from .loops import handleLoopStatement


def executeBlock(self, statementNodes, currentEnvironment: Environment, *, createScope=True):
    if createScope:
        blockEnvironment = Environment(parentEnvironment=currentEnvironment)
    else:
        blockEnvironment = currentEnvironment

    for statementNode in statementNodes or []:
        self.executeStatement(statementNode, blockEnvironment)

def executeStatement(self, statementNode, currentEnvironment: Environment):
    if statementNode is None:
        return

    if handleDeclarationStatement(self, statementNode, currentEnvironment):
        return

    if handleAssignmentIncrementDecrementStatement(self, statementNode, currentEnvironment):
        return

    if handleInputOutputStatement(self, statementNode, currentEnvironment):
        return

    if handleConditionalStatement(self, statementNode, currentEnvironment):
        return

    if handleLoopStatement(self, statementNode, currentEnvironment):
        return

    if handleControlStatement(self, statementNode, currentEnvironment):
        return

    raise RuntimeErrorBase(
        statementNode,
        "This statement is not yet supported during execution."
    )

def bindStatementMethods(interpreterClass):
    interpreterClass.executeBlock = executeBlock
    interpreterClass.executeStatement = executeStatement
    interpreterClass.isTruthy = isTruthy
    interpreterClass.evaluateVerseMatch = evaluateVerseMatch
    interpreterClass.handleVerseEnd = handleVerseEnd