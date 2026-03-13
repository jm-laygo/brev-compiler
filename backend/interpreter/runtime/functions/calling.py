from __future__ import annotations

from backend.interpreter.control import AbsolveSignal, DismissSignal, FallSignal, ProceedSignal
from backend.interpreter.environment import Environment
from backend.errors import RuntimeErrorBase, RuntimeNameError

# CALLING RITES
def _call_rite(self, rite_name: str, argument_values, *, call_node=None):
    rite_node = self.rites.get(rite_name)
    if rite_node is None:
        raise RuntimeNameError(call_node, f"Undefined rite '{rite_name}'.")

    rite_environment = Environment(parent=self.globals)

    parameter_nodes = getattr(rite_node, "params", []) or []
    if len(argument_values) != len(parameter_nodes):
        raise RuntimeErrorBase(
            call_node,
            f"Rite '{rite_name}' expected {len(parameter_nodes)} argument(s), but received {len(argument_values)}.",
        )

    for parameter_node, argument_value in zip(parameter_nodes, argument_values):
        rite_environment.declare(parameter_node.name, argument_value, is_const=False)

    self._exec_local_declarations(getattr(rite_node, "local_decls", []) or [], rite_environment)

    try:
        rite_body_statements = getattr(rite_node, "body", []) or []
        self._exec_block(rite_body_statements, rite_environment, create_scope=False)

        final_dismiss_statement = getattr(rite_node, "dismiss", None)
        if final_dismiss_statement is not None:
            self._exec_stmt(final_dismiss_statement, rite_environment)

    except DismissSignal as dismiss_signal:
        return dismiss_signal.value
    except ProceedSignal:
        raise RuntimeErrorBase(call_node or rite_node, "'proceed' may only be used inside loops.")
    except FallSignal:
        raise RuntimeErrorBase(call_node or rite_node, "'fall' may only be used inside loops or valid discern flow.")
    except AbsolveSignal:
        raise RuntimeErrorBase(call_node or rite_node, "'absolve' may only be used inside discern statements.")

    return None
