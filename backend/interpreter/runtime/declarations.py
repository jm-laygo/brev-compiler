from __future__ import annotations
from backend.ast.ast_nodes import OrderDecl, OrdainDecl, SacredDecl, VarDecl, VarItem
from backend.interpreter.environment import Environment
from backend.errors import RuntimeErrorBase, RuntimeTypeError

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
            node=declared_item
        )

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
            is_const=False,
            node=declared_item
        )

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
            node=declared_item
        )

def _materialize_var_item(
    self,
    declared_type_name: str,
    declared_item: VarItem,
    current_environment: Environment,
):
    dimension_nodes = getattr(declared_item, "dims", None) or []
    initializer_node = getattr(declared_item, "init", None)

    if dimension_nodes:
        evaluated_shape = []
        for dimension_node in dimension_nodes:
            evaluated_shape.append(
                self._require_int_dim(dimension_node, current_environment, declared_item)
            )

        if initializer_node is not None:
            return self._eval_expr(initializer_node, current_environment)

        return self._make_array_of(
            lambda: self._default_value_for_type(declared_type_name),
            evaluated_shape,
        )

    if initializer_node is not None:
        return self._eval_expr(initializer_node, current_environment)

    return self._default_value_for_type(declared_type_name)

def _make_order_instance(self, order_declaration: OrderDecl):
    order_instance = {"__order__": order_declaration.name}

    member_nodes = getattr(order_declaration, "members", []) or []
    for member_node in member_nodes:
        member_dimension_nodes = getattr(member_node, "dims", None) or []
        member_initializer_node = getattr(member_node, "init", None)

        if member_dimension_nodes:
            evaluated_shape = []
            for dimension_node in member_dimension_nodes:
                evaluated_shape.append(
                    self._require_int_dim(dimension_node, self.globals, member_node)
                )

            order_instance[member_node.name] = self._make_array_of(
                lambda: self._default_value_for_type(member_node.type_name),
                evaluated_shape,
            )

        elif member_initializer_node is not None:
            order_instance[member_node.name] = self._eval_expr(
                member_initializer_node,
                self.globals,
            )

        else:
            order_instance[member_node.name] = self._default_value_for_type(
                member_node.type_name
            )

    return order_instance

def _make_array_of(self, value_factory, shape):
    if not shape:
        return value_factory()

    current_dimension_size = shape[0]
    return [
        self._make_array_of(value_factory, shape[1:])
        for _ in range(current_dimension_size)
    ]

def _require_int_dim(self, dimension_expression, current_environment: Environment, node):
    evaluated_dimension_value = self._eval_expr(dimension_expression, current_environment)

    if not isinstance(evaluated_dimension_value, int):
        raise RuntimeTypeError(node, "Array dimensions must evaluate to tally values.")

    if evaluated_dimension_value < 0:
        raise RuntimeErrorBase(node, "Array dimensions cannot be negative.")

    return evaluated_dimension_value

def _default_value_for_type(self, declared_type_name: str):
    lowered_type_name = (declared_type_name or "").lower()

    if lowered_type_name == "tally":
        return 0

    if lowered_type_name == "divine":
        return 0.0

    if lowered_type_name == "sigil":
        return "\0"

    if lowered_type_name == "scripture":
        return ""

    if lowered_type_name == "verity":
        return False

    if lowered_type_name == "hollow":
        return None

    if declared_type_name in self.orders:
        return self._make_order_instance(self.orders[declared_type_name])

    return None

def bind_declaration_methods(cls):
    cls._exec_var_decl = _exec_var_decl
    cls._exec_sacred_decl = _exec_sacred_decl
    cls._exec_ordain_decl = _exec_ordain_decl
    cls._materialize_var_item = _materialize_var_item
    cls._make_order_instance = _make_order_instance
    cls._make_array_of = _make_array_of
    cls._require_int_dim = _require_int_dim
    cls._default_value_for_type = _default_value_for_type