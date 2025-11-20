class LexicalError(Exception):
    def __init__(self, pos, details):
        super().__init__(details)
        self.pos = pos
        self.details = details

    def as_string(self):
        """Returns the error message in string format"""
        safe_details = self.details.replace('\n', '\\n')
        return f"Ln {self.pos.ln} Lexical Error: {safe_details}"
