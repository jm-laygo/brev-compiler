from __future__ import annotations
import difflib
from typing import List

class SuggestionsMixin:
    def _all_visible_names(self) -> List[str]:
        names = set()
        s = self.scope
        while s is not None:
            names.update(getattr(s, "table", {}).keys())
            s = getattr(s, "parent", None)

        names.update(getattr(self, "funcs", {}).keys())
        names.update(getattr(self, "orders", {}).keys())
        return sorted(names)

    def _did_you_mean(self, name: str, cutoff: float = 0.72) -> str:
        if not name:
            return ""
        matches = difflib.get_close_matches(name, self._all_visible_names(), n=1, cutoff=cutoff)
        return f" Did you mean '{matches[0]}'?" if matches else ""

    def _did_you_mean_from(self, name: str, candidates: List[str], cutoff: float = 0.72) -> str:
        if not name:
            return ""
        matches = difflib.get_close_matches(name, candidates or [], n=1, cutoff=cutoff)
        return f" Did you mean '{matches[0]}'?" if matches else ""