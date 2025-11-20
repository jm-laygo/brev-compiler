from lexer.tokens import Token
from lexer.tokens import *
from lexer.errors import LexicalError
from lexer.positions import Position
from lexer.reserved_words import RESERVED_WORDS, is_prefix
from lexer.delimiters import *

from lexer.scanners.scan_comments import scan_comment
from lexer.scanners.scan_alphabet import scan_alphabet_manual
from lexer.scanners.scan_identifiers import scan_identifier
from lexer.scanners.scan_numbers import scan_number
from lexer.scanners.scan_chars import scan_char
from lexer.scanners.scan_strings import scan_string
from lexer.scanners.scan_constants import scan_constant
from lexer.scanners.scan_operators import scan_operator
from lexer.scanners.scan_symbol import scan_symbol

class Lexer:
    def __init__(self, source_code): 
        self.source_code = source_code
        self.pos = Position(-1, 1)
        self.current_char = None
        self.advance()

    def peek(self): # for comment lang
        next_pos = self.pos.index + 1
        if next_pos >= len(self.source_code):
            return None
        return self.source_code[next_pos]

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.source_code[self.pos.index] if self.pos.index<len(self.source_code) else None

    def make_tokens(self):
        tokens = []  # list of tokens
        line = 1
        errors = []

        while self.current_char is not None:
            # LETTERS / KEYWORDS
            if self.current_char.isalpha():
                try:
                    tok = scan_identifier(self)
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

            # COMMENTS
            if self.current_char == "/":
                if self.peek() == "/" or self.peek() == "*":
                    try:
                        tok = scan_comment(self)
                        tokens.append(tok)
                    except LexicalError as e:
                        errors.append(e)
                    continue

            # NUMBER LITERALS
            if self.current_char.isdigit() or self.current_char == "~":
                try:
                    tok = scan_number(self)
                    tokens.append(tok)
                except LexicalError as e:
                    errors.append(e)
                    self.advance()
                continue

            # IDENTIFIERS / RESERVED
            if self.current_char.isalpha():
                try:
                    tok = scan_identifier(self, allow_reserved_as_type=True)
                    tokens.append(tok)
                except LexicalError as e:
                    errors.append(e)
                    self.advance()

            # SCRIPTURE
            if self.current_char == '"':
                try:
                    tok = scan_string(self)
                    tokens.append(tok)
                except LexicalError as e:
                    errors.append(e)
                    self.advance()
                continue

            # SIGIL
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

            #  SYMBOLS
            try:
                tok = scan_symbol(self)
                if tok:
                    tokens.append(tok)
                    continue
            except LexicalError as e:
                errors.append(e)
                self.advance()
                continue

            # VERITY
            if self.current_char.isalpha():
                start_pos = self.pos.copy()
                word = ""
                while self.current_char and self.current_char.isalpha():
                    word += self.current_char
                    self.advance()
                
                if word in ["holy", "unholy"]:
                    tokens.append(Token(TK_LIT_BOOL, word, start_pos))
                    continue
                elif word == "verity":
                    tokens.append(Token(TK_DTYPE_VERITY, word, start_pos))
                    continue
                else:
                    tokens.append(Token(TK_IDENTIFIER, word, start_pos))
                    continue

            # SACRED
            if self.current_char.isalpha():
                peek_word = ""
                temp_pos = self.pos.index
                while temp_pos < len(self.source_code) and self.source_code[temp_pos].isalpha():
                    peek_word += self.source_code[temp_pos]
                    temp_pos += 1

                if peek_word == "sacred":
                    try:
                        tok = scan_constant(self)
                        tokens.append(tok)
                    except LexicalError as e:
                        errors.append(e)
                        self.advance()
                    continue

            # UNEXPECTED CHARACTERS
            pos = self.pos.copy()
            errors.append(LexicalError(pos, f"Unexpected character '{self.current_char}'"))
            self.advance()

        return tokens, errors