from __future__ import annotations

from backend.tokens import *
from backend.errors import ParserError
from backend.parser.predict_set import PREDICT
from backend.ast.ast_nodes import *
from backend.parser.parser import Parser, _tok_lexeme, _tok_pos


def parse_declaration_stmt(self: Parser) -> Statement:
    lookahead_type = self.current_type(0)

    if lookahead_type in (
        TK_DTYPE_TALLY,
        TK_DTYPE_DIVINE,
        TK_DTYPE_SIGIL,
        TK_DTYPE_SCRIPTURE,
        TK_DTYPE_VERITY,
    ):
        declaration_node = VarDecl(
            pos=_tok_pos(self.peek(0)),
            type_name=self.parse_data_type(),
            items=self.parse_var_decl_group()
        )
        self.expect(TK_SYM_SEMICOL)
        return VarDeclStmt(pos=declaration_node.pos, decl=declaration_node)

    if lookahead_type == TK_OTHERS_ORDAIN:
        ordain_token = self.expect(TK_OTHERS_ORDAIN)
        declaration_name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        declaration_items = self.parse_ordain_dec_list()
        self.expect(TK_SYM_SEMICOL)

        return OrdainStmt(
            pos=_tok_pos(ordain_token),
            decl=OrdainDecl(
                pos=_tok_pos(ordain_token),
                name=declaration_name,
                items=declaration_items
            )
        )

    if lookahead_type == TK_OTHERS_ORDER:
        order_token = self.expect(TK_OTHERS_ORDER)
        declaration_name = _tok_lexeme(self.expect(TK_IDENTIFIER))
        self.expect(TK_SYM_OPBRACE)
        member_list = self.parse_member_list_opt()
        self.expect(TK_SYM_CLSBRACE)
        self.expect(TK_SYM_SEMICOL)

        return OrderStmt(
            pos=_tok_pos(order_token),
            decl=OrderDecl(
                pos=_tok_pos(order_token),
                name=declaration_name,
                members=member_list
            )
        )

    raise ParserError(
        self.peek(0) or self.peek(-1),
        expected=list(PREDICT["<statement>"].keys())
    )


Parser.parse_declaration_stmt = parse_declaration_stmt
