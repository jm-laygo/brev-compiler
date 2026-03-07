from __future__ import annotations
from typing import Any

from backend.semantic.symbols import Scope
from .helpers import _class
from backend.semantic.typesys import BaseType


class ProgramFlowMixin:
    def _check_program(self, program_node: Any) -> None:
        global_declarations = getattr(program_node, "globals", []) or []

        for global_declaration in global_declarations:
            declaration_kind = _class(global_declaration)

            if declaration_kind == "VarDecl":
                self._check_var_decl_init(global_declaration)

            elif declaration_kind == "SacredDecl":
                self._check_sacred_decl_init(global_declaration)

            elif declaration_kind == "OrdainDecl":
                self._check_ordain_decl_init(global_declaration)

        entry_function = getattr(program_node, "entry", None)
        if entry_function is not None:
            self._check_function(entry_function)

        function_declarations = getattr(program_node, "functions", []) or []
        for function_declaration in function_declarations:
            self._check_function(function_declaration)

    def _block_guarantees_dismiss(self, statement_list: list[Any]) -> bool:
        for statement_node in statement_list or []:
            if self._stmt_guarantees_dismiss(statement_node):
                return True
        return False

    def _stmt_guarantees_dismiss(self, statement_node: Any) -> bool:
        if statement_node is None:
            return False

        statement_kind = _class(statement_node)

        if statement_kind == "DismissStmt":
            return True

        if statement_kind == "DecreeStmt":
            decree_body = getattr(statement_node, "body", []) or []
            edict_clauses = getattr(statement_node, "edicts", []) or []
            absolution_clause = getattr(statement_node, "absolution", None)

            if absolution_clause is None:
                return False

            if not self._block_guarantees_dismiss(decree_body):
                return False

            for edict_clause in edict_clauses:
                if not self._stmt_guarantees_dismiss(edict_clause):
                    return False

            if not self._stmt_guarantees_dismiss(absolution_clause):
                return False

            return True

        if statement_kind == "EdictClause":
            edict_body = getattr(statement_node, "body", []) or []
            return self._block_guarantees_dismiss(edict_body)

        if statement_kind == "AbsolutionClause":
            absolution_body = getattr(statement_node, "body", []) or []
            return self._block_guarantees_dismiss(absolution_body)

        return False

    def _check_function(self, function_node: Any) -> None:
        if _class(function_node) != "RiteDecl":
            return

        function_name = getattr(function_node, "name", "")
        function_symbol = self.funcs.get(function_name)
        self.current_func = function_symbol

        previous_scope = self.scope
        self.scope = Scope(self.global_scope)

        try:
            if function_symbol:
                seen_parameter_names = set()

                for parameter_symbol in function_symbol.params:
                    if parameter_symbol.name in seen_parameter_names:
                        self._error(
                            parameter_symbol.pos,
                            f"Duplicate parameter '{parameter_symbol.name}' in function '{function_name}'."
                        )

                    seen_parameter_names.add(parameter_symbol.name)
                    self.scope.define(parameter_symbol)

            local_declarations = getattr(function_node, "local_decls", []) or []

            for local_declaration in local_declarations:
                declaration_kind = _class(local_declaration)

                if declaration_kind == "VarDecl":
                    self._declare_var_decl(local_declaration, is_global=False)
                    self._check_var_decl_init(local_declaration)

                elif declaration_kind == "SacredDecl":
                    self._declare_var_decl(local_declaration, is_global=False, force_const=True)
                    self._check_sacred_decl_init(local_declaration)

                elif declaration_kind == "OrdainDecl":
                    self._declare_ordain_decl(local_declaration, is_global=False)
                    self._check_ordain_decl_init(local_declaration)

                elif declaration_kind == "OrderDecl":
                    self._error(
                        local_declaration,
                        "Order declarations are not allowed inside functions."
                    )

            body_statements = getattr(function_node, "body", []) or []
            for statement_node in body_statements:
                self._check_stmt(statement_node)

            dismiss_statement = getattr(function_node, "dismiss", None)
            if dismiss_statement is not None:
                self._check_stmt(dismiss_statement)

            if function_symbol is not None and not function_symbol.return_type.is_base(BaseType.HOLLOW):
                body_guarantees_dismiss = self._block_guarantees_dismiss(body_statements)
                final_dismiss_exists = dismiss_statement is not None
                function_guarantees_dismiss = body_guarantees_dismiss or final_dismiss_exists

                if not function_guarantees_dismiss:
                    self._error(
                        function_node,
                        f"Function '{function_name}' must dismiss a value of type {function_symbol.return_type}."
                    )

        finally:
            self.scope = previous_scope
            self.current_func = None