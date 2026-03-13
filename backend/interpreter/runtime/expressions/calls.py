from __future__ import annotations

from backend.ast.ast_nodes import CallExpr

def _handle_call_expr(self, expression_node, current_environment):
    if not isinstance(expression_node, CallExpr):
        return None

    evaluated_argument_values = []
    for argument_node in expression_node.args:
        evaluated_argument_values.append(self._eval_expr(argument_node, current_environment))

    call_result = self._call_rite(expression_node.callee, evaluated_argument_values, call_node=expression_node)

    call_access_chain = getattr(expression_node, "access", None)
    if call_access_chain is not None:
        return self._read_lvalue_from_value(call_access_chain, call_result, expression_node)

    return call_result
