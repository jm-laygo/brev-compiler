from __future__ import annotations
from typing import Any, List

from backend.semantic.typesys import Type, BaseType, can_assign


class CallsMixin:
    def _check_call(self, callee: str, args: List[Any], node: Any) -> Type:
        if not callee:
            self._error(node, "Call missing callee.")
            return Type.error()

        fs = self.funcs.get(callee)
        if fs is None:
            hint = self._did_you_mean_from(callee, list(self.funcs.keys()))
            self._error(node, f"Call to undeclared function '{callee}'.{hint}")
            return Type.error()

        if len(args) != len(fs.params):
            self._error(node, f"Function '{callee}' expects {len(fs.params)} args, got {len(args)}.")

        n = min(len(args), len(fs.params))
        for i in range(n):
            at = self._expr_type(args[i])
            pt = fs.params[i].typ

            if at.base == BaseType.ERROR:
                continue

            if not can_assign(pt, at):
                self._error(
                    args[i] if args[i] is not None else node,
                    f"Arg {i + 1} of '{callee}': cannot pass {self._fmt_type(at)} to {self._fmt_type(pt)}.",
                )

        return fs.return_type