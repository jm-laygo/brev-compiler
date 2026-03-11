from __future__ import annotations

from backend.ast.ast_nodes import (
    AbsolutionClause,
    AbsolveStmt,
    AssignStmt,
    CallStmt,
    DecreeStmt,
    DismissStmt,
    DiscernStmt,
    EdictClause,
    EndureStmt,
    FallStmt,
    IncDecStmt,
    OrdainStmt,
    OrderStmt,
    ProcessionStmt,
    ProclaimStmt,
    ProceedStmt,
    ReceiveStmt,
    RitualStmt,
    VarDeclStmt,
    VerseEnd,
    IdentifierRef,
)
from backend.interpreter.environment import Environment
from backend.interpreter.control import (
    AbsolveSignal,
    DismissSignal,
    FallSignal,
    ProceedSignal,
)
from backend.errors import (
    DivisionByZeroRuntimeError,
    RuntimeErrorBase,
    RuntimeTypeError,
)

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

    # DECLARATION STATEMENTS
    if isinstance(statement_node, VarDeclStmt):
        self._exec_var_decl(statement_node.decl, current_environment)
        return

    if isinstance(statement_node, OrderStmt):
        self.orders[statement_node.decl.name] = statement_node.decl
        return

    if isinstance(statement_node, OrdainStmt):
        self._exec_ordain_decl(statement_node.decl, current_environment)
        return

    # ASSIGNMENT
    if isinstance(statement_node, AssignStmt):
        assigned_value = self._eval_expr(statement_node.value, current_environment)
        assignment_operator = getattr(statement_node, "op", "=")

        if assignment_operator == "=":
            self._assign_lvalue(statement_node.target, assigned_value, current_environment, statement_node)
            return

        current_target_value = self._read_lvalue(statement_node.target, current_environment)

        if assignment_operator == "+=":
            computed_result = current_target_value + assigned_value
        elif assignment_operator == "-=":
            computed_result = current_target_value - assigned_value
        elif assignment_operator == "*=":
            computed_result = current_target_value * assigned_value
        elif assignment_operator == "/=":
            if assigned_value == 0:
                raise DivisionByZeroRuntimeError(statement_node, "Division by zero.")
            computed_result = current_target_value / assigned_value
        elif assignment_operator == "%=":
            if assigned_value == 0:
                raise DivisionByZeroRuntimeError(statement_node, "Modulo by zero.")
            computed_result = current_target_value % assigned_value
        elif assignment_operator == "**=":
            computed_result = current_target_value ** assigned_value
        else:
            raise RuntimeErrorBase(
                statement_node,
                f"Assignment operator '{assignment_operator}' is not supported during execution."
            )

        self._assign_lvalue(statement_node.target, computed_result, current_environment, statement_node)
        return

    # INC / DEC
    if isinstance(statement_node, IncDecStmt):
        current_target_value = self._read_lvalue(statement_node.target, current_environment)

        if not isinstance(current_target_value, (int, float)):
            raise RuntimeTypeError(statement_node, "Increment and decrement require a numeric variable.")

        if statement_node.op == "++":
            self._assign_lvalue(statement_node.target, current_target_value + 1, current_environment, statement_node)
            return

        if statement_node.op == "--":
            self._assign_lvalue(statement_node.target, current_target_value - 1, current_environment, statement_node)
            return

        raise RuntimeErrorBase(statement_node, "Unsupported increment/decrement operator.")

    # CALL / IO
    if isinstance(statement_node, CallStmt):
        evaluated_argument_values = []
        for argument_node in statement_node.args:
            evaluated_argument_values.append(self._eval_expr(argument_node, current_environment))

        self._call_rite(statement_node.callee, evaluated_argument_values, call_node=statement_node)
        return

    if isinstance(statement_node, ReceiveStmt):
        raw_input_value = self.input_provider(statement_node.target)
        converted_input_value = self._convert_input_for_target(
            statement_node.target,
            raw_input_value,
            current_environment,
        )
        self._assign_lvalue(statement_node.target, converted_input_value, current_environment, statement_node)
        return

    if isinstance(statement_node, ProclaimStmt):
        output_parts = []
        for argument_node in statement_node.args:
            evaluated_value = self._eval_expr(argument_node, current_environment)
            output_parts.append(self.stringify(evaluated_value))
        self._write_inline("".join(output_parts))
        return

    # CONDITIONALS
    if isinstance(statement_node, DecreeStmt):
        decree_condition_value = self._eval_expr(statement_node.expr, current_environment)

        if self._truthy(decree_condition_value):
            self._exec_block(statement_node.body, current_environment)
            return

        edict_clauses = getattr(statement_node, "edicts", []) or []
        for edict_clause in edict_clauses:
            edict_condition_value = self._eval_expr(edict_clause.expr, current_environment)

            if self._truthy(edict_condition_value):
                self._exec_block(edict_clause.body, current_environment)
                return

        absolution_clause = getattr(statement_node, "absolution", None)
        if absolution_clause is not None:
            self._exec_block(absolution_clause.body, current_environment)

        return

    if isinstance(statement_node, DiscernStmt):
        discern_value = self._eval_expr(statement_node.expr, current_environment)
        has_matched_case = False

        verse_cases = getattr(statement_node, "verses", []) or []
        for verse_case in verse_cases:
            verse_match_value = self._eval_verse_match(verse_case.match, current_environment)

            if has_matched_case or discern_value == verse_match_value:
                has_matched_case = True

                try:
                    self._exec_block(verse_case.body, current_environment)

                    if getattr(verse_case, "end", None) is not None:
                        self._handle_verse_end(verse_case.end)

                except FallSignal:
                    break
                except AbsolveSignal:
                    break

        grace_clause = getattr(statement_node, "grace", None)
        if (not has_matched_case) and grace_clause is not None:
            try:
                self._exec_block(grace_clause.body, current_environment)

                if getattr(grace_clause, "end", None) is not None:
                    self._handle_verse_end(grace_clause.end)

            except FallSignal:
                pass
            except AbsolveSignal:
                pass

        return

    # LOOPS
    if isinstance(statement_node, ProcessionStmt):
        loop_environment = Environment(parent=current_environment)

        initialization_statement = getattr(statement_node, "init", None)
        loop_condition_expression = getattr(statement_node, "condition", None)
        update_statement = getattr(statement_node, "update", None)
        body_statements = getattr(statement_node, "body", []) or []

        if initialization_statement is not None:
            self._exec_stmt(initialization_statement, loop_environment)

        while True:
            if loop_condition_expression is not None:
                loop_condition_value = self._eval_expr(loop_condition_expression, loop_environment)
                if not self._truthy(loop_condition_value):
                    break

            try:
                self._exec_block(body_statements, loop_environment, create_scope=True)
            except ProceedSignal:
                pass
            except FallSignal:
                break

            if update_statement is not None:
                self._exec_stmt(update_statement, loop_environment)

        return

    if isinstance(statement_node, EndureStmt):
        while self._truthy(self._eval_expr(statement_node.condition, current_environment)):
            try:
                self._exec_block(statement_node.body, current_environment)
            except ProceedSignal:
                continue
            except FallSignal:
                break
        return

    if isinstance(statement_node, RitualStmt):
        while True:
            try:
                self._exec_block(statement_node.body, current_environment)
            except ProceedSignal:
                pass
            except FallSignal:
                break

            ritual_condition_value = self._eval_expr(statement_node.condition, current_environment)
            if not self._truthy(ritual_condition_value):
                break

        return

    # CONTROL TRANSFER
    if isinstance(statement_node, ProceedStmt):
        raise ProceedSignal()

    if isinstance(statement_node, FallStmt):
        raise FallSignal()

    if isinstance(statement_node, AbsolveStmt):
        raise AbsolveSignal()

    if isinstance(statement_node, DismissStmt):
        dismiss_value_node = getattr(statement_node, "value", None)
        if dismiss_value_node is not None:
            dismiss_value = self._eval_expr(dismiss_value_node, current_environment)
        else:
            dismiss_value = None

        raise DismissSignal(dismiss_value)

    # SUPPORT CLAUSES
    if isinstance(statement_node, EdictClause):
        edict_condition_value = self._eval_expr(statement_node.expr, current_environment)
        if self._truthy(edict_condition_value):
            self._exec_block(statement_node.body, current_environment)
        return

    if isinstance(statement_node, AbsolutionClause):
        self._exec_block(statement_node.body, current_environment)
        return

    raise RuntimeErrorBase(statement_node, "This statement is not yet supported during execution.")

def _truthy(self, value) -> bool:
    if isinstance(value, bool):
        return value
    return bool(value)

def _eval_verse_match(self, match_node, current_environment: Environment):
    if isinstance(match_node, IdentifierRef):
        return current_environment.get(match_node.name, node=match_node)
    return self._eval_expr(match_node, current_environment)

def _handle_verse_end(self, verse_end_node: VerseEnd):
    end_kind = (getattr(verse_end_node, "kind", "") or "").lower()

    if end_kind == "fall":
        raise FallSignal()

    if end_kind == "absolve":
        raise AbsolveSignal()

def bind_statement_methods(cls):
    cls._exec_block = _exec_block
    cls._exec_stmt = _exec_stmt
    cls._truthy = _truthy
    cls._eval_verse_match = _eval_verse_match
    cls._handle_verse_end = _handle_verse_end