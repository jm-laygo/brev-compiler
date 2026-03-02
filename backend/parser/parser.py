from backend.tokens import *
from backend.errors import ParserError

try:
    from backend.parser.predict_set import PREDICT, EPSILON
except Exception:
    from backend.parser.predict_set import PREDICT, EPSILON

def _is_nonterminal(sym):
    return isinstance(sym, str) and sym.startswith("<") and sym.endswith(">")

def _tok_name(tok_type):
    return TOKEN_DISPLAY_NAMES.get(tok_type, tok_type)

def _make_eof_token(last_tok):
    pos = getattr(last_tok, "pos", None) if last_tok else None
    return Token(TK_EOF, value=None, pos=pos)

class LL1Parser:
    def __init__(self, start_symbol = "<program>", predict_table=None, ignore_types=None):
        self.start = start_symbol
        self.table = predict_table if predict_table is not None else PREDICT
        self.ignore = set(ignore_types) if ignore_types is not None else {
            TK_SYM_SPACE, TK_SYM_NEWLINE, TK_SYM_TAB,
            TK_COMMENT, TK_COMMENT_BLOCK
        }

    def _skip_ignored(self, tokens, i):
        while i < len(tokens) and tokens[i].type in self.ignore:
            i += 1
        return i

    def _expected_for(self, nonterminal):
        row = self.table.get(nonterminal, {})
        return list(row.keys())

    def _peek_type(self, tokens, i, k):
        j = i + k
        if j < len(tokens):
            return tokens[j].type
        return TK_EOF

    def _is_genesis_header(self, tokens, i):
        t0 = self._peek_type(tokens, i, 0)
        t1 = self._peek_type(tokens, i, 1)
        t2 = self._peek_type(tokens, i, 2)
        return (
            t0 == TK_CF_RITE
            and t1 in (TK_DTYPE_TALLY, TK_DTYPE_HOLLOW)
            and t2 == TK_OTHERS_GENESIS
        )

    def parse(self, tokens):
        tokens = list(tokens)
        if not tokens or tokens[-1].type != TK_EOF:
            tokens.append(_make_eof_token(tokens[-1] if tokens else None))

        stack = [TK_EOF, self.start]
        i = 0
        trace = []

        while stack:
            top = stack.pop()

            i = self._skip_ignored(tokens, i)
            if i >= len(tokens):
                # end of input: treat as EOF
                raise ParserError(tokens[-1], expected=[TK_EOF], details = "Unexpected end of input")

            lookahead = tokens[i]
            la_type = lookahead.type

            if top == EPSILON:
                continue

            # Terminal symbol
            if not _is_nonterminal(top):
                if top == la_type:
                    i += 1
                    continue

                raise ParserError(
                    lookahead,
                    expected=[top],
                    details=None
                )

            # Nonterminal
            nt = top

            if nt == "<subfunc_list_opt>" and la_type == TK_CF_RITE:
                rhs = [EPSILON] if self._is_genesis_header(tokens, i) else ["<subfunc_list>"]
            else:
                row = self.table.get(nt, {})
                rhs = row.get(la_type)

            if rhs is None:
                expected_types = self._expected_for(nt)
                raise ParserError(
                    lookahead,
                    expected = expected_types,
                   details = None
                )

            trace.append({"nonterminal": nt, "lookahead": la_type, "rhs": rhs})

            # Epsilon production
            if len(rhs) == 1 and rhs[0] == EPSILON:
                continue

            for sym in reversed(rhs):
                if sym != EPSILON:
                    stack.append(sym)

        i = self._skip_ignored(tokens, i)
        if i < len(tokens) and tokens[i].type != TK_EOF:
            raise ParserError(tokens[i], expected = [TK_EOF], details = "Extra input after program end")

        return trace

def validate(tokens):
    parser = LL1Parser()
    return parser.parse(tokens)