from __future__ import annotations

from backend.ast.ast_nodes import (
    Program,
    OrderDeclaration,
    SacredDeclaration,
    VariableDeclaration,
)
from backend.errors import RuntimeErrorBase, InputConversionRuntimeError


def run(self, programNode: Program):
    self.registerProgram(programNode)

    entryRite = getattr(programNode, "entryRite", None)

    if entryRite is None:
        raise RuntimeErrorBase(
            programNode,
            "No entry rite was found."
        )

    entryRiteName = getattr(entryRite, "name", None)

    if not entryRiteName:
        raise RuntimeErrorBase(
            programNode,
            "Entry rite has no valid name."
        )

    return self.callRite(
        entryRiteName,
        [],
        callNode=entryRite
    )


def defaultInputProvider(self, targetNode=None):
    raise InputConversionRuntimeError(
        targetNode,
        "Input was requested during execution, but no runtime input provider was supplied."
    )


def registerProgram(self, programNode: Program):
    globalDeclarations = getattr(programNode, "globalDeclarations", []) or []

    # register global order types first so variables can use them as types
    for globalDeclaration in globalDeclarations:
        if isinstance(globalDeclaration, OrderDeclaration):
            self.orderDeclarations[globalDeclaration.name] = globalDeclaration

    entryRite = getattr(programNode, "entryRite", None)

    if entryRite is not None:
        self.riteDeclarations[entryRite.name] = entryRite

    functionRites = getattr(programNode, "riteDeclarations", []) or []

    for functionRite in functionRites:
        self.riteDeclarations[functionRite.name] = functionRite

    # execute only valid global declarations
    for globalDeclaration in globalDeclarations:
        if isinstance(globalDeclaration, SacredDeclaration):
            self.executeSacredDeclaration(
                globalDeclaration,
                self.globalEnvironment
            )

        elif isinstance(globalDeclaration, VariableDeclaration):
            self.executeVariableDeclaration(
                globalDeclaration,
                self.globalEnvironment
            )

        elif isinstance(globalDeclaration, OrderDeclaration):
            pass


def bindProgramMethods(interpreterClass):
    interpreterClass.run = run
    interpreterClass.defaultInputProvider = defaultInputProvider
    interpreterClass.registerProgram = registerProgram