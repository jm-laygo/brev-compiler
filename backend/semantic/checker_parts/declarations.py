from __future__ import annotations
from typing import Any, List, Optional

from backend.semantic.typesys import BaseType, Type
from backend.semantic.symbols import VarSymbol, FuncSymbol, OrderSymbol, MemberSymbol
from .helpers import _class, _pos

class DeclarationsMixin:
    def _declare_globals(self, program_node: Any) -> None:
        global_declarations = getattr(program_node, "globals", []) or []

        for global_declaration in global_declarations:
            declaration_kind = _class(global_declaration)

            if declaration_kind in ("VarDecl", "SacredDecl"):
                self._declare_var_decl(global_declaration, is_global=True)

            elif declaration_kind == "OrdainDecl":
                self._declare_ordain_decl(global_declaration, is_global=True)

            elif declaration_kind == "OrderDecl":
                continue

            else:
                continue

    def _const_int(self, expression_node: Any) -> Optional[int]:
        if expression_node is None:
            return None

        if _class(expression_node) == "LiteralExpr":
            literal_type = (getattr(expression_node, "literal_type", "") or "").lower()
            if literal_type == "int":
                try:
                    return int(getattr(expression_node, "value"))
                except Exception:
                    return None

        return None

    def _extract_array_sizes(self, dimension_nodes: list[Any], owner_node: Any) -> Optional[list[int]]:
        array_sizes: list[int] = []

        for dimension_node in dimension_nodes:
            constant_size = self._const_int(dimension_node)

            if constant_size is None:
                self._error(owner_node, "Array size must be a constant integer literal (tally).")
                return None

            if constant_size <= 0:
                self._error(owner_node, f"Array size must be > 0, got {constant_size}.")
                return None

            array_sizes.append(constant_size)

        return array_sizes

    def _declare_orders(self, program_node: Any) -> None:
        global_declarations = getattr(program_node, "globals", []) or []

        for global_declaration in global_declarations:
            if _class(global_declaration) != "OrderDecl":
                continue

            order_name = getattr(global_declaration, "name", None)
            if not order_name:
                self._error(global_declaration, "Order declaration missing name.")
                continue

            if order_name in self.orders:
                self._error(global_declaration, f"Order '{order_name}' already declared.")
                continue

            order_symbol = OrderSymbol(
                name=order_name,
                typ=Type.order(order_name),
                pos=_pos(global_declaration)
            )

            member_declarations = getattr(global_declaration, "members", []) or []

            for member_declaration in member_declarations:
                member_name = getattr(member_declaration, "name", None)

                if not member_name:
                    self._error(member_declaration, f"Order '{order_name}' member missing name.")
                    continue

                if member_name in order_symbol.members:
                    self._error(member_declaration, f"Duplicate member '{member_name}' in order '{order_name}'.")
                    continue

                member_type = self._type_from_decl(member_declaration)
                order_symbol.members[member_name] = MemberSymbol(
                    name=member_name,
                    typ=member_type,
                    pos=_pos(member_declaration)
                )

            self.orders[order_name] = order_symbol

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

    def _declare_var_decl(self, declaration_node: Any, is_global: bool, force_const: bool = False) -> None:
        declared_type_name = getattr(declaration_node, "type_name", "")
        declared_type = Type.base_t(declared_type_name)

        if declared_type.base == BaseType.UNKNOWN and isinstance(getattr(declaration_node, "type_name", None), str):
            declared_type = Type.order(getattr(declaration_node, "type_name"))

        is_constant = force_const or (_class(declaration_node) == "SacredDecl")
        declared_items = getattr(declaration_node, "items", []) or []

        for declared_item in declared_items:
            variable_name = getattr(declared_item, "name", None)

            if not variable_name:
                self._error(declared_item, "Variable item missing name.")
                continue

            dimension_nodes = getattr(declared_item, "dims", []) or []
            array_sizes = self._extract_array_sizes(dimension_nodes, declared_item) if len(dimension_nodes) > 0 else None
            variable_type = Type.array(declared_type, len(dimension_nodes)) if len(dimension_nodes) > 0 else declared_type

            if self.scope.resolve_local(variable_name):
                self._error(declared_item, f"Redeclaration of '{variable_name}' in the same scope.")
                continue

            self.scope.define(
                VarSymbol(
                    name=variable_name,
                    typ=variable_type,
                    pos=_pos(declared_item),
                    is_const=is_constant,
                    array_sizes=array_sizes,
                )
            )

    def _declare_ordain_decl(self, declaration_node: Any, is_global: bool) -> None:
        order_name = getattr(declaration_node, "name", None)

        if not order_name:
            self._error(declaration_node, "ordain declaration missing order name.")
            return

        if order_name not in self.orders:
            self._error(declaration_node, f"Unknown order type '{order_name}'.")

        order_type = Type.order(order_name)
        declared_items = getattr(declaration_node, "items", []) or []

        for declared_item in declared_items:
            variable_name = getattr(declared_item, "name", None)

            if not variable_name:
                self._error(declared_item, "ordain item missing name.")
                continue

            dimension_nodes = getattr(declared_item, "dims", []) or []
            array_sizes = self._extract_array_sizes(dimension_nodes, declared_item) if len(dimension_nodes) > 0 else None
            variable_type = Type.array(order_type, len(dimension_nodes)) if len(dimension_nodes) > 0 else order_type

            if self.scope.resolve_local(variable_name):
                self._error(declared_item, f"Redeclaration of '{variable_name}' in the same scope.")
                continue

            self.scope.define(
                VarSymbol(
                    name=variable_name,
                    typ=variable_type,
                    pos=_pos(declared_item),
                    is_const=False,
                    array_sizes=array_sizes,
                )
            )