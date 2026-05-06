from __future__ import annotations
from typing import Any

from ..helper_functions import getClassName


class GlobalDeclarationsMixin:
    def declareGlobals(self, programNode: Any) -> None:
        globalDeclarations = getattr(programNode, "globalDeclarations", []) or []

        for globalDeclaration in globalDeclarations:
            declarationKind = getClassName(globalDeclaration)

            if declarationKind in ("VariableDeclaration", "SacredDeclaration"):
                self.declareVariableDeclaration(globalDeclaration, isGlobal=True)

            elif declarationKind == "OrderDeclaration":
                continue