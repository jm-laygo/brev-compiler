from backend.tokens import (
    TK_SYM_SPACE,
    TK_SYM_NEWLINE,
    TK_SYM_TAB,
    TK_COMMENT,
    TK_COMMENT_BLOCK,
)


IGNORED_PARSER_TOKENS = {
    TK_SYM_SPACE,
    TK_SYM_NEWLINE,
    TK_SYM_TAB,
    TK_COMMENT,
    TK_COMMENT_BLOCK,
}


def filterParserTokens(tokenList):
    return [
        token for token in tokenList
        if token.type not in IGNORED_PARSER_TOKENS
    ]