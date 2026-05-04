from __future__ import annotations

from .calling import callRite
from .locals import executeLocalDeclarations


def bindFunctionMethods(interpreterClass):
    interpreterClass.callRite = callRite
    interpreterClass.executeLocalDeclarations = executeLocalDeclarations