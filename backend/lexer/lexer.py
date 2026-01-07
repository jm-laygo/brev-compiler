from backend.lexer.tokens import Token
from backend.lexer.tokens import *
from backend.lexer.errors import LexicalError
from backend.lexer.positions import Position
from backend.lexer.reserved_words import RESERVED_WORDS
from backend.lexer.delimiters import *

from backend.lexer.scanners.scan_comments import scan_comment
from backend.lexer.scanners.scan_identifiers import scan_identifier
from backend.lexer.scanners.scan_numbers import scan_number
from backend.lexer.scanners.scan_chars import scan_char
from backend.lexer.scanners.scan_strings import scan_string
from backend.lexer.scanners.scan_constants import scan_constant
from backend.lexer.scanners.scan_operators import scan_operator
from backend.lexer.scanners.scan_symbol import scan_symbol

class Lexer:
    def __init__(self, source_code): 
        self.source_code = source_code.replace('\r', '')
        self.pos = Position(-1, 1)
        self.current_char = None
        self.advance()

    def peek(self):
        next_pos = self.pos.index + 1
        if next_pos >= len(self.source_code):
            return None
        return self.source_code[next_pos]

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.source_code[self.pos.index] if self.pos.index < len(self.source_code) else None

    def make_tokens(self):
        tokens = []
        errors = []

        while self.current_char is not None:

            # Handle escape sequences
            if self.current_char == "\\":
                peek = self.peek()
                escape_seq = "\\" + peek if peek else "\\"
                start_pos = self.pos.copy()
                if escape_seq == r"\n":
                    tokens.append(Token(TK_SYM_NEWLINE, r"\n", start_pos))
                    self.advance(); self.advance()
                    continue
                elif escape_seq == r"\t":
                    tokens.append(Token(TK_SYM_SPACE, r"\t", start_pos))
                    self.advance(); self.advance()
                    continue
                else:
                    errors.append(LexicalError(start_pos, f"Unexpected escape sequence '{escape_seq}'"))
                    self.advance(); self.advance()
                    continue

            # IDENTIFIERS / RESERVED WORDS
            if self.current_char.isalpha():
                try:
                    tok = scan_identifier(self)
                    
                    # ENFORCE SIGIL CHAR RULE
                    if tok.type == TK_DTYPE_SIGIL:
                        # peek ahead to see next non-space character
                        temp_pos = self.pos.index
                        while temp_pos < len(self.source_code) and self.source_code[temp_pos] == " ":
                            temp_pos += 1
                        next_char = self.source_code[temp_pos] if temp_pos < len(self.source_code) else None
                        if next_char == '"':
                            errors.append(LexicalError(tok.pos, "sigil literal must be a char, not a string"))
                    
                    tokens.append(tok)
                except LexicalError as e:
                    errors.append(e)
                    self.advance()
                continue

            # SPACE
            if self.current_char == " ":
                tokens.append(Token(TK_SYM_SPACE, " ", self.pos.copy()))
                self.advance()
                continue

            # NEWLINE
            if self.current_char == "\n":
                pos_copy = self.pos.copy()
                self.advance()
                tokens.append(Token(TK_SYM_NEWLINE, "\n", pos_copy))
                continue

            # COMMENTS
            if self.current_char == "/" and (self.peek() == "/" or self.peek() == "*"):
                try:
                    tok = scan_comment(self)
                    tokens.append(tok)
                except LexicalError as e:
                    errors.append(e)
                continue

            # NUMBERS
            if self.current_char.isdigit() or self.current_char == "~":
                try:
                    tok = scan_number(self)
                    tokens.append(tok)  # append token first

                    # dangling operator check AFTER token
                    if self.current_char in op_delim and self.current_char != "=":
                        pos_copy = self.pos.copy()
                        errors.append(LexicalError(pos_copy, f"Dangling operator '{self.current_char}' after number '{tok.value}'"))
                        self.advance()  # skip dangling operator

                    # REQUIRE DELIMITER
                    if self.current_char not in int_decdelim:
                        pos_copy = self.pos.copy()
                        errors.append(LexicalError(pos_copy, f"Missing delimiter after number '{tok.value}'"))
                except LexicalError as e:
                    errors.append(e)
                    self.advance()
                continue

            # STRING LITERALS
            if self.current_char == '"':
                try:
                    tok = scan_string(self)
                    tokens.append(tok)
                except LexicalError as e:
                    errors.append(e)
                    self.advance()
                continue

            # CHAR LITERALS
            if self.current_char == "'":
                try:
                    tok = scan_char(self)
                    tokens.append(tok)
                except LexicalError as e:
                    errors.append(e)
                    self.advance()
                continue

            # OPERATORS
            try:
                tok = scan_operator(self)
                if tok:
                    tokens.append(tok)
                    continue
            except LexicalError as e:
                errors.append(e)
                self.advance()
                continue

            # SYMBOLS
            try:
                tok = scan_symbol(self)
                if tok:
                    tokens.append(tok)
                    continue
            except LexicalError as e:
                errors.append(e)
                self.advance()
                continue

            # FALLBACK: unexpected character
            pos_copy = self.pos.copy()
            errors.append(LexicalError(pos_copy, f"Unexpected character '{self.current_char}'"))
            self.advance()

        return tokens, errors
