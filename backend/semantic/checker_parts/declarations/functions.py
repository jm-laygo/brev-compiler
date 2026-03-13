from __future__ import annotations
from typing import Any, List

from backend.semantic.symbols import FuncSymbol, VarSymbol
from backend.semantic.typesys import Type

from ..helpers import _class, _pos


class FunctionDeclarationsMixin:
    def _declare_functions(self, program_node: Any) -> None:
        function_declarations: List[Any] = []

        entry_rite = getattr(program_node, "entry", None)
        if entry_rite is not None:
            function_declarations.append(entry_rite)

        function_declarations.extend(getattr(program_node, "functions", []) or [])

        for function_declaration in function_declarations:
            if function_declaration is None or _class(function_declaration) != "RiteDecl":
                continue

            function_name = getattr(function_declaration, "name", None)
            if not function_name:
                self._error(function_declaration, "Function missing name.")
                continue

            if function_name in self.funcs:
                self._error(function_declaration, f"Function '{function_name}' already declared.")
                continue

            return_type = self._type_from_return_type(getattr(function_declaration, "return_type", None))

            function_symbol = FuncSymbol(
                name=function_name,
                typ=Type.unknown(),
                return_type=return_type,
                pos=_pos(function_declaration)
            )

            parameter_symbols: List[VarSymbol] = []
            parameter_declarations = getattr(function_declaration, "params", []) or []

            for parameter_declaration in parameter_declarations:
                parameter_name = getattr(parameter_declaration, "name", None)
                parameter_type = self._type_from_decl(parameter_declaration)

                parameter_symbols.append(
                    VarSymbol(
                        name=parameter_name,
                        typ=parameter_type,
                        pos=_pos(parameter_declaration),
                        is_const=False
                    )
                )

            function_symbol.params = parameter_symbols
            self.funcs[function_name] = function_symbol
            self.global_scope.define(function_symbol)