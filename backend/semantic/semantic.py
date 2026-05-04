from __future__ import annotations
from typing import List, Tuple

from backend.ast.ast_nodes import Program
from backend.errors import SemanticError
from backend.semantic.checker import SemanticChecker, CheckerConfig


def runSemanticAnalysis(
    program: Program,
    *,
    config: CheckerConfig | None = None
) -> Tuple[Program, List[SemanticError]]:
    # run semantic checker
    semanticChecker = SemanticChecker(config=config)

    try:
        checkedProgram, errorList = semanticChecker.check(program)

        return checkedProgram, errorList

    except SemanticError as semanticError:
        return program, [semanticError]

    except Exception as exception:
        programPosition = getattr(program, "position", None)

        internalError = SemanticError(
            programPosition,
            f"Internal semantic error: {exception}"
        )

        return program, [internalError]