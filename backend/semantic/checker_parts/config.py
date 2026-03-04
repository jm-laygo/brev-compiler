from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CheckerConfig:
    allow_concat_coercion: bool = True
    allow_numeric_to_string_in_concat: bool = True