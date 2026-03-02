from __future__ import annotations
from dataclasses import dataclass
from typing import List
from backend.ast.ast_nodes import Program
from backend.semantic.checker import SemanticChecker
from backend.errors import SemanticError

@dataclass
class SemanticResult:
    program: Program
    errors: List[SemanticError]

def run_semantic(program: Program) -> SemanticResult:
    checker = SemanticChecker()
    errors = checker.check(program)
    return SemanticResult(program=program, errors=errors)