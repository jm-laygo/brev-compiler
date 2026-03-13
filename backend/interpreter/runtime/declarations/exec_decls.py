from __future__ import annotations

from backend.ast.ast_nodes import OrdainDecl, SacredDecl, VarDecl
from backend.errors import RuntimeErrorBase
from backend.interpreter.environment import Environment

# VARIABLE DECLARATION
def _exec_var_decl(self, declaration_node: VarDecl, current_environment: Environment):
    declared_type_name = getattr(declaration_node, "type_name", "")

    declared_items = getattr(declaration_node, "items", []) or []
    for declared_item in declared_items:
        materialized_value = self._materialize_var_item(
            declared_type_name,
            declared_item,
            current_environment,
        )

        dimension_nodes = getattr(declared_item, "dims", None) or []

        if dimension_nodes:
            coerced_value = materialized_value
        else:
            coerced_value = self._coerce_value_to_type(
                declared_type_name,
                materialized_value,
                declared_item,
            )

        current_environment.declare(
            declared_item.name,
            coerced_value,
            is_const=False,
            node=declared_item,
        )

# SACRED DECLARATION
def _exec_sacred_decl(self, declaration_node: SacredDecl, current_environment: Environment):
    declared_type_name = getattr(declaration_node, "type_name", "")

    declared_items = getattr(declaration_node, "items", []) or []
    for declared_item in declared_items:
        value_node = getattr(declared_item, "value", None)

        if value_node is not None:
            evaluated_value = self._eval_expr(value_node, current_environment)
        else:
            evaluated_value = self._default_value_for_type(declared_type_name)

        coerced_value = self._coerce_value_to_type(
            declared_type_name,
            evaluated_value,
            declared_item,
        )
        current_environment.declare(
            declared_item.name,
            coerced_value,
            is_const=True,
            node=declared_item,
        )

# ORDAIN DECLARATION
def _exec_ordain_decl(self, declaration_node: OrdainDecl, current_environment: Environment):
    order_name = declaration_node.name
    order_declaration = self.orders.get(order_name)

    if order_declaration is None:
        raise RuntimeErrorBase(declaration_node, f"Unknown order type '{order_name}'.")

    declared_items = getattr(declaration_node, "items", []) or []
    for declared_item in declared_items:
        dimension_nodes = getattr(declared_item, "dims", None) or []
        initializer_node = getattr(declared_item, "init", None)

        if dimension_nodes:
            evaluated_shape = []
            for dimension_node in dimension_nodes:
                evaluated_shape.append(
                    self._require_int_dim(dimension_node, current_environment, declared_item)
                )

            runtime_value = self._make_array_of(
                lambda: self._make_order_instance(order_declaration),
                evaluated_shape,
            )

        elif initializer_node is not None:
            runtime_value = self._eval_expr(initializer_node, current_environment)

        else:
            runtime_value = self._make_order_instance(order_declaration)

        current_environment.declare(
            declared_item.name,
            runtime_value,
            is_const=False,
            node=declared_item,
        )
