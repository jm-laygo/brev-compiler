from __future__ import annotations

from backend.tokens import *
from backend.ast.ast_nodes import RiteDecl, Param, Node


class RitesMixin:
    # ---------- rites ----------
    def parse_rite(self) -> RiteDecl:
        rite_tok = self.match(TK_CF_RITE)
        return_type = self.parse_return_type_any()

        # genesis() { ... }
        if self.at(TK_OTHERS_GENESIS):
            self.match(TK_OTHERS_GENESIS)
            self.match(TK_SYM_OPPAREN)
            self.match(TK_SYM_CLSPAREN)
            self.match(TK_SYM_OPBRACE)

            local_decls = self.parse_local_decls()
            body = self.parse_statement_list_until(TK_CF_DISMISS, TK_SYM_CLSBRACE)

            dismiss = None
            if self.at(TK_CF_DISMISS):
                dismiss = self.parse_dismiss_stmt()

            self.match(TK_SYM_CLSBRACE)

            return RiteDecl(
                name="genesis",
                return_type=return_type,
                params=[],
                local_decls=local_decls,
                body=body,
                dismiss=dismiss,
                pos=rite_tok.pos,
            )

        # normal function: id ( params ) { ... }
        name_tok = self.match(TK_IDENTIFIER)

        self.match(TK_SYM_OPPAREN)
        params = self.parse_param_list_opt()
        self.match(TK_SYM_CLSPAREN)

        self.match(TK_SYM_OPBRACE)
        local_decls = self.parse_local_decls()
        body = self.parse_statement_list_until(TK_CF_DISMISS, TK_SYM_CLSBRACE)

        dismiss = None
        if self.at(TK_CF_DISMISS):
            dismiss = self.parse_dismiss_stmt()

        self.match(TK_SYM_CLSBRACE)

        return RiteDecl(
            name=name_tok.value,
            return_type=return_type,
            params=params,
            local_decls=local_decls,
            body=body,
            dismiss=dismiss,
            pos=rite_tok.pos,
        )

    def parse_return_type_any(self) -> str:
        if self.at(TK_DTYPE_HOLLOW):
            tok = self.match(TK_DTYPE_HOLLOW)
            return tok.type
        return self.parse_data_type_id()

    # ---------- params ----------
    def parse_param_list_opt(self) -> list[Param]:
        if self.at(TK_SYM_CLSPAREN):
            return []
        params = [self.parse_param()]
        while self.accept(TK_SYM_COMMA):
            params.append(self.parse_param())
        return params

    def parse_param(self) -> Param:
        type_tok = self.peek()
        type_name = self.parse_data_type_id()
        name_tok = self.match(TK_IDENTIFIER)

        dims = 0
        while self.accept(TK_SYM_OPBRACK):
            self.match(TK_SYM_CLSBRACK)
            dims += 1

        return Param(type_name=type_name, name=name_tok.value, array_dims=dims, pos=type_tok.pos)

    # ---------- local decls ----------
    def parse_local_decls(self) -> list[Node]:
        decls: list[Node] = []
        while self.peek().type in self.DECL_START:
            decls.append(self.parse_decl_item(global_scope=False))
        return decls