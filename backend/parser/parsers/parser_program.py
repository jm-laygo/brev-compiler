from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.ast.ast_nodes import Program


class ProgramMixin:
    def parse_program(self) -> Program:
        """
        program:
          globals*  (sacred | dtype | order | ordain) ... until 'rite'
          rites*    'rite' ...
          EOF
        """
        globals_ = []
        functions = []
        entry = None

        # globals until we hit 'rite'
        while self.peek().type in self.DECL_START and self.peek().type != TK_CF_RITE:
            globals_.append(self.parse_decl_item(global_scope=True))

        # rites
        while self.at(TK_CF_RITE):
            rite = self.parse_rite()
            if rite.name == "genesis":
                entry = rite
            else:
                functions.append(rite)

        # EOF
        if not self.at(TK_EOF):
            raise ParserError(self.peek(), expected=[TK_EOF], details="Extra input after program end")

        pos = globals_[0].pos if globals_ else (entry.pos if entry else (functions[0].pos if functions else None))
        return Program(globals=globals_, functions=functions, entry=entry, pos=pos)