from backend.tokens import TOKEN_DISPLAY_NAMES

def _pos_line_col(pos):
    if pos is None:
        return "?", "?"
    ln = getattr(pos, "ln", "?")
    col = getattr(pos, "col", "?")
    return ln, col

class LexicalError(Exception):
    def __init__(self, pos, details: str, hint: str | None = None):
        super().__init__(details)
        self.pos = pos
        self.details = details
        self.hint = hint

    def as_string(self) -> str:
        ln = getattr(self.pos, "ln", "?")
        col = getattr(self.pos, "col", "?")
        details = self.details
        details = details.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
        msg = f"Ln {ln}, Col {col} Lexical Error: {details}"
        if self.hint:
            msg += f" Did you mean '{self.hint}'?"
        return msg

class ParserError(Exception):
    def __init__(self, token, expected, details=None):
        self.token = token
        if expected is None:
            self.expected = []
        elif isinstance(expected, (set, tuple)):
            self.expected = list(expected)
        elif isinstance(expected, list):
            self.expected = expected
        else:
            self.expected = [expected]
        self.details = details

    def as_string(self):
        pos = getattr(self.token, "pos", None)
        line = getattr(pos, "ln", "?")
        col = getattr(pos, "col", "?")

        def friendly(t):
            return TOKEN_DISPLAY_NAMES.get(t, t)

        expected_str = ", ".join(friendly(t) for t in self.expected) if self.expected else "<?>"
        found_type = getattr(self.token, "type", None)
        found_str = friendly(found_type) if found_type else "<?>"

        msg = f"Ln {line}, Col {col} Syntax Error: Expected {expected_str} but found '{found_str}'"
        if self.details:
            msg += f" ({self.details})"
        return msg
    
class SemanticError(Exception):
    def __init__(self, node_or_token, details: str):
        super().__init__(details)
        self.node_or_token = node_or_token
        self.details = details

    def as_string(self) -> str:
        x = self.node_or_token

        if x is not None and hasattr(x, "ln") and hasattr(x, "col"):
            pos = x
        else:
            pos = getattr(x, "pos", None)

        ln = getattr(pos, "ln", "?")
        col = getattr(pos, "col", "?")

        details = self.details.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
        return f"Ln {ln}, Col {col} Semantic Error: {details}"