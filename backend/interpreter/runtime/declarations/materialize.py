from __future__ import annotations

from backend.ast.ast_nodes import OrderDecl, VarItem
from backend.errors import RuntimeErrorBase, RuntimeTypeError
from backend.interpreter.environment import Environment

MAX_ARRAY_DIMENSION_SIZE = 100000

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

    if not isinstance(evaluated_dimension_value, int) or isinstance(evaluated_dimension_value, bool):
        raise RuntimeTypeError(node, "Array dimensions must evaluate to tally values.")

    if evaluated_dimension_value <= 0:
        raise RuntimeErrorBase(node, "Array dimensions must be positive.")

    if evaluated_dimension_value > MAX_ARRAY_DIMENSION_SIZE:
        raise RuntimeErrorBase(
            node,
            f"Array dimension exceeds maximum size of {MAX_ARRAY_DIMENSION_SIZE}.",
        )

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
