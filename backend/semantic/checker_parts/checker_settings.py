from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CheckerConfig:
    allowConcatCoercion: bool = True
    allowNumericToStringInConcat: bool = True