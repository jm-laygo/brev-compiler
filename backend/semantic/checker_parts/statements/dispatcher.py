from __future__ import annotations
from typing import Any

from ..conditionals import DecreeChainMixin, DiscernFlowMixin
from ..helpers import _class
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
    _STATEMENT_HANDLERS = {
        "VarDeclStmt": "_check_vardeclstmt",
        "OrdainStmt": "_check_ordainstmt",
        "OrderStmt": "_check_orderstmt",
        "AssignStmt": "_check_assignstmt",
        "IncDecStmt": "_check_incdecstmt",
        "CallStmt": "_check_callstmt",
        "ReceiveStmt": "_check_receivestmt",
        "ProclaimStmt": "_check_proclaimstmt",
        "DecreeStmt": "_check_decreestmt",
        "EdictClause": "_check_edictclause",
        "AbsolutionClause": "_check_absolutionclause",
        "DiscernStmt": "_check_discernstmt",
        "VerseCase": "_check_versecase",
        "VerseEnd": "_check_verseend",
        "GraceDefault": "_check_gracedefault",
        "ProcessionStmt": "_check_processionstmt",
        "EndureStmt": "_check_endurestmt",
        "RitualStmt": "_check_ritualstmt",
        "ProceedStmt": "_check_proceedstmt",
        "FallStmt": "_check_fallstmt",
        "AbsolveStmt": "_check_absolvestmt",
        "DismissStmt": "_check_dismissstmt",
    }

    def _check_stmt(self, statement_node: Any) -> None:
        statement_kind = _class(statement_node)
        handler_name = self._STATEMENT_HANDLERS.get(statement_kind)
        if handler_name is None:
            return
        getattr(self, handler_name)(statement_node)
