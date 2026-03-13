from __future__ import annotations
from typing import Any

from backend.semantic.symbols import VarSymbol
from backend.semantic.typesys import BaseType, Type

from ..helpers import _class, _pos


class VariableDeclarationsMixin:
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