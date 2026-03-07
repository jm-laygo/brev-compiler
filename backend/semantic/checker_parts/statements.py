from __future__ import annotations
from typing import Any

from backend.semantic.typesys import (
    BaseType,
    can_assign,
    is_numeric,
    is_bool,
)

from .helpers import _class

class StatementsMixin:
    def _check_stmt(self, statement_node: Any) -> None:
        statement_kind = _class(statement_node)

        if statement_kind == "VarDeclStmt":
            declaration_node = getattr(statement_node, "decl", None)
            if declaration_node:
                self._declare_var_decl(declaration_node, is_global=False)
                self._check_var_decl_init(declaration_node)
            return

        if statement_kind == "OrdainStmt":
            declaration_node = getattr(statement_node, "decl", None)
            if declaration_node:
                self._declare_ordain_decl(declaration_node, is_global=False)
                self._check_ordain_decl_init(declaration_node)
            return

        if statement_kind == "OrderStmt":
            self._error(statement_node, "order statement inside function is not supported in semantics yet.")
            return

        if statement_kind == "AssignStmt":
            target_reference = getattr(statement_node, "target", None)
            value_expression = getattr(statement_node, "value", None)
            operator_text = getattr(statement_node, "op", "=")

            from backend.semantic.symbols import VarSymbol
            root_symbol = self._lvalue_root_symbol(target_reference)

            if isinstance(root_symbol, VarSymbol) and getattr(root_symbol, "is_const", False):
                self._error(
                    target_reference if target_reference is not None else statement_node,
                    f"Cannot modify sacred constant '{root_symbol.name}'."
                )
                return

            target_type = self._lvalue_type(target_reference)
            value_type = self._expr_type(value_expression)

            if self._has_type_error(target_type) or self._has_type_error(value_type):
                return

            if operator_text != "=" and not is_numeric(target_type):
                self._error(
                    target_reference if target_reference is not None else statement_node,
                    f"Type error: '{operator_text}' requires numeric target, got {self._tname(target_type)}."
                )
                return

            if not can_assign(target_type, value_type):
                self._error(
                    value_expression if value_expression is not None else statement_node,
                    f"Type mismatch: cannot assign {self._tname(value_type)} to {self._tname(target_type)}."
                )
            return

        if statement_kind == "IncDecStmt":
            target_reference = getattr(statement_node, "target", None)

            from backend.semantic.symbols import VarSymbol
            root_symbol = self._lvalue_root_symbol(target_reference)

            if isinstance(root_symbol, VarSymbol) and getattr(root_symbol, "is_const", False):
                self._error(statement_node, f"Cannot increment/decrement sacred constant '{root_symbol.name}'.")
                return

            target_type = self._lvalue_type(target_reference)
            if not is_numeric(target_type):
                self._error(statement_node, f"++/-- requires numeric lvalue, got {target_type}.")
            return

        if statement_kind == "CallStmt":
            function_name = getattr(statement_node, "callee", None)
            argument_nodes = getattr(statement_node, "args", []) or []
            self._check_call(function_name, argument_nodes, statement_node)
            return

        if statement_kind == "ReceiveStmt":
            target_reference = getattr(statement_node, "target", None)

            from backend.semantic.symbols import VarSymbol
            root_symbol = self._lvalue_root_symbol(target_reference)

            if isinstance(root_symbol, VarSymbol) and getattr(root_symbol, "is_const", False):
                self._error(statement_node, f"Cannot store input into sacred constant '{root_symbol.name}'.")
                return

            self._lvalue_type(target_reference)
            return

        if statement_kind == "ProclaimStmt":
            argument_nodes = getattr(statement_node, "args", []) or []
            for argument_node in argument_nodes:
                self._expr_type(argument_node)
            return

        if statement_kind == "DecreeStmt":
            condition_expression = getattr(statement_node, "expr", None)
            condition_type = self._expr_type(condition_expression)

            if not is_bool(condition_type):
                self._error(condition_expression, f"Type error: decree condition must be verity, got {condition_type}.")

            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)

            edict_nodes = getattr(statement_node, "edicts", []) or []
            for edict_node in edict_nodes:
                self._check_stmt(edict_node)

            absolution_node = getattr(statement_node, "absolution", None)
            if absolution_node:
                self._check_stmt(absolution_node)

            return

        if statement_kind == "EdictClause":
            condition_expression = getattr(statement_node, "expr", None)
            condition_type = self._expr_type(condition_expression)

            if not is_bool(condition_type):
                self._error(statement_node, f"edict condition must be verity, got {condition_type}.")

            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)

            return

        if statement_kind == "AbsolutionClause":
            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)
            return

        if statement_kind == "DiscernStmt":
            self.in_discern += 1

            switch_expression = getattr(statement_node, "expr", None)
            self._expr_type(switch_expression)

            verse_nodes = getattr(statement_node, "verses", []) or []
            for verse_node in verse_nodes:
                self._check_stmt(verse_node)

            grace_node = getattr(statement_node, "grace", None)
            if grace_node:
                self._check_stmt(grace_node)

            self.in_discern -= 1
            return

        if statement_kind == "VerseCase":
            match_expression = getattr(statement_node, "match", None)
            self._expr_type(match_expression)

            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)

            end_node = getattr(statement_node, "end", None)
            if end_node:
                self._check_stmt(end_node)

            return

        if statement_kind == "VerseEnd":
            if self.in_discern <= 0:
                self._error(statement_node, "absolve/fall verse-end used outside discern.")
            return

        if statement_kind == "GraceDefault":
            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)
            return

        if statement_kind == "ProcessionStmt":
            self.in_loop += 1

            init_statement = getattr(statement_node, "init", None)
            if init_statement:
                self._check_stmt(init_statement)

            condition_expression = getattr(statement_node, "condition", None)
            if condition_expression:
                condition_type = self._expr_type(condition_expression)
                if not is_bool(condition_type):
                    self._error(statement_node, f"procession condition must be verity, got {condition_type}.")

            update_statement = getattr(statement_node, "update", None)
            if update_statement:
                self._check_stmt(update_statement)

            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)

            self.in_loop -= 1
            return

        if statement_kind == "EndureStmt":
            self.in_loop += 1

            condition_expression = getattr(statement_node, "condition", None)
            condition_type = self._expr_type(condition_expression)

            if not is_bool(condition_type):
                self._error(statement_node, f"endure condition must be verity, got {condition_type}.")

            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)

            self.in_loop -= 1
            return

        if statement_kind == "RitualStmt":
            self.in_loop += 1

            body_statements = getattr(statement_node, "body", []) or []
            for body_statement in body_statements:
                self._check_stmt(body_statement)

            condition_expression = getattr(statement_node, "condition", None)
            condition_type = self._expr_type(condition_expression)

            if not is_bool(condition_type):
                self._error(statement_node, f"ritual endure condition must be verity, got {condition_type}.")

            self.in_loop -= 1
            return

        if statement_kind == "ProceedStmt":
            if self.in_loop <= 0:
                self._error(statement_node, "proceed used outside a loop.")
            return

        if statement_kind == "FallStmt":
            if self.in_loop <= 0 and self.in_discern <= 0:
                self._error(statement_node, "fall used outside loop/discern.")
            return

        if statement_kind == "AbsolveStmt":
            if self.in_loop <= 0 and self.in_discern <= 0:
                self._error(statement_node, "absolve used outside loop/discern.")
            return

        if statement_kind == "DismissStmt":
            if self.current_func is None:
                return

            return_type = self.current_func.return_type
            return_value = getattr(statement_node, "value", None)

            if return_type.is_base(BaseType.HOLLOW):
                if return_value is not None:
                    self._error(statement_node, "hollow function cannot dismiss a value.")
            else:
                if return_value is None:
                    self._error(statement_node, f"Function must dismiss a value of type {return_type}.")
                else:
                    value_type = self._expr_type(return_value)
                    if not can_assign(return_type, value_type):
                        self._error(statement_node, f"Cannot dismiss {value_type} from function returning {return_type}.")
            return