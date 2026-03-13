from __future__ import annotations

from backend.ast.ast_nodes import (
    ArrayInit,
    BinaryExpr,
    CallExpr,
    GroupExpr,
    LiteralExpr,
    UnaryExpr,
    VarExpr,
    VerseOfExpr,
)
from backend.errors import RuntimeErrorBase

from .calls import _handle_call_expr
from .operators import _handle_unary_expr, _handle_binary_expr
from .primitives import _handle_primitive_expr

def _eval_expr(self, expression_node, current_environment):
    if expression_node is None:
        return None

    if isinstance(expression_node, (LiteralExpr, GroupExpr, VarExpr, ArrayInit, VerseOfExpr)):
        return _handle_primitive_expr(self, expression_node, current_environment)

    if isinstance(expression_node, CallExpr):
        return _handle_call_expr(self, expression_node, current_environment)

    if isinstance(expression_node, UnaryExpr):
        return _handle_unary_expr(self, expression_node, current_environment)

    if isinstance(expression_node, BinaryExpr):
        return _handle_binary_expr(self, expression_node, current_environment)

    raise RuntimeErrorBase(expression_node, "This expression is not yet supported during execution.")

def bind_expression_methods(cls):
    cls._eval_expr = _eval_expr
