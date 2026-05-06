from __future__ import annotations
from typing import Any

from ..conditions_checks import DecreeChainMixin, DiscernFlowMixin
from ..helper_functions import getClassName
from ..loop_checks import LoopStatementsMixin
from .input_output_and_returns import StatementActionsMixin
from .declaration_statements import StatementDeclarationsMixin
from .assignment_checks import StatementMutationsMixin


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