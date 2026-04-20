from __future__ import annotations
from typing import Any
from backend.errors import RuntimeErrorBase
from backend.interpreter.builtins import stringify

def _write_inline(self, text: Any):
    try:
        self.current_line += str(text)
    except Exception as exc:
        raise RuntimeErrorBase(None, "Failed to convert output text.") from exc

def _write_line(self, text: Any = ""):
    try:
        self.current_line += str(text)
    except Exception as exc:
        raise RuntimeErrorBase(None, "Failed to convert output text.") from exc
    self.output.append(self.current_line)
    self.current_line = ""

def _flush_output(self):
    if self.current_line:
        self.output.append(self.current_line)
        self.current_line = ""

def stringify_method(self, value: Any):
    return stringify(value)

def bind_output_methods(cls):
    cls._write_inline = _write_inline
    cls._write_line = _write_line
    cls._flush_output = _flush_output
    cls.stringify = stringify_method