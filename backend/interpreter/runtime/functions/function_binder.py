from __future__ import annotations

from .function_calls import callRite
from .local_declaration import executeLocalDeclarations


def bindFunctionMethods(interpreterClass):
    interpreterClass.callRite = callRite
    interpreterClass.executeLocalDeclarations = executeLocalDeclarations