from __future__ import annotations
from typing import List, Optional, Tuple

from backend.tokens import *
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.errors import ParserError
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_rite_seq(self: Parser) -> Tuple[Optional[RiteDecl], List[RiteDecl]]:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<rite_seq>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<rite_seq>"].keys()),
        )

    self.expect(TK_CF_RITE)
    return_type_name = self.parse_return_type_any()

    lookahead_type = self.current_type(0)
    if lookahead_type not in PREDICT["<rite_after_type>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<rite_after_type>"].keys()),
        )

    entry_rite: Optional[RiteDecl] = None
    rite_declarations: List[RiteDecl] = []

    if lookahead_type == TK_OTHERS_GENESIS:
        genesis_token = self.expect(TK_OTHERS_GENESIS)
        self.expect(TK_SYM_OPPAREN)
        self.expect(TK_SYM_CLSPAREN)
        self.expect(TK_SYM_OPBRACE)

        local_declarations = self.parse_main_local_dec_opt()
        statement_list = self.parse_statement_list()
        dismiss_stmt = self.parse_dismiss_opt()

        self.expect(TK_SYM_CLSBRACE)

        entry_rite = RiteDecl(
            pos=_tok_pos(genesis_token),
            name="genesis",
            return_type=return_type_name,
            params=[],
            local_decls=local_declarations,
            body=statement_list,
            dismiss=dismiss_stmt,
        )
        return entry_rite, rite_declarations

    if lookahead_type == TK_IDENTIFIER:
        identifier_token = self.expect(TK_IDENTIFIER)
        rite_name = _tok_lexeme(identifier_token)

        self.expect(TK_SYM_OPPAREN)
        parameter_list = self.parse_param_list_opt()
        self.expect(TK_SYM_CLSPAREN)

        self.expect(TK_SYM_OPBRACE)
        local_declarations = self.parse_func_local_dec_opt()
        statement_list = self.parse_statement_list()
        dismiss_stmt = self.parse_dismiss_opt()
        self.expect(TK_SYM_CLSBRACE)

        rite_decl = RiteDecl(
            pos=_tok_pos(identifier_token),
            name=rite_name,
            return_type=return_type_name,
            params=parameter_list,
            local_decls=local_declarations,
            body=statement_list,
            dismiss=dismiss_stmt,
        )

        rite_declarations.append(rite_decl)

        if self.current_type(0) == TK_CF_RITE:
            next_entry_rite, next_rite_declarations = self.parse_rite_seq()
            if next_entry_rite is not None and entry_rite is None:
                entry_rite = next_entry_rite
            rite_declarations.extend(next_rite_declarations)

        return entry_rite, rite_declarations

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=list(PREDICT["<rite_after_type>"].keys()),
    )


def parse_return_type_any(self: Parser) -> str:
    lookahead_type = self.current_type(0)

    if lookahead_type not in PREDICT["<return_type_any>"]:
        raise ParserError(
            self.peek(0) or self.peek(-1),
            expected=list(PREDICT["<return_type_any>"].keys()),
        )

    if lookahead_type == TK_DTYPE_HOLLOW:
        self.expect(TK_DTYPE_HOLLOW)
        return "hollow"

    return self.parse_data_type_id()


Parser.parse_rite_seq = parse_rite_seq
Parser.parse_return_type_any = parse_return_type_any
