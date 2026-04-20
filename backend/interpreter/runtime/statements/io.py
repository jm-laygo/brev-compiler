from __future__ import annotations

from backend.ast.ast_nodes import CallStmt, ProclaimStmt, ReceiveStmt
from backend.errors import InputConversionRuntimeError, RuntimeErrorBase
from backend.interpreter.input_request import InputRequest


def _handle_io_stmt(self, statement_node, current_environment):
    if isinstance(statement_node, CallStmt):
        evaluated_argument_values = []
        for argument_node in statement_node.args:
            evaluated_argument_values.append(self._eval_expr(argument_node, current_environment))

        self._call_rite(statement_node.callee, evaluated_argument_values, call_node=statement_node)
        return True

    if isinstance(statement_node, ReceiveStmt):
        try:
            raw_input_value = self.input_provider(statement_node.target)
        except (InputRequest, RuntimeErrorBase):
            raise
        except Exception as exc:
            raise InputConversionRuntimeError(
                statement_node.target,
                f"Input provider failure: {type(exc).__name__}.",
            ) from exc
        converted_input_value = self._convert_input_for_target(
            statement_node.target,
            raw_input_value,
            current_environment,
        )
        self._assign_lvalue(statement_node.target, converted_input_value, current_environment, statement_node)
        return True

    if isinstance(statement_node, ProclaimStmt):
        output_parts = []
        for argument_node in statement_node.args:
            evaluated_value = self._eval_expr(argument_node, current_environment)
            output_parts.append(self.stringify(evaluated_value))
        self._write_inline("".join(output_parts))
        return True

    return False
