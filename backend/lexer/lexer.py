from backend.tokens import *
from backend.errors import LexicalError
from backend.positions import Position

from backend.lexer.scanners.scan_identifiers import scan_identifier
from backend.lexer.scanners.scan_comments import scan_comment
from backend.lexer.scanners.scan_numbers import scan_numbers
from backend.lexer.scanners.scan_chars import scan_char
from backend.lexer.scanners.scan_strings import scan_string
from backend.lexer.scanners.scan_operator import scan_operator
from backend.lexer.scanners.scan_symbol import scan_symbol
from backend.lexer.scanners.scan_keywords import scan_keywords

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code.replace("\r", "")
        self.pos = Position(-1, 1)
        self.current_char = None
        self.advance()

    def peek_non_ws(self):
        i = self.pos.index + 1
        while i < len(self.source_code):
            c = self.source_code[i]
            if c in (" ", "\t", "\n", "\r"):
                i += 1
                continue
            return c
        return None

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.source_code[self.pos.index]
            if self.pos.index < len(self.source_code)
            else None
        )

    def peek(self):
        next_pos = self.pos.index + 1
        return self.source_code[next_pos] if next_pos < len(self.source_code) else None

    def make_tokens(self):
        tokens = []
        errors = []

        while self.current_char is not None:

            # SPACES AND NEWLINES 
            if self.current_char == " ":
                tokens.append(Token(TK_SYM_SPACE, " ", self.pos.copy()))
                self.advance()
                continue

            if self.current_char == "\t":
                tokens.append(Token(TK_SYM_TAB, "\t", self.pos.copy()))
                self.advance()
                continue

            if self.current_char == "\n":
                tokens.append(Token(TK_SYM_NEWLINE, "\n", self.pos.copy()))
                self.advance()
                continue

            # COMMENTS
            if scan_comment(self, tokens, errors):
                continue

            # NUMBERS 
            if scan_numbers(self, tokens, errors):
                continue

            # STRINGS 
            if self.current_char == '"':
                if scan_string(self, tokens, errors):
                    continue

            # CHARS 
            if self.current_char == "'":
                if scan_char(self, tokens, errors):
                    continue

            # KEYWORDS 
            if self.current_char.isalpha():
                if scan_keywords(self, tokens, errors):
                    continue

            # IDENTIFIERS 
            if scan_identifier(self, tokens, errors):
                continue

            # OPERATORS 
            try:
                if scan_operator(self, tokens, errors):
                    continue
            except LexicalError as e:
                errors.append(e)
                if self.current_char is not None:
                    self.advance()
                continue

            # SYMBOLS 
            try:
                if scan_symbol(self, tokens, errors):
                    continue
            except LexicalError as e:
                errors.append(e)
                if self.current_char is not None:
                    self.advance()
                continue

            # INVALID / UNRECOGNIZED 
            bad_pos = self.pos.copy()
            bad_char = self.current_char
            errors.append(LexicalError(bad_pos, f"Unexpected character '{bad_char}'"))
            self.advance()

        tokens.append(Token(TK_EOF, None, self.pos.copy()))
        return tokens, errors
