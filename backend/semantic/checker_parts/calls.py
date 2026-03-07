from __future__ import annotations
from typing import Any, List

from backend.semantic.typesys import Type, BaseType, can_assign


class CallsMixin:
    def _check_call(self, function_name: str, argument_nodes: List[Any], call_node: Any) -> Type:
        if not function_name:
            self._error(call_node, "Call missing function name.")
            return Type.error()

        function_symbol = self.funcs.get(function_name)
        if function_symbol is None:
            suggestion_text = self._did_you_mean_from(function_name, list(self.funcs.keys()))
            self._error(call_node, f"Call to undeclared function '{function_name}'.{suggestion_text}")
            return Type.error()

        expected_argument_count = len(function_symbol.params)
        actual_argument_count = len(argument_nodes)

        if actual_argument_count != expected_argument_count:
            self._error(
                call_node,
                f"Function '{function_name}' expects {expected_argument_count} args, got {actual_argument_count}."
            )

        arguments_to_check = min(actual_argument_count, expected_argument_count)

        for argument_index in range(arguments_to_check):
            argument_node = argument_nodes[argument_index]
            argument_type = self._expr_type(argument_node)
            parameter_type = function_symbol.params[argument_index].typ

            if argument_type.base == BaseType.ERROR:
                continue

            if not can_assign(parameter_type, argument_type):
                self._error(
                    argument_node if argument_node is not None else call_node,
                    f"Arg {argument_index + 1} of '{function_name}': cannot pass {self._fmt_type(argument_type)} to {self._fmt_type(parameter_type)}."
                )

        return function_symbol.return_type