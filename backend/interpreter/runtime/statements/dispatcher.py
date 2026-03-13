from __future__ import annotations

from backend.interpreter.environment import Environment
from backend.errors import RuntimeErrorBase

from .assignments import _handle_assign_incdec_stmt
from .conditionals import _eval_verse_match, _handle_conditional_stmt, _handle_verse_end, _truthy
from .control import _handle_control_stmt
from .declarations import _handle_decl_stmt
from .io import _handle_io_stmt
from .loops import _handle_loop_stmt


def _exec_block(self, statement_nodes, current_environment: Environment, *, create_scope=True):
    if create_scope:
        block_environment = Environment(parent=current_environment)
    else:
        block_environment = current_environment

    for statement_node in statement_nodes or []:
        self._exec_stmt(statement_node, block_environment)


def _exec_stmt(self, statement_node, current_environment: Environment):
    if statement_node is None:
        return

    if _handle_decl_stmt(self, statement_node, current_environment):
        return

    if _handle_assign_incdec_stmt(self, statement_node, current_environment):
        return

    if _handle_io_stmt(self, statement_node, current_environment):
        return

    if _handle_conditional_stmt(self, statement_node, current_environment):
        return

    if _handle_loop_stmt(self, statement_node, current_environment):
        return

    if _handle_control_stmt(self, statement_node, current_environment):
        return

    raise RuntimeErrorBase(statement_node, "This statement is not yet supported during execution.")


def bind_statement_methods(cls):
    cls._exec_block = _exec_block
    cls._exec_stmt = _exec_stmt
    cls._truthy = _truthy
    cls._eval_verse_match = _eval_verse_match
    cls._handle_verse_end = _handle_verse_end
