class LexicalError(Exception):
    def __init__(self, pos, details, hint=None):
        super().__init__(details)
        self.pos = pos
        self.details = details
        self.hint = hint  # <-- NEW (optional suggested keyword)

    def as_string(self):
        safe_details = self.details.replace('\n', '\\n')
        msg = f"Ln {self.pos.ln} Lexical Error: {safe_details}"
        if self.hint:
            msg += f"  Did you mean '{self.hint}'?"
        return msg
