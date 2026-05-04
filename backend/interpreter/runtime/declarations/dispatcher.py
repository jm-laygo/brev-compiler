from __future__ import annotations

from .exec_decls import (
    executeOrdainDeclaration,
    executeSacredDeclaration,
    executeVariableDeclaration,
)
from .materialize import (
    getDefaultValueForType,
    makeArrayOf,
    makeOrderInstance,
    materializeVariableItem,
    requireIntegerDimension,
)


def bindDeclarationMethods(interpreterClass):
    interpreterClass.executeVariableDeclaration = executeVariableDeclaration
    interpreterClass.executeSacredDeclaration = executeSacredDeclaration
    interpreterClass.executeOrdainDeclaration = executeOrdainDeclaration
    interpreterClass.materializeVariableItem = materializeVariableItem
    interpreterClass.makeOrderInstance = makeOrderInstance
    interpreterClass.makeArrayOf = makeArrayOf
    interpreterClass.requireIntegerDimension = requireIntegerDimension
    interpreterClass.getDefaultValueForType = getDefaultValueForType