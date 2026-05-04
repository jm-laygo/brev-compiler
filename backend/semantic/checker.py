from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from backend.semantic.typesys import Type
from backend.semantic.symbols import Scope, FunctionSymbol, OrderSymbol
from backend.errors import SemanticError

from backend.semantic.checker_parts import (
    CheckerConfig,
    formatType,
    isBadType,
    formatTypeForMessage,
    getBinaryOperationErrorMessage,
    hasTypeError,
    getTypeName,
    DeclarationsMixin,
    SuggestionsMixin,
    TypeBuildersMixin,
    InitializersMixin,
    ProgramFlowMixin,
    StatementsMixin,
    ExpressionsMixin,
    LValuesMixin,
    CallsMixin,
)


class SemanticChecker(
    DeclarationsMixin,
    SuggestionsMixin,
    TypeBuildersMixin,
    InitializersMixin,
    ProgramFlowMixin,
    StatementsMixin,
    ExpressionsMixin,
    LValuesMixin,
    CallsMixin,
):
    def __init__(self, config: Optional[CheckerConfig] = None):
        self.config = config or CheckerConfig()
        self.globalScope = Scope(None)
        self.orders: Dict[str, OrderSymbol] = {}
        self.functions: Dict[str, FunctionSymbol] = {}
        self.currentScope: Scope = self.globalScope
        self.currentFunction: Optional[FunctionSymbol] = None
        self.loopDepth: int = 0
        self.discernDepth: int = 0
        self.errorList: List[SemanticError] = []

    def check(self, programNode: Any) -> Tuple[Any, List[SemanticError]]:
        self.declareOrders(programNode)
        self.declareGlobals(programNode)
        self.declareFunctions(programNode)
        self.checkProgram(programNode)

        return programNode, self.errorList

    def addError(self, nodeOrToken: Any, message: str) -> None:
        self.errorList.extend([SemanticError(nodeOrToken, message)])

    def formatType(self, typeValue: Type) -> str:
        return formatType(typeValue)

    def isBadType(self, typeValue: Type) -> bool:
        return isBadType(typeValue)

    def formatTypeForMessage(self, typeValue: Type) -> str:
        return formatTypeForMessage(typeValue)

    def getBinaryOperationErrorMessage(
        self,
        operatorText: str,
        leftType: Type,
        rightType: Type
    ) -> str:
        return getBinaryOperationErrorMessage(operatorText, leftType, rightType)

    def hasTypeError(self, typeValue: Type) -> bool:
        return hasTypeError(typeValue)

    def getTypeName(self, typeValue: Type) -> str:
        return getTypeName(typeValue)