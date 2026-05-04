from __future__ import annotations
from typing import Any

from ..conditionals import DecreeChainMixin, DiscernFlowMixin
from ..helpers import getClassName
from ..loops import LoopStatementsMixin
from .actions import StatementActionsMixin
from .declarations import StatementDeclarationsMixin
from .mutations import StatementMutationsMixin


class StatementsMixin(
    StatementDeclarationsMixin,
    StatementMutationsMixin,
    StatementActionsMixin,
    DecreeChainMixin,
    DiscernFlowMixin,
    LoopStatementsMixin,
):
    statementHandlers = {
        "VariableDeclarationStatement": "checkVariableDeclarationStatement",
        "OrdainDeclarationStatement": "checkOrdainDeclarationStatement",
        "OrderDeclarationStatement": "checkOrderDeclarationStatement",
        "AssignmentStatement": "checkAssignmentStatement",
        "IncrementDecrementStatement": "checkIncrementDecrementStatement",
        "FunctionCallStatement": "checkFunctionCallStatement",
        "ReceiveStatement": "checkReceiveStatement",
        "ProclaimStatement": "checkProclaimStatement",
        "DecreeStatement": "checkDecreeStatement",
        "EdictClause": "checkEdictClause",
        "AbsolutionClause": "checkAbsolutionClause",
        "DiscernStatement": "checkDiscernStatement",
        "VerseCase": "checkVerseCase",
        "GraceDefault": "checkGraceDefault",
        "ProcessionStatement": "checkProcessionStatement",
        "EndureStatement": "checkEndureStatement",
        "RitualStatement": "checkRitualStatement",
        "ProceedStatement": "checkProceedStatement",
        "FallStatement": "checkFallStatement",
        "AbsolveStatement": "checkAbsolveStatement",
        "DismissStatement": "checkDismissStatement",
    }

    def checkStatement(self, statementNode: Any) -> None:
        statementKind = getClassName(statementNode)

        handlerName = self.statementHandlers.get(statementKind)

        if handlerName is None:
            return

        statementHandler = getattr(self, handlerName)
        statementHandler(statementNode)