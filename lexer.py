# CONSTANTS

ZERO = '0'
DIGIT = '123456789'
ZERODIGIT = ZERO + DIGIT

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_DIG = ALPHABET + DIGIT

# --- Delimiters ---

space = ' '
colon = ':'
semicolon = ';'
underscore = '_'
op_par = '{'
op_brc = '['
comma = ','
newline = '\n'

id_sym = set(ALPHA_DIG + "_")
els_delim = {space, newline, '{'}
bool_delim = {space, ')', semicolon, comma}
op_delim = {'+', '-', '*', '/', '%', '!', '&', '|', '='}
int_decdelim = {space, *op_delim, semicolon, colon, comma, '}', ')', ']'}
chr_delim = {space, semicolon, comma, colon, '}', ')', '&'}
str_delim = {comma, semicolon, space, colon, ')', '}', '&'}
idnt_delim = {space, semicolon, comma, '.', *op_delim, '(', ')', '}', '[', ']'}

delim1 = set(ALPHA_DIG) | {space, '"', '('}
delim2 = {semicolon} | set(ALPHA_DIG) | {')'}
delim3 = {space, '~'} | set(ALPHA_DIG) | {'('}
delim4 = {'"', '~', "'", '('} | set(ALPHABET) | {space, '{'}
delim5 = {space} | set(ALPHA_DIG) | {'~', '"', "'", '('}
delim6 = {'(', ')', '!', "'", '"', space} | set(ALPHA_DIG)
delim7 = {';', '{', ')', '<', '>', '=', '|', '&', '+', '-', '/', '*', '%', space, '\n', ':', ','}
delim8 = {']', '(', space} | set(ALPHA_DIG)
delim9 = {'=', ';', '[', ')', space, '\n'}
delim10 = {"'", '"', '~', '{', space} | set(ALPHA_DIG) | {'\n'}
delim11 = {'{', ';', '}', ',', space} | set(ALPHABET) | {'\n'}
delim12 = {space, "'", '"'} | set(ALPHA_DIG)

asciichr = {chr(i) for i in range(32, 127) if chr(i) != "'"}
asciistr = {chr(i) for i in range(32, 127) if chr(i) != '"'}


#TOKENS

# --- Reserved Words ---

TK_IO_RECEIVE    = "receive"
TK_IO_PROCLAIM   = "proclaim"

TK_DTYPE_SIGIL       = "sigil"
TK_DTYPE_TALLY       = "tally"
TK_DTYPE_DIVINE      = "divine"
TK_DTYPE_SCRIPTURE   = "scripture"
TK_DTYPE_HOLLOW      = "hollow"
TK_DTYPE_VERITY      = "verity"

TK_CF_DECREE        = "decree"
TK_CF_ABSOLUTION    = "absolution"
TK_CF_EDICT         = "edict"
TK_CF_DISCERN       = "discern"
TK_CF_VERSE         = "verse"
TK_CF_GRACE         = "grace"
TK_CF_ABSOLVE       = "absolve"
TK_CF_PROCEED       = "proceed"
TK_CF_PROCESSION    = "procession"
TK_CF_ENDURE        = "endure"
TK_CF_RITUAL        = "ritual"
TK_CF_DISMISS       = "dismiss"

TK_QUAL_SACRED      = "sacred"

TK_OTHERS_GENESIS     = "genesis"
TK_OTHERS_HOLY        = "holy"
TK_OTHERS_UNHOLY      = "unholy"
TK_OTHERS_ORDER       = "order"
TK_OTHERS_ORDAIN      = "ordain"
TK_OTHERS_MASSOF      = "massof"
TK_OTHERS_VERSEOF     = "verseof"

# --- Resereved Symbols ---

TK_OP_PLUS      = "+"
TK_OP_MINUS     = "-"
TK_OP_MUL       = "*"
TK_OP_DIV       = "/"
TK_OP_MOD       = "%"
TK_OP_POW       = "**"
TK_OP_TILDE     = "~"

TK_OP_ASSIGN    = "="
TK_OP_PLUS_EQ   = "+="
TK_OP_MINUS_EQ  = "-="
TK_OP_MUL_EQ    = "*="
TK_OP_DIV_EQ    = "/="
TK_OP_MOD_EQ    = "%="
TK_OP_POW_EQ    = "**="

TK_OP_EQ        = "=="
TK_OP_NOTEQ     = "!="
TK_OP_GT        = ">"
TK_OP_LT        = "<"
TK_OP_GTE       = ">="
TK_OP_LTE       = "<="

TK_OP_AND       = "&&"
TK_OP_OR        = "||"
TK_OP_NOT      = "!!"

TK_OP_INC       = "++"
TK_OP_DEC       = "--"

TK_SYM_COMMA    = ","
TK_SYM_SEMICOL  = ";"
TK_SYM_SINGLEQ  = "‘’"
TK_SYM_DOUBLEQ  = "“”"
TK_SYM_PAREN    = "()"
TK_SYM_OPPAREN    = "("
TK_SYM_CLSPAREN    = ")"
TK_SYM_BRACK    = "[]"
TK_SYM_OPBRACK    = "["
TK_SYM_CLSBRACK    = "]"
TK_SYM_BRACE    = "{}"
TK_SYM_OPBRACE    = "{"
TK_SYM_CLSBRACE    = "}"
TK_SYM_COLON    = ":"
TK_SYM_DOT      = "."
TK_SYM_AMP      = "&"

# --- Literals ---

TK_LIT_INT        = "int literal"
TK_LIT_DECIMAL    = "decimal literal"
TK_LIT_CHAR       = "letter literal"
TK_LIT_STRING     = "string literal"
TK_LIT_BOOL       = "holy/unholy"
TK_IDENTIFIER        = "identifier"
TK_COMMENT           = "comment"
TK_COMMENT_BLOCK     = "comment block"

class Position:
    def __init__(self, index, ln):
        self.index = index
        self.ln = ln

    def advance(self, current_char): #Advance to the next character
        self.index += 1

        if current_char == '\n':
            self.ln +=1

        return self
    
    def copy(self): #Returnss the current position(index, line) of the character
        return Position(self.index, self.ln)
        
#ERROR
class LexicalError:
    def __init__(self, pos, details):
        self.pos = pos
        self.details = details

    def as_string(self): #Returns the error message in string format
        self.details = self.details.replace('\n', '\\n')
        return f"Ln {self.pos.ln} Lexical Error: {self.details}"
    
#TOKEN
class Token:
    def __init__(self, type_, value=None, line=1): 
        self.type = type_
        self.value = value
        self.line = line
        

#LEXER
class Lexer:
    def __init__(self, source_code): 
        self.source_code = source_code
        self.pos = Position(-1, 1)
        self.current_char = None
        self.advance()

    def advance(self): #Advance to the next character
        self.pos.advance(self.current_char)
        self.current_char = self.source_code[self.pos.index] if self.pos.index<len(self.source_code) else None

# --- following 'yung MGA NASA TD
    def make_tokens(self):
            tokens = [] # lists of toekns
            line = 1
            errors = []
            while self.current_char is not None:
                if self.current_char in [' ', '\t']:
                    self.advance()
                    continue
                if self.current_char in ALPHABET:
                    ident_str = ''
                    pos = self.pos.copy()
                    # Letter A
                    if self.current_char == "a":
                        ident_str += self.current_char
                        self.advance()

                        # ABSOLUTION
                        if self.current_char == "b":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "u":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "l":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "u":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "t":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char == "i":
                                                    ident_str += self.current_char
                                                    self.advance()
                                                    if self.current_char == "o":
                                                        ident_str += self.current_char
                                                        self.advance()
                                                        if self.current_char == "n":
                                                            ident_str += self.current_char
                                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_CF_ABSOLUTION, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue
                        # ABSOLVE
                        elif self.current_char == "b":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "o":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "l":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "v":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "e":
                                                ident_str += self.current_char
                                                self.advance()
                                if self.current_char is not None and self.current_char in delim4:
                                    tokens.append(Token(TK_CF_ABSOLVE, ident_str, line))
                                    continue
                                elif self.current_char is not None and self.current_char not in delim4 and self.current_char not in ALPHA_DIG:
                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                    self.advance()
                                    continue

                    # LETTER D
                    if self.current_char == "d":
                        ident_str += self.current_char
                        self.advance()

                        # DECREE
                        if self.current_char == "e":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "c":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "r":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "e":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "e":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_CF_DECREE, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue

                        # DISCERN / DISMISS
                        elif self.current_char == "i":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                self.advance()
                                # DISCERN
                                if self.current_char == "c":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "e":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "r":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "n":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_CF_DISCERN, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                                # DISMISS
                                elif self.current_char == "m":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "i":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "s":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "s":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_CF_DISMISS, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                            # DIVINE
                            elif self.current_char == "v":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "i":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "n":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "e":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_DTYPE_DIVINE, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue

                    # LETTER E
                    if self.current_char == "e":
                        ident_str += self.current_char
                        self.advance()

                        # EDICT
                        if self.current_char == "d":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "i":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "c":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "t":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char is not None and self.current_char in space:
                                            tokens.append(Token(TK_CF_EDICT, ident_str, line))
                                            continue
                                        elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                            self.advance()
                                            continue

                            # ENDURE
                            elif self.current_char == "n":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "d":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "u":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "r":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "e":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_CF_ENDURE, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                    # LETTER G
                    if self.current_char == "g":
                        ident_str += self.current_char
                        self.advance()

                        # GENESIS
                        if self.current_char == "e":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "n":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "s":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "i":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "s":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_OTHERS_GENESIS, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                            # GRACE
                            elif self.current_char == "r":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "a":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "c":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "e":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_CF_GRACE, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue

                    # LETTER H
                    if self.current_char == "h":
                        ident_str += self.current_char
                        self.advance()

                        # HOLLOW
                        if self.current_char == "o":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "l":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "l":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "o":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "w":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_DTYPE_HOLLOW, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue

                                # HOLY
                                elif self.current_char == "o":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "l":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "y":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_OTHERS_HOLY, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue

                    # LETTER M
                    if self.current_char == "m":
                        ident_str += self.current_char
                        self.advance()

                        # MASSOF
                        if self.current_char == "a":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "s":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "s":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "o":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "f":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_OTHERS_MASSOF, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue
                    # LETTER O
                    if self.current_char == "o":
                        ident_str += self.current_char
                        self.advance()

                        # ORDAIN
                        if self.current_char == "r":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "d":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "a":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "i":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "n":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_OTHERS_ORDAIN, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue

                                # ORDER
                                elif self.current_char == "r":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "d":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "e":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "r":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_OTHERS_ORDER, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                    # LETTER P
                    if self.current_char == "p":
                        ident_str += self.current_char
                        self.advance()

                        # PROCEED
                        if self.current_char == "r":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "o":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "c":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "e":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "e":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "d":
                                                ident_str += self.current_char
                                                self.advance()
                                                ident_str += self.current_char
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_CF_PROCEED, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                                # PROCLAIM
                                if self.current_char == "l":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "a":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "i":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "m":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_IO_PROCLAIM, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                                        # PROCESSION
                                        elif self.current_char == "s":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "s":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char == "i":
                                                    ident_str += self.current_char
                                                    self.advance()
                                                    if self.current_char == "o":
                                                        ident_str += self.current_char
                                                        self.advance()
                                                        if self.current_char == "n":
                                                            ident_str += self.current_char
                                                            self.advance()
                                                            if self.current_char is not None and self.current_char in space:
                                                                tokens.append(Token(TK_CF_PROCESSION, ident_str, line))
                                                                continue
                                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                                self.advance()
                                                                continue

                    # LETTER R
                    if self.current_char == "r":
                        ident_str += self.current_char
                        self.advance()

                        # RECEIVE
                        if self.current_char == "e":
                            ident_str += self.current_char
                            self.advance()
                            if self.current_char == "c":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "i":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "v":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "e":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_IO_RECEIVE, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                                # RITUAL
                                elif self.current_char == "i":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "t":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "u":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "a":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char == "l":
                                                    ident_str += self.current_char
                                                    self.advance()
                                                    if self.current_char is not None and self.current_char in space:
                                                        tokens.append(Token(TK_CF_RITUAL, ident_str, line))
                                                        continue
                                                    elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                        self.advance()
                                                        continue

                                        # RITE
                                        elif self.current_char == "i":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "t":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char == "e":
                                                    ident_str += self.current_char
                                                    self.advance()
                                                    if self.current_char is not None and self.current_char in space:
                                                        tokens.append(Token(TK_QUAL_SACRED, ident_str, line))
                                                        continue
                                                    elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                        self.advance()
                                                        continue

                        # LETTER S
                        if self.current_char == "s":
                            ident_str += self.current_char
                            self.advance()

                            # SACRED
                            if self.current_char == "a":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "c":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "r":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "e":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "d":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_QUAL_SACRED, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                                    # SCRIPTURE
                                    elif self.current_char == "c":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "r":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "i":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char == "p":
                                                    ident_str += self.current_char
                                                    self.advance()
                                                    if self.current_char == "t":
                                                        ident_str += self.current_char
                                                        self.advance()
                                                        if self.current_char == "u":
                                                            ident_str += self.current_char
                                                            self.advance()
                                                            if self.current_char == "r":
                                                                ident_str += self.current_char
                                                                self.advance()
                                                                if self.current_char == "e":
                                                                    ident_str += self.current_char
                                                                    self.advance()
                                                                    if self.current_char is not None and self.current_char in space:
                                                                        tokens.append(Token(TK_DTYPE_SCRIPTURE, ident_str, line))
                                                                        continue
                                                                    elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                                        self.advance()
                                                                        continue

                                            # SIGIL
                                            elif self.current_char == "i":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char == "g":
                                                    ident_str += self.current_char
                                                    self.advance()
                                                    if self.current_char == "i":
                                                        ident_str += self.current_char
                                                        self.advance()
                                                        if self.current_char == "l":
                                                            ident_str += self.current_char
                                                            self.advance()
                                                            if self.current_char is not None and self.current_char in space:
                                                                tokens.append(Token(TK_DTYPE_SIGIL, ident_str, line))
                                                                continue
                                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                                self.advance()
                                                                continue

                        # LETTER T
                        if self.current_char == "t":
                            ident_str += self.current_char
                            self.advance()

                            # TALLY
                            if self.current_char == "a":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "l":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "l":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "y":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char is not None and self.current_char in space:
                                                tokens.append(Token(TK_DTYPE_TALLY, ident_str, line))
                                                continue
                                            elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                self.advance()
                                                continue

                        # LETTER U
                        if self.current_char == "u":
                            ident_str += self.current_char
                            self.advance()

                            # UNHOLY
                            if self.current_char == "n":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "h":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "o":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "l":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "y":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_OTHERS_UNHOLY, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                        # LETTER V
                        if self.current_char == "v":
                            ident_str += self.current_char
                            self.advance()

                            # VERITY
                            if self.current_char == "e":
                                ident_str += self.current_char
                                self.advance()
                                if self.current_char == "r":
                                    ident_str += self.current_char
                                    self.advance()
                                    if self.current_char == "i":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "t":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "y":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char is not None and self.current_char in space:
                                                    tokens.append(Token(TK_DTYPE_VERITY, ident_str, line))
                                                    continue
                                                elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                    errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                    self.advance()
                                                    continue

                                    # VERSE
                                    elif self.current_char == "s":
                                        ident_str += self.current_char
                                        self.advance()
                                        if self.current_char == "e":
                                            ident_str += self.current_char
                                            self.advance()
                                            if self.current_char == "r":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char == "s":
                                                    ident_str += self.current_char
                                                    self.advance()
                                                    if self.current_char == "e":
                                                        ident_str += self.current_char
                                                        self.advance()
                                                        if self.current_char is not None and self.current_char in space:
                                                            tokens.append(Token(TK_CF_VERSE, ident_str, line))
                                                            continue
                                                        elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                            self.advance()
                                                            continue

                                            # VERSEOF
                                            elif self.current_char == "o":
                                                ident_str += self.current_char
                                                self.advance()
                                                if self.current_char == "f":
                                                    ident_str += self.current_char
                                                    self.advance()
                                                    if self.current_char is not None and self.current_char in space:
                                                        tokens.append(Token(TK_OTHERS_VERSEOF, ident_str, line))
                                                        continue
                                                    elif self.current_char is not None and self.current_char not in space and self.current_char not in ALPHA_DIG:
                                                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                                                        self.advance()
                                                        continue

                #IDENTIFIEr        
                    maxIdentifierLength = 32 # from 0 to 31
                    while self.current_char is not None and self.current_char in ALPHA_DIG + "_":
                        if len(ident_str) + 1 > maxIdentifierLength:
                            errors.append(LexicalError(pos, f"Identifier '{ident_str}...' exceeds maximum length of {maxIdentifierLength} characters."))
                            # consume invalid identifiers
                            while self.current_char is not None and self.current_char in ALPHA_DIG + "_":
                                self.advance()
                            break
                        ident_str += self.current_char
                        self.advance()

                    if len(ident_str) <= maxIdentifierLength:
                        if self.current_char is None or self.current_char in idnt_delim:
                            tokens.append(Token(TK_IDENTIFIER, ident_str, line))
                            continue
                        elif self.current_char is not None and self.current_char not in idnt_delim and self.current_char not in ALPHA_DIG:
                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                            self.advance()
                            continue
                    else:
                        continue

                
                elif self.current_char == "-":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char == "-":
                        ident_str += self.current_char
                        self.advance()
                        if self.current_char is None or self.current_char in unary_dlm: # --- wala pa, wag una pakelamn ---
                            tokens.append(Token(TK_OP_DEC, ident_str, line))
                            continue
                        else:
                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                            self.advance()
                            continue
                    elif self.current_char is not None and self.current_char in op_delim:
                        tokens.append(Token(TK_OP_MINUS, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                
                elif self.current_char == "~":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char is not None and self.current_char in tilde_dlm: # --- wala pa ---
                        tokens.append(Token(TK_OP_TILDE, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'."))
                        self.advance()
                        continue
                
                elif self.current_char == "!":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char == "=":
                        ident_str += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in op_delim:
                            tokens.append(Token(TK_OP_NOTEQ, ident_str, line))
                            continue
                        else:
                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                            self.advance()
                            continue
                    elif self.current_char is not None and self.current_char in op_delim:
                        tokens.append(Token(TK_OP_NOT, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                
                elif self.current_char == "%":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char is not None and self.current_char in op_delim:
                        tokens.append(Token(TK_OP_MOD, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
        
                elif self.current_char == "&":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char == "&":
                        ident_str += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in op_delim:
                            tokens.append(Token(TK_OP_AND, ident_str, line))
                            continue
                        else:
                            errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                            self.advance()
                            continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid character '{ident_str}'"))
                        self.advance()
                        continue
                        
                elif self.current_char == "(":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char is not None and self.current_char in idnt_delim:
                        tokens.append(Token(TK_SYM_OPPAREN, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                    
                elif self.current_char == ")":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char is None or self.current_char in idnt_delim:
                        tokens.append(Token(TK_SYM_CLSPAREN, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                    
                elif self.current_char == "*":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char is None or self.current_char in op_delim:
                        tokens.append(Token(TK_OP_MUL, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                    
                elif self.current_char == ",":
                    ident_str = self.current_char
                    pos = self.pos.copy()
                    self.advance()
                    if self.current_char is not None and self.current_char in comma:
                        tokens.append(Token(TK_SYM_COMMA, ident_str, line))
                        continue
                    else:
                        errors.append(LexicalError(pos, f"Invalid delimiter '{self.current_char}' after '{ident_str}'"))
                        self.advance()
                        continue
                    pos = self.pos.copy()
                    errors.append(LexicalError(pos, f"Unexpected character '{self.current_char}'"))
                    if self.current_char == '\n':
                        line += 1
                    self.advance()
            return tokens, errors

