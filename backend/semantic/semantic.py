from __future__ import annotations
from typing import Any, List, Tuple
from backend.ast.ast_nodes import Program
from backend.errors import SemanticError
from backend.semantic.checker import SemanticChecker, CheckerConfig

def run_semantic(program: Program, *, config: CheckerConfig | None = None) -> Tuple[Program, List[SemanticError]]:
    checker = SemanticChecker(config=config)
    try:
        checked_ast, errors = checker.check(program)
        return checked_ast, errors
    except SemanticError as e:
        return program, [e]
    except Exception as e:
        pos = getattr(program, "pos", None)
        return program, [SemanticError(pos, f"Internal semantic error: {e}")]