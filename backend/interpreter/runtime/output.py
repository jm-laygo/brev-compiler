from __future__ import annotations
from typing import Any
from backend.interpreter.builtins import stringify

def _write_inline(self, text: Any):
    self.current_line += str(text)

def _write_line(self, text: Any = ""):
    self.current_line += str(text)
    self.output.append(self.current_line)
    self.current_line = ""

def stringify_method(self, value: Any):
    return stringify(value)

def bind_output_methods(cls):
    cls._write_inline = _write_inline
    cls._write_line = _write_line
    cls.stringify = stringify_method