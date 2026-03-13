from __future__ import annotations

from backend.ast.ast_nodes import ArrayInit, GroupExpr, LiteralExpr, VarExpr, VerseOfExpr
from backend.errors import RuntimeTypeError

# PRIMITIVE EXPRESSIONS
def _handle_primitive_expr(self, expression_node, current_environment):
    if isinstance(expression_node, LiteralExpr):
        return expression_node.value

    if isinstance(expression_node, GroupExpr):
        return self._eval_expr(expression_node.expr, current_environment)

    if isinstance(expression_node, VarExpr):
        return self._read_lvalue(expression_node.ref, current_environment)

    if isinstance(expression_node, ArrayInit):
        evaluated_items = []
        for item_node in expression_node.items:
            evaluated_items.append(self._eval_expr(item_node, current_environment))
        return evaluated_items

    if isinstance(expression_node, VerseOfExpr):
        inner_value = self._eval_expr(expression_node.expr, current_environment)

        if isinstance(inner_value, list):
            return len(inner_value)

        if isinstance(inner_value, str):
            return len(inner_value)

        raise RuntimeTypeError(expression_node, "The verseof operator requires an array or scripture value.")

    return None
