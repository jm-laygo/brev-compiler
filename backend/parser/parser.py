from __future__ import annotations

from backend.ast.ast_nodes import Program
from backend.parser.parsers import (
    ParserBase, ProgramMixin, DeclsMixin, ExprsMixin, LValuesMixin, StmtsMixin, RitesMixin
)

class ASTParser(
    ParserBase,
    ProgramMixin,
    DeclsMixin,
    ExprsMixin,
    LValuesMixin,
    StmtsMixin,
    RitesMixin,
):
    pass


def parse_ast(tokens) -> Program:
    return ASTParser(tokens).parse_program()