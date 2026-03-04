from __future__ import annotations
from typing import Any

def _pos(node: Any) -> Any:
    return getattr(node, "pos", None)

def _name(node: Any, fallback: str = "") -> str:
    return getattr(node, "name", fallback)

def _class(node: Any) -> str:
    return node.__class__.__name__ if node is not None else "None"