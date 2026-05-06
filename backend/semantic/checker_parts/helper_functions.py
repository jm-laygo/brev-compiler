from __future__ import annotations
from typing import Any


def getNodePosition(node: Any) -> Any:
    return getattr(node, "position", None)

def getNodeName(node: Any, fallbackName: str = "") -> str:
    return getattr(node, "name", fallbackName)

def getClassName(node: Any) -> str:
    if node is None:
        return "None"

    return node.__class__.__name__