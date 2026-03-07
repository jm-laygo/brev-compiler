from __future__ import annotations
from typing import Any, List

from backend.semantic.typesys import (
    BaseType,
    Type,
    can_assign,
    is_numeric,
    result_of_unary,
    result_of_binary,
)
from .helpers import _class

class ExpressionsMixin:
    def _expr_type(self, expression_node: Any) -> Type:
        if expression_node is None:
            return Type.unknown()

        expression_kind = _class(expression_node)

        if expression_kind == "LiteralExpr":
            literal_type_name = (getattr(expression_node, "literal_type", None) or "").lower()

            if literal_type_name == "int":
                return Type.base_t(BaseType.TALLY)

            if literal_type_name == "decimal":
                return Type.base_t(BaseType.DIVINE)

            if literal_type_name == "char":
                return Type.base_t(BaseType.SIGIL)

            if literal_type_name == "string":
                return Type.base_t(BaseType.SCRIPTURE)

            if literal_type_name == "bool":
                return Type.base_t(BaseType.VERITY)

            return Type.unknown()

        if expression_kind == "ArrayInit":
            item_nodes = getattr(expression_node, "items", []) or []

            if not item_nodes:
                return Type.unknown()

            item_types: List[Type] = []
            for item_node in item_nodes:
                item_types.append(self._expr_type(item_node))

            for item_type in item_types:
                if item_type.base == BaseType.ERROR:
                    return Type.error()

            first_item_type = item_types[0]

            if all(is_numeric(item_type) for item_type in item_types):
                resulting_numeric_type = Type.base_t(BaseType.TALLY)

                for item_type in item_types:
                    if item_type.is_base(BaseType.DIVINE):
                        resulting_numeric_type = Type.base_t(BaseType.DIVINE)
                        break

                return Type.array(resulting_numeric_type, 1)

            if all(str(item_type) == str(first_item_type) for item_type in item_types):
                return Type.array(first_item_type, 1)

            self._error(
                expression_node,
                f"Inconsistent array initializer types: {', '.join(str(item_type) for item_type in item_types)}"
            )
            return Type.error()

        if expression_kind == "GroupExpr":
            inner_expression = getattr(expression_node, "expr", None)
            return self._expr_type(inner_expression)

        if expression_kind == "VarExpr":
            reference_node = getattr(expression_node, "ref", None)
            return self._lvalue_type(reference_node)

        if expression_kind == "CallExpr":
            function_name = getattr(expression_node, "callee", None)
            argument_nodes = getattr(expression_node, "args", []) or []
            return self._check_call(function_name, argument_nodes, expression_node)

        if expression_kind == "VerseOfExpr":
            inner_expression = getattr(expression_node, "expr", None)
            self._expr_type(inner_expression)
            return Type.base_t(BaseType.TALLY)

        if expression_kind == "UnaryExpr":
            operator_text = getattr(expression_node, "op", "") or ""
            operand_node = getattr(expression_node, "operand", None)
            operand_type = self._expr_type(operand_node)

            if self._has_type_error(operand_type):
                return Type.error()

            result_type = result_of_unary(operator_text, operand_type)

            if self._has_type_error(result_type):
                self._error(
                    expression_node,
                    f"Invalid unary op '{operator_text}' for type {self._tname(operand_type)}."
                )

            return result_type

        if expression_kind == "BinaryExpr":
            operator_text = getattr(expression_node, "op", "") or ""
            left_expression = getattr(expression_node, "left", None)
            right_expression = getattr(expression_node, "right", None)

            left_type = self._expr_type(left_expression)
            right_type = self._expr_type(right_expression)

            if self._has_type_error(left_type) or self._has_type_error(right_type):
                return Type.error()

            result_type = result_of_binary(operator_text, left_type, right_type)

            if self._has_type_error(result_type):
                self._error(
                    expression_node,
                    f"Invalid binary op '{operator_text}' for types {self._tname(left_type)} and {self._tname(right_type)}."
                )
                return Type.error()

            return result_type

        if expression_kind == "IdentifierRef":
            identifier_name = getattr(expression_node, "name", None)
            resolved_symbol = self.scope.resolve(identifier_name) if identifier_name else None

            from backend.semantic.symbols import VarSymbol

            if isinstance(resolved_symbol, VarSymbol):
                return resolved_symbol.typ

            suggestion_text = self._did_you_mean(identifier_name)
            self._error(expression_node, f"Undeclared identifier '{identifier_name}'.{suggestion_text}")
            return Type.error()

        return Type.unknown()