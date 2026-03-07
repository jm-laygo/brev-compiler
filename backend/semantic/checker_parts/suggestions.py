from __future__ import annotations
import difflib
from typing import List

class SuggestionsMixin:
    def _all_visible_names(self) -> List[str]:
        visible_names = set()

        current_scope = self.scope
        while current_scope is not None:
            scope_symbols = getattr(current_scope, "table", {})
            visible_names.update(scope_symbols.keys())
            current_scope = getattr(current_scope, "parent", None)

        function_names = getattr(self, "funcs", {}).keys()
        order_names = getattr(self, "orders", {}).keys()

        visible_names.update(function_names)
        visible_names.update(order_names)

        return sorted(visible_names)

    def _did_you_mean(self, entered_name: str, cutoff: float = 0.72) -> str:
        if not entered_name:
            return ""

        visible_names = self._all_visible_names()
        closest_matches = difflib.get_close_matches(
            entered_name,
            visible_names,
            n=1,
            cutoff=cutoff
        )

        if closest_matches:
            return f" Did you mean '{closest_matches[0]}'?"

        return ""

    def _did_you_mean_from(self, entered_name: str, candidate_names: List[str], cutoff: float = 0.72) -> str:
        if not entered_name:
            return ""

        closest_matches = difflib.get_close_matches(
            entered_name,
            candidate_names or [],
            n=1,
            cutoff=cutoff
        )

        if closest_matches:
            return f" Did you mean '{closest_matches[0]}'?"

        return ""