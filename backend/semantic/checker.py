from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from backend.semantic.typesys import Type
from backend.semantic.symbols import Scope, FuncSymbol, OrderSymbol
from backend.errors import SemanticError

from backend.semantic.checker_parts import (
    CheckerConfig,

    # diagnostics helpers
    _fmt_type, _is_bad, _fmt_type_for_msg,
    _binop_error_msg, _has_type_error, _tname,

    # mixins
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
        self.cfg = config or CheckerConfig()

        self.global_scope = Scope(None)
        self.orders: Dict[str, OrderSymbol] = {}
        self.funcs: Dict[str, FuncSymbol] = {}

        self.scope: Scope = self.global_scope
        self.current_func: Optional[FuncSymbol] = None
        self.in_loop: int = 0
        self.in_discern: int = 0

        self.errors: List[SemanticError] = []

    def check(self, program: Any) -> Tuple[Any, List[SemanticError]]:
        # collect symbols
        self._declare_globals(program)
        self._declare_orders(program)
        self._declare_functions(program)

        # validate program (from ProgramFlowMixin)
        self._check_program(program)

        return program, self.errors

    # error sink used by all mixins
    def _error(self, node_or_token: Any, msg: str) -> None:
        self.errors.append(SemanticError(node_or_token, msg))

    def _fmt_type(self, t: Type) -> str:
        return _fmt_type(t)

    def _is_bad(self, t: Type) -> bool:
        return _is_bad(t)

    def _fmt_type_for_msg(self, t: Type) -> str:
        return _fmt_type_for_msg(t)

    def _binop_error_msg(self, op: str, lt: Type, rt: Type) -> str:
        return _binop_error_msg(op, lt, rt)

    def _has_type_error(self, t: Type) -> bool:
        return _has_type_error(t)

    def _tname(self, t: Type) -> str:
        return _tname(t)