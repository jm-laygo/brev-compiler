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

    def _check_function(self, function_node: Any) -> None:
        if _class(function_node) != "RiteDecl":
            return

        function_name = getattr(function_node, "name", "")
        function_symbol = self.funcs.get(function_name)
        self.current_func = function_symbol

        previous_scope = self.scope
        self.scope = Scope(self.global_scope)

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

        has_dismiss_in_body = any(_class(statement_node) == "DismissStmt" for statement_node in body_statements)
        has_any_dismiss = (dismiss_statement is not None) or has_dismiss_in_body

        if function_symbol is not None and not function_symbol.return_type.is_base(BaseType.HOLLOW):
            if not has_any_dismiss:
                self._error(
                    function_node,
                    f"Function '{function_name}' must dismiss a value of type {function_symbol.return_type}."
                )

        self.scope = previous_scope
        self.current_func = None