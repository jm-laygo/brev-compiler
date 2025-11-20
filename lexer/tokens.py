class Token:
    def __init__(self, type_, value=None, pos=None): 
        self.type = type_
        self.value = value
        self.pos = pos

    def to_dict(self):
        if isinstance(self.pos, int):
            return {
                "type": self.type,
                "value": self.value,
                "pos": {"index": self.pos, "line": None, "col": None}
            }
        elif self.pos:
            return {
                "type": self.type,
                "value": self.value,
                "pos": {"index": self.pos.index, "line": self.pos.ln, "col": self.pos.col}
            }
        else:
            return {
                "type": self.type,
                "value": self.value,
                "pos": None
            }


    def __repr__(self):
        return f"{self.type}:{self.value}"

# IO TOKENS
TK_IO_RECEIVE    = "receive"
TK_IO_PROCLAIM   = "proclaim"

# DATA TYPES
TK_DTYPE_SIGIL       = "sigil"
TK_DTYPE_TALLY       = "tally"
TK_DTYPE_DIVINE      = "divine"
TK_DTYPE_SCRIPTURE   = "scripture"
TK_DTYPE_HOLLOW      = "hollow"
TK_DTYPE_VERITY      = "verity"

# CONTROL FLOW TOKENS
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
TK_CF_RITE          = "rite"
TK_CF_DISMISS       = "dismiss"

# QUALIFIERS
TK_CONST            = "sacred"

# OTHERS
TK_OTHERS_MAIN     = "genesis"
TK_OTHERS_HOLY     = "holy"
TK_OTHERS_UNHOLY   = "unholy"
TK_OTHERS_ORDER    = "order"
TK_OTHERS_ORDAIN   = "ordain"
TK_OTHERS_MASSOF   = "massof"
TK_OTHERS_VERSEOF  = "verseof"

# OPERATOR TOKENS
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
TK_OP_NOT       = "!!"

TK_OP_INC       = "++"
TK_OP_DEC       = "--"

# SYMBOL TOKENS
TK_SYM_SPACE    = " "
TK_SYM_COMMA    = ","
TK_SYM_SEMICOL  = ";"
TK_SYM_SINGLEQ  = "‘’"
TK_SYM_DOUBLEQ  = "“”"
TK_SYM_PAREN    = "()"
TK_SYM_OPPAREN  = "("
TK_SYM_CLSPAREN = ")"
TK_SYM_BRACK    = "[]"
TK_SYM_OPBRACK  = "["
TK_SYM_CLSBRACK = "]"
TK_SYM_BRACE    = "{}"
TK_SYM_OPBRACE  = "{"
TK_SYM_CLSBRACE = "}"
TK_SYM_COLON    = ":"
TK_SYM_DOT      = "."
TK_SYM_AMP      = "&"

# LITERAL TOKENS
TK_LIT_INT      = "int literal"
TK_LIT_DECIMAL  = "decimal literal"
TK_LIT_CHAR     = "letter literal"
TK_LIT_STRING   = "string literal"
TK_LIT_BOOL     = "bool literal"

# SPECIAL TOKENS
TK_IDENTIFIER        = "identifier"
TK_COMMENT           = "comment"
TK_COMMENT_BLOCK     = "comment block"
