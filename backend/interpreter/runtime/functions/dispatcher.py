from __future__ import annotations

from .calling import _call_rite
from .locals import _exec_local_declarations

def bind_function_methods(cls):
    cls._call_rite = _call_rite
    cls._exec_local_declarations = _exec_local_declarations
