from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from backend.semantic.typesys import Type
from backend.semantic.symbols import Scope, FuncSymbol, OrderSymbol
from backend.errors import SemanticError

from backend.semantic.checker_parts import (
    CheckerConfig,

    _fmt_type,
    _is_bad,
    _fmt_type_for_msg,
    _binop_error_msg,
    _has_type_error,
    _tname,

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

        self.global_scope = Scope(None)
        self.orders: Dict[str, OrderSymbol] = {}
        self.funcs: Dict[str, FuncSymbol] = {}

        self.scope: Scope = self.global_scope
        self.current_func: Optional[FuncSymbol] = None
        self.in_loop: int = 0
        self.in_discern: int = 0

        self.errors: List[SemanticError] = []

    def check(self, program_node: Any) -> Tuple[Any, List[SemanticError]]:
        self._declare_orders(program_node)
        self._declare_globals(program_node)
        self._declare_functions(program_node)
        self._check_program(program_node)
        return program_node, self.errors

    def _error(self, node_or_token: Any, message: str) -> None:
        self.errors.append(SemanticError(node_or_token, message))

    def _fmt_type(self, type_value: Type) -> str:
        return _fmt_type(type_value)

    def _is_bad(self, type_value: Type) -> bool:
        return _is_bad(type_value)

    def _fmt_type_for_msg(self, type_value: Type) -> str:
        return _fmt_type_for_msg(type_value)

    def _binop_error_msg(self, operator_text: str, left_type: Type, right_type: Type) -> str:
        return _binop_error_msg(operator_text, left_type, right_type)

    def _has_type_error(self, type_value: Type) -> bool:
        return _has_type_error(type_value)

    def _tname(self, type_value: Type) -> str:
        return _tname(type_value)